
# generic_a::implementation[private]

> fn aT0D0(&self, T: f64, D: f64) -> f64; Equal to
> $$a\left(T,D\right)
> =a^i\left(T,D\right)
> +a^r\left(T,D\right)
> =iT0(T)+RT\ln D+rT0D0(T,D)$$

> fn aT0D1(&self, T: f64, D: f64) -> f64; Equal to
> $$D\left(\frac{\partial a}{\partial D}\right)_T
> =D\left(\frac{\partial a^i}{\partial D}\right)_T
> +D\left(\frac{\partial a^r}{\partial D}\right)_T
> =RT+rT0D1(T,D)$$

> fn aT0D2(&self, T: f64, D: f64) -> f64; Equal to
> $$D^2\left(\frac{\partial^2a}{\partial D^2}\right)_T
> =D^2\left(\frac{\partial^2a^i}{\partial D^2}\right)_T
> +D^2\left(\frac{\partial^2a^r}{\partial D^2}\right)_T
> =-RT+rT0D2(T,D)$$

> fn aT1D0(&self, T: f64, D: f64) -> f64; Equal to
> $$T\left(\frac{\partial a}{\partial T}\right)_D
> =T\left(\frac{\partial a^i}{\partial T}\right)_D
> +T\left(\frac{\partial a^r}{\partial T}\right)_D
> =iT1(T)+RT\ln D+rT1D0(T,D)$$

> fn aT1D1(&self, T: f64, D: f64) -> f64; Equal to
> $$TD\left(\frac{\partial^2a}{\partial T\partial D}\right)
> =TD\left(\frac{\partial^2a^i}{\partial T\partial D}\right)
> +TD\left(\frac{\partial^2a^r}{\partial T\partial D}\right)
> =RT+rT1D1(T,D)$$

> fn aT2D0(&self, T: f64, D: f64) -> f64; Equal to
> $$T^2\left(\frac{\partial^2a}{\partial T^2}\right)_D
> =T^2\left(\frac{\partial^2a^i}{\partial T^2}\right)_D
> +T^2\left(\frac{\partial^2a^r}{\partial T^2}\right)_D
> =iT2(T)+rT2D0(T,D)$$

# generic_a::implementation[private]

> $$Z
> =\frac{1}{RT}D\left(\frac{\partial a}{\partial D}\right)_T$$

> $$p
> =D^2\left(\frac{\partial a}{\partial D}\right)_T$$

> $$Dp\\_DT\\_D=\left(\frac{\partial p}{\partial T}\right)_D
> =D^2\left(\frac{\partial^2a}{\partial D\partial T}\right)$$

> $$Dp\\_DD\\_T=\left(\frac{\partial p}{\partial D}\right)_T
> =2D\left(\frac{\partial a}{\partial D}\right)_T
> +D^2\left(\frac{\partial^2a}{\partial D^2}\right)_T$$

> $$c_v
> =-T\left(\frac{\partial^2a}{\partial T^2}\right)_D$$

> $$c_p
> =-T\left(\frac{\partial^2a}{\partial T^2}\right)_D
> +TD\left(\frac{\partial^2a}{\partial T\partial D}\right)^2
> \left[2\left(\frac{\partial a}{\partial D}\right)_T
> +D\left(\frac{\partial^2a}{\partial D^2}\right)_T\right]^{-1}$$

> $$w
> =2D\left(\frac{\partial a}{\partial D}\right)_T
> +D^2\left(\frac{\partial^2a}{\partial D^2}\right)
> -D^2\left(\frac{\partial^2a}{\partial D\partial T}\right)^2
> \left(\frac{\partial^2a}{\partial T^2}\right)^{-1}$$

> $$s
> =-\left(\frac{\partial a}{\partial T}\right)_D$$

> $$Ds\\_DT\\_D=\left(\frac{\partial s}{\partial T}\right)_D
> =-\left(\frac{\partial^2a}{\partial T^2}\right)_D$$

> $$Ds\\_DD\\_T=\left(\frac{\partial s}{\partial D}\right)_T
> =-\left(\frac{\partial^2a}{\partial T\partial D}\right)$$

> $$s\\_res
> =-\left(\frac{\partial a^r}{\partial T}\right)_D$$

> $$u
> =a\left(T,D\right)
> -T\left(\frac{\partial a}{\partial T}\right)_D$$

> $$u\\_res
> =a^r\left(T,D\right)
> -T\left(\frac{\partial a^r}{\partial T}\right)_D$$

> $$h
> =a\left(T,D\right)
> -T\left(\frac{\partial a}{\partial T}\right)_D
> +D\left(\frac{\partial a}{\partial D}\right)_T$$

> $$Dh\\_DT\\_D=\left(\frac{\partial h}{\partial T}\right)
> =-T\left(\frac{\partial^2a}{\partial T^2}\right)_D
> +D\left(\frac{\partial^2a}{\partial D\partial T}\right)$$

> $$Dh\\_DD\\_T=\left(\frac{\partial h}{\partial D}\right)_T
> =2\left(\frac{\partial a}{\partial D}\right)_T
> -T\left(\frac{\partial^2a}{\partial T\partial D}\right)
> +D\left(\frac{\partial^2a}{\partial D^2}\right)_T$$

> $$h\\_res
> =a^r\left(T,D\right)
> -T\left(\frac{\partial a^r}{\partial T}\right)_D
> +D\left(\frac{\partial a^r}{\partial D}\right)_T$$

> $$a
> =a\left(T,D\right)$$

> $$a\\_res
> =a^r\left(T,D\right)$$

> $$g
> =a\left(T,D\right)
> +D\left(\frac{\partial a}{\partial D}\right)_T$$

> $$Dg\\_DT\\_D=\left(\frac{\partial g}{\partial T}\right)_D
> =\left(\frac{\partial a}{\partial T}\right)_D
> +D\left(\frac{\partial^2a}{\partial D\partial T}\right)$$

> $$Dg\\_DD\\_T=\left(\frac{\partial g}{\partial D}\right)_T
> =2\left(\frac{\partial a}{\partial D}\right)
> +D\left(\frac{\partial^2a}{\partial D^2}\right)_T$$

> $$g\\_res
> =a^r\left(T,D\right)
> +D\left(\frac{\partial a^r}{\partial D}\right)_T$$

> $$B
> =\frac{1}{RT}\left(\frac{\partial a^r}{\partial D}\right)_T$$

> $$C
> =\frac{1}{RT}\left(\frac{\partial^2a^r}{\partial D^2}\right)_T$$

> $$k_T
> =-\frac{v}{p}\left(\frac{\partial p}{\partial v}\right)_T
> =\frac{\rho}{p}\left(\frac{\partial p}{\partial\rho}\right)_T$$

> $$k_s
> =-\frac{v}{p}\left(\frac{\partial p}{\partial v}\right)_s
> =\frac{\rho w^2}{p}$$

> $$\kappa_T
> =-\frac{1}{v}\left(\frac{\partial v}{\partial p}\right)_T
> =\frac{1}{\rho}\left(\frac{\partial p}{\partial\rho}\right)_T^{-1}$$

> $$\kappa_s
> =-\frac{1}{v}\left(\frac{\partial v}{\partial p}\right)_s
> =\frac{1}{\rho w^2}$$

