import pyspinw
m = pyspinw.Matlab()


def pvoigt(x=None, p=None, **kwargs):
    """
% pseudovoigt function
%
% ### Syntax
%
% `y = func.pvoigt(x,p)`
%
% ### Description
%
% `y = func.pvoigt(x,p)` calculates the $y$ values for a pseudovoigt
% function evaluated at $x$ and with parameters defined in `p`. The
% Gaussian and Lorentzian functions are normalized to amplitude 1 before
% the mixing.
%
% ### Input Arguments
%
% `x`
% : Coordinate vector where the function will be evaluated.
%
% `p`
% : Parameter vector with the following elements `p=[A x0 wG wL mu]` where:
%   * `A`       amplitude of the signal,
%   * `x0`      center of the peak,
%   * `wG`      FWHM value of the Gaussian, has to be positive,
%   * `wL`      FWHM value of the Lorentzian, has to be positive,
%   * `mu`      mixing constant, `mu=1` for pure Lorenzian, `mu=0` for pure
%               Gaussian, the value has to be within the $(0,1)$ range.
%
% ### See Also
%
% [swfunc.gaussfwhm] \| [swfunc.lorfwhm] \| [swfunc.voigtfwhm]
%
% *[FWHM]: Full Width at Half Maximum
%
    """
    args = tuple(v for v in [x, p] if v is not None)
    return m.swfunc.pvoigt(*args, **kwargs)


def gaussfwhm(x=None, p=None, **kwargs):
    """
% normalized Gaussian function
%
% ### Syntax
%
% `y = func.gaussfwhm(x,p)`
%
% ### Description
%
% `y = func.gaussfwhm(x,p)` calculates the $y$ values for a Gaussian
% function evaluated at $x$ and with parameters defined in `p`.
%
% ### Input Arguments
%
% `x`
% : Coordinate vector where the function will be evaluated.
%
% `p`
% : Parameter vector with the following elements `p=[I x0 FWHM]` where:
%   * `I`       integrated intensity,
%   * `x0`      center,
%   * `FWHM`    Full Width at Half Maximum value.
%
% ### See Also
%
% [swfunc.pvoigt] \| [swfunc.gauss]
%
    """
    args = tuple(v for v in [x, p] if v is not None)
    return m.swfunc.gaussfwhm(*args, **kwargs)


def gauss(x=None, p=None, **kwargs):
    """
% normalized Gaussian function
%
% ### Syntax
%
% `y = func.gauss(x,p)`
%
% ### Description
%
% `y = func.gauss(x,p)` calculates the $y$ values for a Gaussian function
% evaluated at $x$ and with parameters defined in `p`.
%
% ### Input Arguments
%
% `x`
% : Coordinate vector where the function will be evaluated.
%
% `p`
% : Parameter vector with the following elements `p=[I x0 \\sigma]` where:
%   * `I` integrated intensity,
%   * `x0` center,
%   * `\\sigma` standard deviation.
%
% ### See Also
%
% [swfunc.pvoigt] \| [swfunc.gaussfwhm]
%
    """
    args = tuple(v for v in [x, p] if v is not None)
    return m.swfunc.gauss(*args, **kwargs)


def lorfwhm(x=None, p=None, **kwargs):
    """
% normalized Lorentzian function
%
% ### Syntax
%
% `y = func.lorfwhm(x,p)`
%
% ### Description
%
% `y = func.lorfwhm(x,p)` calculates the $y$ values for a Lorentzian
% function evaluated at $x$ and with parameters defined in `p`.
%
% ### Input Arguments
%
% `x`
% : Coordinate vector where the function will be evaluated.
%
% `p`
% : Parameter vector with the following elements `p=[I x0 FWHM]` where:
%   * `I`       integrated intensity,
%   * `x0`      center,
%   * `FWHM`    Full Width at Half Maximum value.
%
% ### See Also
%
% [swfunc.pvoigt] \| [swfunc.gaussfwhm]
%
    """
    args = tuple(v for v in [x, p] if v is not None)
    return m.swfunc.lorfwhm(*args, **kwargs)


def voigtfwhm(x=None, p=None, **kwargs):
    """
% normalized voigt function
%
% ### Syntax
%
% `y = fitfun.voigtfwhm(x,p)`
%
% ### Description
%
% `y = fitfun.voigtfwhm(x,p)` calculates the voigt function. The width
% parameters define the FWHM value. The
% integral of the function is normalized assuming that $dx = 1$. The
% conversion between different width:
%
% * gamma parameter of the Lorentzian $\gamma = w_L/2$
% * standard deviation of the Gaussian $\sigma = w_G/\sqrt{8\cdot\ln(2)}$
%
% ### Input Arguments
%
% `x`
% : Input coordinates where the function will be calculated.
%
% `p`
% : Parameters in a vector with elements `[A x0 wG wL]`:
%
%   * `A` integral of the output assuming $dx=1$ (for different $dx$
%      multiply the amplitude with $dx$ to keep the integral constant).
%   * `x0` peak center positions.
%   * `wG` FWHM of the Gaussian component.
%   * `wL` FWHM of the Lorentzian component.
%
%
% ### See also
%
% [swfunc.gauss] \| [swfunc.gaussfwhm] \| [swfunc.pvoigt]
%
% *[FWHM]: Full Width at Half Maximum
%
    """
    args = tuple(v for v in [x, p] if v is not None)
    return m.swfunc.voigtfwhm(*args, **kwargs)


