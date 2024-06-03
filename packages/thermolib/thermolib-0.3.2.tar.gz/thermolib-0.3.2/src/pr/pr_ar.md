
# impl core_traits::CalcAr for PrAr { }

> fn rT0D0(&self, T: f64, D: f64) -> f64; Equal to =  
> $$a^r\left(T,D\right)=
> -RT\ln\left|1-b\rho\right|
> +\frac{a\left(T\right)}{2\sqrt{2}b}
> \ln\left|
> \frac{1+\left(1-\sqrt{2}b\rho\right)}{1+\left(1+\sqrt{2}\right)b\rho}
> \right|$$

> fn rT0D1(&self, T: f64, D: f64) -> f64; Equal to =  
> $$D\left(\frac{\partial a^r}{\partial D}\right)_T=
> \rho\left(
> \frac{bRT}{1-b\rho}
> -\frac{a\left(T\right)}{1+2b\rho-b^2\rho^2}
> \right)$$

> fn rT0D2(&self, T: f64, D: f64) -> f64; Equal to =  
> $$D^2\left(\frac{\partial^2a^r}{\partial D^2}\right)_T=
> \rho^2\left(
> -\frac{b^2RT}{\left(1-b\rho\right)^2}
> -\frac{a\left(T\right)\left(2b-2b^2\rho\right)}{\left(1+2b\rho-b^2\rho^2\right)^2}
> \right)$$

> fn rT1D0(&self, T: f64, D: f64) -> f64; Equal to =  
> $$T\left(\frac{\partial a^r}{\partial T}\right)_D=
> T\left(
> -R\ln\left|1-b\rho\right|
> +\frac{a_T\left(T\right)}{2\sqrt{2}b}
> \ln\left|\frac{1+\left(1-\sqrt{2}\right)b\rho}{1+\left(1+\sqrt{2}\right)b\rho}\right|
> \right)$$

> fn rT1D1(&self, T: f64, D: f64) -> f64; Equal to =  
> $$TD\left(\frac{\partial^2a^r}{\partial T\partial D}\right)=
> T\rho\left(
> \frac{bR}{1-b\rho}
> -\frac{a_T\left(T\right)}{1+2b\rho-b^2\rho^2}
> \right)$$

> fn rT2D0(&self, T: f64, D: f64) -> f64; Equal to =  
> $$T^2\left(\frac{\partial^2a^r}{\partial T^2}\right)_D=
> T^2\frac{a _{TT}\left(T\right)}{2\sqrt{2}b}
> \ln\left|\frac{1+\left(1-\sqrt{2}\right)b\rho}{1+\left(1+\sqrt{2}\right)b\rho}\right|$$

# impl PrAr { }

> $$a\left(T\right)=
> a\left(T_c\right)\left(1+\kappa-\kappa\sqrt{\frac{T}{T_c}}\right)^2$$

> $$a_T\left(T\right)=
> a\left(T_c\right)\left(-2\kappa\right)
> \left(\frac{1+\kappa}{\sqrt{TT_c}}-\frac{\kappa}{T_c}\right)$$

> $$a_{TT}\left(T\right)=
> a\left(T_c\right)\frac{\kappa\left(1+\kappa\right)}{\sqrt{T^3T_c}}$$

