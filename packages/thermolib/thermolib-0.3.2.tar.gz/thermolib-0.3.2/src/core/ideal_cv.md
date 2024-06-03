
# ideal_cv::IdealCv

> $$a^0\left(T,\rho\right)
> =RT\ln\rho
> +RT\ln T
> +h^0_0
> +T\left(-s^0_0-R-R\ln\rho_0T_0\right)
> +\int_{T_0}^Tc_p^0dT-T\int_{T_0}^T\frac{c_p^0}{T}dT$$

> $$T\left(\frac{\partial a^0}{\partial T}\right)
> =RT\ln\rho
> +RT\left(\ln T+1\right)
> +T\left(-s^0_0-R-R\ln\rho_0T_0\right)
> +...$$

> $$T^2\left(\frac{\partial^2a^0}{\partial T^2}\right)
> =RT
> +...$$

> $$\frac{c_p^0}{R}
> =c_0
> +\sum c_iT^{t_i}
> +\sum\nu_i
> \left(\frac{\mu_i}{T}\right)^2
> \frac{\exp\left(-\mu_i/T\right)}{\left(\exp\left(\mu_i/T\right)-1\right)^2}$$

## coefficient

> $$\int_{T_0}^Tc_p^0dT-T\int_{T_0}^T\frac{c_p^0}{T}dT
> =-c_0RT\ln T
> -Rc_0T_0
> +RT\left(c_0+c_0\ln T_0\right)$$

> $$T\left(\frac{\partial a^0}{\partial T}\right)
> =-c_0RT\left(\ln T+1\right)
> +RT\left(c_0+\ln T_0\right)$$

> $$T^2\left(\frac{\partial^2a^0}{\partial T^2}\right)
> =-c_0RT$$

## polynomial term

> $$\int_{T_0}^Tc_p^0dT-T\int_{T_0}^T\frac{c_p^0}{T}dT
> =-RT\sum\frac{c_iT^{t_i}}{t_i\left(t_i+1\right)}
> -R\sum\frac{c_iT_0^{t_i+1}}{t_i+1}
> +RT\sum\frac{c_iT_0^{t_i}}{t_i}$$

> $$T\left(\frac{\partial a^0}{\partial T}\right)
> =-RT\sum\frac{c_iT^{t_i}}{t_i}
> +RT\sum\frac{c_iT_0^{t_i}}{t_i}$$

> $$T^2\left(\frac{\partial^2a^0}{\partial T^2}\right)
> =-RT\sum c_iT^{t_i}$$

## plank-einstein term

> $$\int_{T_0}^Tc_p^0dT-T\int_{T_0}^T\frac{c_p^0}{T}dT
> =RT\sum\nu_i\ln\left(1-\exp\left(-\mu_i/T\right)\right)
> +R\sum\frac{\nu_u\mu_i}{1-\exp\left(\mu_i/T_0\right)}
> +RT\left(
> -\sum\nu_i\frac{\mu_i/T_0}{1-\exp\left(\mu_i/T_0\right)}
> -\sum\nu_i\ln\left(1-\exp\left(-\mu_i/T_0\right)\right)
> \right)$$

> $$T\left(\frac{\partial a^0}{\partial T}\right)
> =RT\left(
> \sum\nu_i\ln\left(1-\exp\left(-\mu_i/T\right)\right)
> -\sum\nu_i\frac{\mu_i}{T}\frac{\exp\left(-\mu_i/T\right)}{1-\exp\left(-\mu_i/T\right)}
> \right)
> +RT\left(
> -\sum\nu_i\frac{\mu_i/T_0}{1-\exp\left(\mu_i/T_0\right)}
> -\sum\nu_i\ln\left(1-\exp\left(-\mu_i/T_0\right)\right)
> \right)$$

> $$T^2\left(\frac{\partial^2a^0}{\partial T^2}\right)
> =-RT\sum\nu_i\left(\frac{\mu_i}{T}\right)^2
> \frac{\exp\left(-\mu_i/T\right)}{\left(1-\exp\left(-\mu_i/T\right)\right)^2}$$

