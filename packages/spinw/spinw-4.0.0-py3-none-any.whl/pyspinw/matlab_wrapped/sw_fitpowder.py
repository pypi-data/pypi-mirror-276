import pyspinw
m = pyspinw.Matlab()

from libpymcr import MatlabProxyObject
from libpymcr.utils import get_nlhs

class sw_fitpowder(MatlabProxyObject):
    """
  Class to fit powder averaged spectra to inelastic neutron scattering data
  
  ### Syntax
  
  `fitpow = <strong>sw_fitpowder</strong>(swobj, data, fit_func, model_params, Name,Value)`
  
  ### Description
  
  Fits powder averaged spectra to constant-|Q| cuts or 2D |Q| vs en slices
  of inelastic neutron scattering data accounting for the instrument 
  resolution  
  
  ### Input Arguments
  
  `swobj`
  : spinwave object with magnetic structure defined
 
  `data`
  : Possible inputs depend on dimensionality of the data:
    * 2D data 
      Either a struct containing fields `x`, `y` and `e` or a 2D HORACE 
      object (sqw or d2d)
      where `y` is a matrix of intensities with shape (N|Q|, NEnergy)
            `e` is a matrix of errorsbars with shape (N|Q|, NEnergy)
            `x` is a cell array of size (1,2): 
                x{1} contains a vector of energy bin centers
                x{2} contains a vector of |Q| bin centers.
    * Vector of 1d datasets at constant |Q|
      Either a struct containing fields `x`, `y` and `e`  `qmin` and `qmax`
      or a 1D HORACE object (sqw or d1d)
      where `y` is a vector of intensities with shape (1, NEnergy)
            `e` is a vector of errorsbars with shape (1, NEnergy)
            `x` is a vector of energy bin centers
                x{2} contains a vector of |Q| bin centers.
            `qmin` is a scalar denoting the lower Q value of the cut
            `qmax` is a scalar denoting the upper Q value of the cut
  
  `fit_func`
  : Function handle changing the interactions in the spinwave model.
    For example if the spinw model had matrices `J1`, `J2` and `D` then a
    `fit_func` could be
    ```
    fit_func =  @(obj, p) matparser(obj, 'param', p, 'mat', 
                                    {'J1', 'J2', 'D(3,3)'}, 'init', true);
    ```
 
  `model_params`
  : Vector of initial paramers to pass to fit_func
 
  `background_strategy` (optional)
  : A string determining the type of background:
    * `planar` (default) - 2D planar background in |Q| and energy transfer
    * `independent` - 1D linear background as function of energy transfer
 
  `nQ` (optional)
  : Scalar int correpsonding to number of Q-points to subdivide cuts into 
    for averaging
 
  ### Output Arguments
  
  `'result'` 
  : cell array containing output of <strong>sw_fitpowder</strong>.optimizer
    For ndbase optimizers in the spinw package then the reuslt can be
    unpacked as follows
    ```
    [fitted_params, cost_val, stat] = result{:}
    ```
    See docs for e.g. ndbase.simplex (default) for details
  
  ### Examples
  
  ```
  >> % init spinw object
  >> J1 = -0.05;
  >> J2 = 0.3;
  >> D = 0.05;
  >> mnf2 = spinw;
  >> mnf2.genlattice('lat_const', [4.87 4.87 3.31], 'angle', [90 90 90]*pi/180, 'sym', 'P 42/m n m');
  >> mnf2.addatom('r', [0 0 0], 'S', 2.5, 'label', 'MMn2', 'color', 'b')
  >> mnf2.gencoupling('maxDistance', 5)
  >> mnf2.addmatrix('label', 'J1', 'value', J1, 'color', 'red');
  >> mnf2.addmatrix('label', 'J2', 'value', J2, 'color', 'green');
  >> mnf2.addcoupling('mat', 'J1', 'bond', 1)
  >> mnf2.addcoupling('mat', 'J2', 'bond', 2)
  >> mnf2.addmatrix('label', 'D', 'value', diag([0 0 D]), 'color', 'black');
  >> mnf2.addaniso('D')
  >> mnf2.genmagstr('mode', 'direct', 'S', [0 0; 0 0; 1 -1])
  >> 
  >> % define fit_func
  >> fit_func =  @(obj, p) matparser(obj, 'param', p, 'mat', {'J1', 'J2', 'D(3,3)'}, 'init', true);
  >> 
  >> % define resolution (from PyChop)
  >> Ei = 20;
  >> eres = @(en) 512.17*sqrt((Ei-en).^3 .* ( 8.26326e-10*(0.169+0.4*(Ei./(Ei-en)).^1.5).^2 + 2.81618e-11*(1.169+0.4*(Ei./(Ei-en)).^1.5).^2));
  >> % Q-resolution (parameters for MARI)
  >> e2k = @(en) sqrt( en .* (2*1.67492728e-27*1.60217653e-22) )./1.05457168e-34./1e10;
  >> L1 = 11.8;  % Moderator to Sample distance in m
  >> L2 = 2.5;   % Sample to detector distance in m
  >> ws = 0.05;  % Width of sample in m
  >> wm = 0.12;  % Width of moderator in m
  >> wd = 0.025; % Width of detector in m
  >> ki = e2k(Ei);
  >> a1 = ws/L1; % Angular width of sample seen from moderator
  >> a2 = wm/L1; % Angular width of moderator seen from sample
  >> a3 = wd/L2; % Angular width of detector seen from sample
  >> a4 = ws/L2; % Angular width of sample seen from detector
  >> dQ = 2.35 * sqrt( (ki*a1)^2/12 + (ki*a2)^2/12 + (ki*a3)^2/12 + (ki*a4)^2/12 );
  >> 
  >> % fit powder
  >> backgroundStrategy = 'planar';  % 'planar' or 'independent'
  >> nQ = 10;   % Number of Q-points to subdivide cuts into for averaging
  >>
  >> fitpow = <strong>sw_fitpowder</strong>(mnf2, mnf2dat,  fit_func, [J1 J2 D], backgroundStrategy, nQ);
  >> fitpow.crop_energy_range(2.0, 8.0);
  >> fitpow.powspec_args.dE = eres;
  >> fitpow.sw_instrument_args = struct('dQ', dQ, 'ThetaMin', 3.5, 'Ei', Ei);
  >> fitpow.estimate_constant_background();
  >> fitpow.estimate_scale_factor();
  >> fitpow.set_model_parameter_bounds(1:3, [-1 0 -0.2], [0 1 0.2]) % Force J1 to be ferromagnetic to agree with structure
  >> fitpow.set_bg_parameter_bounds(3, 0.0, []) % Set lb of constant bg = 0
  >> fitpow.fix_bg_parameters(1:2); % fix slopes of background to 0
  >> fitpow.cost_function = "Rsq";  % or "chisq"
  >> fitpow.optimizer = @ndbase.simplex;
  >> result = fitpow.fit('MaxIter', 1);  % passes varargin to optimizer
  >> 
  >> [pfit,cost_val,stat] = result{:};
  >> fitpow.plot_result(pfit, 26, 'EdgeAlpha', 0.9, 'LineWidth', 2)
  ```
 
  [spinw.spinwave] \| [sw_fitspec]

    <a href="matlab:doc sw_fitpowder">Documentation for sw_fitpowder</a>


    """
    def __init__(self, swobj=None, data=None, fit_func=None, model_params=None, background_strategy=None, nQ=None, **kwargs):
        """
  constructor

    <a href="matlab:doc sw_fitpowder">Documentation for sw_fitpowder/sw_fitpowder</a>


        """
        self.__dict__['interface'] = m._interface
        self.__dict__['_methods'] = []
        self.__dict__['__name__'] = 'sw_fitpowder'
        self.__dict__['__origin__'] = sw_fitpowder
        args = tuple(v for v in [swobj, data, fit_func, model_params, background_strategy, nQ] if v is not None)
        args += sum(kwargs.items(), ())
        self.__dict__['handle'] = self.interface.call('sw_fitpowder', *args, nargout=1)

    @property
    def swobj(self):
        """
  data


        """
        return self.__getattr__('swobj')

    @swobj.setter
    def swobj(self, val):
        self.__setattr__('swobj', val)

    @property
    def y(self):
        """
<strong>sw_fitpowder/y</strong> is a property.


        """
        return self.__getattr__('y')

    @y.setter
    def y(self, val):
        self.__setattr__('y', val)

    @property
    def e(self):
        """
<strong>sw_fitpowder/e</strong> is a property.


        """
        return self.__getattr__('e')

    @e.setter
    def e(self, val):
        self.__setattr__('e', val)

    @property
    def ebin_cens(self):
        """
<strong>sw_fitpowder/ebin_cens</strong> is a property.


        """
        return self.__getattr__('ebin_cens')

    @ebin_cens.setter
    def ebin_cens(self, val):
        self.__setattr__('ebin_cens', val)

    @property
    def modQ_cens(self):
        """
<strong>sw_fitpowder/modQ_cens</strong> is a property.


        """
        return self.__getattr__('modQ_cens')

    @modQ_cens.setter
    def modQ_cens(self, val):
        self.__setattr__('modQ_cens', val)

    @property
    def nQ(self):
        """
 <strong>nQ</strong> -  number |Q| bins to calc. in integration limits of 1D cut


        """
        return self.__getattr__('nQ')

    @nQ.setter
    def nQ(self, val):
        self.__setattr__('nQ', val)

    @property
    def ndim(self):
        """
<strong>sw_fitpowder/ndim</strong> is a property.


        """
        return self.__getattr__('ndim')

    @ndim.setter
    def ndim(self, val):
        self.__setattr__('ndim', val)

    @property
    def ncuts(self):
        """
<strong>sw_fitpowder/ncuts</strong> is a property.


        """
        return self.__getattr__('ncuts')

    @ncuts.setter
    def ncuts(self, val):
        self.__setattr__('ncuts', val)

    @property
    def sw_instrument_args(self):
        """
  spinw funtion inputs


        """
        return self.__getattr__('sw_instrument_args')

    @sw_instrument_args.setter
    def sw_instrument_args(self, val):
        self.__setattr__('sw_instrument_args', val)

    @property
    def powspec_args(self):
        """
<strong>sw_fitpowder/powspec_args</strong> is a property.


        """
        return self.__getattr__('powspec_args')

    @powspec_args.setter
    def powspec_args(self, val):
        self.__setattr__('powspec_args', val)

    @property
    def fit_func(self):
        """
  functions


        """
        return self.__getattr__('fit_func')

    @fit_func.setter
    def fit_func(self, val):
        self.__setattr__('fit_func', val)

    @property
    def cost_function(self):
        """
 <strong>cost_function</strong> -  "Rsq" or "chisq"


        """
        return self.__getattr__('cost_function')

    @cost_function.setter
    def cost_function(self, val):
        self.__setattr__('cost_function', val)

    @property
    def background_strategy(self):
        """
 <strong>background_strategy</strong> -  "planar" or "independent" (1D only - fbg = @(en, p1, p2, ..., pN)


        """
        return self.__getattr__('background_strategy')

    @background_strategy.setter
    def background_strategy(self, val):
        self.__setattr__('background_strategy', val)

    @property
    def fbg(self):
        """
<strong>sw_fitpowder/fbg</strong> is a property.


        """
        return self.__getattr__('fbg')

    @fbg.setter
    def fbg(self, val):
        self.__setattr__('fbg', val)

    @property
    def optimizer(self):
        """
  fit and parameters


        """
        return self.__getattr__('optimizer')

    @optimizer.setter
    def optimizer(self, val):
        self.__setattr__('optimizer', val)

    @property
    def nparams_model(self):
        """
<strong>sw_fitpowder/nparams_model</strong> is a property.


        """
        return self.__getattr__('nparams_model')

    @nparams_model.setter
    def nparams_model(self, val):
        self.__setattr__('nparams_model', val)

    @property
    def nparams_bg(self):
        """
<strong>sw_fitpowder/nparams_bg</strong> is a property.


        """
        return self.__getattr__('nparams_bg')

    @nparams_bg.setter
    def nparams_bg(self, val):
        self.__setattr__('nparams_bg', val)

    @property
    def params(self):
        """
<strong>sw_fitpowder/params</strong> is a property.


        """
        return self.__getattr__('params')

    @params.setter
    def params(self, val):
        self.__setattr__('params', val)

    @property
    def bounds(self):
        """
<strong>sw_fitpowder/bounds</strong> is a property.


        """
        return self.__getattr__('bounds')

    @bounds.setter
    def bounds(self, val):
        self.__setattr__('bounds', val)

    @property
    def liveplot_interval(self):
        """
<strong>sw_fitpowder/liveplot_interval</strong> is a property.


        """
        return self.__getattr__('liveplot_interval')

    @liveplot_interval.setter
    def liveplot_interval(self, val):
        self.__setattr__('liveplot_interval', val)

    @property
    def fbg_planar(self):
        """
<strong>sw_fitpowder/fbg_planar</strong> is a property.


        """
        return self.__getattr__('fbg_planar')

    @fbg_planar.setter
    def fbg_planar(self, val):
        self.__setattr__('fbg_planar', val)

    @property
    def fbg_indep(self):
        """
<strong>sw_fitpowder/fbg_indep</strong> is a property.


        """
        return self.__getattr__('fbg_indep')

    @fbg_indep.setter
    def fbg_indep(self, val):
        self.__setattr__('fbg_indep', val)

    @property
    def do_cache(self):
        """
<strong>sw_fitpowder/do_cache</strong> is a property.


        """
        return self.__getattr__('do_cache')

    @do_cache.setter
    def do_cache(self, val):
        self.__setattr__('do_cache', val)

    @property
    def ycalc_cached(self):
        """
<strong>sw_fitpowder/ycalc_cached</strong> is a property.


        """
        return self.__getattr__('ycalc_cached')

    @ycalc_cached.setter
    def ycalc_cached(self, val):
        self.__setattr__('ycalc_cached', val)

    @property
    def model_params_cached(self):
        """
<strong>sw_fitpowder/model_params_cached</strong> is a property.


        """
        return self.__getattr__('model_params_cached')

    @model_params_cached.setter
    def model_params_cached(self, val):
        self.__setattr__('model_params_cached', val)

    @property
    def liveplot_counter(self):
        """
<strong>sw_fitpowder/liveplot_counter</strong> is a property.


        """
        return self.__getattr__('liveplot_counter')

    @liveplot_counter.setter
    def liveplot_counter(self, val):
        self.__setattr__('liveplot_counter', val)

    def add_data(self, obj=None, data=None, **kwargs):
        """
<strong>sw_fitpowder/add_data</strong> is a function.
    <strong>add_data</strong>(obj, data)


        """
        args = tuple(v for v in [obj, data] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('add_data')), 1)
        return m.add_data(self.handle, *args, nargout=nout)

    def apply_energy_mask(self, obj=None, ikeep=None, **kwargs):
        """
<strong>sw_fitpowder/apply_energy_mask</strong> is a function.
    <strong>apply_energy_mask</strong>(obj, ikeep)


        """
        args = tuple(v for v in [obj, ikeep] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('apply_energy_mask')), 1)
        return m.apply_energy_mask(self.handle, *args, nargout=nout)

    def calc_background(self, obj=None, params=None, **kwargs):
        """
  add background


        """
        args = tuple(v for v in [obj, params] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('calc_background')), 1)
        return m.calc_background(self.handle, *args, nargout=nout)

    def calc_cost_func(self, obj=None, params=None, **kwargs):
        """
  evaluate fit function


        """
        args = tuple(v for v in [obj, params] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('calc_cost_func')), 1)
        return m.calc_cost_func(self.handle, *args, nargout=nout)

    def calc_spinwave_spec(self, obj=None, params=None, **kwargs):
        """
<strong>sw_fitpowder/calc_spinwave_spec</strong> is a function.
    [ycalc, bg] = <strong>calc_spinwave_spec</strong>(obj, params)


        """
        args = tuple(v for v in [obj, params] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(2, get_nlhs('calc_spinwave_spec')), 1)
        return m.calc_spinwave_spec(self.handle, *args, nargout=nout)

    def clear_cache(self, obj=None, **kwargs):
        """
<strong>sw_fitpowder/clear_cache</strong> is a function.
    <strong>clear_cache</strong>(obj)


        """
        args = tuple(v for v in [obj] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('clear_cache')), 1)
        return m.clear_cache(self.handle, *args, nargout=nout)

    def convert_horace_to_struct(self, data=None, **kwargs):
        """
<strong>sw_fitpowder.convert_horace_to_struct</strong> is a function.
    data_struct = <strong>sw_fitpowder.convert_horace_to_struct</strong>(data)


        """
        args = tuple(v for v in [data] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('convert_horace_to_struct')), 1)
        return m.convert_horace_to_struct(self.handle, *args, nargout=nout)

    def crop_energy_range(self, obj=None, emin=None, emax=None, **kwargs):
        """
  crop data


        """
        args = tuple(v for v in [obj, emin, emax] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('crop_energy_range')), 1)
        return m.crop_energy_range(self.handle, *args, nargout=nout)

    def crop_q_range(self, obj=None, qmin=None, qmax=None, **kwargs):
        """
<strong>sw_fitpowder/crop_q_range</strong> is a function.
    <strong>crop_q_range</strong>(obj, qmin, qmax)


        """
        args = tuple(v for v in [obj, qmin, qmax] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('crop_q_range')), 1)
        return m.crop_q_range(self.handle, *args, nargout=nout)

    def estimate_constant_background(self, obj=None, **kwargs):
        """
<strong>sw_fitpowder/estimate_constant_background</strong> is a function.
    <strong>estimate_constant_background</strong>(obj)


        """
        args = tuple(v for v in [obj] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('estimate_constant_background')), 1)
        return m.estimate_constant_background(self.handle, *args, nargout=nout)

    def estimate_scale_factor(self, obj=None, **kwargs):
        """
  set scale factor to 1


        """
        args = tuple(v for v in [obj] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('estimate_scale_factor')), 1)
        return m.estimate_scale_factor(self.handle, *args, nargout=nout)

    def exclude_energy_range(self, obj=None, elo=None, ehi=None, **kwargs):
        """
<strong>sw_fitpowder/exclude_energy_range</strong> is a function.
    <strong>exclude_energy_range</strong>(obj, elo, ehi)


        """
        args = tuple(v for v in [obj, elo, ehi] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('exclude_energy_range')), 1)
        return m.exclude_energy_range(self.handle, *args, nargout=nout)

    def fit(self, obj=None, *args, **kwargs):
        """
<strong>sw_fitpowder/fit</strong> is a function.
    result = fit(obj, varargin)


        """
        args = tuple(v for v in [obj] if v is not None) + args
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('fit')), 1)
        return m.fit(self.handle, *args, nargout=nout)

    def fix_bg_parameters(self, obj=None, iparams_bg=None, icuts=None, **kwargs):
        """
<strong>sw_fitpowder/fix_bg_parameters</strong> is a function.
    <strong>fix_bg_parameters</strong>(obj, iparams_bg, icuts)


        """
        args = tuple(v for v in [obj, iparams_bg, icuts] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('fix_bg_parameters')), 1)
        return m.fix_bg_parameters(self.handle, *args, nargout=nout)

    def fix_model_parameters(self, obj=None, iparams=None, **kwargs):
        """
<strong>sw_fitpowder/fix_model_parameters</strong> is a function.
    <strong>fix_model_parameters</strong>(obj, iparams)


        """
        args = tuple(v for v in [obj, iparams] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('fix_model_parameters')), 1)
        return m.fix_model_parameters(self.handle, *args, nargout=nout)

    def fix_parameters(self, obj=None, iparams=None, **kwargs):
        """
<strong>sw_fitpowder/fix_parameters</strong> is a function.
    <strong>fix_parameters</strong>(obj, iparams)


        """
        args = tuple(v for v in [obj, iparams] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('fix_parameters')), 1)
        return m.fix_parameters(self.handle, *args, nargout=nout)

    def fix_scale(self, obj=None, **kwargs):
        """
<strong>sw_fitpowder/fix_scale</strong> is a function.
    <strong>fix_scale</strong>(obj)


        """
        args = tuple(v for v in [obj] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('fix_scale')), 1)
        return m.fix_scale(self.handle, *args, nargout=nout)

    def get(self, rhs1=None, rhs2=None, **kwargs):
        """
 <strong>get</strong>    Get MATLAB object properties.
    V = <strong>get</strong>(H, 'PropertyName') returns the value of the specified
    property for the MATLAB object with handle H.  If H is an array of  
    handles, <strong>get</strong> returns an M-by-1 cell array of values, where M is equal
    to length(H). If 'PropertyName' is replaced by a 1-by-N or N-by-1
    cell array of strings containing property names, <strong>get</strong> returns an M-by-N
    cell array of values.  For non-scalar H, if 'PropertyName' is a 
    dynamic  property, <strong>get</strong> returns a value only if the property exists in 
    all objects of the array.
  
    V = <strong>get</strong>(H, 'InexactPropertyName') returns the value of the specified
    property for the MATLAB object with handle H. <strong>get</strong> matches partial and 
    case-insensitive names that are not ambiguous. Inexact name matching 
    applies only to class properties. Dynamic properties require exact name matches.
 
    V = <strong>get</strong>(H) returns a structure in which each field name is the name of
    a user-gettable property of H and each field contains the value of that
    property.  If H is non-scalar, <strong>get</strong> returns a struct array with 
    dimensions M-by-1, where M = numel(H).  If H is non-scalar, <strong>get</strong> does 
    not return dynamic properties.
 
    <strong>get</strong>(H) displays the names of all user-gettable properties and their 
    current values for the MATLAB object with handle H.  The class can 
    override the GETDISP method to control how this information is 
    displayed.  H must be scalar.
 
    See also <a href="matlab:help get -displayBanner">get</a>, <a href="matlab:help sw_fitpowder -displayBanner">sw_fitpowder</a>, <a href="matlab:help sw_fitpowder/getdisp -displayBanner">sw_fitpowder/getdisp</a>, <a href="matlab:help handle -displayBanner">handle</a>

Help for <strong>sw_fitpowder/get</strong> is inherited from superclass <a href="matlab:help matlab.mixin.SetGet -displayBanner">matlab.mixin.SetGet</a>

    <a href="matlab:doc matlab.mixin.SetGet/get">Documentation for sw_fitpowder/get</a>


        """
        args = tuple(v for v in [rhs1, rhs2] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('get')), 1)
        return m.get(self.handle, *args, nargout=nout)

    def get_index_of_background_parameters(self, obj=None, iparams_bg=None, icuts=None, **kwargs):
        """
<strong>sw_fitpowder/get_index_of_background_parameters</strong> is a function.
    iparams = <strong>get_index_of_background_parameters</strong>(obj, iparams_bg, icuts)


        """
        args = tuple(v for v in [obj, iparams_bg, icuts] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('get_index_of_background_parameters')), 1)
        return m.get_index_of_background_parameters(self.handle, *args, nargout=nout)

    def get_nparams_in_background_func(self, obj=None, **kwargs):
        """
  get background parameters


        """
        args = tuple(v for v in [obj] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('get_nparams_in_background_func')), 1)
        return m.get_nparams_in_background_func(self.handle, *args, nargout=nout)

    def getdisp(self, rhs1=None, **kwargs):
        """
 <strong>getdisp</strong>    Specialized MATLAB object property display.
    <strong>getdisp</strong> is called by GET when GET is called with no output argument 
    and a single input parameter H an array of handles to MATLAB objects.  
    This method is designed to be overridden in situations where a
    special display format is desired to display the results returned by
    GET(H).  If not overridden, the default display format for the class
    is used.
 
    See also <a href="matlab:help sw_fitpowder -displayBanner">sw_fitpowder</a>, <a href="matlab:help sw_fitpowder/get -displayBanner">sw_fitpowder/get</a>, <a href="matlab:help handle -displayBanner">handle</a>

Help for <strong>sw_fitpowder/getdisp</strong> is inherited from superclass <a href="matlab:help matlab.mixin.SetGet -displayBanner">matlab.mixin.SetGet</a>

    <a href="matlab:doc matlab.mixin.SetGet/getdisp">Documentation for sw_fitpowder/getdisp</a>


        """
        args = tuple(v for v in [rhs1] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('getdisp')), 1)
        return m.getdisp(self.handle, *args, nargout=nout)

    def initialise_parameters_and_bounds(self, obj=None, model_params=None, **kwargs):
        """
<strong>sw_fitpowder/initialise_parameters_and_bounds</strong> is a function.
    <strong>initialise_parameters_and_bounds</strong>(obj, model_params)


        """
        args = tuple(v for v in [obj, model_params] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('initialise_parameters_and_bounds')), 1)
        return m.initialise_parameters_and_bounds(self.handle, *args, nargout=nout)

    def plot_1d_cuts_on_data(self, obj=None, ycalc=None, *args, **kwargs):
        """
<strong>sw_fitpowder/plot_1d_cuts_on_data</strong> is a function.
    <strong>plot_1d_cuts_on_data</strong>(obj, ycalc, varargin)


        """
        args = tuple(v for v in [obj, ycalc] if v is not None) + args
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('plot_1d_cuts_on_data')), 1)
        return m.plot_1d_cuts_on_data(self.handle, *args, nargout=nout)

    def plot_1d_or_2d(self, obj=None, ycalc=None, *args, **kwargs):
        """
<strong>sw_fitpowder/plot_1d_or_2d</strong> is a function.
    <strong>plot_1d_or_2d</strong>(obj, ycalc, varargin)


        """
        args = tuple(v for v in [obj, ycalc] if v is not None) + args
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('plot_1d_or_2d')), 1)
        return m.plot_1d_or_2d(self.handle, *args, nargout=nout)

    def plot_2d_contour_on_data(self, obj=None, ycalc=None, *args, **kwargs):
        """
<strong>sw_fitpowder/plot_2d_contour_on_data</strong> is a function.
    <strong>plot_2d_contour_on_data</strong>(obj, ycalc, varargin)


        """
        args = tuple(v for v in [obj, ycalc] if v is not None) + args
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('plot_2d_contour_on_data')), 1)
        return m.plot_2d_contour_on_data(self.handle, *args, nargout=nout)

    def plot_2d_data(self, obj=None, y=None, **kwargs):
        """
<strong>sw_fitpowder/plot_2d_data</strong> is a function.
    ax = <strong>plot_2d_data</strong>(obj, y)


        """
        args = tuple(v for v in [obj, y] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('plot_2d_data')), 1)
        return m.plot_2d_data(self.handle, *args, nargout=nout)

    def plot_result(self, obj=None, params=None, *args, **kwargs):
        """
<strong>sw_fitpowder/plot_result</strong> is a function.
    <strong>plot_result</strong>(obj, params, varargin)


        """
        args = tuple(v for v in [obj, params] if v is not None) + args
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('plot_result')), 1)
        return m.plot_result(self.handle, *args, nargout=nout)

    def rebin_powspec_to_1D_cuts(self, obj=None, ycalc=None, **kwargs):
        """
  sum up successive nQ points along |Q| axis (dim=2)


        """
        args = tuple(v for v in [obj, ycalc] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('rebin_powspec_to_1D_cuts')), 1)
        return m.rebin_powspec_to_1D_cuts(self.handle, *args, nargout=nout)

    def set(self, rhs1=None, rhs2=None, **kwargs):
        """
 <strong>set</strong>    Set MATLAB object property values.
    <strong>set</strong>(H,'PropertyName',PropertyValue) sets the value of the specified 
    property for the MATLAB object with handle H.  If H is an array of 
    handles, the specified property's value is set for all objects in H.  
 
    <strong>set</strong>(H,'InexactPropertyName',PropertyValue) sets the value of the specified 
    property for the MATLAB object with handle H. <strong>set</strong> matches partial and 
    case-insensitive names that are not ambiguous. Inexact name matching 
    applies only to class properties. Dynamic properties require exact name matches.
 
    <strong>set</strong>(H,'PropertyName1',Value1,'PropertyName2',Value2,...) sets multiple
    property values with a single statement. 
 
    <strong>set</strong>(H,pn,pv) sets the named properties specified in the cell array of
    strings pn to the corresponding values in the cell array pv for all
    objects specified in H.  The cell array pn must be 1-by-N, but the cell
    array pv can be M-by-N where M is equal to length(H), so that each
    object will be updated with a different set of values for the list of
    property names contained in pn.
 
    Given S a structure whose field names are object property names, 
    <strong>set</strong>(H,S) sets the properties identified by each field name of S with
    the values contained in the structure.
 
    Note that it is permissible to use property/value string pairs, 
    structures, and property/value cell array pairs in the same call to
    <strong>set</strong>.
 
    A = <strong>set</strong>(H, 'PropertyName') returns the possible values for the 
    specified property of the object with handle H.  The returned array
    is a cell array of possible value strings or an empty cell array if
    the property does not have a finite set of possible string values.
 
    <strong>set</strong>(H,'PropertyName') displays the possible values for the specified
    property of object with handle H.
 
    A = <strong>set</strong>(H) returns the names of the user-settable properties and their
    possible values for the object with handle H.  H must be scalar.  
    The return value is a  structure whose field names are the names of the
    user-settable properties of H, and whose values are cell arrays of
    possible property values or empty cell arrays.
 
    <strong>set</strong>(H) displays the names and possible values for all user-settable
    properties of scalar object H.  The class can override the SETDISP 
    method to control how this information is displayed. 
 
    See also <a href="matlab:help set -displayBanner">set</a>, <a href="matlab:help sw_fitpowder -displayBanner">sw_fitpowder</a>, <a href="matlab:help sw_fitpowder/setdisp -displayBanner">sw_fitpowder/setdisp</a>, <a href="matlab:help handle -displayBanner">handle</a>

Help for <strong>sw_fitpowder/set</strong> is inherited from superclass <a href="matlab:help matlab.mixin.SetGet -displayBanner">matlab.mixin.SetGet</a>

    <a href="matlab:doc matlab.mixin.SetGet/set">Documentation for sw_fitpowder/set</a>


        """
        args = tuple(v for v in [rhs1, rhs2] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('set')), 1)
        return m.set(self.handle, *args, nargout=nout)

    def set_bg_parameter_bounds(self, obj=None, iparams_bg=None, lb=None, ub=None, icuts=None, **kwargs):
        """
<strong>sw_fitpowder/set_bg_parameter_bounds</strong> is a function.
    <strong>set_bg_parameter_bounds</strong>(obj, iparams_bg, lb, ub, icuts)


        """
        args = tuple(v for v in [obj, iparams_bg, lb, ub, icuts] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('set_bg_parameter_bounds')), 1)
        return m.set_bg_parameter_bounds(self.handle, *args, nargout=nout)

    def set_bg_parameters(self, obj=None, iparams_bg=None, values=None, icuts=None, **kwargs):
        """
<strong>sw_fitpowder/set_bg_parameters</strong> is a function.
    <strong>set_bg_parameters</strong>(obj, iparams_bg, values, icuts)


        """
        args = tuple(v for v in [obj, iparams_bg, values, icuts] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('set_bg_parameters')), 1)
        return m.set_bg_parameters(self.handle, *args, nargout=nout)

    def set_bounds(self, obj=None, iparams=None, lb=None, ub=None, ibnd=None, **kwargs):
        """
<strong>sw_fitpowder/set_bounds</strong> is a function.
    <strong>set_bounds</strong>(obj, iparams, lb, ub, ibnd)


        """
        args = tuple(v for v in [obj, iparams, lb, ub, ibnd] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('set_bounds')), 1)
        return m.set_bounds(self.handle, *args, nargout=nout)

    def set_caching(self, obj=None, do_cache=None, **kwargs):
        """
<strong>sw_fitpowder/set_caching</strong> is a function.
    <strong>set_caching</strong>(obj, do_cache)


        """
        args = tuple(v for v in [obj, do_cache] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('set_caching')), 1)
        return m.set_caching(self.handle, *args, nargout=nout)

    def set_model_parameter_bounds(self, obj=None, iparams=None, lb=None, ub=None, **kwargs):
        """
<strong>sw_fitpowder/set_model_parameter_bounds</strong> is a function.
    <strong>set_model_parameter_bounds</strong>(obj, iparams, lb, ub)


        """
        args = tuple(v for v in [obj, iparams, lb, ub] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('set_model_parameter_bounds')), 1)
        return m.set_model_parameter_bounds(self.handle, *args, nargout=nout)

    def set_model_parameters(self, obj=None, iparams=None, values=None, **kwargs):
        """
<strong>sw_fitpowder/set_model_parameters</strong> is a function.
    <strong>set_model_parameters</strong>(obj, iparams, values)


        """
        args = tuple(v for v in [obj, iparams, values] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('set_model_parameters')), 1)
        return m.set_model_parameters(self.handle, *args, nargout=nout)

    def set_scale(self, obj=None, scale=None, **kwargs):
        """
<strong>sw_fitpowder/set_scale</strong> is a function.
    <strong>set_scale</strong>(obj, scale)


        """
        args = tuple(v for v in [obj, scale] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('set_scale')), 1)
        return m.set_scale(self.handle, *args, nargout=nout)

    def set_scale_bounds(self, obj=None, lb=None, ub=None, **kwargs):
        """
<strong>sw_fitpowder/set_scale_bounds</strong> is a function.
    <strong>set_scale_bounds</strong>(obj, lb, ub)


        """
        args = tuple(v for v in [obj, lb, ub] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('set_scale_bounds')), 1)
        return m.set_scale_bounds(self.handle, *args, nargout=nout)

    def setdisp(self, rhs1=None, **kwargs):
        """
 <strong>setdisp</strong>    Specialized MATLAB object property display.
    <strong>setdisp</strong> is called by SET when SET is called with no output argument 
    and a single input parameter H an array of handles to MATLAB objects.  
    This method is designed to be overridden in situations where a
    special display format is desired to display the results returned by
    SET(H).  If not overridden, the default display format for the class
    is used.
 
    See also <a href="matlab:help matlab.mixin.SetGet.setdisp -displayBanner">setdisp</a>, <a href="matlab:help sw_fitpowder -displayBanner">sw_fitpowder</a>, <a href="matlab:help sw_fitpowder/set -displayBanner">sw_fitpowder/set</a>, <a href="matlab:help handle -displayBanner">handle</a>

Help for <strong>sw_fitpowder/setdisp</strong> is inherited from superclass <a href="matlab:help matlab.mixin.SetGet -displayBanner">matlab.mixin.SetGet</a>

    <a href="matlab:doc matlab.mixin.SetGet/setdisp">Documentation for sw_fitpowder/setdisp</a>


        """
        args = tuple(v for v in [rhs1] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('setdisp')), 1)
        return m.setdisp(self.handle, *args, nargout=nout)

