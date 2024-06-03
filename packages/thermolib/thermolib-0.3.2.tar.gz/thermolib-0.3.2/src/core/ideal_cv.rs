use super::CalcAi;
/// isochoric heat capacity of ideal gas
/// used to calculate ideal helmholtz energy
#[derive(Clone)]
#[allow(non_snake_case)]
pub struct IdealCv {
    coefficient: f64,
    poly_terms: Vec<PolynomialTerm>,
    pe_terms: Vec<PlankEinsteinTerm>,
    R: f64,
    C0: f64,
    C1: f64,
}
impl Default for IdealCv {
    fn default() -> Self {
        Self {
            coefficient: 0.0,
            poly_terms: Vec::new(),
            pe_terms: Vec::new(),
            R: 8.314462618,
            C0: 0.0,
            C1: 0.0,
        }
    }
}
#[allow(non_snake_case)]
impl CalcAi for IdealCv {
    /// > fn iT0(&self, T: f64) -> f64; Equal to =  
    /// > $$a^i\left(T,D\right)-RT\ln D$$  
    fn iT0(&self, T: f64) -> f64 {
        self.C0
            + self.C1 * T
            + (self.R * T)
                * (-self.coefficient * T.ln()
                    + self.poly_terms.iter().map(|term| term.t0(T)).sum::<f64>()
                    + self.pe_terms.iter().map(|term| term.t0(T)).sum::<f64>())
    }
    /// > fn iT1(&self, _T: f64) -> f64; Equal to =  
    /// > $$T\left(\frac{\partial a^i}{\partial T}\right)_D-RT\ln D$$  
    fn iT1(&self, T: f64) -> f64 {
        self.C1 * T
            + (self.R * T)
                * (-self.coefficient * (T.ln() + 1.0)
                    + self.poly_terms.iter().map(|term| term.t1(T)).sum::<f64>()
                    + self.pe_terms.iter().map(|term| term.t1(T)).sum::<f64>())
    }
    /// > fn iT2(&self, _T: f64) -> f64; Equal to =  
    /// > $$T^2\left(\frac{\partial^2a^i}{\partial T^2}\right)_D$$  
    fn iT2(&self, T: f64) -> f64 {
        (self.R * T)
            * (-self.coefficient
                + self.poly_terms.iter().map(|term| term.t2(T)).sum::<f64>()
                + self.pe_terms.iter().map(|term| term.t2(T)).sum::<f64>())
    }
    /// Used for trait::Setting
    fn set_R(&mut self, R: f64) {
        self.R = R;
    }
}
/// Partial derivatives of ideal polynomial term
#[derive(Clone)]
struct PolynomialTerm {
    c: f64,
    t: f64,
}
#[allow(non_snake_case)]
impl PolynomialTerm {
    fn t0(&self, T: f64) -> f64 {
        -self.c * T.powf(self.t) / self.t / (self.t + 1.0)
    }
    fn t1(&self, T: f64) -> f64 {
        -self.c * T.powf(self.t) / self.t
    }
    fn t2(&self, T: f64) -> f64 {
        -self.c * T.powf(self.t)
    }
}
/// Partial derivatives of ideal plank einstein term
#[derive(Clone)]
struct PlankEinsteinTerm {
    v: f64,
    u: f64,
}
#[allow(non_snake_case)]
impl PlankEinsteinTerm {
    fn t0(&self, T: f64) -> f64 {
        self.v * (1.0 - (-self.u / T).exp()).ln()
    }
    fn t1(&self, T: f64) -> f64 {
        self.v * (1.0 - (-self.u / T).exp()).ln()
            - self.v * self.u / T * (-self.u / T).exp() / (1.0 - (-self.u / T).exp())
    }
    fn t2(&self, T: f64) -> f64 {
        -self.v * (self.u / T).powi(2) * (-self.u / T).exp() / (1.0 - (-self.u / T).exp()).powi(2)
    }
}
/// unit test
#[cfg(test)]
mod tests {
    use super::*;
    use crate::HelmholtzPure;
    use crate::{Flash, Prop};
    #[test]
    #[allow(non_snake_case)]
    fn test_core_ideal_cv() {
        let T: f64 = 300.0;
        let D: f64 = 100.0;
        let R = 8.3144621;
        let a1 = -4.5414235721;
        let a2 = 4.4732289572;
        let Tc: f64 = 430.64;
        let Dc: f64 = 8078.0;
        let coefficient = 3.0;
        let cv = IdealCv {
            coefficient,
            poly_terms: vec![PolynomialTerm {
                c: 0.7397E-4,
                t: 1.0,
            }],
            pe_terms: vec![
                PlankEinsteinTerm {
                    v: 1.0875,
                    u: 783.0,
                },
                PlankEinsteinTerm {
                    v: 1.916,
                    u: 1864.0,
                },
            ],
            R,
            C0: a2 * Tc * R,
            C1: (a1 - Dc.ln() + coefficient * Tc.ln()) * R,
        };
        let mut SO2: HelmholtzPure = HelmholtzPure::read_json("SO2.json").expect("no SO2.json");
        SO2.td_unchecked(T, D);
        let mut SO22 = SO2.set_ai(cv);
        SO22.td_unchecked(T, D);
        assert_eq!(SO2.p().unwrap(), SO22.p().unwrap());
        // assert_eq!(SO2.s().unwrap(), SO22.s().unwrap());
        assert_eq!(SO2.w().unwrap(), SO22.w().unwrap());
        assert_eq!(SO2.cv().unwrap(), SO22.cv().unwrap());
        assert_eq!(SO2.cp().unwrap(), SO22.cp().unwrap());
    }
}
