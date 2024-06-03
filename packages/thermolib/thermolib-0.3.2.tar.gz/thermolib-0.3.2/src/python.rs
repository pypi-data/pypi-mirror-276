/// A Python module implemented in Rust.
use crate::{HelmholtzPure, PcSaftPure, PrPure};
enum Models {
    Helmholtz(Box<HelmholtzPure>),
    PcSaft(PcSaftPure),
    Pr(PrPure),
}
use crate::{Flash, Prop, Setting};
use pyo3::prelude::*;
use pyo3::types::PyDict;
#[pymodule]
#[pyo3(name = "thermolib")] // Rename pymodule
pub fn pylib(_py: Python, pm: &PyModule) -> PyResult<()> {
    // The name of this function must match the `lib.name` in the `Cargo.toml`,
    // else python will not be able to import the module.
    pm.add_class::<NewModel>()?;
    Ok(())
}
#[pyclass]
pub struct NewModel {
    model: Models,
}
#[pymethods]
#[allow(non_snake_case)]
impl NewModel {
    #[new]
    #[pyo3(signature = (model, **kwargs))]
    fn new(model: &str, kwargs: Option<&PyDict>) -> Self {
        match model {
            "HELMHOLTZ" => {
                let kw = kwargs.expect("for model::HELMHOLTZ, necessary parameters = (fluid)");
                let fluid: String = kw
                    .get_item("fluid")
                    .expect("for model::HELMHOLTZ, necessary parameters = (fluid)")
                    .expect("for model::HELMHOLTZ, necessary parameters = (fluid)")
                    .extract()
                    .expect("for model::HELMHOLTZ, necessary parameters = (fluid = 'SO2')");
                NewModel {
                    model: Models::Helmholtz(Box::new(
                        HelmholtzPure::read_json(&(fluid + ".json")).expect("no fluid.json"),
                    )),
                }
            }
            "PCSAFT" => {
                let kw =
                    kwargs.expect("for model::PCSAFT, necessary parameters = (m,sigma,epsilon,M)");
                let m: f64 = kw
                    .get_item("m")
                    .expect("for model::PCSAFT, necessary parameter = (m)")
                    .expect("for model::PCSAFT, necessary parameter = (m)")
                    .extract()
                    .expect("for model::PCSAFT, necessary parameter = (m = 1.0)");
                let sigma: f64 = kw
                    .get_item("sigma")
                    .expect("for model::PCSAFT, necessary parameter = (sigma)")
                    .expect("for model::PCSAFT, necessary parameter = (sigma)")
                    .extract()
                    .expect("for model::PCSAFT, necessary parameter = (sigma = 1.0)");
                let epsilon: f64 = kw
                    .get_item("epsilon")
                    .expect("for model::PCSAFT, necessary parameter = (epsilon)")
                    .expect("for model::PCSAFT, necessary parameter = (epsilon)")
                    .extract()
                    .expect("for model::PCSAFT, necessary parameter = (epsilon = 1.0)");
                let M: f64 = kw
                    .get_item("M")
                    .expect("for model::PCSAFT, necessary parameter = (M)")
                    .expect("for model::PCSAFT, necessary parameter = (M)")
                    .extract()
                    .expect("for model::PCSAFT, necessary parameter = (M = 1.0)");
                NewModel {
                    model: Models::PcSaft(PcSaftPure::new_pc_saft(m, sigma, epsilon, M)),
                }
            }
            "PR" => {
                let kw = kwargs.expect("for model::PR, necessary parameters = (Tc,Pc,omega,M)");
                let Tc: f64 = kw
                    .get_item("Tc")
                    .expect("for model::PR, necessary parameter = (Tc)")
                    .expect("for model::PR, necessary parameter = (Tc)")
                    .extract()
                    .expect("for model::PR, necessary parameter = (Tc = 1.0)");
                let Pc: f64 = kw
                    .get_item("Pc")
                    .expect("for model::PR, necessary parameter = (Pc)")
                    .expect("for model::PR, necessary parameter = (Pc)")
                    .extract()
                    .expect("for model::PR, necessary parameter = (Pc = 1.0)");
                let omega: f64 = kw
                    .get_item("M")
                    .expect("for model::PR, necessary parameter = (omega)")
                    .expect("for model::PR, necessary parameter = (omega)")
                    .extract()
                    .expect("for model::PR, necessary parameter = (omega = 1.0)");
                let M: f64 = kw
                    .get_item("M")
                    .expect("for model::PR, necessary parameter = (M)")
                    .expect("for model::PR, necessary parameter = (M)")
                    .extract()
                    .expect("for model::PR, necessary parameter = (M = 1.0)");
                NewModel {
                    model: Models::Pr(PrPure::new_pr(Tc, Pc, omega, M)),
                }
            }
            _ => {
                panic!("error input, model = (HELMHOLTZ, PCSAFT, PR)");
            }
        }
    }
    fn set_molar_unit(&mut self) {
        match &mut self.model {
            Models::Helmholtz(model) => model.set_molar_unit(),
            Models::PcSaft(model) => model.set_molar_unit(),
            Models::Pr(model) => model.set_molar_unit(),
        }
    }
    fn set_mass_unit(&mut self) {
        match &mut self.model {
            Models::Helmholtz(model) => model.set_mass_unit(),
            Models::PcSaft(model) => model.set_mass_unit(),
            Models::Pr(model) => model.set_mass_unit(),
        }
    }
    fn td_unchecked(&mut self, T: f64, D: f64) {
        match &mut self.model {
            Models::Helmholtz(model) => model.td_unchecked(T, D),
            Models::PcSaft(model) => model.td_unchecked(T, D),
            Models::Pr(model) => model.td_unchecked(T, D),
        }
    }
    fn t_flash(&mut self, Ts: f64) -> anyhow::Result<()> {
        match &mut self.model {
            Models::Helmholtz(model) => model.t_flash(Ts),
            Models::PcSaft(model) => model.t_flash(Ts),
            Models::Pr(model) => model.t_flash(Ts),
        }
    }
    fn td_flash(&mut self, T: f64, D: f64) -> anyhow::Result<()> {
        match &mut self.model {
            Models::Helmholtz(model) => model.td_flash(T, D),
            Models::PcSaft(model) => model.td_flash(T, D),
            Models::Pr(model) => model.td_flash(T, D),
        }
    }
    fn tp_flash(&mut self, T: f64, P: f64) -> anyhow::Result<()> {
        match &mut self.model {
            Models::Helmholtz(model) => model.tp_flash(T, P),
            Models::PcSaft(model) => model.tp_flash(T, P),
            Models::Pr(model) => model.tp_flash(T, P),
        }
    }
    fn T(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.T(),
            Models::PcSaft(model) => model.T(),
            Models::Pr(model) => model.T(),
        }
    }
    fn D(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.D(),
            Models::PcSaft(model) => model.D(),
            Models::Pr(model) => model.D(),
        }
    }
    fn Z(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.Z(),
            Models::PcSaft(model) => model.Z(),
            Models::Pr(model) => model.Z(),
        }
    }
    fn p(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.p(),
            Models::PcSaft(model) => model.p(),
            Models::Pr(model) => model.p(),
        }
    }
    fn Dp_DT_D(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.Dp_DT_D(),
            Models::PcSaft(model) => model.Dp_DT_D(),
            Models::Pr(model) => model.Dp_DT_D(),
        }
    }
    fn Dp_DD_T(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.Dp_DD_T(),
            Models::PcSaft(model) => model.Dp_DD_T(),
            Models::Pr(model) => model.Dp_DD_T(),
        }
    }
    fn cv(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.cv(),
            Models::PcSaft(model) => model.cv(),
            Models::Pr(model) => model.cv(),
        }
    }
    fn cp(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.cp(),
            Models::PcSaft(model) => model.cp(),
            Models::Pr(model) => model.cp(),
        }
    }
    fn w(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.w(),
            Models::PcSaft(model) => model.w(),
            Models::Pr(model) => model.w(),
        }
    }
    fn s(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.s(),
            Models::PcSaft(model) => model.s(),
            Models::Pr(model) => model.s(),
        }
    }
    fn Ds_DT_D(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.Ds_DT_D(),
            Models::PcSaft(model) => model.Ds_DT_D(),
            Models::Pr(model) => model.Ds_DT_D(),
        }
    }
    fn Ds_DD_T(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.Ds_DD_T(),
            Models::PcSaft(model) => model.Ds_DD_T(),
            Models::Pr(model) => model.Ds_DD_T(),
        }
    }
    fn s_res(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.s_res(),
            Models::PcSaft(model) => model.s_res(),
            Models::Pr(model) => model.s_res(),
        }
    }
    fn u(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.u(),
            Models::PcSaft(model) => model.u(),
            Models::Pr(model) => model.u(),
        }
    }
    fn u_res(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.u_res(),
            Models::PcSaft(model) => model.u_res(),
            Models::Pr(model) => model.u_res(),
        }
    }
    fn h(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.h(),
            Models::PcSaft(model) => model.h(),
            Models::Pr(model) => model.h(),
        }
    }
    fn Dh_DT_D(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.Dh_DT_D(),
            Models::PcSaft(model) => model.Dh_DT_D(),
            Models::Pr(model) => model.Dh_DT_D(),
        }
    }
    fn Dh_DD_T(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.Dh_DD_T(),
            Models::PcSaft(model) => model.Dh_DD_T(),
            Models::Pr(model) => model.Dh_DD_T(),
        }
    }
    fn h_res(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.h_res(),
            Models::PcSaft(model) => model.h_res(),
            Models::Pr(model) => model.h_res(),
        }
    }
    fn a(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.a(),
            Models::PcSaft(model) => model.a(),
            Models::Pr(model) => model.a(),
        }
    }
    fn a_res(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.a_res(),
            Models::PcSaft(model) => model.a_res(),
            Models::Pr(model) => model.a_res(),
        }
    }
    fn g(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.g(),
            Models::PcSaft(model) => model.g(),
            Models::Pr(model) => model.g(),
        }
    }
    fn Dg_DT_D(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.Dg_DT_D(),
            Models::PcSaft(model) => model.Dg_DT_D(),
            Models::Pr(model) => model.Dg_DT_D(),
        }
    }
    fn Dg_DD_T(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.Dg_DD_T(),
            Models::PcSaft(model) => model.Dg_DD_T(),
            Models::Pr(model) => model.Dg_DD_T(),
        }
    }
    fn g_res(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.g_res(),
            Models::PcSaft(model) => model.g_res(),
            Models::Pr(model) => model.g_res(),
        }
    }
    fn B(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.B(),
            Models::PcSaft(model) => model.B(),
            Models::Pr(model) => model.B(),
        }
    }
    fn C(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.C(),
            Models::PcSaft(model) => model.C(),
            Models::Pr(model) => model.C(),
        }
    }
    fn k_T(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.k_T(),
            Models::PcSaft(model) => model.k_T(),
            Models::Pr(model) => model.k_T(),
        }
    }
    fn k_s(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.k_s(),
            Models::PcSaft(model) => model.k_s(),
            Models::Pr(model) => model.k_s(),
        }
    }
    fn kappa_T(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.kappa_T(),
            Models::PcSaft(model) => model.kappa_T(),
            Models::Pr(model) => model.kappa_T(),
        }
    }
    fn kappa_s(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.kappa_s(),
            Models::PcSaft(model) => model.kappa_s(),
            Models::Pr(model) => model.kappa_s(),
        }
    }
    fn ps(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.ps(),
            Models::PcSaft(model) => model.ps(),
            Models::Pr(model) => model.ps(),
        }
    }
    fn Dgs(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.Dgs(),
            Models::PcSaft(model) => model.Dgs(),
            Models::Pr(model) => model.Dgs(),
        }
    }
    fn Dls(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.Dls(),
            Models::PcSaft(model) => model.Dls(),
            Models::Pr(model) => model.Dls(),
        }
    }
    fn h_evap(&mut self) -> anyhow::Result<f64> {
        match &mut self.model {
            Models::Helmholtz(model) => model.h_evap(),
            Models::PcSaft(model) => model.h_evap(),
            Models::Pr(model) => model.h_evap(),
        }
    }
}
