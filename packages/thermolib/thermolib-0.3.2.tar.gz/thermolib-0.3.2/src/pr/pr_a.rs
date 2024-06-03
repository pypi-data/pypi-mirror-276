use super::PrAr;
use crate::core::{GenericA, IdealCv, Phase, TlErr};
use anyhow::anyhow;
/// fundumental helmholtz equation of state
/// transformed from pr equation of state
pub type PrA = GenericA<IdealCv, PrAr>;
#[allow(non_snake_case)]
impl PrA {
    /// Calculate A&B return (A,B)
    fn calc_AB(&self, T: f64, P: f64) -> (f64, f64) {
        let pr_ar = self.ref_ar();
        (
            pr_ar.a(T) * P / pr_ar.R().powi(2) / T.powi(2),
            pr_ar.b() * P / pr_ar.R() / T,
        )
    }
    /// Calculate fugacity coefficient
    fn calc_lnfp(&self, Z: f64, A: f64, B: f64) -> f64 {
        let sqrt2 = f64::sqrt(2.0);
        (Z - 1.0)
            - (Z - B).ln()
            - A / (2.0 * sqrt2 * B) * ((Z + B + sqrt2 * B) / (Z + B - sqrt2 * B)).ln()
    }
    /// Calculate fugacity coefficient of different phase
    fn calc_diff_lnfpgl(&self, T: f64, P: f64) -> f64 {
        let (A, B) = self.calc_AB(T, P);
        let (Zg, Zl) = self.calc_root(A, B);
        if Zl != 0.0 {
            self.calc_lnfp(Zg, A, B) - self.calc_lnfp(Zl, A, B)
        } else if Zg > 0.307 {
            self.calc_lnfp(Zg, A, B) // gas phase
        } else {
            -self.calc_lnfp(Zg, A, B) // liquid phase
        }
    }
    /// return (Zg,Zl) where double root
    /// return (Zg, 0) where single root
    fn calc_root(&self, A: f64, B: f64) -> (f64, f64) {
        let b = -(1.0 - B);
        let c = A - 3.0 * B.powi(2) - 2.0 * B;
        let d = -(A * B - B.powi(2) - B.powi(3));
        let A = b.powi(2) - 3.0 * c;
        let B = b * c - 9.0 * d;
        let C = c.powi(2) - 3.0 * b * d;
        let Delta = B.powi(2) - 4.0 * A * C;
        if Delta > 0.0 {
            let Y1 = A * b + 1.5 * (-B + Delta.sqrt());
            let Y2 = A * b + 1.5 * (-B - Delta.sqrt());
            ((-b - (Y1.cbrt() + Y2.cbrt())) / 3.0, 0.0)
        } else if Delta < 0.0 {
            let theta3 = ((2.0 * A * b - 3.0 * B) / (2.0 * A * A.sqrt())).acos() / 3.0;
            let x1 = (-b - 2.0 * A.sqrt() * theta3.cos()) / 3.0;
            let x2 = (-b + A.sqrt() * (theta3.cos() + 3.0_f64.sqrt() * theta3.sin())) / 3.0;
            let x3 = (-b + A.sqrt() * (theta3.cos() - 3.0_f64.sqrt() * theta3.sin())) / 3.0;
            let Zg = x1.max(x2).max(x3);
            let Zl = x1.min(x2).min(x3);
            if Zl < 0.0 {
                (Zg, 0.0)
            } else {
                (Zg, Zl)
            }
        } else {
            (B / A - b, 0.0)
        }
    }
}
#[allow(non_snake_case)]
impl PrA {
    pub fn new_pr(Tc: f64, Pc: f64, omega: f64, M: f64) -> Self {
        let ai = IdealCv::default();
        let ar = PrAr::new(Tc, Pc, omega, 8.314462618);
        GenericA::new(ai, ar, M)
    }
    /// impl methods to overwrite Flash::t_flash
    pub fn t_flash(&mut self, Ts: f64) -> anyhow::Result<()> {
        // use ps_min = 1Pa
        let mut ps_min = 1.0;
        let mut lnfp_min = self.calc_diff_lnfpgl(Ts, ps_min);
        // use ps_max = Pc -1Pa
        let mut ps_max = 0.07780 * self.R() * self.ref_ar().Tc() / self.ref_ar().b() - 1.0;
        let mut lnfp_max = self.calc_diff_lnfpgl(Ts, ps_max);
        // check root or not
        if lnfp_min * lnfp_max < 0.0 {
            let mut ps;
            let mut lnfp;
            let mut counter = 0;
            loop {
                ps = (ps_min + ps_max) / 2.0;
                lnfp = self.calc_diff_lnfpgl(Ts, ps);
                if lnfp.abs() < 1E-6 {
                    let (A, B) = self.calc_AB(Ts, ps);
                    let (Zg, Zl) = self.calc_root(A, B);
                    self.set_phase(Phase::Two {
                        Ts,
                        Dg: ps / Zg / self.R() / Ts,
                        Dl: ps / Zl / self.R() / Ts,
                        X: 1.0,
                    });
                    return Ok(());
                }
                if lnfp * lnfp_min < 0.0 {
                    ps_max = ps;
                    lnfp_max = lnfp;
                }
                if lnfp * lnfp_max < 0.0 {
                    ps_min = ps;
                    lnfp_min = lnfp;
                }
                if counter < 1000 {
                    counter += 1;
                } else {
                    break;
                }
            }
        }
        Err(anyhow!(TlErr::NotConvForT))
    }
    /// impl methods to overwrite Flash::td_flash
    pub fn td_flash(&mut self, T: f64, D: f64) -> anyhow::Result<()> {
        if T > self.ref_ar().Tc() {
            self.set_phase(Phase::One { T, D });
            Ok(()) // one phase
        } else if let Err(why) = self.t_flash(T) {
            Err(why) // Self::t_flash diverge
        } else if let Phase::Two { Dg, Dl, .. } = self.phase() {
            if D < Dg || D > Dl {
                self.set_phase(Phase::One { T, D });
                Ok(()) // one phase
            } else {
                self.set_phase(Phase::Two {
                    Ts: T,
                    Dg,
                    Dl,
                    X: (1.0 / D - 1.0 / Dl) / (1.0 / Dg + 1.0 / Dl),
                });
                Ok(()) // two phase
            }
        } else {
            Err(anyhow!(TlErr::NotConvForTD))
        }
    }
    /// impl methods to overwrite Flash::tp_flash
    pub fn tp_flash(&mut self, T: f64, P: f64) -> anyhow::Result<()> {
        let (A, B) = self.calc_AB(T, P);
        let (Zg, Zl) = self.calc_root(A, B);
        let Z = if Zl == 0.0 {
            Zg
        } else {
            let lnfpg = self.calc_lnfp(Zg, A, B);
            let lnfpl = self.calc_lnfp(Zl, A, B);
            if lnfpg < lnfpl {
                Zg
            } else {
                Zl
            }
        };
        self.set_phase(Phase::One {
            T,
            D: P / Z / self.R() / T,
        });
        Ok(())
    }
}
/// unit test
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    #[allow(non_snake_case)]
    fn test_pr_pr_a() {
        let Tc = 430.64;
        let Pc = 7886600.0;
        let omega = 0.256;
        let M = 0.064064;
        let mut pr_a = PrA::new_pr(Tc, Pc, omega, M); // Parameters for SO2
        let Ts = 0.6 * Tc;
        if let Err(_) = pr_a.t_flash(Ts) {
            panic!("t_flash failed at T = {} K", Ts);
        }
    }
}
