
# core_traits::CalcAi

> fn iT0(&self, _T: f64) -> f64; Equal to =
> $$a^i\left(T,D\right)-RT\ln D$$

> fn iT0D1(&self, _T:f64) -> f64; Equal to = $+RT$

> fn iT0D2(&self, _T:f64) -> f64; Equal to = $-RT$

> fn iT1(&self, _T: f64) -> f64; Equal to =
> $$T\left(\frac{\partial a^i}{\partial T}\right)_D-RT\ln D$$

> fn iT1D1(&self, _T:f64) -> f64; Equal to = $+RT$

> fn iT1D2(&self, _T:f64) -> f64; Equal to = $-RT$

> fn iT2(&self, _T: f64) -> f64; Equal to =
> $$T^2\left(\frac{\partial^2 a^i}{\partial T^2}\right)_D$$

> fn iT2D1(&self, _T:f64) -> f64; Equal to = $0$

> fn iT2D2(&self, _T:f64) -> f64; Equal to = $0$

# core_traits::CalcAr

> fn rT0D0(&self, _T: f64, _D: f64) -> f64; Equal to =
> $$a^r\left(T,D\right)$$

> fn rT0D1(&self, _T: f64, _D: f64) -> f64; Equal to =
> $$D\left(\frac{\partial a^r}{\partial D}\right)_T$$

> fn rT0D2(&self, _T: f64, _D: f64) -> f64; Equal to =
> $$D^2\left(\frac{\partial^2a^r}{\partial D^2}\right)_T$$

> fn rT1D0(&self, _T: f64, _D: f64) -> f64; Equal to =
> $$T\left(\frac{\partial a^r}{\partial T}\right)_D$$

> fn rT1D1(&self, _T: f64, _D: f64) -> f64; Equal to =
> $$TD\left(\frac{\partial^2a^r}{\partial T\partial D}\right)$$

> fn rT2D0(&self, _T: f64, _D: f64) -> f64; Equal to =
> $$T^2\left(\frac{\partial^2a^r}{\partial T^2}\right)_D$$

