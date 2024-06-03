/// All module implemented for pr equation of state.
mod density;
mod pr_a;
mod pr_ar;
pub use density::calc_density_using_pr;
pub use pr_a::PrA as PrPure;
pub use pr_ar::PrAr;
