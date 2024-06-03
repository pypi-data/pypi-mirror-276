use crate::core::CalcAr;
/// residual fundumental helmholtz equation of state
/// transformed from pr equation of state
#[derive(Clone)]
#[allow(non_snake_case)]
pub struct PrAr {
    R: f64,
    Tc: f64,
    ac: f64,
    bc: f64, // b=bc
    kappa: f64,
}
#[allow(non_snake_case)]
impl PrAr {
    pub fn new(Tc: f64, Pc: f64, omega: f64, R: f64) -> Self {
        Self {
            R,
            Tc,
            ac: 0.45724 * R.powi(2) * Tc.powi(2) / Pc,
            bc: 0.07780 * R * Tc / Pc,
            kappa: 0.37464 + 1.54226 * omega - 0.26992 * omega.powi(2),
        }
    }
    pub fn R(&self) -> f64 {
        self.R
    }
    pub fn Tc(&self) -> f64 {
        self.Tc
    }
    pub fn b(&self) -> f64 {
        self.bc
    }
    /// > $$a\left(T\right)=
    /// > a\left(T_c\right)\left(1+\kappa-\kappa\sqrt{\frac{T}{T_c}}\right)^2$$
    pub fn a(&self, T: f64) -> f64 {
        self.ac * (1.0 + self.kappa - self.kappa * (T / self.Tc).sqrt()).powi(2)
    }
    /// > $$a_T\left(T\right)=
    /// > a\left(T_c\right)\left(-2\kappa\right)
    /// > \left(\frac{1+\kappa}{\sqrt{TT_c}}-\frac{\kappa}{T_c}\right)$$
    fn a_T(&self, T: f64) -> f64 {
        self.ac
            * (-2.0 * self.kappa)
            * ((1.0 + self.kappa) / (T * self.Tc).sqrt() - self.kappa / self.Tc)
    }
    /// > $$a_{TT}\left(T\right)=
    /// > a\left(T_c\right)\frac{\kappa\left(1+\kappa\right)}{\sqrt{T^3T_c}}$$
    fn a_TT(&self, T: f64) -> f64 {
        self.ac * self.kappa * (1.0 + self.kappa) / (T.powi(3) * self.Tc).sqrt()
    }
}
#[allow(non_snake_case)]
impl CalcAr for PrAr {
    /// > fn rT0D0(&self, T: f64, D: f64) -> f64; Equal to =  
    /// > $$a^r\left(T,D\right)=
    /// > -RT\ln\left|1-b\rho\right|
    /// > +\frac{a\left(T\right)}{2\sqrt{2}b}
    /// > \ln\left|
    /// > \frac{1+\left(1-\sqrt{2}\right)b\rho}{1+\left(1+\sqrt{2}\right)b\rho}
    /// > \right|$$
    fn rT0D0(&self, T: f64, D: f64) -> f64 {
        -self.R * T * (1.0 - self.bc * D).abs().ln()
            + self.a(T) / (2.0 * 2.0_f64.sqrt() * self.bc)
                * ((1.0 + (1.0 - 2.0_f64.sqrt()) * self.bc * D)
                    / (1.0 + (1.0 + 2.0_f64.sqrt()) * self.bc * D))
                    .abs()
                    .ln()
    }
    /// > fn rT0D1(&self, T: f64, D: f64) -> f64; Equal to =  
    /// > $$D\left(\frac{\partial a^r}{\partial D}\right)_T=
    /// > \rho\left(
    /// > \frac{bRT}{1-b\rho}
    /// > -\frac{a\left(T\right)}{1+2b\rho-b^2\rho^2}
    /// > \right)$$
    fn rT0D1(&self, T: f64, D: f64) -> f64 {
        D * (self.bc * self.R * T / (1.0 - self.bc * D)
            - self.a(T) / (1.0 + 2.0 * self.bc * D - (self.bc * D).powi(2)))
    }
    /// > fn rT0D2(&self, T: f64, D: f64) -> f64; Equal to =  
    /// > $$D^2\left(\frac{\partial^2a^r}{\partial D^2}\right)_T=
    /// > \rho^2\left(
    /// > -\frac{b^2RT}{\left(1-b\rho\right)^2}
    /// > -\frac{a\left(T\right)\left(2b-2b^2\rho\right)}{\left(1+2b\rho-b^2\rho^2\right)^2}
    /// > \right)$$
    fn rT0D2(&self, T: f64, D: f64) -> f64 {
        D.powi(2)
            * (-self.bc.powi(2) * self.R * T / (1.0 - self.bc * D).powi(2)
                - self.a(T) * (2.0 * self.bc - 2.0 * self.bc.powi(2) * D)
                    / (1.0 + 2.0 * self.bc * D - (self.bc * D).powi(2)).powi(2))
    }
    /// > fn rT1D0(&self, T: f64, D: f64) -> f64; Equal to =  
    /// > $$T\left(\frac{\partial a^r}{\partial T}\right)_D=
    /// > T\left(
    /// > -R\ln\left|1-b\rho\right|
    /// > +\frac{a_T\left(T\right)}{2\sqrt{2}b}
    /// > \ln\left|\frac{1+\left(1-\sqrt{2}\right)b\rho}{1+\left(1+\sqrt{2}\right)b\rho}\right|
    /// > \right)$$
    fn rT1D0(&self, T: f64, D: f64) -> f64 {
        T * (-self.R * (1.0 - self.bc * D).abs().ln()
            + self.a_T(T) / (2.0 * 2.0_f64.sqrt() * self.bc)
                * ((1.0 + (1.0 - 2.0_f64.sqrt()) * self.bc * D)
                    / (1.0 + (1.0 + 2.0_f64.sqrt()) * self.bc * D))
                    .abs()
                    .ln())
    }
    /// > fn rT1D1(&self, T: f64, D: f64) -> f64; Equal to =  
    /// > $$TD\left(\frac{\partial^2a^r}{\partial T\partial D}\right)=
    /// > T\rho\left(
    /// > \frac{bR}{1-b\rho}
    /// > -\frac{a_T\left(T\right)}{1+2b\rho-b^2\rho^2}
    /// > \right)$$
    fn rT1D1(&self, T: f64, D: f64) -> f64 {
        T * D
            * (self.bc * self.R / (1.0 - self.bc * D)
                - self.a_T(T) / (1.0 + 2.0 * self.bc * D - (self.bc * D).powi(2)))
    }
    /// > fn rT2D0(&self, T: f64, D: f64) -> f64; Equal to =  
    /// > $$T^2\left(\frac{\partial^2a^r}{\partial T^2}\right)_D=
    /// > T^2\frac{a_{TT}\left(T\right)}{2\sqrt{2}b}
    /// > \ln\left|\frac{1+\left(1-\sqrt{2}\right)b\rho}{1+\left(1+\sqrt{2}\right)b\rho}\right|$$
    fn rT2D0(&self, T: f64, D: f64) -> f64 {
        T.powi(2) * self.a_TT(T) / (2.0 * 2.0_f64.sqrt() * self.bc)
            * ((1.0 + (1.0 - 2.0_f64.sqrt()) * self.bc * D)
                / (1.0 + (1.0 + 2.0_f64.sqrt()) * self.bc * D))
                .abs()
                .ln()
    }
    /// Used for trait::Setting
    fn set_RM(&mut self, R: f64, _M: f64) {
        self.R = R;
    }
}
