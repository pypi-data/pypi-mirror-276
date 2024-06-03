use super::{CalcAi, CalcAr, Flash, Prop, Setting, TlErr};
use anyhow::anyhow;
use serde::{Deserialize, Serialize};
/// Phase enum of fluid state, so for it's limited to pure-component.
#[allow(non_snake_case)]
#[derive(Debug, Clone)]
pub enum Phase {
    /// + One-phase region of fluid, 2 independent variables is required.
    /// + T(Temperature) and D(Density).
    One { T: f64, D: f64 },
    /// + Two-phase region of fluid, 1 independent variables is required.
    /// + Ts(Temperature of Saturated Phase).
    /// + Dg(Density of Saturated Gas), Dl(Density of Saturated Liquid), X(Quality).
    Two { Ts: f64, Dg: f64, Dl: f64, X: f64 },
}
#[allow(non_snake_case)]
#[derive(Debug, Clone, Default)]
struct Cache {
    T: f64,
    D: f64,
    value: f64,
}
/// Generic struct of fundumental helmholtz equation of state.
#[allow(non_snake_case)]
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct GenericA<I: CalcAi, R: CalcAr> {
    ai: I,
    ar: R,
    R: f64,
    M: f64,
    #[serde(skip, default)]
    phase: Phase,
    #[serde(skip, default)]
    aT0D0: Cache,
    #[serde(skip, default)]
    aT0D1: Cache,
    #[serde(skip, default)]
    aT0D2: Cache,
    #[serde(skip, default)]
    aT1D0: Cache,
    #[serde(skip, default)]
    aT1D1: Cache,
    #[serde(skip, default)]
    aT2D0: Cache,
    #[serde(skip, default)]
    aT0D0_sub_aT1D0: Cache,
}
impl Default for Phase {
    fn default() -> Self {
        Phase::One { T: 1.0, D: 1.0 }
    }
}
#[allow(non_snake_case)]
impl<I: CalcAi, R: CalcAr> GenericA<I, R> {
    pub fn new(ai: I, ar: R, M: f64) -> Self {
        GenericA {
            ai,
            ar,
            M,
            R: 8.314462618,
            phase: Phase::default(),
            aT0D0: Cache::default(),
            aT0D1: Cache::default(),
            aT0D2: Cache::default(),
            aT1D0: Cache::default(),
            aT1D1: Cache::default(),
            aT2D0: Cache::default(),
            aT0D0_sub_aT1D0: Cache::default(),
        }
    }
}
/// Get internal fields of generic struct
#[allow(non_snake_case)]
impl<I: CalcAi + Clone, R: CalcAr + Clone> GenericA<I, R> {
    pub fn set_ai<A: CalcAi>(&self, ai: A) -> GenericA<A, R> {
        GenericA::<A, R> {
            ai,
            R: self.R,
            M: self.M,
            ar: self.ar.clone(),
            phase: Phase::default(),
            aT0D0: Cache::default(),
            aT0D1: Cache::default(),
            aT0D2: Cache::default(),
            aT1D0: Cache::default(),
            aT1D1: Cache::default(),
            aT2D0: Cache::default(),
            aT0D0_sub_aT1D0: Cache::default(),
        }
    }
    pub fn set_ar<A: CalcAr>(&self, ar: A) -> GenericA<I, A> {
        GenericA::<I, A> {
            ar,
            R: self.R,
            M: self.M,
            ai: self.ai.clone(),
            phase: Phase::default(),
            aT0D0: Cache::default(),
            aT0D1: Cache::default(),
            aT0D2: Cache::default(),
            aT1D0: Cache::default(),
            aT1D1: Cache::default(),
            aT2D0: Cache::default(),
            aT0D0_sub_aT1D0: Cache::default(),
        }
    }
    pub fn ref_ar(&self) -> &R {
        &self.ar
    }
    pub fn set_phase(&mut self, phase: Phase) {
        self.phase = phase;
    }
    pub fn phase(&self) -> Phase {
        self.phase.clone()
    }
    pub fn R(&self) -> f64 {
        self.R
    }
}
/// Calculate partial derivatives of fundumental helmholtz equation of state.  
/// Equal to $$ T^(dT) * D^(dD) * A_DT(dT)_DD(dD) $$  
/// Used to calculate thermodynamic properties.  
#[allow(non_snake_case)]
impl<I: CalcAi, R: CalcAr> GenericA<I, R> {
    /// > fn aT0D0(&self, T: f64, D: f64) -> f64; Equal to
    /// > $$a\left(T,D\right)
    /// > =a^i\left(T,D\right)
    /// > +a^r\left(T,D\right)
    /// > =iT0(T)+RT\ln D+rT0D0(T,D)$$
    fn aT0D0(&mut self, T: f64, D: f64) -> f64 {
        if self.aT0D0.T != T || self.aT0D0.D != D {
            self.aT0D0.T = T;
            self.aT0D0.D = D;
            self.aT0D0.value = self.ai.iT0(T) + self.R * T * D.ln() + self.ar.rT0D0(T, D);
        }
        self.aT0D0.value
    }
    /// > fn aT0D1(&self, T: f64, D: f64) -> f64; Equal to
    /// > $$D\left(\frac{\partial a}{\partial D}\right)_T
    /// > =D\left(\frac{\partial a^i}{\partial D}\right)_T
    /// > +D\left(\frac{\partial a^r}{\partial D}\right)_T
    /// > =RT+rT0D1(T,D)$$
    fn aT0D1(&mut self, T: f64, D: f64) -> f64 {
        if self.aT0D1.T != T || self.aT0D1.D != D {
            self.aT0D1.T = T;
            self.aT0D1.D = D;
            self.aT0D1.value = self.R * T + self.ar.rT0D1(T, D);
        }
        self.aT0D1.value
    }
    /// > fn aT0D2(&self, T: f64, D: f64) -> f64; Equal to
    /// > $$D^2\left(\frac{\partial^2a}{\partial D^2}\right)_T
    /// > =D^2\left(\frac{\partial^2a^i}{\partial D^2}\right)_T
    /// > +D^2\left(\frac{\partial^2a^r}{\partial D^2}\right)_T
    /// > =-RT+rT0D2(T,D)$$
    fn aT0D2(&mut self, T: f64, D: f64) -> f64 {
        if self.aT0D2.T != T || self.aT0D2.D != D {
            self.aT0D2.T = T;
            self.aT0D2.D = D;
            self.aT0D2.value = -self.R * T + self.ar.rT0D2(T, D);
        }
        self.aT0D2.value
    }
    /// > fn aT1D0(&self, T: f64, D: f64) -> f64; Equal to
    /// > $$T\left(\frac{\partial a}{\partial T}\right)_D
    /// > =T\left(\frac{\partial a^i}{\partial T}\right)_D
    /// > +T\left(\frac{\partial a^r}{\partial T}\right)_D
    /// > =iT1(T)+RT\ln D+rT1D0(T,D)$$
    fn aT1D0(&mut self, T: f64, D: f64) -> f64 {
        if self.aT1D0.T != T || self.aT1D0.D != D {
            self.aT1D0.T = T;
            self.aT1D0.D = D;
            self.aT1D0.value = self.ai.iT1(T) + self.R * T * D.ln() + self.ar.rT1D0(T, D);
        }
        self.aT1D0.value
    }
    /// > fn aT1D1(&self, T: f64, D: f64) -> f64; Equal to
    /// > $$TD\left(\frac{\partial^2a}{\partial T\partial D}\right)
    /// > =TD\left(\frac{\partial^2a^i}{\partial T\partial D}\right)
    /// > +TD\left(\frac{\partial^2a^r}{\partial T\partial D}\right)
    /// > =RT+rT1D1(T,D)$$
    fn aT1D1(&mut self, T: f64, D: f64) -> f64 {
        if self.aT1D1.T != T || self.aT1D1.D != D {
            self.aT1D1.T = T;
            self.aT1D1.D = D;
            self.aT1D1.value = self.R * T + self.ar.rT1D1(T, D)
        }
        self.aT1D1.value
    }
    /// > fn aT2D0(&self, T: f64, D: f64) -> f64; Equal to
    /// > $$T^2\left(\frac{\partial^2a}{\partial T^2}\right)_D
    /// > =T^2\left(\frac{\partial^2a^i}{\partial T^2}\right)_D
    /// > +T^2\left(\frac{\partial^2a^r}{\partial T^2}\right)_D
    /// > =iT2(T)+rT2D0(T,D)$$
    fn aT2D0(&mut self, T: f64, D: f64) -> f64 {
        if self.aT2D0.T != T || self.aT2D0.D != D {
            self.aT2D0.T = T;
            self.aT2D0.D = D;
            self.aT2D0.value = self.ai.iT2(T) + self.ar.rT2D0(T, D);
        }
        self.aT2D0.value
    }
    /// shit-code
    fn aT0D0_sub_aT1D0(&mut self, T: f64, D: f64) -> f64 {
        if self.aT0D0_sub_aT1D0.T != T || self.aT0D0_sub_aT1D0.D != D {
            self.aT0D0_sub_aT1D0.T = T;
            self.aT0D0_sub_aT1D0.D = D;
            self.aT0D0_sub_aT1D0.value =
                self.ai.iT0(T) + self.ar.rT0D0(T, D) - self.ai.iT1(T) - self.ar.rT1D0(T, D);
        }
        self.aT0D0_sub_aT1D0.value
    }
}
/// Calculate thermodynamic properties of fundumental helmholtz equation of state.
#[allow(non_snake_case)]
impl<I: CalcAi, R: CalcAr> GenericA<I, R> {
    /// > $$Z
    /// > =\frac{1}{RT}D\left(\frac{\partial a}{\partial D}\right)_T$$
    fn Z(&mut self, T: f64, D: f64) -> f64 {
        self.aT0D1(T, D) / self.R / T
    }
    /// > $$p
    /// > =D^2\left(\frac{\partial a}{\partial D}\right)_T$$
    fn p(&mut self, T: f64, D: f64) -> f64 {
        D * self.aT0D1(T, D)
    }
    /// > $$Dp\\_DT\\_D=\left(\frac{\partial p}{\partial T}\right)_D
    /// > =D^2\left(\frac{\partial^2a}{\partial D\partial T}\right)$$
    fn Dp_DT_D(&mut self, T: f64, D: f64) -> f64 {
        D * self.aT1D1(T, D) / T
    }
    /// > $$Dp\\_DD\\_T=\left(\frac{\partial p}{\partial D}\right)_T
    /// > =2D\left(\frac{\partial a}{\partial D}\right)_T
    /// > +D^2\left(\frac{\partial^2a}{\partial D^2}\right)_T$$
    fn Dp_DD_T(&mut self, T: f64, D: f64) -> f64 {
        2.0 * self.aT0D1(T, D) + self.aT0D2(T, D)
    }
    /// > $$c_v
    /// > =-T\left(\frac{\partial^2a}{\partial T^2}\right)_D$$
    fn cv(&mut self, T: f64, D: f64) -> f64 {
        -self.aT2D0(T, D) / T
    }
    /// > $$c_p
    /// > =-T\left(\frac{\partial^2a}{\partial T^2}\right)_D
    /// > +TD\left(\frac{\partial^2a}{\partial T\partial D}\right)^2
    /// > \left[2\left(\frac{\partial a}{\partial D}\right)_T
    /// > +D\left(\frac{\partial^2a}{\partial D^2}\right)_T\right]^{-1}$$
    fn cp(&mut self, T: f64, D: f64) -> f64 {
        -self.aT2D0(T, D) / T
            + self.aT1D1(T, D).powi(2) / T / (2.0 * self.aT0D1(T, D) + self.aT0D2(T, D))
    }
    /// > $$w
    /// > =2D\left(\frac{\partial a}{\partial D}\right)_T
    /// > +D^2\left(\frac{\partial^2a}{\partial D^2}\right)
    /// > -D^2\left(\frac{\partial^2a}{\partial D\partial T}\right)^2
    /// > \left(\frac{\partial^2a}{\partial T^2}\right)^{-1}$$
    fn w(&mut self, T: f64, D: f64) -> f64 {
        let w2 =
            2.0 * self.aT0D1(T, D) + self.aT0D2(T, D) - self.aT1D1(T, D).powi(2) / self.aT2D0(T, D);
        if self.R < 10.0 {
            (w2 / self.M).sqrt()
        } else {
            w2.sqrt()
        }
    }
    /// > $$s
    /// > =-\left(\frac{\partial a}{\partial T}\right)_D$$
    fn s(&mut self, T: f64, D: f64) -> f64 {
        -self.aT1D0(T, D) / T
    }
    /// > $$Ds\\_DT\\_D=\left(\frac{\partial s}{\partial T}\right)_D
    /// > =-\left(\frac{\partial^2a}{\partial T^2}\right)_D$$
    fn Ds_DT_D(&mut self, T: f64, D: f64) -> f64 {
        -self.aT2D0(T, D) / T.powi(2)
    }
    /// > $$Ds\\_DD\\_T=\left(\frac{\partial s}{\partial D}\right)_T
    /// > =-\left(\frac{\partial^2a}{\partial T\partial D}\right)$$
    fn Ds_DD_T(&mut self, T: f64, D: f64) -> f64 {
        -self.aT1D1(T, D) / T / D
    }
    /// > $$s\\_res
    /// > =-\left(\frac{\partial a^r}{\partial T}\right)_D$$
    fn s_res(&mut self, T: f64, D: f64) -> f64 {
        -self.ar.rT1D0(T, D) / T
    }
    /// > $$u
    /// > =a\left(T,D\right)
    /// > -T\left(\frac{\partial a}{\partial T}\right)_D$$
    fn u(&mut self, T: f64, D: f64) -> f64 {
        self.aT0D0_sub_aT1D0(T, D)
    }
    /// > $$u\\_res
    /// > =a^r\left(T,D\right)
    /// > -T\left(\frac{\partial a^r}{\partial T}\right)_D$$
    fn u_res(&mut self, T: f64, D: f64) -> f64 {
        self.ar.rT0D0(T, D) - self.ar.rT1D0(T, D)
    }
    /// > $$h
    /// > =a\left(T,D\right)
    /// > -T\left(\frac{\partial a}{\partial T}\right)_D
    /// > +D\left(\frac{\partial a}{\partial D}\right)_T$$
    fn h(&mut self, T: f64, D: f64) -> f64 {
        self.aT0D0_sub_aT1D0(T, D) + self.aT0D1(T, D)
    }
    /// > $$Dh\\_DT\\_D=\left(\frac{\partial h}{\partial T}\right)
    /// > =-T\left(\frac{\partial^2a}{\partial T^2}\right)_D
    /// > +D\left(\frac{\partial^2a}{\partial D\partial T}\right)$$
    fn Dh_DT_D(&mut self, T: f64, D: f64) -> f64 {
        (-self.aT2D0(T, D) + self.aT1D1(T, D)) / T
    }
    /// > $$Dh\\_DD\\_T=\left(\frac{\partial h}{\partial D}\right)_T
    /// > =2\left(\frac{\partial a}{\partial D}\right)_T
    /// > -T\left(\frac{\partial^2a}{\partial T\partial D}\right)
    /// > +D\left(\frac{\partial^2a}{\partial D^2}\right)_T$$
    fn Dh_DD_T(&mut self, T: f64, D: f64) -> f64 {
        (2.0 * self.aT0D1(T, D) - self.aT1D1(T, D) + self.aT0D2(T, D)) / D
    }
    /// > $$h\\_res
    /// > =a^r\left(T,D\right)
    /// > -T\left(\frac{\partial a^r}{\partial T}\right)_D
    /// > +D\left(\frac{\partial a^r}{\partial D}\right)_T$$
    fn h_res(&mut self, T: f64, D: f64) -> f64 {
        self.ar.rT0D0(T, D) - self.ar.rT1D0(T, D) + self.ar.rT0D1(T, D)
    }
    /// > $$a
    /// > =a\left(T,D\right)$$
    fn a(&mut self, T: f64, D: f64) -> f64 {
        self.aT0D0(T, D)
    }
    /// > $$a\\_res
    /// > =a^r\left(T,D\right)$$
    fn a_res(&mut self, T: f64, D: f64) -> f64 {
        self.ar.rT0D0(T, D)
    }
    /// > $$g
    /// > =a\left(T,D\right)
    /// > +D\left(\frac{\partial a}{\partial D}\right)_T$$
    fn g(&mut self, T: f64, D: f64) -> f64 {
        self.aT0D0(T, D) + self.aT0D1(T, D)
    }
    /// > $$Dg\\_DT\\_D=\left(\frac{\partial g}{\partial T}\right)_D
    /// > =\left(\frac{\partial a}{\partial T}\right)_D
    /// > +D\left(\frac{\partial^2a}{\partial D\partial T}\right)$$
    fn Dg_DT_D(&mut self, T: f64, D: f64) -> f64 {
        (self.aT1D0(T, D) + self.aT1D1(T, D)) / T
    }
    /// > $$Dg\\_DD\\_T=\left(\frac{\partial g}{\partial D}\right)_T
    /// > =2\left(\frac{\partial a}{\partial D}\right)
    /// > +D\left(\frac{\partial^2a}{\partial D^2}\right)_T$$
    fn Dg_DD_T(&mut self, T: f64, D: f64) -> f64 {
        (2.0 * self.aT0D1(T, D) + self.aT0D2(T, D)) / D
    }
    /// > $$g\\_res
    /// > =a^r\left(T,D\right)
    /// > +D\left(\frac{\partial a^r}{\partial D}\right)_T$$
    fn g_res(&mut self, T: f64, D: f64) -> f64 {
        self.ar.rT0D0(T, D) + self.ar.rT0D1(T, D)
    }
    /// > $$B
    /// > =\frac{1}{RT}\left(\frac{\partial a^r}{\partial D}\right)_T$$
    fn B(&mut self, T: f64, _D: f64) -> f64 {
        let D = 1E-16;
        self.ar.rT0D1(T, D) / D / self.R / T
    }
    /// > $$C
    /// > =\frac{1}{RT}\left(\frac{\partial^2a^r}{\partial D^2}\right)_T$$
    fn C(&mut self, T: f64, _D: f64) -> f64 {
        let D = 1E-16;
        self.ar.rT0D2(T, D) / D.powi(2) / self.R / T
    }
    /// > $$k_T
    /// > =-\frac{v}{p}\left(\frac{\partial p}{\partial v}\right)_T
    /// > =\frac{\rho}{p}\left(\frac{\partial p}{\partial\rho}\right)_T$$
    fn k_T(&mut self, T: f64, D: f64) -> f64 {
        D / self.p(T, D) * self.Dp_DD_T(T, D)
    }
    /// > $$k_s
    /// > =-\frac{v}{p}\left(\frac{\partial p}{\partial v}\right)_s
    /// > =\frac{\rho w^2}{p}$$
    fn k_s(&mut self, T: f64, D: f64) -> f64 {
        D / self.p(T, D) * self.w(T, D).powi(2)
    }
    /// > $$\kappa_T
    /// > =-\frac{1}{v}\left(\frac{\partial v}{\partial p}\right)_T
    /// > =\frac{1}{\rho}\left(\frac{\partial p}{\partial\rho}\right)_T^{-1}$$
    fn kappa_T(&mut self, T: f64, D: f64) -> f64 {
        1.0 / D / self.Dp_DD_T(T, D)
    }
    /// > $$\kappa_s
    /// > =-\frac{1}{v}\left(\frac{\partial v}{\partial p}\right)_s
    /// > =\frac{1}{\rho w^2}$$
    fn kappa_s(&mut self, T: f64, D: f64) -> f64 {
        1.0 / D / self.w(T, D).powi(2)
    }
}
/// Settings for fundumental helmholtz equation of state.
#[allow(non_snake_case)]
impl<I: CalcAi, R: CalcAr> Setting for GenericA<I, R> {
    fn set_mass_unit(&mut self) {
        if self.R < 10.0 {
            self.R /= self.M;
        }
        self.ai.set_R(self.R);
        self.ar.set_RM(self.R, self.M);
    }
    fn set_molar_unit(&mut self) {
        if self.R > 10.0 {
            self.R *= self.M;
        }
        self.ai.set_R(self.R);
        self.ar.set_RM(self.R, self.M);
    }
}
/// Flash calculation of fundumental helmholtz equation of state.
#[allow(non_snake_case)]
impl<I: CalcAi, R: CalcAr> Flash for GenericA<I, R> {
    /// Temperature and Density UNCHECKED
    fn td_unchecked(&mut self, T: f64, D: f64) {
        self.phase = Phase::One { T, D };
    }
    /// Critical point
    fn c_flash(&mut self) -> anyhow::Result<()> {
        Err(anyhow!(TlErr::NoImplementation))
    }
    /// Temperature of saturated state
    fn t_flash(&mut self, Ts: f64) -> anyhow::Result<()> {
        // Initial guessed value of saturated pressure
        let ps_guess = [1E3, 1E4, 1E5, 1E6, 2E6, 3E6, 4E6, 5E6, 6E6, 7E6, 8E6, 9E6];
        'outer: for ps in ps_guess.iter() {
            let mut p_diff: f64;
            // Iteration from gas phase: Zg=1
            let mut Dg = ps / (self.R * Ts);
            loop {
                p_diff = self.p(Ts, Dg) - ps;
                if (p_diff / ps).abs() < 1E-9 {
                    break;
                }
                Dg -= p_diff / self.Dp_DD_T(Ts, Dg);
                if Dg.is_sign_negative() {
                    continue 'outer;
                }
            }
            // Iteration from liquid phase: Zl=0.1
            let mut Dl = ps / (self.R * Ts * 0.1);
            loop {
                p_diff = self.p(Ts, Dl) - ps;
                if (p_diff / ps).abs() < 1E-9 {
                    break;
                }
                Dl -= p_diff / self.Dp_DD_T(Ts, Dl);
                if Dl.is_sign_negative() {
                    continue 'outer;
                }
            }
            // Loop to find the correct result
            if (Dg / Dl - Dl / Dg).abs() < 1E-6 {
                continue;
            }
            let (mut p_g, mut p_l, mut gibbs_g, mut gibbs_l): (f64, f64, f64, f64);
            let (mut P_diff, mut P_diff_Dg, mut P_diff_Dl): (f64, f64, f64);
            let (mut G_diff, mut G_diff_Dg, mut G_diff_Dl): (f64, f64, f64);
            loop {
                if !Dg.is_normal() || !Dl.is_normal() {
                    break;
                }
                p_g = self.p(Ts, Dg);
                p_l = self.p(Ts, Dl);
                gibbs_g = self.g(Ts, Dg);
                gibbs_l = self.g(Ts, Dl);
                if (p_g / p_l - p_l / p_g).abs() < 1E-6
                    && (gibbs_g / gibbs_l - gibbs_l / gibbs_g).abs() < 1E-6
                {
                    self.phase = Phase::Two { Ts, Dg, Dl, X: 1.0 };
                    return Ok(());
                } else {
                    P_diff = p_g - p_l;
                    P_diff_Dg = self.Dp_DD_T(Ts, Dg);
                    P_diff_Dl = -self.Dp_DD_T(Ts, Dl);
                    G_diff = gibbs_g - gibbs_l;
                    G_diff_Dg = self.Dg_DD_T(Ts, Dg);
                    G_diff_Dl = -self.Dg_DD_T(Ts, Dl);
                    Dg -= (P_diff * G_diff_Dl - G_diff * P_diff_Dl)
                        / (P_diff_Dg * G_diff_Dl - G_diff_Dg * P_diff_Dl);
                    Dl -= (P_diff * G_diff_Dg - G_diff * P_diff_Dg)
                        / (P_diff_Dl * G_diff_Dg - G_diff_Dl * P_diff_Dg);
                }
            }
        }
        Err(anyhow!(TlErr::NotConvForT))
    }
    /// Temperature and Density
    fn td_flash(&mut self, T: f64, D: f64) -> anyhow::Result<()> {
        self.t_flash(T)?;
        match self.phase {
            Phase::Two { Dg, Dl, .. } => {
                if D < Dg || D > Dl {
                    self.phase = Phase::One { T, D };
                    Ok(()) // one phase
                } else {
                    self.phase = Phase::Two {
                        Ts: T,
                        Dg,
                        Dl,
                        X: (1.0 / D - 1.0 / Dl) / (1.0 / Dg + 1.0 / Dl),
                    };
                    Ok(()) // two phase
                }
            }
            _ => Err(anyhow!(TlErr::NotConvForTD)), // shit-code
        }
    }
    /// Temperature and Pressure
    fn tp_flash(&mut self, T: f64, P: f64) -> anyhow::Result<()> {
        let mut p_diff: f64;
        // Iteration from gas phase: Zg=1
        let mut D_g = P / (self.R * T);
        loop {
            p_diff = self.p(T, D_g) - P;
            if (p_diff / P).abs() < 1E-9 {
                break;
            }
            D_g -= p_diff / self.Dp_DD_T(T, D_g);
            if D_g.is_sign_negative() {
                break;
            }
        }
        let gibbs_g = if D_g.is_sign_negative() || self.Dp_DD_T(T, D_g).is_sign_negative() {
            1E16
        } else {
            self.g(T, D_g)
        };
        // Iteration from liquid phase: Zl=0.1
        let mut D_l = P / (self.R * T * 0.1);
        loop {
            p_diff = self.p(T, D_l) - P;
            if (p_diff / P).abs() < 1E-9 {
                break;
            }
            D_l -= p_diff / self.Dp_DD_T(T, D_l);
            if D_l.is_sign_negative() {
                break;
            }
        }
        let gibbs_l = if D_l.is_sign_negative() || self.Dp_DD_T(T, D_l).is_sign_negative() {
            1E16
        } else {
            self.g(T, D_l)
        };
        // Select the correct output
        if gibbs_g < 1E16 && gibbs_l < 1E16 {
            if gibbs_g < gibbs_l {
                self.phase = Phase::One { T, D: D_g };
            } else {
                self.phase = Phase::One { T, D: D_l };
            }
            Ok(())
        } else if gibbs_g < 1E16 && gibbs_l == 1E16 {
            self.phase = Phase::One { T, D: D_g };
            Ok(())
        } else if gibbs_l < 1E16 && gibbs_g == 1E6 {
            self.phase = Phase::One { T, D: D_l };
            Ok(())
        } else {
            Err(anyhow!(TlErr::NotConvForTD))
        }
    }
}
/// Get thermodynamic properties of corresponding fluid phase.
#[allow(non_snake_case)]
impl<I: CalcAi, R: CalcAr> Prop for GenericA<I, R> {
    fn T(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, .. } => Ok(T),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn D(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { D, .. } => Ok(D),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn Z(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.Z(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn p(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.p(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn Dp_DT_D(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.Dp_DT_D(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn Dp_DD_T(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.Dp_DD_T(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn cv(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.cv(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn cp(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.cp(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn w(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.w(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn s(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.s(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn Ds_DT_D(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.Ds_DT_D(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn Ds_DD_T(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.Ds_DD_T(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn s_res(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.s_res(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn u(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.u(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn u_res(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.u_res(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn h(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.h(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn Dh_DT_D(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.Dh_DT_D(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn Dh_DD_T(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.Dh_DD_T(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn h_res(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.h_res(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn a(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.a(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn a_res(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.a_res(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn g(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.g(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn Dg_DT_D(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.Dg_DT_D(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn Dg_DD_T(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.Dg_DD_T(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn g_res(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.g_res(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn B(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.B(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn C(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.C(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn k_T(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.k_T(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn k_s(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.k_s(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn kappa_T(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.kappa_T(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn kappa_s(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.kappa_s(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn ps(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { .. } => Err(anyhow!(TlErr::NotInOnePhase)),
            Phase::Two { Ts, Dg, Dl, .. } => Ok(self.p(Ts, Dg) / 2.0 + self.p(Ts, Dl) / 2.0),
        }
    }
    fn Dgs(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { .. } => Err(anyhow!(TlErr::NotInOnePhase)),
            Phase::Two { Dg, .. } => Ok(Dg),
        }
    }
    fn Dls(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { .. } => Err(anyhow!(TlErr::NotInOnePhase)),
            Phase::Two { Dl, .. } => Ok(Dl),
        }
    }
    fn h_evap(&mut self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { .. } => Err(anyhow!(TlErr::NotInOnePhase)),
            Phase::Two { Ts, Dg, Dl, .. } => Ok(self.h(Ts, Dg) - self.h(Ts, Dl)),
        }
    }
}
