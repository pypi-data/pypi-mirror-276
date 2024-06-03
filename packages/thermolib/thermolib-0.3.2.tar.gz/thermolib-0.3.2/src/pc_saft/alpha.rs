use super::AlphaR;
use crate::core::{GenericA, IdealCv};
/// PC-SAFT equation of state
pub type Alpha = GenericA<IdealCv, AlphaR>;
/// Methods of PC-SAFT equation of state
#[allow(non_snake_case)]
impl Alpha {
    pub fn new_pc_saft(m: f64, sigma: f64, epsilon: f64, M: f64) -> Self {
        Self::new(IdealCv::default(), AlphaR::new(m, sigma, epsilon, M), M)
    }
}
/// unit test
#[cfg(test)]
mod tests {
    use super::*;
    use crate::{Flash, Prop};
    #[test]
    #[allow(non_snake_case)]
    fn test_pc_saft_alpha() {
        let mut pc_saft = Alpha::new(
            IdealCv::default(),
            AlphaR::new(1.6069, 3.5206, 191.42, 30.07),
            30.07,
        ); // parameters for ethane
        let T = 300.0; // K
        let D = 1000.0; // mol/m3
        if let Err(_) = pc_saft.td_flash(T, D) {
            panic!("td_flash failed at T = {} K and D = {} mol/m3", T, D);
        }
        let p = if let Ok(p) = pc_saft.p() {
            p
        } else {
            panic!("td_flash at T = {} K and D = {} mol.m3 is Phase::Two", T, D);
        };
        if let Err(_) = pc_saft.tp_flash(T, p) {
            panic!("tp_flash failed at T = {} K and p = {} Pa", T, p);
        } else {
            assert!(pc_saft.D().unwrap() / D - 1.0 < 1E-12);
        }
        if let Err(_) = pc_saft.t_flash(T) {
            panic!("t_flash failed at T = {} K", T);
        }
    }
}
