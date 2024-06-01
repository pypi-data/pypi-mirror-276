import pyspinw
m = pyspinw.Matlab()

from .sw_fitpowder import sw_fitpowder
from .spinw import spinw
from .swpref import swpref
from .cif import cif
from .YAML import YAML
from . import swfunc
from . import ndbase
from . import swsym
from . import swplot

def swdoc(funName0=None, *args, **kwargs):
    """
% opens the SpinW documentation
%
% ### Syntax
%
% `swdoc(funName)`
%
% `link = swdoc(funName)`
%
% ### Description
%
% `swdoc(funName)` shows the documentation on the given function name,
% method, property name. Package functions can be referenced as
% `'packagename.functionname'`, e.g. `'swpref.getpref'`, class methods and
% properties can be referenced the same way, e.g. `'spinw.genmagstr'`. Also
% class, package or folder (that contains `.m` files) names can be
% referenced as well, e.g. `'swsym'`.
%
% `link = swdoc(funName)` returns the web link pointing to the right
% documentation.
%
    """
    args = tuple(v for v in [funName0] if v is not None) + args
    return m.swdoc(*args, **kwargs)


def sw_tofres(spec=None, *args, **kwargs):
    """
% convolutes the spectrum with a Q bin
%
% ### Syntax
%
% `spectra = sw_tofres(spectra,Name,Value)`
%
% ### Description
%
% `spectra = sw_tofres(spectra,Name,Value)` simulates the finite bin size
% of the cuts of direct TOF neutron scattering data. It calculates the
% spectrum at multiple points within the given bin volume and sums them up.
% The function is usefull if relatively large bins were used to analyse the
% data due to low signal to noise ratio of the measurement.
%
% ### Input Arguments
%
% `spectra`
% : Input structure, contains calculated correlation functions
%   withouth the resolution effect.
%
% ### Name-Value Pair Arguments
%
% `'method'`
% : String that determines the method to generate the $Q$ points, options:
%   * `'random'`    The bin volume will be randomly sampled.
%   * `'grid'`      The bin volume will be split up to a finer regular
%                   grid.
%
% `'dQ'`
% : Row vector with 3 elements. The width of the $Q$ bin
%   along the three reciprocal lattice directions. The spectrum
%   will be integrated in the $Q\pm (\delta Q/2)$ range. Default value is
%   `[0.1 0.1 0.1]`.
%
% `'nQ'`
% : Row vector with 3 elements when `method` is `grid` and gives the
%   number of $Q$ points along the three reciprocal lattice directions to
%   average over. When `method` is `random` it is a scalar that determines
%   the number of random $Q$ points.
%
% `'fid'`
% : Defines whether to provide text output. The default value is determined
%   by the `fid` preference stored in [swpref]. The possible values are:
%   * `0`   No text output is generated.
%   * `1`   Text output in the MATLAB Command Window.
%   * `fid` File ID provided by the `fopen` command, the output is written
%           into the opened file stream.
%
% `'tid'`
% : Determines if the elapsed and required time for the calculation is
%   displayed. The default value is determined by the `tid` preference
%   stored in [swpref]. The following values are allowed (for more details
%   see [sw_timeit]):
%   * `0` No timing is executed.
%   * `1` Display the timing in the Command Window.
%   * `2` Show the timing in a separat pup-up window.
%
% ### Output Arguments
%
% `spectra`
% : Same as the input except that it contains the calculated intensity in
%   the `swConv` field.
%
% ### See Also
%
% [sw_egrid] \| [sw_instrument]
%
% *[TOF]: Time Of Flight
%
    """
    args = tuple(v for v in [spec] if v is not None) + args
    return m.sw_tofres(*args, **kwargs)


def sw_econtract(Q=None, *args, **kwargs):
    """
% converts (Q,E) values to Q values for diffraction instrument
%
% ### Syntax
%
% `Qm = sw_econtract(Q,Name,Value)`
%
% ### Description
%
% `Qm = sw_econtract(Q,Name,Value)` converts $(Q,E)$ values in the phase
% space into $Q$ values as it would appear when measuring it with via
% neutron diffraction.
%
% ### Input Arguments
%
% `Q`
% : Input values in reciprocal space in the scattering plane in
%   \\ang$^{-1}$ units, dimensions are $[2\times n_Q]$.
%
% ### Name-Value Pair Arguments
%
% `'E'`
% : Energy transfer value in meV, default value is zero.
%
% `'lambda'`
% : Wavelength of the incident neutron beam in \\ang.
%
% `'ki'`
% : Momentum of the incidend neutron beam in \\ang$^{-1}$, alternative
%   input to `lambda`.
%
% `'sense'`
% : Scattering sense:
%
%   * `1`  detectors are on the right hand side from the incident beam direction, default.
%   * `-1` detectors are on the left hand side from the incident beam direction.
%
% ### See Also
%
% [sw_converter]
%
    """
    args = tuple(v for v in [Q] if v is not None) + args
    return m.sw_econtract(*args, **kwargs)


def gm_planard(M0=None, x=None, **kwargs):
    """
% planar magnetic structure constraint function
%
% ### Syntax
%
% `[m, k, n, name, pname, limit] = gm_planard(m0, x) `
%
% ### Description
%
% Same function as [gm_planar], except that the input angles are all in
% degree.
%
%
% ### See Also
%
% [gm_planar]
%
    """
    args = tuple(v for v in [M0, x] if v is not None)
    return m.gm_planard(*args, **kwargs)


def sw_resconv(M=None, x=None, dx=None, func0=None, **kwargs):
    """
% convolution of a matrix and a Gaussian
%
% ### Syntax
%
% `Mout = sw_resconv(M,x,dx,func)`
%
% ### Description
%
% `Mout = sw_resconv(M,x,dx,func)` convolutes a 2D matrix with a Gaussian
% along the first dimension of the matrix. The convolution keeps the
% integrated intensity $\sum I\cdot dx$ constant. It assumes the `x` vector
% contains the center points of the bins and the distances between the
% generated bin edges is calculated by interpolating from the distances
% between the given `x` bin center positions.
%
% ### Input Arguments
%
% `M`
% : Arbitrary matrix with dimensions of $[m_1\times m_2]$.
%
% `x`
% : Column vector of coordinates along the first dimension of the
%   matrix.
%
% `dx`
% : FWHM value of the Gaussian as a
%   function of $dx$. Either a function handle with a header `fwhm =
%   dx(xVal)` or a vector of polynomial coefficients that produces the
%   right standard deviation. In this case in the function the following
%   line will be executed `fwhm = polyval(dx,xVal)` or a constant FWHM
%   value.
%
%   The standard deviation of the Gaussian is calculated from the given
%   $dx$ value using the formula $\sigma_G = fwhm_G/2/\sqrt{2\cdot log(2)}
%   \sim fwhm_G\cdot 0.424661$
%   If a general resolution function is provided in the `func` argument,
%   it will be called as `y = func(x,[1 x0 fwhm])`. In this case the `fwhm`
%   can be a row vector and the meaning of the different parameters will
%   depend on `func`.
%
% `func`
% : Resolution function shape with header `y = func(x,p)`,
%   where `x` is a column vector, `p` is a row vector of parameters. The
%   meaning of the first 2 elements of the parameter vector are fixed.
%
%   * `p(1)` integral of the function.
%   * `p(2)` center of mass position of the function.
%
%   Optional, default value is `@swfunc.gaussfwhm`.
%
% ### Output Arguments
%
% `Mout`
% : Matrix with same dimensions as the input `M`.
%
% ### See Also
%
% [sw_res] \| [swfunc.gaussfwhm]
%
% *[FWHM]: Full Width at Half Maximum
%
    """
    args = tuple(v for v in [M, x, dx, func0] if v is not None)
    return m.sw_resconv(*args, **kwargs)


def sw_bonddim(C=None, nAtom=None, **kwargs):
    """
% find dimensionality of a periodic bond network
%
% ### Syntax
%
% `l = sw_bonddim(c, {natom})`
%
% ### Description
%
% `l = sw_bonddim(c, {natom})` splits the given periodic bond network into
% disjunct subsystems and determines the dimensionality of each subsystem.
%
% ### Examples
%
% Check the bond dimensionality of the triangular lattice:
%
% ```
% >>tri = sw_model('triAF')>>
% >>sw_bonddim(tri.intmatrix.all)>>
% ```
%
% ### Input Arguments
%
% `C`
% : Bond list in a matrix with dimensions of $[5\times n_{bond}]$, where the meaning of
%   the rows are:
%   * `#1:#3`   Lattice translations between the coupled atoms in
%               lattice units (always integer).
%   * `#4`      Index of the bond starting atom.
%   * `#5`      Index of the bond end atom.
%
%   For example for a chain along b-axis on a Bravais lattice:
%       `C = [1;1;0;1;0]`
%
% `nAtom`
% : Number of atoms in the unit cell. If not given, the maximum
%   atom index from the bond list is taken.
%
% ### Output Arguments
%
% `L`
% : Struct with the number of elements equal to the number of
%           subsystems, it has the following fields:
%   * `D`       Dimensionality of the subsystem $(0\leq D\leq 3)$.
%   * `base`    Basis vectors spanning the subsystem stored in a
%                       $[3\times D]$ matrix where each column denotes a basis
%                       vector.
%   * `site`    List of sites that belong to the subsystem.
%
    """
    args = tuple(v for v in [C, nAtom] if v is not None)
    return m.sw_bonddim(*args, **kwargs)


def sw_fsub(conn=None, _=None, **kwargs):
    """
% simple graph vertex coloring
%
% ### Syntax
%
% `cgraph = sw_fsub(conn, next)`
%
% ### Description
%
% `cgraph = sw_fsub(conn, next)` creates a simple graph vertex coloring,
% determines non-connected sublattices for Monte-Carlo calculation.
%
% ### Input Arguments
%
% `conn`
% : Contains edge indices which are connected
%   `conn(1,idx)-->conn(2,idx)` stored in a matrix with dimensions of $[2times n_{conn}]$.
%
% `nExt`
% : Size of the magnetic supercell in a row vector with 3 integers.
%
% ### Output Arguments
%
% `cGraph`
% : Vector, that assigns every magnetic moment to a sublattice.
%
% ### See Also
%
% [spinw.anneal]
%
    """
    args = tuple(v for v in [conn] if v is not None)
    return m.sw_fsub(*args, **kwargs)


def sw_update(installDir=None, *args, **kwargs):
    """
% updates the SpinW installation from the internet
%
% ### Syntax
%
% `sw_update`
%
% `onlineRev = sw_update(installDir)`
%
% ### Description
%
% `sw_update` creates a new folder with the latest release beside the
% current SpinW installation, downloads the newses SpinW version and adds
% the new version to the Matlab search path and also removes the old
% version from the search path. If the search path is defined in the
% `startup.m` file, it has to be changed manually.
%
% Each step of the update process can be controlled by the user via
% the interactive Command Line provided by the function.
%
% ### Input Arguments
%
% `installDir`
% : Folder name, where the new version is installed. Default is
%   the parent folder of the current version of SpinW. If
%   `installDir` is `'.'`, the update will be installed to current
%   folder.
%
% `'beta'`
% : Retrieve the latest pre-release if it is newer than the latest release.
%   If it is older, download the latest release.
%
% ### Output Arguments
%
% `onlineVer`  If output is defined, the revision number of the online
%               SpinW is given, optional.
%
    """
    args = tuple(v for v in [installDir] if v is not None) + args
    return m.sw_update(*args, **kwargs)


def sw_readparam(format=None, *args, **kwargs):
    """
% parse input arguments
%
% ### Syntax
%
% `parsed = sw_readparam(format,Name,Value)`
%
% ### Description
%
% `parsed = sw_readparam(format,Name,Vale)` parses name-value pair
% arguments. The parsing is controlled by the given `format` input. The
% name-value pairs are converted into the parsed struct which has field
% names identical to the given parameter names and corresponding values
% taken from the input. `format` can also define required dimensionality of
% a given value and default values for select parameters.
%
% `sw_readparam` is used in most of the method functions of [spinw].
%
% ### Input Arguments
%
% `format`
% : A struct with the following fields:
%   * `fname` Field names, $n_{param}$ strings in cell.
%   * `size` Required dimensions of the corresponding value in a cell of
%     $n_{param}$ vectors. Negative integer means dimension has to match with
%     any other dimension which has the identical negative integer.
%   * `defval` Cell of $n_{param}$ values, provides default values for
%     missing parameters.
%   * `soft` Cell of $n_{param}$ logical values, optional. If `soft(i)` is
%     true, in case of missing parameter value $i$, no warning will be
%     given.
%
    """
    args = tuple(v for v in [format] if v is not None) + args
    return m.sw_readparam(*args, **kwargs)


def sw_neutron(spectra=None, *args, **kwargs):
    """
% calculates neutron scattering cross section
%
% ### Syntax
%
% `spectra = sw_neutron(spectra,Name,Value)`
%
% ### Description
%
% `spectra = sw_neutron(spectra,Name,Value)` calculates the neutron
% scattering cross section for polarised and unpolarised neutrons. The
% function reads the calculated spin-spin correlation function
% $\mathcal{S}^{\alpha\beta}(\mathbf{Q},\omega)$ and calculates the neutron
% scattering cross section for unpolarized neutrons using the formula:
%
% $S_\perp(Q,\omega)=\sum_{\alpha\beta}(1-\hat{q}^\alpha\hat{q}^\beta)\cdot S^{\alpha\beta}(Q,\omega)$
%
% It also calculates spin-spin correlation function in the Blume-Maleev
% coordinate system and the complete polarised neutron scattering cross
% section.
%
% {{note The Blume-Maleev coordinate system is a cartesian coordinate
% system with $x_{BM}$, $y_{BM}$ and $z_{BM}$ basis vectors defined as:
% <br> $x_{BM}$    parallel to the momentum transfer $Q$,
% <br> $y_{BM}$    perpendicular to $x_{BM}$ in the scattering plane,
% <br> $z_{BM}$    perpendicular to the scattering plane.
% }}
%
% ### Input Arguments
%
% `spectra`
% : Input structure, contains spin-spin correlation functions. Supported
%   inputs are produced by [spinw.spinwave], [spinw.powspec] and
%   [spinw.scga].
%
% ### Name-Value Pair Arguments
%
% `'n'`
% : Normal vector to the scattering plane, in real space ($xyz$
%   coordinate system), stored in a row vector with 3 elements. Default
%   value is `[0 0 1]`.
%
% `'uv'`
% : Cell, that contains two vectors defining the scattering
%   plane in rlu. If given overwrites the `n` parameter value. For example:
%   `{[1 0 0] [0 1 0]}` stands for the $(h,k,0)$ scattering plane.
%
% `'pol'`
% : If `true` the cross sections in the Blume-Maleev
%   coordinate system will be also calculated (`inP`, `Pab` and `Mab`
%   fields of the output `spectra`). Default value is `false`.
%
% ### Output Arguments
%
% `spectra`
% : Same as the input `spectra` plus the following additional fields:
%   * `param`   Input parameters.
%   * `Sperp`   $S_\perp(i_{mode},\mathbf{Q})$ unpolarised neutron
%               scattering cross section, stored in a matrix with
%               dimensions of $[n_{mode}\times n_{hkl}]$.
%   * `intP`    $I_P(P_i,i_{mode},\mathbf{Q})$ polarised neutron scattering
%               cross section, when only the incident neutron polarization
%               is analyzed. It is stored in a matrix with dimensions of
%               $[3\times n_{mode}\times n_{hkl}]$.
%   * `Pab`     $I_{Pab}(P_f,P_i,i_{mode},\mathbf{Q})$ complete polarised
%               neutron scattering cross section, when the polarisation of
%               both the incident ($P_i$) and the scattered ($P_f$)
%               neutrons are analyzed. Stored in a matrix with dimensions
%               of $[3\times 3\times n_{mode}\times n_{hkl}]$.
%   * `Mab`     $M_{ab}(P_f,P_i,i_{mode},\mathbf{Q})$ components of the
%               spin-spin correlation function in the blume-Maleev
%               coordinate system, stored in a matrix with dimensions of
%               $[3\times \times3 n_{mode}\times n_{hkl}]$.
%
% If several domains exist in the sample, `Sperp`, `intP`, `Pab` and `Mab`
% will be packaged into a cell, that contains $n_{twin}$ number of
% matrices.
%
% The meaning of the indices above:
% * $P_i$: index of incident polarisation ($1=x_{BM}$, $2=y_{BM}$ or $3=z_{BM}$),
% * $P_f$: index of final polarisation ($1=x_{BM}$, $2=y_{BM}$ or $3=z_{BM}$),
% * $i_{mode}$: index of spin wave mode,
% * $\mathbf{Q}$: index of momentum transfer.
%
%
% ### See Also
%
% [sw_egrid] \| [spinw] \| [spinw.spinwave]
%
% *[rlu]: reciprocal lattice units
%
    """
    args = tuple(v for v in [spectra] if v is not None) + args
    return m.sw_neutron(*args, **kwargs)


def sw_model(model=None, param=None, fid=None, **kwargs):
    """
% creates predefined spin models
%
% ### Syntax
%
% `obj = sw_model(model, param)`
%
% ### Description
%
% `obj = sw_model(model, param)` generates spin models, such as triangular
% lattice antiferromagnet, square lattice, etc. It also generates the
% magnetic ground state. For each lattice arbitrary number of further
% neighbor bonds can be defined using a vector of exchange values.
%
% ### Input Arguments
%
% `model`
% : String, name of the model, one of the following:
%   * `'triAF'`     Triangular lattice Heisenberg antiferromagnet
%                   in the $ab$ plane ($a=b=3$ \\ang), with \\gamma =
%                   120\\deg angle and optimised magnetic structure.
%   * `'squareAF'`  Square lattice antiferromagnet.
%   * `'chain'`     Chain with further neighbor interactions.
%   * `swm_*`       Custom models which are in the matlab path can be
%                 evaluated. Checkout:
%                 https://www.github.com/spinw/Models for pre-made models.
%
% `param`
% : Input parameters of the model, row vector which gives the values of the
%   Heisenberg exchange for first, second, thirs etc. neighbor bonds stored
%   in `p(1)`, `p(2)`, `p(3)`, etc. respectively.
%
% ### Output Arguments
%
% `obj`
% : [spinw] class object with the selected model.
%
% ### See Also
%
% [spinw]
%
    """
    args = tuple(v for v in [model, param, fid] if v is not None)
    return m.sw_model(*args, **kwargs)


def sw_import(fName=None, toPlot=None, obj0=None, **kwargs):
    """
% create SpinW object from .cif and FullProf Studio .fst files
%
% ### Syntax
%
% `obj = sw_import(fname, {toplot})`
%
% ### Description
%
% `obj = sw_import(fname, {toplot})` can import Crystallographic
% Information Framework (.cif) files or FullProf Studio (.fst) files. It is
% also able to read .cif files from a web link.
%
% ### Input Arguments
%
% `fName`
% : String that contains the location of the source file, e.g. the full
%   path to the file or a web address.
%
% `toPlot`
% : If `true` the imported structure will be plotted, default value is
%   `false`.
%
    """
    args = tuple(v for v in [fName, toPlot, obj0] if v is not None)
    return m.sw_import(*args, **kwargs)


def sw_cff(atomName=None, Q=None, **kwargs):
    """
% returns the atomic charge form factor values for X-ray scattering
%
% ### Syntax
%
% `[formfactval, coeff] = sw_cff(atomname, {q})`
%
% ### Description
%
% `[formfactval, coeff] = sw_cff(atomname, {q})` returns the atomic charge
% form factors for x-ray scattering. The provided form factor values at Q=0
% are normalized to Z.
%
% ### Input Arguments
%
% `atomName`
% : String, contains the name of the ion in using the symbol of
%   the element following the charge, e.g. `'Cr3+'`. It can be also
%   the coefficients to calculate f. If the string contains
%   whitespace, the first word will be used as input.
%
% `Q`
% : Momentum transfer in \\ang$^{-1}$ units in a matrix with dimensions of
%   $[1\times n_Q]$ or $[3\times n_Q]$, optional.
%
% ### Output Arguments
%
% `formFactVal`
% : Value of form factor, evaluated at the $Q$ points if $Q$ is
%               defined.
%
% `coeff`
% : Form factor coefficients according to the following
%               formula:
%                   $f_0(Q_s) = c + \sum_{i=1}^5 a_i\cdot \exp(-b_i Q_s^2)$,
%               where $Q_s = \frac{Q}{4*\pi}$ and $[a_1, b_1, a_2, b_2, ... c]$ are the
%               coefficients.
%
% ### See Also
%
% [sw_mff]
%
    """
    args = tuple(v for v in [atomName, Q] if v is not None)
    return m.sw_cff(*args, **kwargs)


def sw_plotspec(spectra=None, *args, **kwargs):
    """
% plots spectrum
%
% ### Syntax
%
% `[fhandle, phandle] = sw_plotspec(spectra,Name,Value)`
%
% ### Description
%
% `[fhandle, phandle] = sw_plotspec(spectra,Name,Value)` plots excitation
% spectrum that is calculated either by [spinw.spinwave] or
% [spinw.powspec]. It can plot dispersion or intensities as line plots or
% the energy binned spectrum as a color plot. The color plots uses
% [cm_inferno] as a default colormap. To change the default colormap use
% the `swpref.setpref('colormap',@my_colomap)` command. The function is
% able to plot the spectrum if it is calculated along a path in the
% Brillouin-zone and display the labels of the high symmetry Brillouon-zone
% points.
%
% ### Name-Value Pair Arguments
%
% `'mode'`
% : Choose the type of plot using the following strings:
%   * `'disp'`  Plot dispersion as line plot.
%   * `'int'`   PLot intensity of each mode as line plot.
%   * `'color'` Color plot of energy binned spectrum.
%   * `'auto'`  Auto plot mode that tries to determine the best
%               parameteres, default.
%
% `'imag'`
% : If `true` also the imaginary part of the dispersion
%   and the correlation function values will be shown as red lines on top
%   the real values. For color plot if `true` only the imaginary part of
%   the binned data will be shown. Default value is `false`.
%
% `'aHandle'`
% : Handle of the axis object which will show the plot. If undefined the
%   active axis will be used, see [gca].
%
% `'colorbar'`
% : Plot colorbar for dispersion and intensity, default value is `true`.
%
% `'nCol'`
% : Number of colors in the colormap, default value is 500.
%
% `'dashed'`
% : If `true` dashed vertical lines between linear $Q$ segments will be
%   shown. Default is `false`.
%
% `'dE'`
% : If given, a Gaussian will be convoluted with the binned data to simulate finite
%   energy resolution. Only works if `mode=3`. If zero, no convolution
%   performed. Default value is 0.
%
% `'fontSize'`
% : Font size in pt for the labels on the plot, default value is 14 pt.
%
% `'colormap'`
% : Colormap for plotting, default value is stored in
%   `swpref.getpref('colormap')`. For single plot and for multiple plot it
%   will be a continuous scale from white to different color. This is the
%   `'auto'` mode. Also colormap can be given directly using standard
%   colormaps as function handles, e.g. `@jet`. To overplot multiple
%   spectra `colormap` option will be a matrix, with dimensions [3 nConv],
%   where every column defines a color for the maximum intensity. It is
%   also used for plotting dispersion curves. In case a single color all
%   dispersion curves have the same color (e.g. `[255 0 0]` for red), or as
%   many colors as dispersion curves in a matrix with dimensions of
%   $[3\times n_{mode}]$ or as a colormap function handle. In this case
%   every mode will have different color and the color is determined from
%   the index of the mode after the colormap is applied. Default value is
%   `'auto'`.
%
% `'sortMode'`
% : Sorting the modes by energy before plotting. Default is `false`. Can
%   improve the quality of the dispersion line plots if modes are crossing.
%
% `'axLim'`
% : Upper limit for energy axis (for `mode` 1,2) or color axis (for `mode`
%   3), default value is `'auto'`. For color plot of multiple spectra
%   the color axis cannot be changed after the plot.
%
% `'legend'`
% : Whether to plot legend for multiple convoluted spectras,
%   default value is `true`.
%
% `'title'`
% : If `true` a title will be added to the figure, default value is `true`.
%
% `'twin'`
% : Select which twins to be plotted for dispersion plots, by default the
%   spectrum corresponding to all twins will be plotted. The dimensions are
%   $[1\times n_{twinToPlot}]$.
%
% `'lineStyle'`
% : Line style for line plots (dispersion and intensity), default value
%   `{'-' 'o-' '--'}` for plotting modes that correspond to line style of
%   $S(Q,\omega)$, $S(Q+k,\omega)$ and $S(Q-k,\omega)$ cross modes in case
%   of incommensurate magnetic systems. For commensurate systems only thte
%   first string in the cell will be considered. For example '--' gives
%   dashed lines.
%
% `'lineWidth'`
% : Line width of line plots, default value is 0.5 pt.
%
% `'log'`
% : If true, the 10-based logarithmic intensity will be plotted, default
%   value is `false`.
%
% `'plotf'`
% : Function handle of the plot function for color plot. Default is
%   `surf`.
%
% `'maxPatch'`
% : Maximum number of pixels that can be plotted using the [patch]
%   function within [sw_surf]. Using [patch] for color plot can be
%   slow on older machines, but the figure can be exported
%   afterwards as a vector graphics, using the [print] function.
%   Default value is 1000.
%
% `'norm'`
% : If true, the convolution with a Gaussian function (in case of
%   non-zero `dE` parameter) keeps the energy integrated intensity. If
%   `false` the amplitude is kept constant. Default is determined by the
%   value stored in the input `spectra.norm`.
%
% `'x0'`
% : Row vector with two numbers `[x0_min x0_max]`. By default the $x$ range
%   of the plot is `[0 1]` irrespective of the values of the $Q$ values. To
%   change this the lower and upper limits can be given here.
%
% `'qlabel'`
% : Provide a list of strings for the special $Q$ points along the path in
%   the Brillouin zone, e.g. `{'X' '\Gamma' 'M' 'K' '\Gamma'}`.
%
% `'dat'`
% : Experimental data points to plot over the calculated spectrum.
%   Can be either the name of a data file that contains the
%   experimentally fitted dispersion (needs to have the same format
%   as the input file of [spinw.fitspec] see help for details on the file
%   format), or it is a structure that contains the already imported data
%   using the [sw_readtable] function, e.g.
%
%   ```
%   T = sw_readtable('myExpData.txt','\t');
%   sw_plotspec(spectra,'dat',T);
%   ```
%
% `'ddat'`
% : Maximum distance between any $Q$ point in the simulated spectrum
%   and an experimental data point in \\ang$^{-1}$ unit. If an
%   experimental data point is further from any $Q$ point than the given
%   limit, it will be omitted. Default value is 0.01.
%
% ### Output Arguments
%
% `fHandle`
% : Handle of the plot figure.
%
% `pHandle`
% : Vector that contains the handle of the graphics objects on the figure.
%
% ### See Also
%
% [spinw.plot] \| [spinw.spinwave] \| [sw_surf] \| [sw_label]
%
% *[FWHM]: Full Width at Half Maximum
%
    """
    args = tuple(v for v in [spectra] if v is not None) + args
    return m.sw_plotspec(*args, **kwargs)


def sw_rootdir(**kwargs):
    """
% path to the SpinW folder
%
% ### Syntax
%
% `rootdir = sw_rootdir`
%
% ### Description
%
% `rootdir = sw_rootdir` returns the parent folder of the `swfiles` folder.
%
% ### See Also
%
% [spinw]
%
    """
    args = []
    return m.sw_rootdir(*args, **kwargs)


def sw_res(fid=None, polDeg=None, toplot=None, *args, **kwargs):
    """
% fits energy resolution with polynomial
%
% ### Syntax
%
% `p = sw_res(source,poldeg)`
%
% `p = sw_res(source,poldeg,true)`
%
% ### Description
%
% `p = sw_res(fid,poldeg)` reads tabulated resolution data from the
% `source` file which contains the FWHM energy resolution values as a
% function of energy transfer in two columns. First  column is the energy
% transfer values (positive is energy loss), while the second is the FWHM
% of the Gaussian resolution at the given energy transfer.
%
% `p = sw_res(fid,poldeg,plot)` the polynomial fit will be shown in a
% figure if `plot` is true.
%
% ### Examples
%
% This example shows how to fit a tabulated resolution data (MERLIN energy
% resolution for $E_i=50$ meV and 300 Hz chopper frequency). Using the
% fitted polynomial, the energy resolution can be calculated at an
% arbitrary energy transfer value.
%
% ```
% >>resDat = [0 2.31;10 1.80;20 1.37;30 1.02;40 0.78;49 0.67]>>
% >>polyRes = sw_res(resDat,3)
% >>snapnow
% >>EN = 13
% >>dE = polyval(polyRes,EN)>>
% ```
%
% ### Input Arguments
%
% `source`
% : String, path to the resolution file or a matrix with two columns, where
%   the first column gives the energy transfer value and second column
%   gives the resolution FWHM.
%
% `polDeg`
% : Degree of the fitted polynomial, default value is 5.
%
% `plot`
% : If `true` the resolution will be plotted, default value
%   is `true`.
%
% ### Output Arguments
%
% `p`
% : The coefficients for a polynomial $p(x)$ of degree $n$
%   that is a best fit (in a least-squares sense) for the resolution data.
%   The coefficients in $p$  are in descending powers, and
%   the length of $p$ is $n+1$:
%
%   $p(x)=p_1\cdot x^n+p_2\cdot x^{n-1}+...+p_n\cdot x+p_{n+1}$
%
% ### See Also
%
% [polyfit] \| [sw_instrument]
%
% *[FWHM]: Full Width at Half Maximum
%
    """
    args = tuple(v for v in [fid, polDeg, toplot] if v is not None) + args
    return m.sw_res(*args, **kwargs)


def sw_mirror(n=None, V=None, **kwargs):
    """
% mirrors a 3D vector
%
% ### Syntax
%
% `[~, M] = sw_mirror(n)`
%
% `[Vp, M] = sw_mirror(n,V)`
%
% ### Description
%
% [~, M] = sw_mirror(n) generates the transformation matrix corresponding
% to a mirror plane perpendicular to `n`.
%
% `[Vp, M] = sw_mirror(n,V)` mirrors the vectors in `V`.
%
% To mirror any column vector use the following:
%
% ```
% Vp = M * V
% ```
%
% To apply mirror plane operation on tensors ($3\times 3$ matrices) use the
% following command:
%
% ```
% Ap = M * A * M'
% ```
%
% ### Input Arguments
%
% `n`
% : 3D Row vector, normal to the mirror plane.
%
% `V`
% : Matrix of 3D vectors, dimensions are $[3\times N]$.
%
% ### Output Arguments
%
% `Vp`
% : Mirrored vectors in a matrix with dimensions of $[3\times N]$.
%
% `mirM`
% : Matrix of the mirror transformation, dimensions are $[3\times 3]$.
%
% ### See Also
%
% [sw_rot]
%
    """
    args = tuple(v for v in [n, V] if v is not None)
    return m.sw_mirror(*args, **kwargs)


def sw_filelist(*args, **kwargs):
    """
% lists spinw objects in the Matlab workspace or in a .mat file
%
% ### Syntax
%
% `list = sw_filelist(Name,Value)`
%
% ### Description
%
%  `list = sw_filelist(Name,Value)` lists SpinW objects and calculated
%  spectra in the Matlab workspace of in a given .mat file.
%
% ### Examples
%
% After calculating a few spectra, we list them:
%
% ```
% >>tri = sw_model('triAF',1)
% >>sq  = sw_model('squareAF',1)
% >>specSq  = sq.spinwave({[0 0 0] [1 1 0] 21})
% >>specTri = tri.spinwave({[0 0 0] [1 0 0] 21})
% >>sw_filelist>>
% ```
%
% ### Name-Value Pair Arguments
%
% `'fName'`
% : File path in a string pointing to a .mat file, default value is empty
%   when no files are checked.
%
% `'sort'`
% : Selects the column to sort the generated table with positive/nagetive
%   sign means ascending, descending:
%   * `'+1'`/`'-1'`    variable name,
%   * `'+2'`/`'-2'`    title,
%   * `'+3'`/`'-3'`    creation date,
%   * `'+4'`/`'-4'`    completion date, default value.
%
% ### Output Arguments
%
% `list`
% : Cell of strings, lists each simulation data in the Matlab
%   memory, even data stored in cells.
%
% ### See Also
%
% [spinw.anneal] \| [spinw.spinwave]
%
    """
    
    return m.sw_filelist(*args, **kwargs)


def sw_instrument(spectra=None, *args, **kwargs):
    """
% convolutes spectrum with resolution function
%
% ### Syntax
%
% `spectra = sw_instrument(spectra,Name,Value)`
%
% ### Description
%
% `spectra = sw_instrument(spectra,Name,Value)` can convolute an energy
% binned spectrum with different energy resolution functions and add other
% effects that introduced by measurement (such as the kinematic limit for
% neutron scattering, finite momentum resolution or finite detector
% coverage).
%
%
% ### Name-Value Pair Arguments
%
% `'dE'`
% : Convolutes the spectrum with a Gaussian in energy, where the width is
%   defined by the FWHM value. The accepted values are:
%   * *string*   File name, that contains the FWHM energy
%                resolution values as a function of energy
%                transfer. The file has to contain two columns,
%                first is the energy values, the second is the
%                FWHM resolution at the given energy transfer
%                value, see [sw_res] function for details.
%   * *number*   Constant FWHM energy resolution given by the number.
%   * *matrix*   Dimensions of $[N\times 2]$, where the first column contains the
%                energy transfer values, second column contains
%                the FWHM resolution values. These discrete values will
%                be fitted using a polynomial with a fixed
%                degree, see [sw_res] for details.
%   * *function* Function handle of a resolution function
%   with the following header:
%   ```
%   E_FWHM = res_fun(E)
%   ```
%   where `E_FWHM` is the FWHM energy resolution and `E` is the energy transfer
%   value.
%
% `'func'`
% : Shape of the energy resolution function if different from Gaussian.
%   For details see [sw_resconv].
%
% `'polDeg'`
% : Degree of the polynomial that is fitted to the discrete energy
%   resolution data. Only used if `dE` is a matrix of string. Default value
%   is 5.
%
% `'dQ'`
% : Momentum transfer resolution of the instrument, FWHM is
%   given in \\ang$^{-1}$ units by default, unless different units
%   are defined in [spinw.unit]. Default value is 0 for no convolution.
%
% `'thetaMin'`
% : Minimum scattering angle in \\deg, default value is 0. Can be only
%   applied if one of the `ki`, `Ei`, `kf` or `Ef` parameters is defined.
%
% `'thetaMax'`
% : Maximum scattering angle in \\deg, default value is 135. Can be only
%   applied if one of the `ki`, `Ei`, `kf` or `Ef` parameters is defined.
%
% `'plot'`
% : If the resolution is read from file and plot option is
%   true, the energy dependent resolution values together with the
%   polynomial fit will be plotted in a new figure. Default value is
%   `true`.
%
% `'norm'`
% : If true, the data is normalized to mbarn units. Default is
%   false. If no g-tensor is included in the spin wave
%   calculation, $g = 2$ will be assumed for the conversion.
%
% `'useRaw'`
% : If `false`, the already modified `spectra.swConv` field is
%   modified further instead of the original powder spectrum
%   stored in `spectra.swRaw`. Default value is `true`.
%
% For simulating the effect of the neutron kinematic limit or the finite
% detector coverage of a neutron spectrometer one of the following
% parameter has to be given. The unit of these quantities is defined in
% [spinw.unit] with default momentum unit of \\ang$^{-1}$ and energy
% unit of meV.
%
% `'ki'`
% : Fixed momentum of the incident neutrons.
%
% `'Ei'`
% : Fixed energy of the incident neutrons.
%
% `'kf'`
% : Fixed final momentum of the neutrons.
%
% `'Ef'`
% : Fixed final energy of the neutrons.
%
% `'fid'`
% : Defines whether to provide text output. The default value is determined
%   by the `fid` preference stored in [swpref]. The possible values are:
%   * `0`   No text output is generated.
%   * `1`   Text output in the MATLAB Command Window.
%   * `fid` File ID provided by the `fopen` command, the output is written
%           into the opened file stream.
%
% ### Output Arguments
%
% `spectra`
% : Struct variable, same as input with following additional fields:
% * `norm`      `true`, if the spectrum is normalised to mbarn units.
% * `ki`        Fixed incident neutron wave vector if defined in the input.
% * `kf`        Fixed final neutron wave vector if defined in the input.
% * `dE`        Energy resolution polynomial as given in the input.
% * `dQ`        FWHM of the momentum resolution.
% * `swRaw`     Original simulated data before the application of
%               `sw_instrument`.
%
% ### See Also
%
% [polyfit] \| [polyval] \| [sw_res] \| [sw_resconv]
%
% *[FWHM]: Full Width at Half Maximum
%
    """
    args = tuple(v for v in [spectra] if v is not None) + args
    return m.sw_instrument(*args, **kwargs)


def sw_basismat(symOp=None, r=None, tol=None, **kwargs):
    """
% determines allowed tensor components in a given point group symmetry
%
% ### Syntax
%
% `[m, asym] = sw_basismat(symop, r, tol)`
%
% ### Description
%
% `[m, asym] = sw_basismat(symop, r, tol)` determines the allowed tensor
% elements compatible with a given point group symmetry. The tensor can
% describe exchange interaction or single ion anisotropy. The function
% applies the symmetry invariance of the classical energy
% $\mathbf{S}_i\cdot \mathcal{M}\cdot \mathbf{S}_j$. Thus this symmetry
% analysis includes the transformation properties of spin operators as
% well.
%
% ### Input Arguments
%
% `symOp`
% : Generators of the point group symmetry, in a matrix with dimensions of
%   $[3\times 3\times n_{sym}]$ where each `symOp(:,:,ii)` matrix defines a rotation.
%
% `r`
% : Distance column vector between the two interacting atoms. For
%   anisotropy $r=0$.
%
% `tol`
% : Tolerance, optional, default value is $10^{-5}$.
%
% ### Output Arguments
%
% `M`
% : Matrices, that span out the vector space of the symmetry
%           allowed matrices, dimensions are $[3\times 3\times n_M]$. Any matrix is
%           allowed that can be expressed as a linear combination of the
%           symmetry allowed matrices.
%
% `asym`
% : Logical vector, for each $[3\times 3]$ matrix in $M$, tells whether it is
%           antisymmetric stored in a row vector with $n_M$ elements.
%
% ### See Also
%
% [spinw.getmatrix] \| [spinw.setmatrix]
%
    """
    args = tuple(v for v in [symOp, r, tol] if v is not None)
    return m.sw_basismat(*args, **kwargs)


def sw_rot(rotAxis=None, rotAngle=None, V=None, **kwargs):
    """
% rotates vectors in 3D
%
% ### Syntax
%
% `[~, R] = sw_rot(rotAxis,rotAngle)`
%
% `[VR, R] = sw_rot(rotAxis,rotAngle,V)`
%
% ### Description
%
% `[~, R] = sw_rot(rotAxis,rotAngle)` produces the `R` rotation matrix that
% rotates any vector around the given `rotAxis` rotation axis by `rotAngle`
% angle in radian. Positive rotation is the right-hand direction around the
% rotation axis and using the following rotation formula:
% ```
% VR = R*V
% ```
%
% To rotate tensors ($3\times 3$ matrices) use the following formula:
% ```
% Mp = R * M * R';
% ```
%
% `[VR, R] = sw_rot(rotAxis,rotAngle,V)` also rotates the given `V`
% vectors where `VR` are the transformed vectors.
%
% ### Input Arguments
%
% `rotAxis`
% : Axis of rotation, stored in a row vector with 3 elements.
%
% `rotAngle`
% : Angle of rotation in radian, can be also a row vector with $n_{ang}$
%   number of elements.
%
% `V`
% : Matrix with 3 rows, where each column is a vector in 3D space.
%
% ### Output Arguments
%
% `VR`
% : Rotated vectors, stored in a matrix with dimensions of $[3\times N
%   n_{ang}]$.
%
% `R`
% : Rotation matrix with dimensions of $[3\times 3]$ if a single rotation
%   angle is given. If `rotAngle` is a vector, `R` will contain a
%   rotation matrix for each angle, it's dimensions are $[3\times 3\times
%   n_{ang}]$.
%
% ### See Also
%
% [sw_rotmat] \| [sw_mirror]
%
    """
    args = tuple(v for v in [rotAxis, rotAngle, V] if v is not None)
    return m.sw_rot(*args, **kwargs)


def gm_spherical3d(M0=None, x=None, **kwargs):
    """
% magnetic structure constraint function with spherical parameterisation
%
% ### Syntax
%
% `[m, k, n, name, pname, limit] = gm_spherical3d(S0, x)`
%
% ### Description
%
% `[m, k, n, name, pname, limit] = gm_spherical3d(S0, x)` generates
% magnetic structure from given parameters while constraining the length of
% the spin on each atom. The parametrization of the magnetic structure
% consists of 2 spherical coordinates $(\theta,\varphi)$ angles per
% magnetic atom. All angles are in radian.
%
% ### Input Arguments
%
% `x`
% : Input parameters in the following order:
%   $[\theta_1, \varphi_1, ... , k_x, k_y, k_z, n_\theta, n_\varphi]$.
%
% `S0`
% : Spin quantum number in a row vector $(S_1, S_2, ...)$ or scalar if all
%   spins are equal.
%
% ### Output Arguments
%
% `S`
% : Matrix, containing the spin orientations with dimensions of $[3\times n_{magExt}]$.
%       Every column contains the $(S_x S_y S_z)$ spin components of
%       a magnetic atom in the $xyz$ coordinate system.
%
% `k`
% : Magnetic ordering wavevector in rlu units in a row vector.
%
% `n`
% : Normal vector around which the spins are rotating for non-zero
%       propagation vector in a row vector.
%
% `name`
% : String, storing the name of the function.
%
% `pname`
% : Name of the input parameters in a cell: `{'Phi1_rad', ...}`.
%
% `limit`
% : Limits on the input parameters in a matrix with dimensions of $[2\times n_{param}]$. Every
%       column contains a lower and upper limit on the corresponding
%       parameter.
%
% ### See Also
%
% [gm_planar]
    """
    args = tuple(v for v in [M0, x] if v is not None)
    return m.gm_spherical3d(*args, **kwargs)


def sw_uniquetol(M=None, tol=None, **kwargs):
    """
% returns the unique column vectors within tolerance
%
% ### Syntax
%
% `[Mu, firstIdx] = sw_uniquetol(M,tol)`
%
% ### Description
%
% `[Mu, firstIdx] = sw_uniquetol(m,tol)` returns unique column vectors
% within the given `tol` tolerance. Two column vectors are considered
% unequal, if the distance between them is larger than the tolerance
% ($\delta$):
%
% $\sqrt{\sum_i (V_i-U_i)^2} < \delta$
%
% ### Input Arguments
%
% `M`
% : Matrix that contains column vectors.
%
% `tol`
% : Distance tolerance, default value is $10^{-5}$.
%
% ### Output Arguments
%
% `Mu`
% : Matrix that contains the unique column vectors.
%
% `firstIdx`
% : Indices pointing to the first occurence of the unique element.
%
% This function is similar to the Matlab built-in
% `unique(M,'rows','first')`, but with controllable tolerance.
%
% ### See Also
%
% [unique](https://ch.mathworks.com/help/matlab/ref/unique.html)
%
    """
    args = tuple(v for v in [M, tol] if v is not None)
    return m.sw_uniquetol(*args, **kwargs)


def sw_markdown(str=None, hotlinks=None, **kwargs):
    """
% converts markdown like text
%
% ### Syntax
%
% `sw_markdown(str,hotlinks)`
%
% ### Description
%
% `sw_markdown(str,hotlinks)` shows the help on the given function name,
% method, property name. Works the same way as the Matlab built-in
% [matlab.help] command.
%
% ### See Also
%
% [swdoc], [matlab.help]
%
    """
    args = tuple(v for v in [str, hotlinks] if v is not None)
    return m.sw_markdown(*args, **kwargs)


def sw_spec2MDHisto(spectra=None, proj=None, dproj=None, filename=None, **kwargs):
    """
% saves spectrum to MDHisto
%
% ### Syntax
%
% sw_spec2MDHisto(spectra,proj,dproj,filename)`
%
% ### Description
%
% `sw_spec2MDHisto(spectra,proj,dproj,filename)` saves a
% spectrum that is calculated by sw_egrid
%
% ### Input Arguments
% spectra: a structure calculated by sw_egrid
%
% proj: a 3x3 matrix defining an orthogonal coordinate system
%       where each column is a vector defining the orientation
%       of the view. One of the vectors must be along the Q axis
%       defined by the direction of the calculation. It is also used to define the units along the x axis.
%
% dproj: is a 3 vector that is the bin size in each of the
%        directions defined in proj. For the direction of the
%        calculation, the value used is internally calcualted from the spectrum.
%        It is wise to enter the step size for clarity.
%
% filename: is the name of the nexus file.  It will overwrite the existing
%           file if one already exists
%
% Example:
% q0 = [0 0 0];
% qmax = [2 0 0];
% nsteps = 100;
% spec = sw_egrid(spinwave(sw_model('triAF', 1), {q0 qmax nsteps}))
% proj = [[1 0 0]' [0 1 0]' [0 0 1]'];
% dproj = [1, 1e-6, 1e-6];
% sw_spec2MDHisto(spec, proj, dproj, 'testmdh.nxs');
% Note that:
% (1) In the call to `spinwave`, only one q-direction may be specified
%    e.g. the HKL specifier must be of the form {q0 q0+qdir nsteps}
% (2) one column in the `proj` matrix must be the q-direction used in
%    `spinwave` (e.g. `qdir`).
    """
    args = tuple(v for v in [spectra, proj, dproj, filename] if v is not None)
    return m.sw_spec2MDHisto(*args, **kwargs)


def sw_version(**kwargs):
    """
% returns the installed version of SpinW
%
% ### Syntax
%
% `sw_version`
%
% `ver = sw_version`
%
% ### Description
%
% `sw_version` returns the installed version of SpinW and the matlab
% version. This version number is identical to the tag of the [GitHub SpinW
% repository](https://github.com/tsdev/spinw).
%
% `ver = sw_version` returns the version information in a struct, that
% contains the program name, version, author, contact, release number,
% release date and license.
%
    """
    args = []
    return m.sw_version(*args, **kwargs)


def sw_nvect(S=None, epsilon=None, **kwargs):
    """
% determines the best normal vector for the set of vectors
%
% ### Syntax
%
% `[n, collinear] = sw_nvect(V)`
%
% `[n, collinear] = sw_nvect(V,epsilon)`
%
% ### Description
%
% `[n, collinear] = sw_nvect(V)` determines whether the given set of
% vectors are collinear or coplanar. If they are coplanar, it returns the
% best fitting normal vector, while if they are collinear returns the
% average of the given vector.
%
% The function can also deal with complex vectors, separating the real and
% complex parts as separate vectors.
%
%
% `[n, collinear] = sw_nvect(V,epsilon)` also gives the upper limit of the
% collinearity controlled by `epsilon`.
%
% ### Input Arguments
%
% `V`
% : Matrix of column vectors with dimensions of $[3\times N]$. Where each
%   column defines a vector.
%
% `epsilon`
% : Defines the limits of collinearity with the following values:
%   * `1`   the function always return the `n` closest to the collinear
%           direction,
%   * `2`   the function always return the `n` vector closest to the normal
%           of the coplanar plane.
%   * `e`   upper limit of collinearity, default value is 0.1, smaller
%           positive values mean stricter limits on collinearity.
%
% ### Output Arguments
%
% `n`
% : Row vector parallel to the collinear vector direction or
%   perpendicular to the best fitting plane of the coplanar vectors.
%
% `collinear`
% : `true` if the given set of vectors are collinear.
%
    """
    args = tuple(v for v in [S, epsilon] if v is not None)
    return m.sw_nvect(*args, **kwargs)


def gm_spherical3dd(M0=None, x=None, **kwargs):
    """
% magnetic structure constraint function with spherical parameterisation
%
% ### Syntax
%
% `[m, k, n, name, pname, limit] = gm_spherical3dd(m0, x) `
%
% ### Description
%
% Same function as [gm_spherical3d], except that the input angles are all in
% degree.
%
%
% ### See Also
%
% [gm_spherical3d]
%
    """
    args = tuple(v for v in [M0, x] if v is not None)
    return m.gm_spherical3dd(*args, **kwargs)


def sw_rotmatd(rotAxis=None, rotAngle=None, **kwargs):
    """
% generates 3D rotation matrix
%
% ### Syntax
%
% `R = sw_rotmatd(rotAxis,rotAngle)`
%
% ### Description
%
% `R = sw_rotmatd(rotAxis,rotAngle)` produces the `R` rotation matrix, for
% identically to [sw_rotmat], except that here the unit of `rotAngle` is
% \\deg.
%
% ### See Also
%
% [sw_rotmat] \| [sw_rot]
%
    """
    args = tuple(v for v in [rotAxis, rotAngle] if v is not None)
    return m.sw_rotmatd(*args, **kwargs)


def sw_mex(*args, **kwargs):
    """
% compiles and tests the mex files
%
% ### Syntax
%
% `sw_mex(Name,Value)`
%
% ### Description
%
% `sw_mex(Name,Value)` compiles and tests the generated mex files. The
% compiled mex files will speed up the [spinw.spinwave] function. The
% expected speedup is larger for smaller magnetic unit cells. Once the mex
% files are compiled, use the `swpref.setpref('usemex',true)` command to
% switch on using mex files in [spinw.spinwave].
%
% ### Name-Value Pair Arguments
%
% `'compile'`
% : If `false`, mex files will not be compiled. Default is
%   `true`.
%
% `'test'`
% : If `true`, the compiled .mex files will be tested. Default is
%   `false`.
%
% `'swtest'`
% : If `true`, 3 spin wave calculation will run with and without .mex
%   files and the results will be compared. Default is `false`.
%
% ### See Also
%
% [swpref]
%
    """
    
    return m.sw_mex(*args, **kwargs)


def sw_mff(atomName=None, Q=None, nCoeff=None, **kwargs):
    """
% returns the magnetic form factor values and coefficients
%
% ### Syntax
%
% `[~, coeff, s] = sw_mff(atomname)`
%
% `[formfactval, coeff, s] = sw_mff(atomname,Q)`
%
% ### Description
%
% `[~, coeff, s] = sw_mff(atomname)` returns the magnetic form
% factor coefficients for the magnetic atom identified by a string, e.g.
% `'MCR3'`. The function reads the [magion.dat] file for the stored form
% factor coefficients.
%
% `[formfactval, coeff, s] = sw_mff(atomname,Q)` also calculates the form
% factor values at the given $Q$ points (in \\ang$^{-1}$ units.
%
% The source of the form factor data are:
% 1. A.-J. Dianoux and G. Lander, Neutron Data Booklet (2003).
% 2. K. Kobayashi, T. Nagao, and M. Ito, Acta Crystallogr. A. 67, 473 (2011).
%
% ### Input Arguments
%
% `atomName`
% : String, contains the name of the magnetic ion in FullProf
%   notation (e.g. for Cr$^{3+} use `'MCR3'` or `'Cr3'`). It can be also a
%   vector of the 7 form factor coefficients. If the string contains
%   whitespace, the first word will be used as input. Can be also a cell of
%   strings to calculate coefficients for multiple ions.
%
% `Q`
% : Momentum transfer in \\ang$^{-1}$ units in a matrix with dimensions of
%   $[1\times n_Q]$ or $[3\times n_Q]$.
%
% ### Output Arguments
%
% `formFactVal`
% : Value of the form factor, evaluated at the given $Q$ points.
%
% `coeff`
% : Form factor coefficients according to the following formula:
%
%   $\langle j_0(Q_s)\rangle = A\exp(-a\cdot Q_s^2) + B\exp(-b\cdot Q_s^2) + C\exp(-c\cdot Q_s^2) + D\exp(-d\cdot Q_s^2) + E$
%
%   where $Q_s = \frac{Q}{4\pi}$ and $A$, $a$, $B$, ... are the coefficients.
%   The $D$ and $d$ coefficients can be zero.
%
% `S`
% : Value of the spin quantum number (read from the spin column in [magion.dat]).
%
    """
    args = tuple(v for v in [atomName, Q, nCoeff] if v is not None)
    return m.sw_mff(*args, **kwargs)


def sw_readspec(path=None, **kwargs):
    """
% read spin wave dispersion data from file
%
% ### Syntax
%
% `data = sw_readspec(datapath)`
%
% ### Description
%
% `data = sw_readspec(datapath)` reads experimental spin wave dispersion
% data from a text file at the given location. The general format of the
% data file is described in [sw_readtable] with `sw_readspec` requires
% predefined header names and only specific tag strings are allowed. The
% following header line is required:
%
% ```none
% QH QK QL minE maxE I1 E1 s1 I2 E2 s2 ...
% ```
% where:
%
% * `QH`        $h$ index of the $Q$ point in rlu,
% * `QK`        $k$ index of the $Q$ point in rlu,
% * `QL`        $l$ index of the $Q$ point in rlu,
% * `minE`      lower boundary of the $E$ scan,
% * `maxE`      upper boundary of the $E$ scan,
% * `In`        intensity of the $n$th spin wave mode,
% * `En`        center of the $n$th spin wave mode, has to be in increasing order,
% * `sn`        standard deviation of the corresponding energy
%
% The number of modes in a single line of the data file is unlimited,
% however in every line the number of modes have to be the same. Rows with
% less modes should contain zero intensities at the position of the missing
% modes.
%
% {{note `sw_readspec` omits modes that have either zero intensity
% or zero energy.}}
%
% Before any data line a special tag line can be inserted that gives the
% measured correlation in square brackets, for axample: `'[Mxx+Myy]'`. For
% the formatting of this string, see [sw_parstr]. If the measured type of
% correlation is undefined, unpolarised neutron scattering intensity is
% assumed (equivalent to `'Sperp'`). When cross sections measured in the
% Blume-Maleev coordinate system, see [sw_egrid], the normal to the
% scattering plane has to be also defined. This can be given in a second
% pair of square brackes in the $xyz$ coordinate system, for example: `'[Myy]
% [1 0 0]'`. If $n$ is undefined, the default value is `'[0 0 1]'`.
%
% ### Examples
%
% Example input data file (polarised scans in the $(0,k,l)$ scattering plane):
%
% ```none
% QH    QK        QL      ENlim1  ENlim2  I1  EN1       s1    I2  EN2       s2
% [Mxx] [1 0 0]
% 0     1        2.9992   0       15      1    3.7128   1.0   1   8.6778    1.0
% 0     1        2.8993   0       15      1    7.0000   1.0   1   11.1249   1.0
% 0     1        2.7993   0       20      1   13.8576   1.0   0   0.0       0.0
% 0     1        2.6994   0       20      1   17.3861   1.0   0   0.0       0.0
% [Myy] [1 0 0]
% 0     1.0000   2.0000   0       25      1   20.2183   1.0   0   0.0       0.0
% 0     1.1000   2.0000   15      30      1   22.7032   1.0   0   0.0       0.0
% 0     1.2000   2.0000   20      35      1   25.1516   1.0   0   0.0       0.0
% ```
%
% ### See Also
%
% [sw_egrid] \| [spinw.fitspec]
%
% *[rlu]: reciprocal lattice unit
%
    """
    args = tuple(v for v in [path] if v is not None)
    return m.sw_readspec(*args, **kwargs)


def gm_planar(absS=None, x=None, **kwargs):
    """
% planar magnetic structure constraint function
%
% ### Syntax
%
% `[s, k, n, name, pname, limit] = gm_planar(S0, x)`
%
% ### Description
%
% `[s, k, n, name, pname, limit] = gm_planar(S0, x)` generates the
% parameters of arbitrary planar magnetic structure from $\varphi$ angles
% (in radian), ordering wave vector (rlu) and spin plane normal vector
% ($xyz$).
%
%
% ### Input Arguments
%
% `x`
% : Input parameters in the following order:
%   $[\varphi_1, \varphi_2, ... , k_x, k_y, k_z, n_\theta, n_\varphi]$.
%
% `S0`
% : Spin quantum number in a row vector $(S_1, S_2, ...)$ or scalar if all
%   spins are equal.
%
% ### Output Arguments
%
% `S`
% : Matrix, containing the spin orientations with dimensions of $[3\times n_{magExt}]$.
%       Every column contains the $(S_x S_y S_z)$ spin components of
%       a magnetic atom in the $xyz$ coordinate system.
%
% `k`
% : Magnetic ordering wavevector in rlu units in a row vector.
%
% `n`
% : Normal vector around which the spins are rotating for non-zero
%       propagation vector in a row vector.
%
% `name`
% : String, storing the name of the function.
%
% `pname`
% : Name of the input parameters in a cell: `{'Phi1_rad', ...}`.
%
% `limit`
% : Limits on the input parameters in a matrix with dimensions of $[2\times n_{param}]$. Every
%       column contains a lower and upper limit on the corresponding
%       parameter.
%
% ### See Also
%
% [gm_spherical3d] \| [gm_planard]
%
% *[rlu]: Reciprocal Lattice Unit
%
    """
    args = tuple(v for v in [absS, x] if v is not None)
    return m.gm_planar(*args, **kwargs)


def sw_nb(atomName=None, **kwargs):
    """
% returns the bound coherent neutron scattering length
%
% ### Syntax
%
% `bc = sw_nb(atomname)`
%
% ### Description
%
% `bc = sw_nb(atomname)` returns the bound coherent neutron scattering
% length of a given nucleus in fm units. The function reads the stored data
% from the [isotope.dat] file.
%
% ### Input Arguments
%
% `atomName`
% : String, contains the name of the atom or isotope (e.g. `'13C'` stands
%   for the carbon-13 isotope).
%
% ### Output Arguments
%
% `bc`
% : Value of the bound coherent neutron scattering length in units of fm.
%
    """
    args = tuple(v for v in [atomName] if v is not None)
    return m.sw_nb(*args, **kwargs)


def sw_mattype(mat=None, epsilon=None, **kwargs):
    """
% classifies square matrices
%
% ### Syntax
%
% `type = sw_mattype(mat)`
%
% `type = sw_mattype(mat,epsilon)`
%
% ### Description
%
% `type = sw_mattype(mat)` determines the type of the input matrix `mat`
% which stacked $[3\times 3]$ matrices. It determines the type of exchnge
% interaction that the matrix belongs to.
%
% {{note Also works on symbolic matrices, but keep all symbols real for consistent
% result!}}
%
% ### Input Arguments
%
% `mat`
% : Matrix with dimensions of $[3\times 3\times N]$.
%
% `epsilon`
% : optional error bar on small matrix elements, default value is $10^{-5}$.
%
% ### Output Arguments
%
% `type`
% : Row vector with $N$ elements each having one of the following value:
%   * `1`   Heisenberg exchange,
%   * `2`   anisotropic exchange,
%   * `3`   DM interaction,
%   * `4`   general matrix.
%
% *[DM]: Dzyaloshinskii-Moriya
%
    """
    args = tuple(v for v in [mat, epsilon] if v is not None)
    return m.sw_mattype(*args, **kwargs)


def sw_readtable(dataSource=None, delimiter=None, nHeader=None, **kwargs):
    """
% reads tabular data from text
%
% ### Syntax
%
% `dat = sw_readtable(datasource)`
%
% `dat = sw_readtable(datasource,delimiter,nheader)`
%
% ### Description
%
% `dat = sw_readtable(datasource)` reads tabular data and converts it into
% a struct with as many number of elements as many data rows can be found
% in the source. The output field names are determined by the header line
% that begins with a string.  Moreover multiple data columns can be
% combined using the same column name in the header line multiple times and
% an additional index in brackets.
%
% The reader also supports tagging of row of data with a string. A line
% that begins with `#` defines a tag which will be applied to all following
% data until a new tag is defined. The tags are saved in the `tag` field
% of the output structure.
%
% ### Examples
%
% The content of the input file (`test.dat`) is the following:
%
% ```none
% # TEST DATA
% Q(1) Q(2)        Q(3) ENlim(1) ENlim(2) I(1)  EN(1)  s(1) I(2)   EN(2)   s(2)
% # [Mxx] [1 0 0]
% 0     1        2.9992   0       15      1    3.7128   1.0   1   8.6778    1.0
% 0     1        2.8993   0       15      1    7.0000   1.0   1   11.1249   1.0
% 0     1        2.7993   0       20      1   13.8576   1.0   0   0.0       0.0
% 0     1        2.6994   0       20      1   17.3861   1.0   0   0.0       0.0
% # [Myy] [1 0 0]
% 0     1.0000   2.0000   0       25      1   20.2183   1.0   0   0.0       0.0
% 0     1.1000   2.0000   15      30      1   22.7032   1.0   0   0.0       0.0
% 0     1.2000   2.0000   20      35      1   25.1516   1.0   0   0.0       0.0
% ```
%
% The command to import the data:
%
% ```
% >>dat = sw_readtable('test.dat')
% >>>dat = sw_readtable(sprintf('# TEST DATA\nQ(1) Q(2) Q(3) ENlim(1) ENlim(2) I(1) EN(1) s(1) I(2) EN(2) s(2)\n# [Mxx] [1 0 0]\n0 1 2.9992 0 15 1 3.7128 1.0 1 8.6778 1.0\n0 1 2.8993 0 15 1 7.0000 1.0 1 11.1249 1.0\n0 1 2.7993 0 20 1 13.8576 1.0 0 0.0 0.0\n0 1 2.6994 0 20 1 17.3861 1.0 0 0.0 0.0\n# [Myy] [1 0 0]\n0 1.0000 2.0000 0 25 1 20.2183 1.0 0 0.0 0.0\n0 1.1000 2.0000 15 30 1 22.7032 1.0 0 0.0 0.0\n0 1.2000 2.0000 20 35 1 25.1516 1.0 0 0.0 0.0\n'))
% >>dat(1)>>
% >>Q = reshape([dat(:).Q],3,[])'>>
% ```
%
% Here the imported `dat` variable will contain the fields `tag`, `Q`,
% `ENlim`, `I`, `EN` and `s` and it will have 7 entry. The `tag` variable
% will contain the `'[Mxx] [1 0 0]'` string for the first 4 entries and
% `'[Myy] [1 0 0]'` for the last 3 entries. For example the field `Q` has 3
% elements per entry and the last command above extracts all $Q$ points
% into a matrix.
%
% ### Input Arguments
%
% `dataSource`
% : Data source, can be file, url or string (must contain the newline
%   character).
%
% `delimiter`
% : Delimiter of the data, default value is whitespace.
%
% `nheader`
% : Number of header lines to be skipped in the beginning of the file.
%   Default value is 0.
%
% ### Output Arguments
%
% `dat`
% : Struct with fields defined in the data.
%
    """
    args = tuple(v for v in [dataSource, delimiter, nHeader] if v is not None)
    return m.sw_readtable(*args, **kwargs)


def sw_rotmat(rotAxis=None, rotAngle=None, **kwargs):
    """
% generates 3D rotation matrix
%
% ### Syntax
%
% `R = sw_rotmat(rotAxis,rotAngle)`
%
% ### Description
%
% `R = sw_rotmat(rotAxis,rotAngle)` produces the `R` rotation matrix that
% rotates any vector around the given `rotAxis` rotation axis by `rotAngle`
% angle in radian. Positive rotation is the right-hand direction around the
% rotation axis and using the following rotation formula:
% ```
% VR = R*V
% ```
%
% To rotate tensors ($3\times 3$ matrices) use the following formula:
% ```
% Mp = R * M * R';
% ```
%
% ### Input Arguments
%
% `rotAxis`
% : Axis of rotation, stored in a row vector with 3 elements.
%
% `rotAngle`
% : Angle of rotation in radian, can be also a row vector with $n_{ang}$
%   number of elements.
%
% ### Output Arguments
%
% `R`
% : Rotation matrix with dimensions of $[3\times 3]$ if a single rotation
%   angle is given. If `rotAngle` is a vector, `R` will contain a
%   rotation matrix for each angle, it's dimensions are $[3\times 3\times
%   n_{ang}]$.
%
% ### See Also
%
% [sw_rot] \| [sw_mirror]
%
    """
    args = tuple(v for v in [rotAxis, rotAngle] if v is not None)
    return m.sw_rotmat(*args, **kwargs)


def swhelp(funName0=None, **kwargs):
    """
% outputs the SpinW help
%
% ### Syntax
%
% `swhelp(funName)`
%
% ### Description
%
% `swhelp(funName)` shows the help on the given function name,
% method, property name. Works the same way as the Matlab built-in
% [matlab.help] command.
%
% ### See Also
%
% [swdoc], [matlab.help]
%
    """
    args = tuple(v for v in [funName0] if v is not None)
    return m.swhelp(*args, **kwargs)


def sw_magdomain(spectra=None, *args, **kwargs):
    """
% calculates the spin-spin correlation function for magnetic domains
%
% ### Syntax
%
% `spectra = sw_magdomain(spectra,Name,Value)`
%
% ### Description
%
% `spectra = sw_magdomain(spectra,Name,Value)` calculates spin-spin
% correlation function averaged over magnetic domains that are related by a
% point group operation. Several domains with different volume ratios can
% be defined. The spin-spin correlation function will be rotated and summed
% according to the domains. The rotations of the magnetic domains are
% defined in the $xyz$ coordinate system, same as the coordinate system for
% the spin-spin correlation function. The function only rotates the
% $\mathcal{S}^{\alpha\beta}$ components of the spin, but not the momentum
% $Q$, thus it cannot be used to simulate magnetic domains with different
% propagation vector.
%
% ### Examples
%
% The above example calculates the spectrum for magnetic domains that are
% related by a 90 \\deg rotation around the $z$-axis (perpendicular to the
% $ab$ plane). All domains have equal volume.
%
% ```
% spec = cryst.spinwave({[0 0 0] [1 0 0]})
% spec = sw_magdomain(spec,'axis',[0 0 1],'angled',[0 90 180 270]);
% ```
%
% ### Input Arguments
%
% `spectra`
% : Calculated spin wave spectrum.
%
% ### Name-Value Pair Arguments
%
% `'axis'`
% : Defines axis of rotation to generate domains in the $xyz$
%   coordinate system, row vector with 3 elements.
%
% `'angle'`
% : Defines the angle of rotation to generate domains in radian
%   units, multiple domains can be defined if angle is a
%   row vector with $n_{dom}$ number of elements.
%
% `'angled'`
% : Same as the `angle` parameter, just in \\deg units.
%
% `'rotC'`
% : Rotation matrices, that define crystallographic domains, alternative
%   input instead of `angle` and `axis`, matrix with dimensions of
%   $[3\times 3\times n_{dom}]$.
%
% `'vol'`
% : Volume fractions of the domains in a row vector with $n_{dom}$ number of
%   elements. Default value is `ones(1,nDom)`.
%
% ### Output Arguments
%
% `spectra`
% : Spectrum (Struct) with the following additional fields:
%   * `Sab`     The multi domain spectrum will be stored here.
%   * `Sabraw`  The original single domain spectrum is kept here, so that a
%               consecutive run of `sw_magdomain` will use the original single
%               domain spectrum, without the need of recalculating the full
%               spectrum.
%   * `domVol`  Volume of each domains in a row vector with $n_{dom}$
%               number of elements.
%   * `domRotC` Rotation matrices for each domain, with dimensions of
%               $[3\times 3\times n_{dom}]$.
%
% ### See Also
%
% [spinw.spinwave] \| [spinw.addtwin] \| [spinw.twinq]
%
    """
    args = tuple(v for v in [spectra] if v is not None) + args
    return m.sw_magdomain(*args, **kwargs)


def sw_omegasum(spectra=None, *args, **kwargs):
    """
% removes degenerate and ghost magnon modes from spectrum
%
% ### Syntax
%
% `spec = sw_omegasum(spec,Name,Value)`
%
% ### Description
%
% `spec = sw_omegasum(spec,Name,Value)` removes the degenerate modes from
% the dispersion stored in `spec.omega` and sorts the modes according to
% increasing energy. It also removes ghost modes if a lower intensity limit
% is given.
%
% The degenerate energies are substituted with `NaN` values.
%
% {{warning Be carefull, after this function [sw_egrid] won't work properly.
% This function won't work with spectra of multiple twins.}}
%
% ### Name-Value Pair Arguments
%
% `'tol'`
% : Energy tolerance, within the given value two energies are considered
%   equal. Default value is $10^{-5}$.
%
% `'zeroint'`
% : The minimum intensity value, below which the mode is removed. Default
%   value is 0 (no modes are dropped due to weak intensity).
%
% `'emptyval'`
% : Value that is assigned to modes that are removed. Default value is NaN
%   (good for plotting). 0 can be used if further numerical analysis, such
%   as binning will be applied.
%
% ### See Also
%
% [spinw.spinwave] \| [sw_egrid]
%
    """
    args = tuple(v for v in [spectra] if v is not None) + args
    return m.sw_omegasum(*args, **kwargs)


def sw_bose(oldT=None, newT=None, E=None, **kwargs):
    """
% coefficient for boson correlation functions
%
% ### Syntax
%
% `c = sw_bose(oldt,newt,e)`
%
% ### Description
%
% `c = sw_bose(oldt,newt,e)` calculates the temperature dependent
% coefficient for boson correlation functions.
%
% ### Input Arguments
%
% `oldT`
% : Original temperature in Kelvin.
%
% `newT`
% : New temperature in Kelvin.
%
% `E`
% : Energy in meV, positive is the particle creation side (neutron
%   energy loss side in a scattering experiment).
%
% ### Output Arguments
%
% `C`
% : Correction coefficients that multiplies the correlation
%           function. If any of the input is a vector, `C` will be also a
%           vector with the same dimensions.
%
    """
    args = tuple(v for v in [oldT, newT, E] if v is not None)
    return m.sw_bose(*args, **kwargs)


def sw_multicolor(vMat=None, cMap=None, cLim=None, nCol=None, cflip=None, **kwargs):
    """
% overlays monochrome maps into a single RGB map
%
% ### Syntax
%
% `cmat = sw_multicolor(vmat, cmap, clim, {ncol}, {flipud})`
%
% ### Description
%
% `cmat = sw_multicolor(vmat, cmap, clim, {ncol}, {flipud})` takes 2D
% matrices and overlays them and generating RGB color additively from the
% user defined colors correspond to each map. The function is used in
% [sw_plotspec] when multiple correlation functions are overlayed on the
% same plot.
%
% ### Examples
%
% In this example we create two intensity maps stored in the square
% matrices `A` and `B` (linearly changing intensity along $x$ and $y$ axes
% respectively, intensity ranging between -2 and 2). We plot these
% intensity maps by converting them to RGB colors using the inline function
% `rgbMap` and the Matlab built-in function `image`. We use `sw_multicolor`
% function to additively combine `A` and `B` and providing a color
% saturation value of 1 (and lowest value of -1). It is clearly visible on
% the resulting plot of `C` that it is white where both `A` and `B` has
% zero value (or below the lowest color value of -1) and it is red+green
% where both `A` and `B` are saturated.
%
% ```
% >>rgbMap  = @(mat,RGB,clim)bsxfun(@plus,ones(1,1,3),bsxfun(@times,(mat-clim(1))/diff(clim),permute(RGB(:)-1,[2 3 1])));
% >>
% >>red   = [1;0;0];
% >>green = [0;1;0];
% >>
% >>[A,B] = ndgrid(linspace(-2,2,501),linspace(-2,2,501));
% >>C = sw_multicolor(cat(3,A,B),[red green],[-1 1]);
% >>
% >>figure
% >>
% >>subplot(1,3,1)
% >>image(rgbMap(A,red,[-1 1]))
% >>title A
% >>
% >>subplot(1,3,2)
% >>image(rgbMap(B,green,[-1 1]))
% >>title B
% >>
% >>subplot(1,3,3)
% >>image(C)
% >>title C=A+B
% >>>pos = get(gcf,'Position')
% >>>pos(4) = round(pos(4)*0.4)
% >>>set(gcf,'Position',pos)
% >>snapnow
% ```
%
% ### Input Arguments
%
% `vMat`
% : Matrix that contains the input 2D intensity data, dimensions are
%   $[d_1\times d_2\times n_{plot}]$, where each intensity map has a
%   dimension of $[d_1\times d_2]$.
%
% `cMap`
% : Defines the color map that maps intensity values within the `cLim`
%   limits to colors, can be the following types:
%   * `matrix`  Matrix of RGB colors, where each column
%               corresponds to an RGB triplet. The dimension of the matrix
%               is $[3\times n_{plot}]$ and the $i$th color corresponds to
%               the color of the $i$th intensity map in the `vMat` stack.
%   * `cell`    Cell of $n_{plot}$ colormap functions. For example
%               `{@copper @gray}`.
%
% `cLim`
% : Defines the maximum and minimum intensity values that the given color
%   map will span. Values in vMat smaller than the minimum and larger than
%   the maximum will be shown with the minimum and maximum color in the
%   colormap respectively. `cLim` is a row vector with 2 elements..
%
% `nCol`
% : Number of colors in the colormap. Optional, default value is
%   100.
%
% `flipud`
% : If `true` the given colormaps are inverted. Optional, default value is
%   `false`.
%
% ### Output Arguments
%
% `cMat`
% : Matrix that contains the RGB image, with dimensions of $[d_1\times
%   d_2\times 3]$. The image can be shown using the `image` built-in Matlab
%   command.
%
% ### See Also
%
% [sw_plotspec]
%
    """
    args = tuple(v for v in [vMat, cMap, cLim, nCol, cflip] if v is not None)
    return m.sw_multicolor(*args, **kwargs)


def sw_extendlattice(nExt=None, aList=None, SS=None, **kwargs):
    """
% creates superlattice
%
% ### Syntax
%
% `aList = sw_extendlattice(nExt,aList)`
%
% `[aList, SSext] = sw_extendlattice(nExt,aList,SS)`
%
% ### Description
%
% `aList = sw_extendlattice(nExt,aList)` creates a superlattice
% and calculates all atomic positions within the new superlattice by
% tiling it with the original cell.
%
% `[aList, SSext] = sw_extendlattice(nExt,aList,SS)` also calculates the
% bond matrix for the supercell by properly including all internal bonds
% and bonds between atoms in different supercells.
%
% ### Input Arguments
%
% `nExt`
% : Size of the supercell in units of the original cell in a row vector
%   with 3 elements.
%
% `aList`
% : List of the atoms, produced by [spinw.matom].
%
% `SS`
% : Interactions matrices in the unit cell. Struct where each field
%   contains an interaction matrix.
%
% ### Output Arguments
%
% `aList`
% : Parameters of the magnetic atoms in a struct with the following fields:
%   * `RRext` Positions of magnetic atoms in lattice units of the supercell stored in a matrix with dimensions of $[3\times n_{magExt}]$.
%   * `Sext`  Spin length of the magnetic atoms in a row vector with $n_{magExt}$ number of elements.
%
% `SSext`
% : Interaction matrix in the extended unit cell, struct type.
%   In the struct every field is a matrix. Every column of the
%   matrices describes a single bond, the following fields are generally
%   defined:
% 	* `iso`     Isotropic exchange interactions.
% 	* `ani`     Anisotropic exchange interations.
% 	* `dm`      Dzyaloshinsky-Moriya interaction terms.
% 	* `gen`     General $[3\times 3]$ matrix contains the exchange interaction.
%
% ### See Also
%
% [spinw.intmatrix]
%
    """
    args = tuple(v for v in [nExt, aList, SS] if v is not None)
    return m.sw_extendlattice(*args, **kwargs)


def sw_converter(value=None, unitIn=None, unitOut=None, particleName=None, invert=None, **kwargs):
    """
% converts energy and momentum units for a given particle
%
% ### Syntax
%
% `out = sw_converter(value, unitIn, unitOut)`
%
% `out = sw_converter(value, unitIn, unitOut, particleName)`
%
% ### Description
%
% `out = sw_converter(value, unitin, unitout)` will convert momentum and
% energy values assuming neutron as a particle.
%
% `out = sw_converter(value, unitin, unitout,particleName)` will convert
% momentum and energy values for a given particle, such as neutron, photon,
% etc.
%
% ### Example
%
% Calculate the energy of a neutron (in meV) which has a wavelength of
% 5 \\ang:
%
% ```
% >>sw_converter(5,'A','meV')>>
% ```
%
% Calculate the wavelength of X-ray in \\ang that has 7.5 keV energy:
%
% ```
% >>sw_converter(7.5,'keV','A','photon')>>
% ```
%
% ### Input Arguments
%
% `value`
% : Numerical input value, can be scalar or matrix with arbitrary
%   dimensions.
%
% `unitIn`
% : Units of the input value, one of the following string:
%   * `'A-1'`        momentum in \\ang$^{-1}$,
%   * `'A^-1'`       momentum in \\ang$^{-1}$,
%   * `'k'`          momentum in \\ang$^{-1}$,
%   * `'Angstrom'`   wavelength in \\ang,
%   * `'lambda'`     wavelength in \\ang,
%   * `'A'`          wavelength in \\ang,
%   * `'\\ang'`          wavelength in \\ang,
%   * `'K'`          temperature in Kelvin,
%   * `'m/s'`        speed in m/s,
%   * `'J'`          energy in Joule,
%   * `'meV'`        energy in meV,
%   * `'eV'`         energy in eV,
%   * `'keV'`        energy in keV,
%   * `'THz'`        frequency in Thz,
%   * `'cm-1'`       $2\pi/\lambda$ in cm$^{-1}$,
%   * `'fs'`         wave period time in fs,
%   * `'ps'`         wave period time in ps,
%   * `'nm'`         wavelength in nm,
%   * `'um'`         wavelength in $\mu$m.
%
% `unitOut`
% : Units of the output value, same strings are accepted as for `unitIn`.
%
% `particleName`
% : String, the name of the particle, one of the following values:
%   `'neutron'` (default), `'proton'`, `'electron'`, `'photon'`, `'xray'`,
%   `'light'`.
%
    """
    args = tuple(v for v in [value, unitIn, unitOut, particleName, invert] if v is not None)
    return m.sw_converter(*args, **kwargs)


def sw_parstr(strIn=None, **kwargs):
    """
% parses input string
%
% ### Syntax
%
% `parsed = sw_parstr(strIn)`
%
% ### Description
%
% `parsed = sw_parstr(strIn)` parses input string containing a mathematical
% expression, a linear combination of symbols with numerical prefactors.
% The numerical symbols begin with `'S'`, `'M'` or `'P'` followed by two
% letters from the set of `'xyz'` or `'P'` can be followed be a single
% letter from the `'xyz'` set. For example a valid input string is
% `'Sxx-0.33*Syy'`.
%
% ### Examples
%
% Simple test:
% ```
% >>sw_parstr('Sxx + Syy')>>
% ```
%
% ### Input Arguments
%
% `strIn`
% : String that contains a linear combination of symbols, e.g
%   `'0.1*Sxx+0.23*Syy'`.
%
% ### Output Arguments
%
% `parsed`
% : Struct type with the following fields:
%   * `type`    Cell contains the same number of elements as in the sum. Each element
%               is a vector as follows:
%     * `type{idx}(1)`    Index of type of cross section:
%       * 1 for `Sperp`,
%       * 2 for `Sab`,
%       * 3 for `Mab`,
%       * 4 for `Pab`,
%       * 5 for  `Pa`.
%     * `type{idx}(2:3)`  Index of the component:
%       * 1 for `x`,
%       * 2 for `y`,
%       * 3 for `z`.
%   * `preFact` Vector contains the values of the prefactors in the sum.
%   * `string`  Original input string.
%
% ### See Also
%
% [sw_egrid] \| [spinw.fitspec]
    """
    args = tuple(v for v in [strIn] if v is not None)
    return m.sw_parstr(*args, **kwargs)


def sw_freemem(**kwargs):
    """
% calculates the available memory
%
% ### Syntax
%
% `mem = sw_freemem`
%
% ### Description
%
% `mem = sw_freemem` determines the available free memory (RAM). If the
% function cannot determine the size of the free memory, it returns zero.
% The function is compatible with Linux, macOS and Windows.
%
% ### Output Arguments
%
% `mem`
% : Size of free memory in bytes.
%
    """
    args = []
    return m.sw_freemem(*args, **kwargs)


def sw_qscan(qLim=None, **kwargs):
    """
% creates continuous line between coordinates
%
% ### Syntax
%
% `qOut = sw_qscan(qLim)`
%
% ### Description
%
%  `qOut = sw_qscan(qLim)` generates connected lines between given
%  positions in $n$-dimensional space ($n>1$). The output contains equally
%  spaced points along each line section in a matrix, by default 100
%  points. The function can be used to generates points along a path
%  defined by corner points.
%
% ### Input Arguments
%
% `qLim`
% : Cell that contains row vectors with $n$ elements each and optionally an
%   additional integer, e.g. `{[0 0] [1 0] 201}`.
%
% ### Examples
%
% To generate a path in the Brillouin-zone between the $(0,0,0)$, $(1,0,0)$
% and $(1,1,0)$ points with 501 points per line segment use:
%
% ```
% >>Q = sw_qscan({[0 0 0] [1 0 0] [1 1 0] [0 0 0] 501});
% >>>figure
% >>plot(Q(1,:),Q(2,:),'linewidth',2)
% >>xlabel H
% >>ylabel K
% >>>axis([-1 2 -1 2])
% >>>grid on
% >>snapnow
% ```
%
% ### See Also
%
% [sw_qgrid]
%
    """
    args = tuple(v for v in [qLim] if v is not None)
    return m.sw_qscan(*args, **kwargs)


def sw_cartesian(n=None, **kwargs):
    """
% creates a right handed Cartesian coordinate system
%
% ### Syntax
%
% `[vy, vz, vx] = sw_cartesian(n)`
%
% `V = sw_cartesian(n)`
%
% ### Description
%
% `[vy, vz, vx] = sw_cartesian(n)` creates an $(x,y,z)$ right handed
% Cartesian coordinate system with $v_x$, $v_y$ and $v_z$ defining the
% basis vectors.
%
% `V = sw_cartesian(n)` the generated basis vectors are stored in the `V`
% matrix: `V = [vx vy vz]` as column vectors.
%
% ### Input Arguments
%
% `n`
% : Either a 3 element row/column vector or a $[3\times 3]$ matrix with
%   columns defining 3 vectors.
%
% ### Output Arguments
%
% `vy,vz,vx`
% : Vectors defining the right handed coordinate system. They are
%           either column of row vectors depending on the shape of the
%           input `n`.
%
    """
    args = tuple(v for v in [n] if v is not None)
    return m.sw_cartesian(*args, **kwargs)


def sw_egrid(spectra=None, *args, **kwargs):
    """
% calculates energy bins of a spectrum
%
% ### Syntax
%
% `spectra = sw_egrid(spectra,Name,Value)`
%
% ### Description
%
% `spectra = sw_egrid(spectra,Name,Value)` takes a calculated spectrum that
% contains $S^{\alpha\beta}(Q,\omega)$ and converts it into an intensity
% map `I(i,j)` via binning the energy values and selecting a given
% component of the $9\times 9$ spin-spin correlation matrix. For example by
% default (setting the `component` parameter to `'Sperp'`) it selects the
% neutron scattering cross section via calculating the following quantity:
%
%   $S_\perp(Q,\omega)=\sum_{\alpha\beta}(1-\hat{q}^\alpha\hat{q}^\beta)\cdot S^{\alpha\beta}(Q,\omega)$
%
%
% ### Examples
%
% The line will create an energy bin, with steps of 0.1 and bins the
% spin-spin correlation function. Two different matrices will be
% calculated, first using the sum of the $S^{xx}$ and $S^{yy}$ components, second
% will contain the $S^{zz}$ component of the correlation function.
%
% ```
% >>tri = sw_model('triAF',1)
% >>spectra = tri.spinwave({[0 0 0] [1 1 0] 501})
% >>E = linspace(0,5,501)
% >>spectra = sw_egrid(spectra,'component',{'Sxx+Syy' 'Szz'},'Evect',E)
% >>figure
% >>sw_plotspec(spectra,'mode','color','axLim',[0 0.5],'dE',0.2)
% >>snapnow
% ```
%
% ### Input Arguments
%
% `spectra`
% : Input structure, contains spin-spin correlation functions. Supported
%   inputs are produced by [spinw.spinwave], [spinw.powspec] and
%   [spinw.scga].
%
% ### Name-Value Pair Arguments
%
% `'component'`
% : A string that Selects a correlation function component that will be
%   binned. The possible values are:
%   * `'Sperp'` bins the magnetic neutron scattering intensity
%     (the $\langle S_\perp S_\perp\rangle$ expectation value). Default.
%   * `'Sab'`   bins the selected components of the spin-spin
%               correlation function. Letter `a` and `b` can be `x`,
%               `y` or `z`. For example: `'Sxx'` will convolute the
%               $S^{xx}(Q,\omega)$ component of the correlation function with the
%               dispersion. Here the $xyz$ is the standard coordinate system.
%   *`'Mab'`    bins the selected components of the spin-spin
%               correlation function in the Blume-Maleev coordinate system.
%               Letter `a` and `b` can be `x`, `y` or `z`. For example:
%               `'Mxx'` will convolute the `xx` component of the
%               correlation function with the dispersion.
%   * `'Pab'`   bins the selected component of the polarisation
%               matrix. Letter `a` and `b` can be `x`, `y` or `z`. For
%               example: `'Pyy'` will convolute the `yy` component of
%               the polarisation matrix with the dispersion. The
%               coordinates used are in the Blume-Maleev coordinate
%               system, see below.
%   * `'Pa'`    bins the intensity of the calculated polarised
%               neutron scattering, with inciden polarisation of
%               `Pa` where letter `a` can be `x`, `y` or `z`. For example:
%               `'Py'` will convolute the scattering intensity
%               simulated for incident polarisation $P_i\|y$. The
%               used coordinates are in the Blume-Maleev coordinate
%               system.
%   * `'fName'` where `fName` is one of the field names of the input
%               structure spectra. This field should contain a
%               matrix with dimensions of $[n_{mode}\times n_{hkl}]$.
%
%   Any linear combination of the above are allowed, for example:
%   `'Sxx+2*Syy'` will bin the linear combination of the `xx` component of
%   the spin-spin correlation function with the `yy` component.
%   Several cross section can be convoluted and stored
%   independently, if component is a cell array containing strings
%   each containing any linear combination of cross sections as
%   above, the cell array needs to have size $[1\times n_{cell}]$, for
%   example `{'Sxx' 'Syy' 'Szz'}`.
%
% `'Evect'`
% : Row vector that defines the center/edge of the energy bins of the
%   calculated output, number of elements is $n_E$. The energy units
%   are defined by the [spinw.unit] property. Default
%   value is an edge bin: `linspace(0,1.1*maxOmega,501)`.
%
% `'binType'`
% : String, determines the type of bin give, possible options:
%   * `'cbin'`      Center bin, the center of each energy bin is given.
%   * `'ebin'`      Edge bin, the edges of each bin is given.
%   Default value is `'ebin'`.
%
% `'T'`
% : Temperature, used to calculate the Bose factor in units
%   depending on the Boltzmann constant stored in [spinw.unit]. Default
%   temperature is taken from `obj.single_ion.T`. The Bose factor is
%   included in `swConv` field of the output.
%
% `'sumtwin'`
% : If true, the spectra of the different twins will be summed
%   together weighted with the normalized volume fractions, see
%   [spinw.twin]. Default value is true.
%
% `'modeIdx'`
% : Select certain spin wave modes from the $2*n_{magatom}$ number of
%   modes to include in the output. Default value is `1:2*nMagAtom` to
%   include all modes.
%
% `'epsilon'`
% : DEPRECATED (previously the error limit, used to determine whether a
%   given energy bin is uniform or not. Default value is $10^{-5}$). This
%   parameter is no longer relevant and is ignored.
%
% `'autoEmin'`
% : Due to the finite numerical precision, the spin wave energies
%   can contain small imaginary values. These can ruin the
%   convoluted spectrum at low energies. To improve the spectrum,
%   the lowest energy bin should start above the imaginary part of
%   the spin wave energy. If `'autoEmin'` is set to `true`, it
%   calculates the bottom of the first energy bin automatically and
%   overwrites the given value. Only works if the input energy bin
%   starts with zero. Default value is `false`.
%
% `'imagChk'`
% : Checks whether the imaginary part of the spin wave dispersion is
%   smaller than the energy bin size. Default value is true.
%
% `dE`
% : Energy resolution (FWHM) can be function, or a numeric matrix that
%   has length 1 or the number of energy bin centers.
%
% {{note The Blume-Maleev coordinate system is a cartesian coordinate
% system with $x_{BM}$, $y_{BM}$ and $z_{BM}$ basis vectors defined as:
% <br> $x_{BM}$    parallel to the momentum transfer $Q$,
% <br> $y_{BM}$    perpendicular to $x_{BM}$ in the scattering plane,
% <br> $z_{BM}$    perpendicular to the scattering plane.
% }}
%
% ### Output Arguments
%
% `spectra` same as the input `spectra` plus additions fields:
%
% `swConv`
% : Stores the selected cross section binned in energy in a matrix with
%   dimensions of $[n_E\times n_{hkl}]$. Includes the Bose factor.
%
% `swInt`
% : Stores the selected cross sections for every mode in a matrix with
%   dimensions of $[n_{mode}\times n_{hkl}]$.
%
% `T`
% : Input temperature.
%
% `component`
% : Cell that contains the input component selector strings.
%
% `Evect`
% : Input energy bin vector, defines the energy bin **edge** positions
%   (converted from the given bin centers if necessary).
%
% `zeroEnergyTol`
% : Eigenvalues with magnitude of the real component less than zeroEnergyTol
%   will be not be included in the structure factor binning
%
% `param`
% : All the input parameters.
%
% If `'component'` parameter is a cell array or the spectra of multiple
% twins are convoluted separately, swConv and swInt will be a cell that
% packages the matrices corresponding to each component/twin. The
% dimensions of the cell are $[n_{conv}\times n_{twin}]$.
%
% ### See Also
%
% [spinw.spinwave] \| [sw_neutron]
%
    """
    args = tuple(v for v in [spectra] if v is not None) + args
    return m.sw_egrid(*args, **kwargs)


def sw_timeit(percent=None, *args, **kwargs):
    """
% timer and remaining time estimator
%
% ### Syntax
%
% `sw_timeit(percent, {mode},{tid},{title})`
%
% ### Description
%
% `sw_timeit(percent, {mode},{tid},{title})` can display remaining time of
% a calculation that is run for a fixed number of iterations. It can output
% the status both in the Command Window and in a pup up window using
% [waitbar].
%
% ### Input Arguments
%
% `percent`
% : Percentage of the calculation that is already done.
%
% `mode`
% : Controls the time estimation, optional parameter:
%   * `1` Starts the time estimation.
%   * `0` Displays of the remaining time, default value.
%   * `2` The calculation finished, show a summary.
%
% `tid`
% : Determines if the elapsed and required time for the calculation is
%   displayed. The default value is determined by the `tid` preference
%   stored in [swpref]. The following values are allowed:
%   * `0` No timing is displayed.
%   * `1` Display the timing in the Command Window.
%   * `2` Show the timing in a separat pup-up window.
%
% `title`
% : The text to show in the pup up window.
%
% ### See Also
%
% [waitbar]
%
    """
    args = tuple(v for v in [percent] if v is not None) + args
    return m.sw_timeit(*args, **kwargs)


def sw_atomdata(atomSymb=None, datType=None, **kwargs):
    """
% returns information on chemical elements
%
% ### Syntax
%
% `data = sw_atomdata(atomsymb)`
%
% `data = sw_atomdata(atomsymb,datatype)`
%
% ### Description
%
% `data = sw_atomdata(atomsymb)` returns information on chemical elements
% (RGB color code, mass, long name) in a struct. The element is identified
% by its short name, such as 'O' for oxygen. If the given atom name does
% not exists, the function returns the data for `'Unobtanium'`. The
% database is stored in the [atom.dat] file.
%
% `data = sw_atomdata(atomsymb,datatype)` returns only the requested type
% of data.
%
% ### Examples
%
% The radius of the hydrogen atom:
% ```
% >>r_H = sw_atomdata('H','radius')>>
% ```
%
% ### Input Arguments
%
% `atomSymb`
% : String of the name of the atom, for example 'He' or the atomic
%   number Z. If the string contains whitespace character, the
%   second word will be used to identify the atom.
%
% `dataType`
% : Type of information requested, following strings are accepted:
%   * `'name'`        Atomic symbol.
%   * `'radius'`      Atomic radius.
%   * `'color'`       Color of the atom from the [CPK color scheme](https://en.wikipedia.org/wiki/CPK_coloring).
%   * `'mass'`        Average mass of the element.
%   * `'longname'`    Name of the element.
%   * `'Z'`           Atomic index.
%   * `'all'`         All atomic data returned in a struct.
%
% ### See Also
%
% [sw_mff] \| [sw_cff]
%
    """
    args = tuple(v for v in [atomSymb, datType] if v is not None)
    return m.sw_atomdata(*args, **kwargs)


def sw_fstat(state=None, parIn=None, T=None, E=None, M=None, _=None, **kwargs):
    """
% calculates thermodynamical averages
%
% ### Syntax
%
% `parOut = sw_fstat(state, parIn, T, E, M, nExt)`
%
% ### Description
%
% `parOut = sw_fstat(state, parIn, T, E, M, nExt)` calculates statistical
% properties of different physical variables over several sampled state.
% The function is called by [spinw.anneal].
%
% ### Input Arguments
%
% `state`
% : Defines the task of the function.
%   * `1`   Initialize the parOut structure.
%   * `2`   Store the parameters of the physical state.
%   * `3`   Calculate physical properties from the variable
%           statistics.
%
% `parIn`
% : Same as `parOut`.
%
% `T`
% : Temperature of the system, row vector with $n_T$ number of elements.
%
% `E`
% : Energy of the system, row vector with $n_T$ number of elements.
%
% `M`
% : Magnetic moment of every atom in a matrix with dimensions of $[d_{spin}\times n_{magExt}\cdot n_T]$.
%
% `nExt`
% : Size of the magnetic supercell, column vector of 3 integers.
%
% `kB`
% : Boltzmann constant, units of temperature.
%
% ### Output Arguments
%
% `parOut`
% : Output parameter structure with the following fields:
%   * `nStat`   The number of evaluated states.
%   * `M`       $\langle M\rangle$ averaged over all magnetic moment stored
%               in a matrix with dimensions of $[d){spin}\times
%               n_{magExt}\cdot n_T]$.
%   * `M2`      $\langle M^2\rangle$ averaged over all magnetic moment
%               stored in a matrix with dimensions of $[d){spin}\times
%               n_{magExt}\cdot n_T]$.
%   * `E`       $\langle E\rangle$  summed over all magnetic moment.
%   * `E2`      $\langle E^2\rangle$  summed over all magnetic moment.
%
% For the final execution, the following parameters are calculated:
% `parOut`
% : Array of struct with $n_T$ number of elements:
%   * `avgM`    Average components of the magnetisation over $n_{stat}$ runs,
%               matrix with dimensions of $[3\times n_{magExt}]$.
%   * `stdM`    Standard deviation of the mgnetisation components over
%               $n_{stat}$ runs, matrix with dimensions of $[3\times n_{magExt}]$.
%   * `avgE`    Average system energy per spin over $n_{stat}$ runs, scalar.
%   * `stdE`    Standard deviation of the system energy per spin over
%               $n_{stat}$ runs, scalar.
%   * `T`       Final temperature of the sample.
%   * `Cp`      Heat capacity of the sample: $(\langle E^2\rangle-\langle E\rangle^2)/k_B/T^2$.
%   * `Chi`     Magnetic susceptibility of the sample: $(\langle M^2\rangle-\langle M\rangle^2)/k_B/T$.
%
% ### See Also
%
% [spinw.anneal]
%
    """
    args = tuple(v for v in [state, parIn, T, E, M] if v is not None)
    return m.sw_fstat(*args, **kwargs)


def sw_qgrid(*args, **kwargs):
    """
% creates a Q grid
%
% ### Syntax
%
% `qgrid = sw_qgrid(Name,Value)`
%
% ### Description
%
% `qgrid = sw_qgrid(Name,Value)` generates n-dimensional grids ($n<=3$) in
% 3D space, e.g. points on a line in 3D. It uses $n$ linearly independent
% vectors ("lattice vectors") and bin values (coordinates in "lattice
% units" or "lu") to generate the points. It works similarly as the d3d
% constructor in [Horace](http://horace.isis.rl.ac.uk/Main_Page).
%
% ### Name-Value Pair Arguments
%
% `'u'`
% :  Row vector with 3 elements, determines the first axis in 3D
%    space, default value is `[1 0 0]`.
%
% `'v'`
% :  Second axis, default value is `[0 1 0]`.
%
% `'w'`
% :  Third axis, default value is `[0 0 1]`.
%
% `'uoffset'`
% :  Row vector with 3 elements, determines the offset of origin
%    in lu, (fourth element is accepted but discarded).
%
% `'ubin'`
% :  Bin points along the first axis. Can be a vector with 1, 2 or 3
%    elements:
%
%    * `[B1]`        single value along the $u$-axis at a coordinate of `B1*u`
%    * `[B1 B2]`     range along the $u$-axis at coordinates of `[B1:1/nExt:B2]*u`
%    * `[B1 dB B2]`  range along the $u$-axis at coordinates of `[B1:dB:B2]*u`
%
% `'vbin'`
% :  Same as `ubin` but along the $v$-axis.
%
% `'wbin'`
% :  Same as `ubin` but along the $w$-axis.
%
% `'nExt'`
% :  Vector with $n$-elements that can define fractional bin steps,
%    default values is `[1 1 1]`.
%
% `'lab'`
% :  Cell array of projection axis labels with 3 elements (4th
%    element discarded), e.g. `{'x' 'y' 'z'}`.
%
% The dimension count $n$ is determined by the number of given bins
% ($1<=n<=3$), so if only `ubin` is given, $n=1$; if both `ubin` and `vbin`
% are defined then $n=2$, etc.
%
% `'fid'`
% : Defines whether to provide text output. The default value is determined
%   by the `fid` preference stored in [swpref]. The possible values are:
%   * `0`   No text output is generated.
%   * `1`   Text output in the MATLAB Command Window.
%   * `fid` File ID provided by the `fopen` command, the output is written
%           into the opened file stream.
%
% ### Output Arguments
%
% `qGrid`
% : A matrix with dimensions of $[3\times n_{ax1}\times n_{ax2},...]$,
%   where $n_{axi}$ is the index of points along $i$th axis with $1<=i<=n$.
%
% ### See Also
%
% [sw_qscan]
%
    """
    
    return m.sw_qgrid(*args, **kwargs)


def sw_xray(spectra=None, *args, **kwargs):
    """
% calculates x-ray scattering cross section
%
% ### Syntax
%
% `spectra = sw_xray(spectra,Name,Value)`
%
% ### Description
%
% `spectra = sw_xray(spectra,Name,Value)` calculates x-ray scattering
% intensity for non-resonant inelastic x-ray scattering on phonons.
%
%
% ### Input Arguments
%
% `spectra`
% : Input structure that contains the displacement-displacement
%   correlation function.
%
% ### Name-Value Pair Arguments
%
% `'formfact'`
% : If true, the magnetic form factor is included in the spin-spin
%   correlation function calculation. The form factor coefficients are
%   stored in `obj.unit_cell.ff(1,:,atomIndex)`. Default value is `false`.
%
% `'formfactfun'`
% : Function that calculates the magnetic form factor for given $Q$ value.
%   value. Default value is `@sw_mff`, that uses a tabulated coefficients
%   for the form factor calculation. For anisotropic form factors a user
%   defined function can be written that has the following header:
%   ```
%   F = formfactfun(atomLabel,Q)
%   ```
%   where the parameters are:
%   * `F`           row vector containing the form factor for every input
%                   $Q$ value
%   * `atomLabel`   string, label of the selected magnetic atom
%   * `Q`           matrix with dimensions of $[3\times n_Q]$, where each
%                   column contains a $Q$ vector in $\\ang^{-1}$ units.
%
% `'fid'`
% : Defines whether to provide text output. The default value is determined
%   by the `fid` preference stored in [swpref]. The possible values are:
%   * `0`   No text output is generated.
%   * `1`   Text output in the MATLAB Command Window.
%   * `fid` File ID provided by the `fopen` command, the output is written
%           into the opened file stream.
%
% ### Output Arguments
%
% `spectra`
% : Structure that is same as the input with the following additional
%   fields:
%   * `param`   Input parameters.
%   * `Sperp`   $S_\perp(i_{mode},\mathbf{Q})$ x-ray scattering cross
%               section, stored in a matrix with dimensions of
%               $[n_{mode n_{hkl}]$.
%
% ### See Also
%
% [spinw] \| [spinw.spinwave] \| [sw_neutron]
%
    """
    args = tuple(v for v in [spectra] if v is not None) + args
    return m.sw_xray(*args, **kwargs)


def sw_hassymtoolbox(**kwargs):
    """
% Checks if the running Matlab instance has the symbolic toolbox
%
% ### Syntax
%
% `has_toolbox = sw_hassymtoolbox()`
%
% ### Description
%
% This function checks if the symbolic toolbox is available
%
    """
    args = []
    return m.sw_hassymtoolbox(*args, **kwargs)


def sw_issymspec(spectra=None, **kwargs):
    """
% Checks if a given spectrum structure is symbolic or not
%
% ### Syntax
%
% `issym = sw_issymspec(spectra)`
%
% ### Description
%
% Calling spinwave() for a symbolic spinw object results in
% a symbolic spectrum which cannot be used with sw_neutron etc.
% This function checks if a given spectrum is symbolic or not.
%
% ### Input Arguments
%
% `spectra`
% : Input spectra structure.
%
    """
    args = tuple(v for v in [spectra] if v is not None)
    return m.sw_issymspec(*args, **kwargs)


def sw_surf(X=None, Y=None, C=None, cLim=None, cMap=None, maxPatch=None, **kwargs):
    """
% SW_SURF draws a two dimensional plot using the patch function when the
% figure is saved in .pdf format, it is saved as a vector image
%
% Usage:
%
% SW_SURF(C)
%
% SW_SURF(X,Y,C,cLim,cMap)
%
% Input:
%
% X         Matrix of x coordinates, dimensions are [nX nY].
% Y         Matrix of y coordinates, dimensions are [nX nY].
% C         Matrix to plot, dimensions are [nX nY].
% cLim      Color axis limits, if undefined the minimum and maximum values
%           C are taken as limits.
% cMap      Colormap, default is @jet.
% maxPatch  Maximum number of pixels that can be plotted using the patch()
%           function. Using patch for color plot can be slow on older
%           machines, but the figure can be exported afterwards as a vector
%           graphics, using the print() function. Default is 1000.
%
% Change of the color axis after plotting is not possible, replot is
% necessary.
%
    """
    args = tuple(v for v in [X, Y, C, cLim, cMap, maxPatch] if v is not None)
    return m.sw_surf(*args, **kwargs)


def sw_sub1(inp=None, *args, **kwargs):
    """
% converts symbolic variables into double by substituting 1 for every symbol
%
% out = SW_SUB1(inp, num)
%
% Input:
%
% inp   Any symbolic/double type matrix.
% num   Can be scalar or vector with the number of elements equal to the
%       number of symbolic variables in inp. If it is 'rand', random values
%       will be assigned to each symbolic variable in inp.
%
% Output:
%
% out   Double type output with the same dimensions as the input.
%
% See also SW_ALWAYS.
%
    """
    args = tuple(v for v in [inp] if v is not None) + args
    return m.sw_sub1(*args, **kwargs)


def sw_createpcr(path=None, pcrFile=None, perm=None, **kwargs):
    """
% SW_CREATEPCR(path, pcrFile, perm) creates the structural part of a pcr
% file from a .cif file.
%
% This function will create the atomic positions from a .cif file.
% pcr file is the control file for FullProf Rietveld refinement software.
%
% perm  Permutation of the (x,y,z) coordinates.
%
    """
    args = tuple(v for v in [path, pcrFile, perm] if v is not None)
    return m.sw_createpcr(*args, **kwargs)


def sw_always(inp=None, **kwargs):
    """
% converts symbolic logical expressions into logical expressions
%
% out = SW_ALWAYS(inp)
%
% Use carefully, for undecided results return false without warning!
%
% Input:
%
% inp   Any symbolic/logical or numeric type matrix.
%
% Output:
%
% out   Logical output with the same dimensions as the input.
%
    """
    args = tuple(v for v in [inp] if v is not None)
    return m.sw_always(*args, **kwargs)


def struct(obj=None, **kwargs):
    """
% converts properties into struct
%
% ### Syntax
%
% `objS = struct(obj)`
%
% ### Description
%
% `objS = struct(obj)` converts all public properties of `obj` and saves
% them into `objS` struct.
%
% ### See Also
%
% [spinw] \| [spinw.copy]
%
    """
    args = tuple(v for v in [obj] if v is not None)
    return m.struct(*args, **kwargs)


def twinq(obj=None, Q0=None, **kwargs):
    """
% calculates equivalent Q point in twins
%
% ### Syntax
%
% `[qTwin, rotQ] = twinq(obj, {Q0})`
%
% ### Description
%
% `[qTwin, rotQ] = twinq(obj, {q0})` calculates the $Q$ values in the twin
% coordinate systems, in rlu. It also returns the rotation matrices, that
% transforms the $Q$ point from the original lattice to the selected twin
% rlu coordinate system.
%
% ### Examples
%
% This example Calculates the $[1,0,0]$ and $[1,1,0]$ Bragg reflections
% equivalent positions in the twins.
%
% ```
% Q1 = [1 0 0; 1 1 0];
% Q2 = cryst.twinq(Q1');
% ```
%
% ### Input Arguments
%
% `Q0`
% : $Q$ values in the original crystal in rlu sotred in a matrix with
% dimensions of $[3\times n_Q]$, optional.
%
% ### Output Arguments
%
% `Qtwin`
% : $Q$ values in the twin oordinate system in a cell element for
%           each twin.
%
% `rotQ`
% : Rotation matrices with dimensions of $[3\times 3\times n_{twin}]$.
%
% ### See Also
%
% [spinw] \| [spinw.addtwin]
%
% *[rlu]: Reciprocal Lattice Unit
%
    """
    args = tuple(v for v in [obj, Q0] if v is not None)
    return m.twinq(*args, **kwargs)


def setunit(obj=None, *args, **kwargs):
    """
% sets the physical units
%
% ### Syntax
%
% `setunit(obj,Name,Value)`
%
% ### Description
%
% `setunit(obj,Name,Value)` sets the physical units of the Hamiltonian.
% This includes the magnetic field, exchange interaction, length and
% temperature.
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% `'mode'`
% : Type of unit system, defined by one of the following strings:
%   * `'AmeVTK'`    Typical units used in neutron/x-ray scattering:
%                       [\\ang, meV, Tesla and Kelvin]
%   * `'1'`         No units, all conversion factors are set to 1.
%
% ### See Also
%
% [spinw.unit]
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.setunit(*args, **kwargs)


def setmatrix(obj=None, *args, **kwargs):
    """
% sets exchange tensor values
%
% ### Syntax
%
% `setmatrix(obj,Name,Value)`
%
% ### Description
%
% `setmatrix(obj,Name,Value)` sets the value of a selected matrix based on
% symmetry analysis.
%
% ### Examples
%
% This example will set 'J1' coupling to the 6th symmetry allowed matrix,
% with prefactor 0.235.
% ```
% setmatrix(crystal,'label','J1','pref',{[6 0.235]})
% ```
% This will set 'J2' to antiferromagnetic Heisenberg exchange, with value
% of 1.25 meV.
% ```
% setmatrix(crystal,'label','J2','pref',{1.25})
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% One of the below options has to be given:
%
% `'mat'`
% : Label or index of the matrix that is already assigned to
%   a bond, anisotropy or g-tensor.
%
% `'bond'`
% : Index of the bond in `spinw.coupling.idx`, e.g. 1 for first neighbor.
%
% `'subIdx'`
% : Selects a certain bond within the symmetry equivalent bonds, within
%   default value is 1.
%
% `'aniso'`
% : Label or index of the magnetic atom that has a single ion
%   anisotropy matrix is assigned, e.g. `'Cr3'` to select anisotropy on
%   atoms with this label.
%
% `'gtensor'`
% : Label or index of the magnetic atom that has a g-tensor is
%   assigned.
%
% Optional inputs:
%
% `'pref'`
% : Defines prefactors as a vector for the symmetry allowed
%           components in a row vector with $n_{symMat}$ number of elements. Alternatively, if only
%           a few of the symmetry allowed matrices have non-zero
%           prefactors, use:
%   ```
%   {[6 0.1 5 0.25]}
%   ```
%   This means, the 6th symmetry allowed matrix have prefactor 0.1,
%           the 5th symmetry allowed matrix have prefactor 0.25. Since
%           Heisenberg isotropic couplings are always allowed, a cell with
%           a single element will create a Heisenberg coupling, example:
%   ```
%   {0.1}
%   ```
%   This is identical to `obj.matrix.mat = eye(3)*0.1`.
%           For DM interactions (antisymmetric coupling matrices), use
%           three element vector in the cell:
%   ```
%   {[D1 D2 D3]}
%   ```
%   In this case, these will be the prefactors of the 3
%           antisymmetric symmetry allowed matrices. In case no crystal
%           symmetry is defined, these will define directly the components
%           of the  DM interaction in the $xyz$ coordinate system. Be
%           carefull with the sign of the DM interaction, it depends on the
%           order of the two interacting atoms! Default value is `{1}`.
%           For anisotropy matrices antisymmetric matrices are not allowed.
%
% ### Output Arguments
%
% The selected `obj.matrix.mat` will contain the new value.
%
% ### See Also
%
% [spinw] \| [spinw.gencoupling] \| [spinw.getmatrix]
%
% *[DM]: Dzyaloshinskii-Moriya
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.setmatrix(*args, **kwargs)


def notwin(obj=None, **kwargs):
    """
% removes all twins
%
% ### Syntax
%
% `notwin(obj)`
%
% ### Description
%
% `notwin(obj)` removes any crystallographic twin added using the
% [spinw.addtwin] function.
%
% ### See Also
%
% [spinw.addtwin]
%
    """
    args = tuple(v for v in [obj] if v is not None)
    return m.notwin(*args, **kwargs)


def optmagk(obj=None, *args, **kwargs):
    """
% determines the magnetic propagation vector
%
% ### Syntax
%
% `res = optmagk(obj,Name,Value)`
%
% ### Description
%
% `res = optmagk(obj,Name,Value)` determines the optimal propagation vector
% using the Luttinger-Tisza method. It calculates the Fourier transform of
% the Hamiltonian as a function of wave vector and finds the wave vector
% that corresponds to the smalles global eigenvalue of the Hamiltonian.
% The global optimization is achieved using Particle-Swarm optimizer. This
% function sets k and F in spinw.mag_str, and also returns them.
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% `kbase`
% : Provides a set of vectors that span the space for possible propagation
%   vectors:
%
%   $ \mathbf{k} = \sum_i C(i)\cdot \mathbf{k}_{base}(i);$
%
%   where the optimiser determines the $C(i)$ values that correspond
%      to the lowest ground state energy. $\mathbf{k}_{base}$ is a
%      matrix with dimensions $[3\times n_{base}]$, where $n_{base}\leq 3$. The basis
%      vectors have to be linearly independent.
%
% The function also accepts all options of [ndbase.pso].
%
% ### Output Arguments
%
% `res`
% : Structure with the following fields:
%   * `k`       Value of the optimal k-vector, with values between 0
%                       and 1/2.
%   * `F`       Fourier components for every spin in the magnetic
%                       cell.
%   * `E`       The most negative eigenvalue at the given propagation
%                       vector.
%   * `stat`    Full output of the [ndbase.pso] optimizer.
%
% ### See Also
%
% [ndbase.pso]
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.optmagk(*args, **kwargs)


def addmatrix(obj=None, *args, **kwargs):
    """
% adds new 3x3 matrix
%
% ### Syntax
%
% `addmatrix(obj,Name,Value)`
%
% ### Description
%
% `addmatrix(obj,Name,Value)` adds a new $[3\times 3]$ matrix to the
% [spinw.matrix] field of `obj`. The added matrices can be later assigned
% to bonds, single ion anisotropy terms or g-tensors of magnetic atoms. If
% the given matrix label already exists in `obj`, instead of adding new
% matrix the existing one will be overwritten.
%
% ### Examples
%
% The first example adds a diagonal matrix `eye(3)`, that can describe
% Heisenberg interaction if assigned to a bond. The second example adds an
% ansisymmetric matrix that can decribe Dzyaloshinskii-Moriya (DM)
% interaction if assigned to a bond.
%
% ```
% >>crystal = spinw
% >>crystal.addmatrix('value',1,'label','J_1')
% >>crystal.matrix.mat>>
% >>crystal.addmatrix('value',[1 0 0],'label','J_1')
% >>crystal.matrix.mat>>
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% `'value'`
% : The actual numerical values to be added as a matrix. It can have the
%   following shapes:
%   * $[3\times 3]$ the given values will be stored in [spinw.matrix] as
%     they are given.
%   * $[1\times 1]$ the given value will be multiplied with `eye(3)`.
%   * `[Mx My Mz]` the given triplet will be used to define an
%     antisymmetric matrix `M = [0 M3 -M2;-M3 0 M1;M2 -M1 0]`.
%
% `'label'`
% : Label string for plotting default value is `'matI'`, where $I$ is the index
%   of the matrix. Add '-' to the end of the label to plot bond as dashed
%   line/cylinder.
%
% `'color'`
% : Color for plotting, either row vector
%   that contains color RGB codes (values of 0-255), or a string with the
%   name of the color, for possible colors names [swplot.color]. Default
%   color is a random color.
%
% ### Output Arguments
%
% The `obj` output will contain the additional matrix in the [spinw.matrix]
% field.
%
% ### See Also
%
% [spinw] \| [swplot.color]
%
% *[DM]: Dzyaloshinski-Moriya
% *[RGB]: Red-Green-Blue
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.addmatrix(*args, **kwargs)


def couplingtable(obj=None, *args, **kwargs):
    """
% creates tabulated list of all bonds as stored
%
% bonds = COUPLINGTABLE(obj,{bondIdx})
%
% Input:
%
% obj       spinw class object.
% bondIdx   List of bond indices, by default all bonds will be output.
%           Optional. If a bond index is mutiplied by -1, the table output
%           is a matlab built in table type, works only for Matlab R2013b
%           or later versions.
%
% Output:
%
% bonds is a struct type data that contains the following fields:
%   table   Matrix, where every column defines a bond. The rows are the
%           following: (dl_x, dl_y, dl_z, atom1, atom2, idx, mat_idx1,
%           mat_idx2, mat_idx3). Where (dl_x, dl_y, dl_z) defines the
%           translation vector between the origin of the unit cells of the
%           two interacting atom (if they are in the same unit cell, all
%           three components are zero) from atom1 to atom2. atom1 and atom2
%           are the indices of the atoms in the obj.matom list. idx is the
%           index of the bond, where equivalent bonds have identical
%           indices, typically index is increasing with bond length. The
%           last 3 rows (mat_idx) contains pointers to matrices if they
%           are defined, otherwise zeros.
%   bondv   Additional information for every bond defined in the .table
%           field. The first three rows define the vector pointing from
%           atom1 to atom2 in lattice units. The last row define the bond
%           length in Angstrom.
%   matrix  Contains the coupling matrix for every bond, dimensions are
%           [3 3 nCoupling].
%
% Example:
%
% ...
% crystal.gencoupling
% bonds = crystal.couplingtable(-[1 2 3]).table
%
% This will list only the 1st, 2nd and 3rd neighbour bonds in a formatted
% table.
%
% See also SPINW.MATOM, SPINW.INTMATRIX, SPINW.ADDCOUPLING, SPINW.GENCOUPLING.
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.couplingtable(*args, **kwargs)


def addaniso(obj=None, matrixIdx=None, *args, **kwargs):
    """
% assigns anisotropy to magnetic sites
%
% ### Syntax
%
% `addaniso(obj, matrixIdx, {atomTypeIdx}, {atomIdx})`
%
% ### Description
%
% `addaniso(obj, matrixIdx, {atomTypeIdx}, {atomIdx})` assigns the
% $[3\times 3]$ matrix selected by `matrixIdx` (using either the matrix
% label or matrix index) to the magnetic sites selected by `atomTypeIdx`
% that can contain a name of an atom or its atom index (see [spinw.atom]).
% If `atomTypeIdx` is not defined, anisotropy will be assigned to all
% magnetic atoms.
%
% ### Examples
%
% To show the effect of a fourfold axis on anisotropy, we add $A_1$
% easy-axis anisotropy to atoms at $(1/4,1/4,1/2)$ and plot the result. The
% 3D plot shows anistropy using ellipsoid around the magnetic atoms.
%
% ```
% >>cryst = spinw
% >>cryst.genlattice('lat_const',[4 4 3],'sym','P 4')
% >>cryst.addatom('r',[1/4 1/4 1/2],'S',1)
% >>cryst.addmatrix('label','A1','value',diag([-0.1 0 0]))
% >>cryst.gencoupling
% >>cryst.addaniso('A1')
% >>plot(cryst)
% >>snapnow
% ```
%
% ### Input arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% `matrixIdx`
% : Either an integer, that selects the matrix according to
%   `obj.matrix.mat(:,:,matrixIdx)`, or a string identical to one
%   of the previously defined matrix labels, stored in
%   `obj.matrix.label`.
%
% `atomTypeIdx`
% : String or cell of strings that select magnetic atoms by
%   their label. Also can be a vector that contains integers, the index of
%   the magnetic atoms in `obj.unit_cell`, with all symmetry equivalent
%   atoms. Maximum value is $n_{atom}$, if undefined anisotropy is assigned to
%   all magnetic atoms. Optional.
%
% `atomIdx`
% : A vector that contains indices selecting some of the
%   symmetry equivalent atoms. Maximum value is the number of symmetry
%   equivalent atoms generated corresponding to `atomTypeIdx` site. If
%   crystal symmetry is not 0, `atomIdx` is not allowed, since the
%   anisotropy matrix for equivalent atoms will be calculated using the
%   symmetry operators of the space group. Optional.
%
% ### Output Arguments
%
% The function adds extra entries in the `obj.single_ion.aniso` field of the
% obj [spinw] object.
%
% ### See Also
%
% [spinw], [spinw.single_ion], [spinw.addcoupling], [spinw.addg] and [spinw.addmatrix]
%
    """
    args = tuple(v for v in [obj, matrixIdx] if v is not None) + args
    return m.addaniso(*args, **kwargs)


def formula(obj=None, **kwargs):
    """
% returns basic physical properties
%
% ### Syntax
%
% `formula = formula(obj)`
%
% ### Description
%
% `result = formula(obj)` returns chemical mass, density, cellvolume etc.
% of `obj`.
%
% ### Examples
%
% The formula of the crystal stored in the
% [https://raw.githubusercontent.com/SpinW/Models/master/cif/Ca2RuO4.cif](https://raw.githubusercontent.com/SpinW/Models/master/cif/Ca2RuO4.cif) linked file will be
% printed onto the Command Window.
%
% ```
% >>cryst = spinw('https://raw.githubusercontent.com/SpinW/Models/master/cif/Ca2RuO4.cif')
% >>cryst.formula>>
% ```
%
% ### Name-Value Pair Arguments
%
% `'obj'`
% : [spinw] object.
%
% ### Output Arguments
%
% `formula` struct variable with the following fields:
% * `m`         Mass of the unit cell in g/mol units.
% * `V`         Calculated volume of the unit cell in length units (defined in [spinw.unit]).
% * `rho`       Density in g/cm$^3$.
% * `chemlabel` List of the different elements.
% * `chemnum`   Number of the listed element names
% * `chemform`  Chemical formula string.
%
    """
    args = tuple(v for v in [obj] if v is not None)
    return m.formula(*args, **kwargs)


def symmetry(obj=None, **kwargs):
    """
% returns whether symmetry is defined
%
% ### Syntax
%
% `sym = symmetry(obj)`
%
% ### Description
%
% `sym = symmetry(obj)` returns `true` if equivalent couplings are
% generated based on the crystal space group and all matrices (interaction,
% anisotropy and g-tensor) are transformed according to the symmetry
% operators. If `false`, equivalent couplings are generated based on bond
% length, equivalent matrices won't be transformed (all identical).
%
% To switch between the two behaviour use [spinw.gencoupling] with the
% `forceNoSym` parameter set to `true`. To remove all symmetry operators
% use [spinw.nosym].
%
% ### See Also
%
% [spinw] \| [spinw.nosym] \| [spinw.gencoupling]
%
    """
    args = tuple(v for v in [obj] if v is not None)
    return m.symmetry(*args, **kwargs)


def disp(obj=None, **kwargs):
    """
% prints information
%
% ### Syntax
%
% `{swdescr} = disp(obj)`
%
% ### Description
%
% `{swdescr} = disp(obj)` generates text summary of a [spinw] object.
% Calling it with output argument, it will generate a text version of the
% internal data structure giving also the dimensions of the different
% matrices.
%
% ### Examples
%
% Here the internal data structure is generated:
%
% ```
% >>crystal = spinw
% >>swFields = disp(crystal)>>
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Output Arguments
%
% `swdescr`
% : If output variable is given, the description of the `obj` object
%   will be output into the `swdescr` variable, instead of being
%   written onto the Command Window/file. Optional.
%
% ### See Also
%
% [spinw]
%
    """
    args = tuple(v for v in [obj] if v is not None)
    return m.disp(*args, **kwargs)


def rl(obj=None, norm=None, **kwargs):
    """
% generates reciprocal lattice vectors
%
% ### Syntax
%
% `rlVec = rl(obj, {norm})`
%
% ### Description
%
% `rlVec = rl(obj, {norm})` returns the lattice vectors of the reciprocal
% lattice in a $[3\times 3]$ matrix, with the $a^*$, $b^*$ and $c^*$ vectors
% stored in **rows**.
%
%
% ### Examples
%
% To convert from reciprocal lattice unit to \\ang$^{-1}$ ($xyz$
% Cartesian coordinate system) use: (`Q_rlu` is a row vector with 3
% elements):
%
% ```
% Q_xyz =  Q_rlu * rlVect
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% `norm`
% : If `true`, the basis vectors are normalized to 1. Default values is
% `false`, optional.
%
% ### Output Arguments
%
% `rlVec`
% : Stores the three basis vectors in the rows of matrix with dimensions of
%   $[3\times 3]$.
%
% ### See Also
%
% [spinw] \| [spinw.abc] \| [spinw.basisvector]
%
    """
    args = tuple(v for v in [obj, norm] if v is not None)
    return m.rl(*args, **kwargs)


def energy(obj=None, *args, **kwargs):
    """
% calculates the ground state energy
%
% ### Syntax
%
% `E = energy(obj,Name,Value)`
%
% ### Description
%
% `E = energy(obj,Name,Value)` calculates the classical ground state energy
% per spin. The calculation correctly takes into account the magnetic
% supercell. The function gives correct results on single-k magnetic
% structures even defined on magnetic supercells. For multi-k magnetic
% structures first a definition of a larger supercell is necessary where an
% effective $k=0$ representation is possible.
%
% ### Examples
%
% After optimising the magnetic structure (by minimizing the ground state
% energy), the energy per spin is calculated. This can be compared to
% different ground state structures to decide which is the right classical
% ground state of the magnetic model in cryst. Here we use the triangular
% lattice antiferromagnet where we define the magnetic structure on a
% $[3\times 3]$ magnetic supercell where the optimal structure (120\\deg
% angle between neighboring spins) has a 0 propagation vector. In this case
% the exact energy is $3\cdot 1^2\cdot \cos(120^\circ) = -1.5$.
%
% ```
% >>cryst = sw_model('triAF',1)
% >>cryst.genmagstr('mode','random','nExt',[3 3 1])
% >>cryst.optmagsteep('nRun',10)
% >>cryst.energy>>
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% `'epsilon'`
% : The smallest value of incommensurability that is tolerated
%   without warning. Default is $10^{-5}$.
%
% ### Output Arguments
%
% `E`
% : Energy per moment (anisotropy + exchange + Zeeman energy).
%
% {{warning The calculated energy can be wrong for incommensurate
% structures. For example a structure where the spins are rotating in $XY$
% plane with an incommensurate wavevector of $(1/3,0,0)$. The function only
% calculates the anisotropy energy in the first unit cell, that is for
% single spin $E_{aniso} = A_{xx}\cdot S_{xx}^2+A_{yy}\cdot S_{yy}^2$.
% While the anisotropy energy in reality is independent of the spin
% orientation in the $XY$ plane $E_{aniso}=3S\cdot (A_{xx}+A_{yy})/2$. Thus
% using `spinw.energy` on incommensurate structures together with single
% ion anisotropy one has to be carefull! In the triangular case one has to
% extend the unit cell to `nExt = [3 3 1]` (in the hexagonal setting), in
% this case the energy will be correct.}}
%
% ### See Also
%
% [spinw] \| [spinw.anneal] \| [spinw.newcell]
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.energy(*args, **kwargs)


def fourier(obj=None, hkl=None, *args, **kwargs):
    """
% calculates the Fourier transformation of the Hamiltonian
%
% ### Syntax
%
% `F = fourier(obj,Q,Name,Value)`
%
% ### Description
%
% `F = fourier(obj,hkl,Name,Value)` calculates the following Fourier sum:
%
% $J(\mathbf{k}) = \sum_{i,j} J_{i,j} * \exp(i \mathbf{k}\cdot \mathbf{d}_{i,j})$
%
% The code is optimised for calculating the sum for large number of wave
% vectors and alternatively for a large number of $d_{i,j}$ vectors (large
% system size). The single ion anisotropy is not included in the sum.
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% `Q`
% : Defines the $Q$ points where the spectra is calculated, in reciprocal
%   lattice units, size is $[3\times n_{Q}]$. $Q$ can be also defined by
%   several linear scan in reciprocal space. In this case `Q` is cell type,
%   where each element of the cell defines a point in $Q$ space. Linear scans
%   are assumed between consecutive points. Also the number of $Q$ points can
%   be specified as a last element, it is 100 by defaults.
%
%   For example to define a scan along $(h,0,0)$ from $h=0$ to $h=1$ using
%   200 $Q$ points the following input should be used:
%   ```
%   Q = {[0 0 0] [1 0 0]  50}
%   ```
%
%   For symbolic calculation at a general reciprocal space point use `sym`
%   type input.
%
%   For example to calculate the spectrum along $(h,0,0)$ use:
%   ```
%   Q = [sym('h') 0 0]
%   ```
%   To calculate spectrum at a specific $Q$ point symbolically, e.g. at
%   $(0,1,0)$ use:
%   ```
%   Q = sym([0 1 0])
%   ```
%
% ### Name-Value Pair Arguments
%
% `'extend'`
% : If `true`, the Fourier transform will be calculated on the
%   magnetic supercell, if `false` the crystallographic cell will
%   be considered. Default is `true.`
%
% `'isomode'`
% : Defines how Heisenberg/non-Heisenberg Hamiltonians are
%   treated. Can have the following values:
%   * `'off'`   Always output the $[3\times 3]$ form of the
%               Hamiltonian, (default).
%   * `'auto'`  If the Hamiltonian is Heisenberg, only output
%               one of the diagonal values from the $[3\times 3]$
%               matrices to reduce memory consumption.
%
% `'fid'`
% : Defines whether to provide text output. The default value is determined
%   by the `fid` preference stored in [swpref]. The possible values are:
%   * `0`   No text output is generated.
%   * `1`   Text output in the MATLAB Command Window.
%   * `fid` File ID provided by the `fopen` command, the output is written
%           into the opened file stream.
%
% ### Output Arguments
%
% `res` struct type with the following fields:
% * `ft`        contains the Fourier transform in a matrix with dimensions
%               $[3\times 3\times n_{magExt}\times n_{magExt}\times
%               n_{hkl}]$ or $[1\times 1\times n_{magExt}\times n_{magExt}\times n_{hkl}]$
%               for Heisenberg and non-Heisenberg Hamiltonians respectively
%               (if isomode is `'auto'`). Here $n_{magExt}$ is the number of
%               magnetic atoms in the magnetic cell and $n_{hkl}$ is the number
%               of reciprocal space points.
% * `hkl`       Matrix with the given reciprocal space points stored in a
%               matrix with dimensions $[3\times n_{hkl}]$.
% * `isiso`     True is the output is in Heisenberg mode, when the `ft`
%               matrix has dimensions of $[1\times 1\times n_{magExt}\times n_{magExt}\times n_{hkl}]$,
%               otherwise it is `false`.
%
% ### See Also
%
% [spinw.optmagk]
%
    """
    args = tuple(v for v in [obj, hkl] if v is not None) + args
    return m.fourier(*args, **kwargs)


def addcoupling(obj=None, *args, **kwargs):
    """
% assigns an exchange matrix to a bond
%
% ### Syntax
%
% `addcoupling(obj,Name,Value)`
%
% ### Description
%
% `addcoupling(obj,Name,Value)` assigns a matrix (will be used as exchange
% matrix) to a given bond after bonds are generated using
% [spinw.gencoupling].
%
% ### Examples
%
% To add the $J_1$ diagonal matrix to all second neighbor bonds
% between magnetic atoms use the following:
%
% ```
% >>cryst = sw_model('squareAF',1)
% >>cryst.addmatrix('label','J1','value',diag([1 0.1 0.1]))
% >>cryst.gencoupling
% >>cryst.addcoupling('mat','J1','bond',2)
% >>plot(cryst,'range',[2 2 1])
% >>snapnow
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% `'mat'`
% : Label (string) or index (integer) of the matrix that will be assigned to
%   selected bonds, e.g. `'J1'`.
%
% `'bond'`
% : Integer that selects bonds, e.g. 1 for first neighbor, 2 for second
%   neighbor, etc. The given value is compared to the `obj.coupling.idx`
%   vector and the exchange matrix will be assigned to matching bonds.
%   `'bond'` can be also a row vector to assign matrices to multiple bonds.
%
% `'atom'`
% : Contains labels of atoms (string) or index of atoms (integer) that is
%   compared to [spinw.unit_cell] where all symmetry inequivalent atoms are
%   stored. If a single string label or number is given, e.g. `'Cr1'` only
%   Cr1-Cr1 bonds will be assigned. If a cell with 2 strings, e.g. `{'Cr1'
%   'Cr2'}` only Cr1-Cr2 bonds will be assigned. Default value is `[]`.
%
% `'subIdx'`
% : If the above options are not enough to select the desired
%   bonds, using `subIdx` bonds can be selected one-by-one from
%   the list of bonds that fulfill the constraint of `atom` and `bond`.
%
% `'type'`
% : Type of the coupling with possible values of:
%   * `'quadratic'`     Quadratic exchange, default.
%   * `'biquadratic'`   Biquadratic exchange.
%
% `'sym'`
% : If `true`, symmetry operators will be applied on the exchange
%   matrices to generate the coupling on symmetry equivalent
%   bonds, if `false` all symmetry equivalent bonds will have the
%   same exhcange matrix.
%
% {{warning Setting `atom` or `subIdx` parameters will remove the symmetry
% operations on the selected bonds. This means that assigning any
% non-Heisenberg exchange matrix will break the space group defined in
% `obj.lattice.sym`. Effectively reducing the symmetry of the given bond to
% `P0`}}
%
% ### Output Arguments
%
% The function adds extra entries to the [spinw.coupling] property of
% `obj`. Specifically it will modify `obj.coupling.mat_idx`,
% `obj.coupling.type` and `obj.coupling.sym` matrices.
%
% ### See Also
%
% [spinw] \| [spinw.gencoupling] \| [spinw.addmatrix]
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.addcoupling(*args, **kwargs)


def symop(obj=None, **kwargs):
    """
% generates the bond symmetry operators
%
% ### Syntax
%
% `op = symop(obj)`
%
% ### Description
%
% `op = symop(obj)` generates the rotation matrices that transform single
% ion anisotropy, g-tensor and exchange interaction matrices between
% symmetry equivalent positions (on atoms or bond centers). The results are
% cached.
%
% ### See Also
%
% [spinw.intmatrix]
%
    """
    args = tuple(v for v in [obj] if v is not None)
    return m.symop(*args, **kwargs)


def magstr(obj=None, *args, **kwargs):
    """
% returns single-k magnetic structure representation
%
% ### Syntax
%
% `magout = magstr(obj,Name,Value)`
%
% ### Description
%
% `magout = magstr(obj,Name,Value)` converts the internally stored magnetic
% structure (general Fourier representation) into a rotating frame
% representation with a single propagation vector, real magnetisation
% vectors and the normal axis of the rotation. The conversion is not always
% possible, in that case the best possible approximation is used, that
% might lead sometimes to unexpected magnetic structures. In this case a
% warning is triggered.
%
% ### Example
%
% The example shows the equivalent represenation of a simple spin helix in
% the $ab$-plane using Fourier components of the magnetization and using
% the rotating frame. The complex magnetization in the Fourier
% representation is converted into a real spin vector and a normal vector
% that defines the axis of rotation.
%
% ```
% >>model = spinw
% >>model.addatom('r',[0 0 0],'S',1)
% >>model.genmagstr('mode','fourier','S',[1i 1 0]','k',[1/3 0 0])
% >>model.mag_str.F>>
% >>model.magstr>>
% >>model.magstr.S>>
% ```
%
% ### Name-Value Pair Arguments
%
% `'exact'`
% : If `true`, a warning appears in case the conversion is not exact.
%   Default is `true`.
%
% `'nExt'`
% : Size of the magnetic supercell, default value is the value stored in
%   the [spinw] object (on which the Fourier expansion is defined).
%
% `'origin'`
% : Origin in lattice units, the magnetic structure will be
%   calculated relative to this point. Default value is `[0 0 0]`.
%   Shifting the origin introduces an overall phase factor.
%
% ### See Also
%
% [spinw.genmagstr]
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.magstr(*args, **kwargs)


def unitcell(obj=None, idx=None, **kwargs):
    """
% returns unit cell data
%
% ### Syntax
%
% `cellInfo = unitcell(obj, idx)`
%
% ### Description
%
% `cellInfo = unitcell(obj, idx)` returns information on symmetry
% inequivalent atoms and allowing to subselect certain atoms using the
% `idx` index vector.
%
% ### Examples
%
% The example keeps only the first and third symmetry inequivalent atoms in
% `cryst` object.
% ```
% cryst.unit_cell = unitcell(cryst,[1 3]);
% ```
% The example keeps only the atoms with labels `'O'` (Oxygen) atoms in
% `cryst` object.
% ```
% cryst.unit_cell = unitcell(cryst,'O');
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% `idx`
% : Selects certain atoms. If undefined `unit_cell(obj)` or
%      `obj.unit_cell` returns information on all atoms. The selection
%      can be also done according to the atom labels, in this case
%      either a string of the label or cell of strings for several
%      labels can be given.
%
% ### Output Arguments
%
% `cellInfo`
% : Structure that contains all the fields of [spinw.unit_cell].
%
% ### See Also
%
% [spinw.addtwin] \| [spinw.twinq] \| [spinw.unit_cell]
%
    """
    args = tuple(v for v in [obj, idx] if v is not None)
    return m.unitcell(*args, **kwargs)


def addatom(obj=None, *args, **kwargs):
    """
% adds new atom
%
% ### Syntax
%
% `addatom(obj,Name,Value)`
%
% ### Description
%
% `addatom(obj,Name,Value)` adds a new atom to the list of symmetry
% inequivalent sites together with its properties, such as position, spin
% quantum number, form factor, etc.
%
% ### Examples
%
% To add a magnetic atom with $S=1$ at position $r=(0,0,0)$ and a
% non-magnetic one at $r=(1/2,0,0)$ with red and blue color respectively
% use the following command
%
% ```
% >>crystal = spinw;
% >>crystal.genlattice('lat_const',[4 3 3])
% >>crystal.addatom('r',[0 1/2; 0 0; 0 0],'S',[1 0],'color',{'red' 'blue'})
% >>crystal.plot
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% `r`
% : Atomic positions stored in a matrix with dimensions of $[3\times
%   n_{atom}]$.
%
% `label`
% : Names of the atoms in a cell for plotting and form factor
%   calculations (see [magion.dat]), e.g. `label={'atom1' 'atom2'
%   'atom3'}`.
%   Default value is `atomi`, where `i` is the atom index.
%
% `S`
% : Spin quantum number stored in a row vector with $n_{atom}$ elements,
%   for non-magnetic atoms set S to zero. If not given the spin quantum
%   number is guessed from the given label of the atom. For example if
%   `label` is `MCr3+` or `Cr3+` then the $S=3/2$ high spin state is
%   assumed for Cr$^{3+}$. The spin values for every ion is stored in the
%   [magion.dat] file. If the atom type is unknown $S=0$ is assumed. Only
%   positive S are allowed.
%
% `color`
% : RGB color of the atoms for plotting stored in a matrix with dimensions
%   of $[3\times n_{atom}]$, where each column describes an RGB color. Each
%   value is between 0 and 255. Default value is the color stored in the
%   [atom.dat] file. Alternatively a name of the color can be given as a
%   string, for example `'White'`, for multiple atoms package it into a
%   cell. For the list of colors, see [swplot.color] or the [color.dat]
%   file.
%
% `ox`
% : Oxidation number given as a double or it will be determined
%   automatically from label. Default value is 0.
%
% `occ`
% : Occupancy, given as double. Default value is 1.
%
% `formfact`
% : Neutron scattering form factor, given as a row vector with 9 numbers,
%   for details see [sw_mff]. Also string labels can be used from the
%   [magion.dat] file.
%
% `formfactn`
% : Same as the `formfact` option.
%
% `formfactx`
% : X-ray scattering form factor, given as 9 numbers, for details
%   see [sw_cff], also labels can be used from the [xrayion.dat] file.
%
% `Z`
% : Atomic number, given as integer or determined from the atom label
%   automatically. Default value is 113 (Unobtanium).
%
% `A`
% : Atomic mass, given as integer. Default is -1 for the natural
%   mixture of isotopes.
%
% `bn`
% : Neutron scattering length, given as double.
%
% `bx`
% : X-ray scattering length, given as double. Not yet implmented, this
%   input will be ignored.
%
% `biso`
% : Isotropic displacement factors in units of \\ang$^2$.
%   Definition is the same as in
%   [FullProf](https://www.ill.eu/sites/fullprof/), defining the
%   Debye-Waller factor as $W(d) = 1/8*b_{iso}/d^2$, which is included in
%   the structure factor as $exp(-2W(d))$.
%
% `update`
% : If `true`, existing atom with the same label and position as a
%   new one will be updated. Default is `true`.
%
% ### Output Arguments
%
% The function modifies the [spinw.unit_cell] property of the obj
% [spinw] object.
%
% ### See Also
%
% [spinw.genlattice] \| [spinw.addmatrix] \| [swplot.color] \| [sw_mff] \| [sw_cff]
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.addatom(*args, **kwargs)


def export(obj=None, *args, **kwargs):
    """
% export data into file
%
% ### Syntax
%
% `export(obj,Name,Value)`
%
% `outStr = export(obj,Name,Value)`
%
% ### Description
%
% `export(obj,Name,Value)` exports different types of spinw object data.
%
% `outStr = export(obj,Name,Value)` returns a string instead of writing the
% data into a file.
%
% ### Examples
%
% In this example the crystal structure is imported from the `test.cif`
% file, and the atomic positions are saved into the `test.pcr` file for
% FullProf refinement (the pcr file needs additional text to work with
% FullProf).
%
% ```
% cryst = sw('test.cif');
% cryst.export('format','pcr','path','test.pcr');
% ```
%
% ### Input arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% `'format'`
% : Determines the output data and file type. The supported file formats
%   are:
%   * `'pcr'`   Creates part of a .pcr file used by [FullProf](https://www.ill.eu/sites/fullprof). It exports the
%     atomic positions.
%   * `'MC'`    Exports data into a custom file format for Monte Carlo simulations.
%
% `'path'`
% : Path to a file into which the data will be exported, `out` will
%   be `true` if the file succesfully saved, otherwise `false`.
%
% `'fileid'`
% : File identifier that is already opened in Matlab using the
%   `fileid = fopen(...)` command. Don't forget to close the file
%   afterwards.
%
% #### File format dependent options:
%
% `'perm'` (`pcr`)
% : Permutation of the $xyz$ atomic positions, default value is `[1 2 3]`.
%
% `'boundary'` (`MC`)
% : Boundary conditions of the extended unit cell. Default value is `{'per'
%   'per' 'per'}`. The following strings are accepted:
%   * `'free'`  Free, interactions between extedned unit cells are omitted.
%   * `'per'`   Periodic, interactions between extended unit cells are
%     retained.
%
% {{note If neither `path` nor `fileid` is given, the `outStr` will be a
% cell containing strings for each line of the text output.}}
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.export(*args, **kwargs)


def optmagstr(obj=None, *args, **kwargs):
    """
% general magnetic structure optimizer
%
% ### Syntax
%
% `optm = optmagstr(obj,Name,Value)`
%
% ### Description
%
% `optm = optmagstr(obj,Name,Value)` is a general magnetic structure
% optimizer that as the name suggests is general however usually less
% efficient than [spinw.optmagk] or [spinw.optmagsteep]. However this
% function enables the usage of constraint functions to improve the
% optimization. This function is most useful if there are 1-2 parameters
% that have to be optimized, such as a canting angle of the spins in
% a magnetic field. To optimize large numbers of spin angles
% [spinw.optmagsteep] might be faster. Only obj.mag_str.nExt is used from
% an already initialised magnetic structure, initial k and S are determined
% from the optimisation function parameters. If a magnetic structure has
% not been initialised in obj, nExt = [1 1 1] is used.
%
% ### Examples
%
% The example determines the propagation vector of the ground state of the
% triangular lattice antiferromagnet. The magnetic structure is constrained
% to be planar in the $xy$-plane. The [gm_planard] constraint function is
% used where the first 3 parameter determined the propagation vector,
% followed by the polar angles of the magnetic moments (here there is only
% 1 magnetic moment in the unit cell) which is fixed to 0. Finally the last
% 2 parameters corresponds to the polar angles of the normal to the
% spin-plane which is the $z$-axis ($\theta=0$, $\varphi=0$). The optimized
% magnetic structure is plotted.
%
% ```
% >>tri = sw_model('triAF',1)
% >>X1 = [0 0 0 0 0 0]
% >>X2 = [0 1/2 1/2 0 0 0]
% >>optRes = tri.optmagstr('func',@gm_planard,'xmin',X1,'xmax',X2)
% >>km = optRes.x(1:3)>>
% >>plot(tri)
% >>>swplot.zoom(1.5)
% >>snapnow
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% `'func'`
% : Function that produces the spin orientations, propagation vector and
%   normal vector from the optimization parameters and has the following
%   argument list:
%   ```
%   [M, k, n] = @(x)func(M0, x)
%   ```
%  here `M` is matrix with dimensions of $[3\times n_{magExt}]$, `k` is the
%  propagation vector (row vector with 3 elements), `n` is the normal vector
%  of the spin rotation plane (row vector with 3 elements). The
%  default value is `@gm_spherical3d`. For planar magnetic structures
%  use `@gm_planar`.
%
% `'xmin'`
% : Lower limit of the optimisation parameters.
%
% `'xmax'`
% : Upper limit of the optimisation parameters.
%
% `'x0'`
% : Starting value of the optimisation parameters. If empty
%   or undefined, then random values are used within the given limits.
%
% `'boundary'`
% : Boundary conditions of the magnetic cell:
%   * `'free'`  Free, interactions between extedned unit cells are
%             omitted.
%   * `'per'`   Periodic, interactions between extended unit cells
%             are retained.
%
%   Default value is `{'per' 'per' 'per'}`.
%
% `'epsilon'`
% : The smallest value of incommensurability that is tolerated
%   without warning. Default value is $10^{-5}$.
%
% `'nRun'`
% : Number of runs. If random starting parameters are given, the
%   optimisation process will be rerun `nRun` times and the best
%   result (lowest ground state energy per spin) will be kept.
%
% `'title'`
% : Gives a title string to the simulation that is saved in the
%   output.
%
% `'tid'`
% : Determines if the elapsed and required time for the calculation is
%   displayed. The default value is determined by the `tid` preference
%   stored in [swpref]. The following values are allowed (for more details
%   see [sw_timeit]):
%   * `0` No timing is executed.
%   * `1` Display the timing in the Command Window.
%   * `2` Show the timing in a separat pup-up window.
%
% #### Limits on selected prameters
%
% Limits can be given on any input parameter of the constraint function by
% giving the name of the parameter. For parameter names see the help of the
% used constraint function. Limits per optimization parameter can be given
% in the following format: `optmagstr('ParName',[min max],...)`. For example
% to fix the `nTheta` value of [gm_planar] during the optimisation to zero
% use: `optmagstr(obj,'func',@gm_planar,'nTheta',[0 0])`.
%
%
% #### Optimisation parameters
%
% The optimization parameters are identical to the input options of the
% Matlab built-in optimizer [matlab.fminsearch].
%
% `'tolx'`
% : Minimum change of `x` when convergence reached, default
%     value is $10^{-4}$.
%
% `'tolfun'`
% : Minimum change of the $R$ value when convergence reached,
%     default value is $10^{-5}$.
%
% `'maxfunevals'`
% : Maximum number of function evaluations, default value
%     is $10^7$.
%
% `'maxiter'`
% : Maximum number of iterations, default value is $10^4$.
%
% ### Output Arguments
%
% `optm`
% : Struct type variable with the following fields:
%   * `obj`       spinw object that contains the optimised magnetic structure.
%   * `x`         Optimised paramters in a row vector with $n_{par}$ number
%                 of elements.
%   * `fname`     Name of the contraint function.
%   * `xname`     Cell containing the name of the $x$ parameters with
%                   $n_{par}$ elements.
%   * `e`         Energy per spin in the optimised structure.
%   * `exitflag`  Exit flag of the optimisation code, see [matlab.fminsearch].
%   * `output`    Detailed output of the optimisation code, see [matlab.fminsearch].
%   * `param`     Input parameters, stored in a struct.
%
% ### See Also
%
% [spinw] \| [spinw.anneal] \| [gm_spherical3d] \| [gm_planar] \| [fminsearch]
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.optmagstr(*args, **kwargs)


def nosym(obj=None, *args, **kwargs):
    """
% reduces symmetry to P0
%
% ### Syntax
%
% `nosym(obj)`
%
% ### Description
%
% `nosym(obj)` reduces the crystal symmetry to $P0$ but keeps all symmetry
% generated atoms, that become all symmetry inequivalent. The function can
% be used to test different types of symmetry breaking terms in the spin
% Hamiltonian.
%
% ### Examples
%
% The example generates an FCC cell using explicit translations. After
% applying the `spinw.nosym` function, the `cryst.unit_cell.r` contains the
% four generated atomic positions, that are not symmetry equivalent any
% more.
%
% ```
% >>symOp = 'x+1/2,y+1/2,z;x+1/2,y,z+1/2;x,y+1/2,z+1/2'
% >>cryst = spinw
% >>cryst.genlattice('lat_const',[8 8 8],'sym',symOp,'label','FCC')
% >>cryst.addatom('r',[0 0 0],'label','Atom1')
% >>cryst.unit_cell.r>>
% >>cryst.nosym
% >>cryst.unit_cell.r>>
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Output Arguments
%
% The `obj` input will have `obj.lattice.sym` field equal to zero and the
% [obj.unit_cell] field will contain all the generated atomic positions.
%
% ### See Also
%
% [spinw] \| [spinw.newcell]
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.nosym(*args, **kwargs)


def gencoupling(obj=None, *args, **kwargs):
    """
% generates bond list
%
% ### Syntax
%
% `gencoupling(obj,Name,Value)`
%
% ### Description
%
% `gencoupling(obj,Name,Value)` generates all bonds up to a certain length
% between magnetic atoms. It also groups bonds based either on crystal
% symmetry (is space group is not $P0$) or bond length (with `tolDist`
% tolerance) is space group is not defined. Sorting bonds based on length
% can be forced by setting the `forceNoSym` parameter to true. To check
% whether a space group is defined call the [spinw.symmetry] function.
%
% {{warning This function has to be used after the crystal structure is defined.
%   The [spinw.addcoupling] function will only work afterwards. }}
%
% ### Examples
%
% A triangular lattice is generated using `spinw.gencoupling` and
% the [spinw.table] function lists the 1st, 2nd and 3rd neighbor bonds:
%
% ```
% >>cryst = spinw
% >>cryst.genlattice('lat_const',[3 3 5],'angled',[90 90 120])
% >>cryst.addatom('r',[0 0 0],'S',1)
% >>cryst.gencoupling
% >>cryst.table('bond',1:3)>>
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% `'forceNoSym'`
% : If `true`, equivalent bonds are always generated based on
%   bond length with `tolDist` length tolerance and effectively reducing
%   the bond symmetry to `P0`. If `false` symmetry operators will be used
%   if they are given ([spinw.symmetry] returns `true`).
%
% `'maxDistance'`
% : Maximum bond length that will be stored in the
%   [spinw.coupling] property in units of \\ang. Default value is 8.
%
% `'maxSym'`
% : Maximum bond length until the symmetry equivalent bonds are
%   generated. It is usefull if long bonds have to be generated for the
%   dipolar interaction, but the symmetry analysis of them is not
%   necessary. Default value is equal to `maxDistance`.
%
% `'tolDist'`
% : Tolerance of distance, within two bonds are considered
%   equivalent, default value is $10^{-3}$\\ang. Only used, when no
%   space group is defined.
%
% `'tolMaxDist'`
% : Tolerance added to maxDistance to ensure bonds between same atom in
%   neighbouring unit cells are included when maxDistance is equal to a
%   lattice parameter.
%
% `'dMin'`
% : Minimum bond length, below which an error is triggered.
%   Default value is 0.5 \\ang.
%
% `'fid'`
% : Defines whether to provide text output. The default value is determined
%   by the `fid` preference stored in [swpref]. The possible values are:
%   * `0`   No text output is generated.
%   * `1`   Text output in the MATLAB Command Window.
%   * `fid` File ID provided by the `fopen` command, the output is written
%           into the opened file stream.
%
% ### Output Arguments
%
% The [spinw.coupling] field of `obj` will store the new bond list, while
% overwriting previous bond list. This will also remove any previous
% assignment of exchange matrices to bonds.
%
% ### See Also
%
% [spinw] \| [spinw.symmetry] \| [spinw.nosym]
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.gencoupling(*args, **kwargs)


def spinwavesym(obj=None, *args, **kwargs):
    """
% calculates symbolic spin wave dispersion
%
% ### Syntax
%
% `spectra = spinwavesym(obj,Name,Value)`
%
% ### Description
%
% `spectra = spinwavesym(obj,Name,Value)` calculates symbolic spin wave
% dispersion as a function of $Q$. The function can deal with arbitrary
% magnetic structure and magnetic interactions as well as single ion
% anisotropy and magnetic field. Biquadratic exchange interactions are also
% implemented, however only for $k=0$ magnetic structures.
%
% If the magnetic propagation vector is non-integer, the dispersion is
% calculated using a coordinate system rotating from cell to cell. In this
% case the Hamiltonian has to fulfill this extra rotational symmetry.
%
% The method works for incommensurate structures, however the calculated
% omega dispersion does not contain the $\omega(\mathbf{k}\pm \mathbf{k}_m)$ terms that has to be
% added manually.
%
% The method for matrix diagonalization is according to R.M. White, PR 139
% (1965) A450. The non-Hermitian g*H matrix will be diagonalised.
%
% ### Examples
%
% The first section of the example calculates the symbolic spin wave
% spectrum. Unfortunatelly the symbolic expression needs manipulations to
% bring it to readable form. To check the solution, the second section
% converts the symbolic expression into a numerical vector and the third
% section plots the real and imaginary part of the solution.
%
% ```
% >>tri = sw_model('triAF',1)
% >>tri.symbolic(true)
% >>tri.genmagstr('mode','direct','k',[1/3 1/3 0],'S',[1 0 0])
% >>symSpec = tri.spinwave
% >>pretty(symSpec.omega)>>
% >>J_1 = 1
% >>h = linspace(0,1,500)
% >>k = h
% >>omega = eval(symSpec.omega)
% >>p1 = plot(h,real(omega(1,:)),'k-')
% >>hold on
% >>plot(h,real(omega(2,:)),'k-')
% >>p2 = plot(h,imag(omega(1,:)),'r-')
% >>plot(h,imag(omega(2,:)),'r-')
% >>xlabel('Momentum (h,h,0) (r.l.u.)')
% >>ylabel('Energy (meV)')
% >>legend([p1 p2],'Real(\omega(Q))','Imag(\omega(Q))')
% >>title('Spin wave dispersion of the TLHAF')
% >>snapnow
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% `'hkl'`
% : Symbolic definition of $Q$ vector. Default is the general $Q$
%   point:
%   ```
%   hkl = [sym('h') sym('k') sym('l')]
%   ```
%
% `'eig'`
% : If true the symbolic Hamiltonian is diagonalised symbolically. For
%   large matrices (many magnetic atom per unit cell) this might be
%   impossible. Set `eig` to `false` to output only the quadratic
%   Hamiltonian. Default is `true`.
%
% `'vect'`
% : If `true` the eigenvectors are also calculated. Default is `false`.
%
% `'tol'`
% : Tolerance of the incommensurability of the magnetic
%   ordering wavevector. Deviations from integer values of the
%   ordering wavevector smaller than the tolerance are
%   considered to be commensurate. Default value is $10^{-4}$.
%
% `'norm'`
% : Whether to produce the normalized symbolic eigenvectors. It can be
%   impossible for large matrices, in that case set it to
%   `false`. Default is `true`.
%
% `'fid'`
% : Defines whether to provide text output. The default value is determined
%   by the `fid` preference stored in [swpref]. The possible values are:
%   * `0`   No text output is generated.
%   * `1`   Text output in the MATLAB Command Window.
%   * `fid` File ID provided by the `fopen` command, the output is written
%           into the opened file stream.
%
% `'title'`
% : Gives a title string to the simulation that is saved in the
%   output.
%
% ### Output Arguments
%
% `spectra`
% : Structure, with the following fields:
%   * `omega`   Calculated spin wave dispersion, dimensins are
%               $[2*n_{magExt}\times n_{hkl}]$, where $n_{magExt}$ is the number of magnetic
%               atoms in the extended unit cell.
%   * `V0`      Eigenvectors of the quadratic Hamiltonian.
%   * `V`       Normalized eigenvectors of the quadratic Hamiltonian.
%   * `ham`     Symbolic matrix of the Hamiltonian.
%   * `incomm`  Whether the spectra calculated is incommensurate or not.
%   * `obj`     The clone of the input `obj`.
%
% ### See Also
%
% [spinw] \| [spinw.spinwave]
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.spinwavesym(*args, **kwargs)


def basisvector(obj=None, *args, **kwargs):
    """
% generates lattice vectors
%
% ### Syntax
%
% `basisVec = basisvector(obj, {norm})`
%
% ### Description
%
% `basisVec = basisvector(obj, {norm})` returns the lattice vectors of the
% unit cell in a $[3\times 3]$ matrix, with the $a$, $b$ and $c$ vectors
% stored in columns. The vectors are normalized to the lattice parameters
% by default.
%
% ### Examples
%
% The `basisVec` matrix can be used to change coordinate system, converting
% between positions expressed in lattice units to positions expressed in
% \\ang, using `r_lu` for lattice unit coordinates and `r_xyz` for
% \\ang units (both stored in a column vector) the conversions are the
% following:
% ```
% r_xyz = basisVec * r_lu
% ```
% or
% ```
% r_lu = inv(basisVec)*r_xyz
% ```
%
% It is also possible to convert between momentum vector in reciprocal
% lattice units (rlu) into \\ang$^{-1}$ units. Assuming that momentum
% vectors are row vectors:
% ```
% Q_xyz =  Q_rlu * 2*pi*inv(basisVec)
% ```
% or
% ```
% Q_rlu = 1/(2*pi)*Q_xyz*basisVect
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% `norm`
% : If `true`, the basis vectors are normalized to 1, otherwise the
%   length of the basis vectors are equal to the lattice constants. Default
%   is `false`.
%
% ### Output Arguments
%
% `basisVec`
% : Stores the three lattice vectors in columns, dimensions are $[3\times 3]$.
%
% ### See Also
%
% [spinw] \| [spinw.abc] \| [spinw.rl]
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.basisvector(*args, **kwargs)


def anneal(obj=None, *args, **kwargs):
    """
% performs simulated annealing of spins
%
% ### Syntax
%
% `stat = anneal(obj,Name,Value)`
%
% ### Description
%
% `stat = anneal(obj,Name,Value)` performs simulated annealing on the spin
% Hamiltonian defined in `obj`. It assumes a classical spin system and
% employs the [Metropolis–Hastings
% algorithm](https://en.wikipedia.org/wiki/Metropolis–Hastings_algorithm)
% for state updates. The annealing is performed from a given initial
% temperature down to final temperature with user defined steps and number
% of Monte-Carlo cycles per temperature. The `spinw.anneal` can also
% measure different thermodynamic quantities, such as heat capacity. The
% function can deal with single ion anisotropy and arbitrary exchange
% interactions. It can also restrict the spin degrees of freedom from 3
% (default) to 2 or 1 to speed up simulation on xy and Ising systems. For
% these restricted dimensions only isotropic exchange interactions are
% allowed. Also the g-tensor is assumed to be 2.
%
% {{warning The calculated energies does not contain the self energy (spin
% coupled to itself), thus the energies calculated here can differ from the
% output of [spinw.energy].}}
%
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% `'spinDim'`
% : Dimensionality of the spins:
%   * **1**     Ising spins.
%   * **2**     XY spins.
%   * **3**     Heisenberg spins, default.
%
%   For Ising (spinDim=1) and XY (spinDim=2) models only isotropic
%   exchange interaction and magnetic field can be used. For Ising
%   the direction of the spins are along x-axis, for XY model the
%   the xy-plane. Magnetic fields perpendicular to these directions
%   are omitted.
%
% `'initT'`
% : The initial temperature, can be any positive number
%   in units of Kelvin. Default value is 1.
%
% `'endT'`
% : Temperature at which the annealing will stop, can be any positive number
%   smaller than `initT`, unit is Kelvin.
%   Default value is $10^{-3}$.
%
% `'cool'`
% : Defines how the following temperature value is calculated from the
%   previous one using a user function. Any function that takes a scalar as input and
%   returns a smaller but positive scalar as output. Default is `@(T)(0.92*T)`.
%
% `'random'`
% : If `true` the initial spin orientation will be random, which is
%   effectively a $T=\infty$ paramagnet. If the initial spin configuration
%   is undefined (`obj.magstr.S` is empty) the initial configuration
%   is always random independently of this parameter.
%   Default value is `false`.
%
% `'nMC'`
% : Number of Monte-Carlo steps per spin at each temperature
%   step  which includes thermalization and the sampling for the extracted
%   TD properties at the last temperature). Default is 100.
%
% `'nORel'`
% : Number of over-relaxation steps after every Monte-Carlo
%   steps. It rotates the spins around the direction of the local field by
%   180\\deg. It is reversible and microcanonical if the single ion
%   anisotropy is 0. Default value is 0, to omit over-relaxation.
%
% `'nStat'`
% : Number of cycles at the last temperature to calculate
%   statistical averages. It has to be smaller or equal $n_{MC}$.
%   Default value is 100.
%
% `'boundary'`
% : Boundary conditions of the extended unit cell:
%   * **free**  Free, interactions between extedned unit cells are
%               omitted.
%   * **per**   Periodic, interactions between extended unit cells
%               are retained.
%   Default value is `{'per' 'per' 'per'}`.
%
% `'verbosity'`
% : Controls the amount of output to the Command Window:
%   * **0**   Suppresses all output.
%   * **1**   Gives final report only.
%   * **2**   Plots temperature changes and final report, default value.
%
% `'nExt'`
% : The size of the magnetic cell in number of unit cells that can override
%   the value stored in `obj.magstr.N_ext`, given by a row vector with
%   three integers
%
% `'fStat'`
% : Function handle to measure TD quantities at the final temperature
%   for `nStat` Monte-Carlo steps. The function returns a single structure
%   and takes fixed input parameters:
%   ```
%   parOut = fStat(state, parIn, T, E, M, nExt).
%   ```
%   The function is called once before the annealing process
%   when `state=1` to initialise the parameters. The function is called
%   after every Monte-Carlo cycle with `state=2` and the output of the
%   previous function call is assigned to the input struct. `fStat` is called
%   once again in the end with `state=3` to calculate final parameters (in
%   the last run, input `parIn.param` contains all the annealing
%   parameters). For comparison see the defaul function [sw_fstat].
%   Default value is `@sw_fstat`.
%
% `'fSub'`
% : Function to define sublattices for Monte-Carlo speedup. Function handle
%   with the following header:
%   ```
%   cGraph = fSub(conn,nExt)
%   ```
%   where `cGraph` is a row vector with $n_{magExt}$ number of elements
%   `conn` is a matrix with dimensions of $[2\times n_{conn}]$ $n_{ext}$ is
%   equal to `nExt`. For the SpinW implementation see [sw_fsub]. Default
%   value is `@sw_fsub`.
%
% `'subLat'`
% : Vector that assigns all magnetic moments into non-interacting
%   sublattices, contains a single index $(1,2,3...)$ for every
%   magnetic moment, row vector with $n_{magExt}$ number of elements. If
%   undefined, the function defined in `fSub` parameter will be used to
%   partition the lattice.
%
% `'title'`
% : Gives a title string to the simulation that is saved in the
%   output.
%
% `'autoK'`
% : Bin length of the autocorrelation vector. Should be a few times
%   smaller than `nMC`. Default value is 0 when no autocorrelation function
%   is calculated.
%
% ### Output Arguments
%
% `stat` struct that contains the calculated TD averages and the parameters
% of the simulation with the following fields:
%
% `param`
% : All input parameter values of the anneal function.
%
% `obj`
% : The clone of the input `obj` updated with the final magnetic
%   structure.
%
% `M`
% : Components of the magnetisation after the last annealing
%   run stored in a matrix with dimensions of $[3\times n_{magExt}]$.
%
% `E`
% : Energy of the system after the last annealing run, excluding the self
%   energy.
%
% `T`
% : Final temperature of the sample.
%
% Depending on the `fStat` parameter, additional fields are included. Using
% the default function [sw_fstat] the following parameters are also
% calculated:
%
% `avgM`
% : Average value of the magnetisation vector sampled over `nStat` runs,
%   stored in a matrix with dimensions of $[3\times n_{magExt}]$.
%
% `stdM`
% : Standard deviation of the mgnetisation vector sampled over
%   `nStat` runs, stored in a matrix with dimensions of $[3\times
%   n_{magExt}]$.
%
% `avgE`
% : Average system energy per spin averaged over `nStat` runs, scalar.
%
% `stdE`
% : Standard deviation of the system energy per spin over
%   `nStat` runs, scalar.
%
% `Cp`
% : Heat capacity of the sample, calculated using the formula $(\langle E^2\rangle-\langle E\rangle^2)/k_B/T^2$.
%
% `Chi`
% : Magnetic susceptibility of the sample calculated using the formula $(\langle M^2\rangle-\langle M\rangle^2)/k_B/T$.
%
%
% ### Reference
%
%    Kirkpatrick, S., Gelatt, C.D., & Vecchi, M.P. (1983). Optimization by
%    Simulated Annealing. _Science, 220_, 671-680.
%
% ### See Also
%
% [spinw] \| [spinw.optmagstr] \| [sw_fsub] \| [sw_fstat]
%
% *[TD]: Thermodynamic
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.anneal(*args, **kwargs)


def symbolic(obj=None, symb=None, **kwargs):
    """
% switches between symbolic/numeric mode
%
% ### Syntax
%
% `symb = symbolic(obj)`
%
% `symbolic(obj, symb)`
%
% ### Description
%
% `symb = symbolic(obj)` returns `true` if symbolic calculation mode is on,
% `false` for numeric mode.
%
% `symbolic(obj, symb)` sets whether the calculations are in
% symbolic/numeric (`true`/`false`) mode. Switching to symbolic mode, the
% spin values, matrix elements, magnetic field, magnetic structure and
% physical units are converted into symbolic variables. If this is not
% desired, start with a symbolic mode from the beggining and have full
% control over the values of the above mentioned variables.
%
% ### See Also
%
% [spinw] \| [spinw.spinwavesym]
%
    """
    args = tuple(v for v in [obj, symb] if v is not None)
    return m.symbolic(*args, **kwargs)


def horace_sqw(obj=None, qh=None, qk=None, ql=None, en=None, pars=None, *args, **kwargs):
    """
% Calculate spectral weight from a spinW model for Horace. Uses disp2sqw
% as the back-end function to calculate the convolution.
%
%   >> weight = swobj.horace_sqw(qh,qk,ql,en,pars,swobj,pars,kwpars)
%
% Input:
% ------
%   qh,qk,ql,en Arrays containing points at which to evaluate sqw from the
%               broadened dispersion
%
%   pars        Arguments needed by the function.
%               - pars = [model_pars scale_factor resolution_pars]
%               - Should be a vector of parameters
%               - The first N parameters relate to the spin wave dispersion
%                 and correspond to spinW matrices in the order defined by
%                 the 'mat' option [N=numel(mat)]
%               - The next M parameters relate to the convolution parameters
%                 corresponding to the convolution function defined by the
%                 'resfun' option (either one or two parameters depending
%                 on function type.
%               - The last parameter is a scale factor for the intensity
%                 If this is omitted, a scale factor of 1 is used;
%
%   kwpars      - A series of 'keywords' and parameters. Specific to this
%                 function is:
%
%               - 'resfun' - determines the convolution / resolution
%                    function to get S(q,w). It can be either a string:
%                      'gauss' - gaussian with single fixed (fittable) FWHM
%                      'lor' - lorentzian with single fixed (fittable) FWHM
%                      'voigt' - pseudo-voigt with single fixed (fittable) FWHM
%                      @fun - a function handle satisfying the requirements of
%                             the 'fwhm' parameter of disp2sqw.
%                    NB. For 'gauss' and 'lor' only one fwhm parameter may be
%                    specified. For 'voigt', fwhm = [width lorz_frac]
%                    contains two parameters - the fwhm and lorentzian fraction
%                    [default: 'gauss']
%               - 'partrans' - a function to transform the fit parameters
%                    This transformation will be applied before each iteration
%                    and the transformed input parameter vector passed to
%                    spinW and the convolution function.
%                    [default: @(y)y  % identity operation]
%               - 'coordtrans' - a matrix to transform the input coordinates
%                    (qh,qk,ql,en) before being sent to SpinW.
%                    [default: eye(4) % identity]
%
%               In addition, the following parameters are used by this function
%                    and will also be passed on to spinw.matparser which will
%                    do the actual modification of spinW model parameters:
%
%               - 'mat' - A cell array of labels of spinW named 'matrix' or
%                    matrix elements. E.g. {'J1', 'J2', 'D(3,3)'}. These will
%                    be the model parameters to be varied in a fit, their
%                    order in this cell array will be the same as in the
%                    fit parameters vector.
%                    [default: [] % empty matrix - no model parameters]
%
%                 All other parameters will be passed to spinW. See the help
%                    for spinw/spinwave, spinw/matparser and spinw/sw_neutron
%                    for more information.
%
%   swobj       The spinwave object which defines the magnetic system to be
%               calculated.
%
% Output:
% -------
%   weight      Array with spectral weight at the q,e points
%               If q and en given:  weight is an nq x ne array, where nq
%                                   is the number of q points, and ne the
%                                   number of energy points
%               If qw given together: weight has the same size and dimensions
%                                     as q{1} i.e. qh
%
% Example:
% --------
%
% tri = sw_model('triAF',[5 1]);                         % J1=5, J2=1 (AFM)
% spinw_pars = {'mat', {'J1', 'J2'}, 'hermit', true, ...
%               'useMex', true, 'optmem', 100};
% [wf,fp] = fit_sqw(w1, @tri.horace_sqw, {[J1 J2 fwhm] spinw_pars});
    """
    args = tuple(v for v in [obj, qh, qk, ql, en, pars] if v is not None) + args
    return m.horace_sqw(*args, **kwargs)


def getmatrix(obj=None, *args, **kwargs):
    """
% determines the symmetry allowed tensor elements
%
% ### Syntax
%
% `amat = getmatrix(obj,Name,Value)`
%
% ### Description
%
% `amat = getmatrix(obj,Name,Value)` determines the symmetry allowed
% elements of the exchange, single-ion anistropy and g-tensor. For bonds,
% the code first determines the point group symmetry on the center of the
% bond and calculates the allowed eelements of the exchange tensor
% accordingly. For anisotropy and g-tensor, the point group symmetry of the
% selected atom is considered. For example the code can correctly calculate
% the allowed Dzyaloshinskii-Moriya vectors.
%
% ### Examples
%
% To following code will determine the allowed anisotropy matrix elements
% in the $C4$ point group (the symmetry at the $(0,0,0)$ atomic position).
% The allowed matrix elements will be `diag([A A B])`:
%
% ```
% >>cryst = spinw
% >>cryst.genlattice('sym','P 4')
% >>cryst.addatom('r',[0 0 0],'label','MCu2')
% >>cryst.addmatrix('label','A','value',1)
% >>cryst.gencoupling
% >>cryst.addaniso('A')
% >>cryst.getmatrix('mat','A')>>
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% At least one of the following option has to be defined:
%
% `mat`
% : Label or index of a matrix that is already assigned to
%   a bond, anisotropy or g-tensor, e.g. `J1`.
%
% `bond`
% : Index of the bond in `spinw.coupling.idx`, e.g. 1 for first neighbor
%   bonds.
%
% `aniso`
% : Label or index of the magnetic atom that has a single ion
%   anisotropy matrix is assigned, e.g. `Cr1` if `Cr1` is a magnetic atom.
%
% `gtensor`
% : Label or index of the magnetic atom that has a g-tensor is
%   assigned.
%
% Optional inputs:
%
% `subIdx`
% : Selects a certain bond, within equivalent bonds. Default value is 1.
%
% `tol`
% : Tolerance for printing the output for the smallest matrix
%   element.
%
% `pref`
% : If defined `amat` will contain a single $[3\times 3]$ matrix by
%   multuplying the calculated tensor components with the given prefactors.
%   Thus `pref` should contain the same number of elements as the number of
%   symmetry allowed tensor components. Alternatively, if only a few of the
%   symmetry allowed matrices have non-zero prefactors, use e.g.
%   `{[6 0.1 5 0.25]}` which means, the 6th symmetry allowed matrix have
%   prefactor 0.1, the 5th symmetry allowed matrix have prefactor 0.25.
%   Since Heisenberg isotropic couplings are always allowed, a cell with a
%   single element will create a Heisenberg coupling, e.g. `{0.1}`, which is
%   identical to `obj.matrix.mat = eye(3)*0.1`. For Dzyaloshinskii-Moriya
%   interactions (antisymmetric exchange matrices), use a three element
%   vector in a cell, e.g. `pref = {[D1 D2 D3]}`. In this case, these will
%   be the prefactors of the 3 antisymmetric allowed matrices. In
%   case no crystal symmetry is defined, these will define directly the
%   components of the  Dzyaloshinskii-Moriya interaction in the xyz
%   coordinate system.
%
%   {{note Be carefull with the sign of the Dzyaloshinskii-Moriya
%   interaction, it depends on the counting order of the two interacting
%   atoms! For single-ion anisotropy and g-tensor antisymmetric matrices
%   are forbidden in any symmetry.}}
%
% `'fid'`
% : Defines whether to provide text output. The default value is determined
%   by the `fid` preference stored in [swpref]. The possible values are:
%   * `0`   No text output is generated.
%   * `1`   Text output in the MATLAB Command Window.
%   * `fid` File ID provided by the `fopen` command, the output is written
%           into the opened file stream.
%
% ### Output Arguments
%
% `aMat`
% : If no prefactors are defined, `aMat` contains all symmetry
%   allowed elements of the selected tensor, dimensions are $[3\times 3\times n_{symmat}]$.
%   If a prefactor is defined, it is a single $[3\times 3]$ matrix, that is
%   a sum of all symmetry allowed elemenets multiplied by the given
%   prefactors.
%
% ### See Also
%
% [spinw.setmatrix]
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.getmatrix(*args, **kwargs)


def field(obj=None, *args, **kwargs):
    """
% get/set magnetic field value
%
% ### Syntax
%
% `field(obj,B)`
% `B = field(obj)`
%
% ### Description
%
% `field(obj,B)` sets the magnetic field stored in `obj.single_ion.field`
% to `B`, where `B` is a $[1\times 3]$ vector.
%
% `B = field(obj)` returns the current value of the magnetic field value
% stored in `obj`.
%
% ### See Also
%
% [spinw] \| [spinw.temperature] \| [spinw.single_ion]
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.field(*args, **kwargs)


def horace(obj=None, qh=None, qk=None, ql=None, *args, **kwargs):
    """
% spin wave calculator with interface to Horace
%
% ### Syntax
%
% `[w, s] = horace(obj, qh, qk, ql,Name,Value)`
%
% ### Description
%
% `[w, s] = horace(obj, qh, qk, ql,Name,Value)` produces spin wave
% dispersion and intensity for [Horace](http://horace.isis.rl.ac.uk).
%
% ### Examples
%
% This example creates a `d3d` object, a square in $(h,k,0)$ plane and in
% energy between 0 and 10 meV. Then calculates the inelastice neutron
% scattering intensity of the square lattice antiferromagnet stored in
% `cryst` and plots a cut between 4 and 5 meV using the Horace `plot`
% command.
% ```
% >>>horace on
% >>cryst = sw_model('squareAF',1)
% >>d3dobj = d3d(cryst.abc,[1 0 0 0],[0,0.02,2],[0 1 0 0],[0,0.02,2],[0 0 0 1],[0,0.1,10])
% >>d3dobj = disp2sqw_eval(d3dobj,@cryst.horace,{'component','Sperp'},0.1)
% >>plot(cut(d3dobj,[],[],[4 5]))
% >>>colorslider('delete')
% >>snapnow
% >>>horace off
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% `qh`, `qk`, `ql`
% : Reciprocal lattice vectors in reciprocal lattice units.
%
% ### Name-Value Pair Arguments
%
% `'component'`
% : Selects the previously calculated intensity component to be
%   convoluted. The possible options are:
%   * `'Sperp'` convolutes the magnetic neutron scattering
%               intensity ($\langle S_\perp \cdot S_\perp\rangle$ expectation value).
%               Default value.
%   * `'Sab'`   convolutes the selected components of the spin-spin
%               correlation function.
%   For details see [sw_egrid].
%
% `'norm'`
% : If `true` the spin wave intensity is normalized to mbarn/meV/(unit
%   cell) units. Default is `false`.
%
% `'dE'`
% : Energy bin size, for intensity normalization. Use 1 for no
%   division by `dE` in the intensity.
%
% `'param'`
% : Input parameters (can be used also within Tobyfit). Additional
%   parameters (`'mat'`,`'selector'`) might be necessary, for details see
%   [spinw.matparser]. All extra parameters of `spinw.horace`
%   will be forwarded to the [spinw.matparser] function before
%   calculating the spin wave spectrum (or any user written parser
%   function). For user written functions defined with the
%   following header:
%   ```
%   func(obj,param)
%   ```
%   the value of the param option will be forwarded. For user
%   functions with variable number of arguments, all input options
%   of `spinw.horace` will be forwarded. In this case it is recommended
%   to use [sw_readparam] function to handle the variable number
%   arguments within `func()`.
%
% `'parfunc'`
% : Parser function of the `param` input. Default value is
%   `@spinw.matparser` which can be used directly by Tobyfit. For user
%   defined functions the minimum header has to be:
%   ```
%   func(obj,param)
%   ```
%   where obj is an spinw type object, param is the parameter
%   values forwarded from` spinw.horace` directly.
%
% `'func'`
% : User function that will be called after the parameters set on
%   the [spinw] object. It can be used to optimize magnetic
%   structure for the new parameters, etc. The input should be a
%   function handle of a function with a header:
%   ```
%   fun(obj)
%   ```
%
% `'fid'`
% : Defines whether to provide text output. The default value is determined
%   by the `fid` preference stored in [swpref]. The possible values are:
%   * `0`   No text output is generated.
%   * `1`   Text output in the MATLAB Command Window.
%   * `fid` File ID provided by the `fopen` command, the output is written
%           into the opened file stream.
%
% `'useFast'`
% : whether to use the 'fastmode' option in spinwave() or not. This method
%           calculates only the unpolarised neutron cross-section and
%           *ignores all negative energy branches*. In general it produces
%           the same spectra as spinw.spinwave, with some rounding errors,
%           but can be 2-3 times faster and uses less memory.
%
% ### Output Arguments
%
% `w`
% : Cell that contains the spin wave energies. Every cell elements
%           contains a vector of spin wave energies for the corresponding
%           input $Q$ vector.
%
% `s`
% : Cell that contains the calculated element of the spin-spin
%           correlation function. Every cell element contains a vector of
%           intensities in the same order as the spin wave energies in `w`.
%
% ### See Also
%
% [spinw] \| [spinw.spinwave] \| [spinw.matparser] \| [sw_readparam]
%
    """
    args = tuple(v for v in [obj, qh, qk, ql] if v is not None) + args
    return m.horace(*args, **kwargs)


def abc(obj=None, ind=None, **kwargs):
    """
% returns lattice parameters and angles
%
% ### Syntax
%
% `latvect = abc(obj)`
%
% ### Description
%
% `latvect = abc(obj)` extracts the lattice vectors and angles from a
% [spinw] object.
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Output Arguments
%
% `latVect`
% : Vector with elements `[a, b, c, \\alpha, \\beta, \\gamma]`,
%   contains the lattice parameters and angles by default in \\ang and
%   degree units respectively (see [spinw.unit] for details).
%
% ### See Also
%
% [spinw.horace]
%
    """
    args = tuple(v for v in [obj, ind] if v is not None)
    return m.abc(*args, **kwargs)


def temperature(obj=None, *args, **kwargs):
    """
% get/set temperature
%
% ### Syntax
%
% `temperature(obj, T)`
%
% `T = temperature(obj)`
%
% ### Description
%
% `temperature(obj, T)` sets the temperature stored in `obj` to `T`, where
% `T` is scalar. The units of temerature is determined by the
% `spinw.unit.kB` value, default unit is Kelvin.
%
% `T = temperature(obj)` returns the current temperature value stored in
% `obj`.
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.temperature(*args, **kwargs)


def table(obj=None, type=None, index=None, showVal=None, **kwargs):
    """
% outputs easy to read tables of internal data
%
% ### Syntax
%
% `T = table(obj,type,{index},{showval})`
%
% ### Description
%
% `T = table(obj,type,{index},{showval})` returns a table that shows in an
% easy to read/export format different internal data, such as magnetic atom
% list, bond list, magnetic structure, etc.
%
% For the matrix labels in the list of bonds, the '>>' sign means that the
% matrix value is determined using the bond symmetry operators.
%
% {{note The `table` data type is only supported in Matlab R2013b or newer.
% When running older versions of Matlab, `spinw.table` returns a struct.}}
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% `type`
% : String, determines the type of data to show, possible values are:
%   * `'matom'`     properties of magnetic atoms in the unit cell,
%   * `'matrix'`    list of matrices,
%   * `'ion'`       single ion term in the Hamiltonian,
%   * `'bond'`      properties of selected bonds,
%   * `'mag'`       magnetic structure.
%
% `index`
% : Indexing into the type of data to show, its meaning depends on the
%   `type` parameter. For `'bond'` indexes the bonds (1 for first
%   neighbors, etc.), if empty all bonds will be shown. For `'mag'` it
%   indexes the propagation vectors, the magnetization of the selected
%   propagation vector will be shown. Default value is 1, if empty vector `[]` is given, all
%   bonds/propagation vector will be shown.
%
% `showVal`
% : If `true`, also the values of the single ion and exchange matrices
%   will be shown. The values shown  are the symmetry transformed exchange
%   values after the symmetry operations (if there is any). Default value
%   is `false`.
%
% ### Output Arguments
%
% `T`
% : Matlab `table` type object.
%
    """
    args = tuple(v for v in [obj, type, index, showVal] if v is not None)
    return m.table(*args, **kwargs)


def annealloop(obj=None, *args, **kwargs):
    """
% parameter sweep for simulated annealing
%
% ### Syntax
%
% `stat = anneal(obj,Name,Value)`
%
% ### Description
%
% `stat = annealloop(obj,Name,Value)` performs simulated annealing while
% stepwise changing a selected parameter such as temperature or magnetic
% field while measuring thermodynamic properties. The function has the same
% parameters as [spinw.anneal] plus an additional
%
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% `'func'`
% : Function that changes the parameters in the spinw object in every
%   loop. Default function is to change the temperature:
%   ```
%   @temperature(obj,x)
%   ```
%   The function takes two inputs a [spinw] object and a parameter value
%   (ir values in a vector) and changes the correspondign property inside
%   the object.
%
% `'x'`
% : Matrix of values of the loop parameter, with dimensions of
%   $[n_{par}\times n_{loop}]$. Default value is 1. In the i-th loop the
%   loop function is called as:
%   ```
%   func(obj,x(:,i));
%   ```
%
% `'saveObj'`
% : If `true`, the spinw object is saved after every annealing step for
%   debugging purposes. Default is `false`.
%
% `'tid'`
% : Determines if the elapsed and required time for the calculation is
%   displayed. The default value is determined by the `tid` preference
%   stored in [swpref]. The following values are allowed (for more details
%   seee [sw_timeit]):
%   * `0` No timing is executed.
%   * `1` Display the timing in the Command Window.
%   * `2` Show the timing in a separat pup-up window.
%
% ### Output Arguments
%
% Same output as of [spinw.anneal], just the struct is packaged into a cell
% with $n_{loop}$ number of elements.
%
% ### Reference
%
%    Kirkpatrick, S., Gelatt, C.D., & Vecchi, M.P. (1983). Optimization by
%    Simulated Annealing. _Science, 220_, 671-680.
%
% ### See Also
%
% [spinw] \| [spinw.anneal] \| [sw_fsub] \| [sw_fstat]
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.annealloop(*args, **kwargs)


def addtwin(obj=None, *args, **kwargs):
    """
% adds crystallographic twins
%
% ### Syntax
%
% `addtwin(obj,Name,Value)`
%
% ### Description
%
% `addtwin(obj,Name,Value)` adds crystallographic twins defined by a
% rotation matrix and its volume fraction. Using crystallographic twins,
% SpinW can simulate imperfect samples and if the relative orientation of
% the crystallographic twins are knows, SpinW simulations can be directly
% compared to the expeiments on the inperfect sample.
%
% ### Examples
%
% This example shows how to add two extra crystallographic twins to the
% crystal.  Together with the original orientation there will be three
% twins with equal volumes.
%
% ```
% cryst.addtwin('axis',[0 0 1],'phid',[60 120],'vol',[1 1])
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% `'axis'`
% : Defines the axis of rotation to generate twins in the xyz
%   coordinate system, dimensions are $[1\times 3]$.
%
% `'phi'`
% : Defines the angle of rotation to generate twins in radian
%   units. Several twins can be defined parallel if `phi` is a
%   row vector. Dimensions are $[1\times n_{twin}]$.
%
% `'phid'`
% : Alternative to `phi` but the unit is \\deg.
%
% `'rotC'`
% : Rotation matrices, that define crystallographic twins. This is an
%   alternative to the `axis`-`phi` parameter pair. Matrix dimensions are
%   $[3\times 3\times n_{twin}]$.
%
% `'vol'`
% : Volume fractions of the twins stored in a row vector with $n_{twin}$
%   elements. Default value is `ones(1,nTwin)`.
%
% `'overwrite'`
% : If `true`, the last twin will be overwritten, instead of adding a
%   new one. Default is `false`.
%
% ### Output Arguments
%
% The function adds extra entries to the [spinw.twin] property.
%
% ### See Also
%
% [spinw] \| [spinw.twinq]
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.addtwin(*args, **kwargs)


def genlattice(obj=None, *args, **kwargs):
    """
% generates crystal lattice
%
% ### Syntax
%
% `genlattice(obj,Name,Value)`
%
% `R = genlattice(___)`
%
% ### Description
%
% `genlattice(obj,Name,Value)` generates all necessary parameters to define
% a lattice including space group symmetry and store the result it in the
% [spinw.lattice] field.
%
% `R = genlattice(___)` also returns the rotation matrix that
% rotates the inpub basis vectors to the internal coordinate system.
%
% Alternatively the lattice parameters can be given directly when the
% [spinw] object is created using the `spinw(inpStr)` command, where struct
% contains the fields with initial parameters, e.g.:
% ```
% inpStr.lattice.lat_const = [3 3 4];
% ```
%
% ### Example
%
% ```
% crystal.genlattice('lat_const',[3 3 4],'angled',[90 90 120],'sym','P 6')
% crystal.genlattice('lat_const',[3 3 4],'angled',[90 90 120],'sym',168)
% crystal.genlattice('lat_const',[3 3 4],'angled',[90 90 120],'sym','-y,x-y,z; -x,-y,z','label','R -3 m')
% ```
%
% The three lines are equivalent, both will create hexagonal lattice, with
% $P6$ space group.
%
% ### Input
%
% `obj`
% : [spinw] object.
%
% ### Options
%
% `angled`
% : `[\\alpha, \\beta, \\gamma]` angles in \\deg, dimensions are $[1\times 3]$.
%
% `angle`
% : `[\\alpha, \\beta, \\gamma]` angles in radian, dimensions are $[1\times 3]$.
%
% `lat_const`
% : `[a, b, c]` lattice parameters in units defined in [spinw.unit] (with \\ang
%   being the default), dimensions are $[1\times 3]$.
%
% `spgr` or 'sym'
% : Defines the space group. Can have the following values:
%
%   * **space group label** string, name of the space group, can be any
%     label defined in the [symmetry.dat] file.
%   * **space group index** line number in the [symmetry.dat] file.
%   * **space group operators** matrix with dimensions
%     $[3\times 4\times n_{op}]$.
%
%   The [symmetry.dat] file stores definition of the 230 space groups in
%   standard settings as it is in the [International Tables of Crystallography](http://it.iucr.org/A/).
%   Additional lines can be added to the [symmetry.dat] file using the
%   [swsym.add] function which later can be used in the `spgr` option.
%
%   If the `spgr` option is 0, no symmetry will be used. The
%   [spinw.gencoupling] function will determine the equivalent bonds based on
%   bond length.
%
%   Can also provide spacegroup and label (see below) in a cell e.g.
%   {'-x,y,-z', 'P 2'}
%
% `label`
% : Optional label for the space group if the generators are given in the
%   `spgr` option.
%
% `bv`
% : Basis vectors given in a matrix with dimensions of $[3\times 3]$, where
%   each column defines a basis vector.
%
% `origin`
% : Origin for the space group operators, default value is `[0 0 0]`.
%
% `perm`
% : Permutation of the abc axes of the space group operators.
%
% `nformula`
% : Gives the number of formula units in the unit cell. It is used
%   to normalize cross section in absolute units. Default value is 0, when
%   cross section is normalized per unit cell.
%
% ### Output
%
% `R`
% : Rotation matrix that brings the input basis vector to the SpinW
%   compatible form:
%   ```
%   BVspinw = R*BV
%   ```
%
% The result of the `spinw.genlattice` function is that `obj.lattice` field
% will be changed based on the input, the lattice parameters are stored
% directly and the optional space group string is converted into space
% group operator matrices.
%
% ### See also
%
% [spinw], [swsym.add], [swsym.operator], [spinw.gencoupling]
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.genlattice(*args, **kwargs)


def quickham(obj=None, J=None, **kwargs):
    """
% quickly generate magnetic Hamiltonian
%
% ### Syntax
%
% `quickham(obj,J)`
%
% ### Description
%
% `quickham(obj,J)` generates the bonds from the predefined crystal
% structure and assigns exchange values to bonds such as `J(1)` to first
% neighbor, `J(2)` for second neighbor etc. The command will erase all
% previous bonds, anisotropy, g-tensor and matrix definitions. Even if
% `J(idx) == 0`, the corresponding bond and matrix will be created.
%
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% `J`
% : Vector that contains the Heisenberg exchange values. `J(1)` for
%      first neighbor bonds, etc.
%
% ### See Also
%
% [spinw.gencoupling] \| [spinw.addcoupling] \| [spinw.matrix] \|
% [spinw.addmatrix]
%
    """
    args = tuple(v for v in [obj, J] if v is not None)
    return m.quickham(*args, **kwargs)


def matom(obj=None, **kwargs):
    """
% generates magnetic lattice
%
% ### Syntax
%
% `mAtomList = matom(obj)`
%
% ### Description
%
% `mAtomList = matom(obj)` is the same as [spinw.atom], but only lists the
% magnetic atoms, which have non-zero spin. Also this function stores the
% generated list in [spinw.cache].
%
% ### Output Arguments
%
% `mAtomList`
% : structure with the following fields:
%   * `r`   Position of the magnetic atoms in a matrix with dimensions of
%     $[3\times n_{magAtom}]$.
%   * `idx` Index in the symmetry inequivalent atom list [spinw.unit_cell]
%     stored in a row vector with $n_{magAtom}]$ number of elements.
%   * `S`   Spin of the magnetic atoms stored in a row vectorwith
%     $n_{magAtom}]$ number of elements.
%
% ### See Also
%
% [spinw.atom]
%
    """
    args = tuple(v for v in [obj] if v is not None)
    return m.matom(*args, **kwargs)


def atom(obj=None, **kwargs):
    """
% generates symmetry equivalent atomic positions
%
% ### Syntax
%
% `atomList = atom(obj)`
%
% ### Description
%
% `atomList = atom(obj)` generates all atomic positions using the symmetry
% operators stored in `obj.lattice.sym` and the symmetry inequivalent
% atomic positions in `obj.unit_cell.r`. If no symmetry is defined (denoted
% $P0$ symmetry) or the symmetry is $P1$ the function returns simply the
% positions stored in `obj.unit_cell.r`.
%
% ### Examples
%
% Here we create a new space group, that contains all the translations of
% the FCC lattice. Then create a crystal with an atom at `[0 0 0]` position.
% The `cryst.atom` lists all 4 symmetry equivalent positions generated using
% the FCC symmetry operators:
%
% ```
% >>cryst = spinw
% >>opStr = 'x+1/2,y+1/2,z;x+1/2,y,z+1/2;x,y+1/2,z+1/2';
% >>cryst.genlattice('lat_const',[8 8 8],'sym',opStr,'label','FCC')
% >>cryst.addatom('r',[0 0 0],'label','Atom1')
% >>atomList = cryst.atom
% >>atomList.r>>
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Output Arguments
%
% `atomList` is a structure with the following fields:
% * `r`     Positions of the atoms in lattice units stored in matrix with
%           dimensions of $[3\times n_{atom}]$.
% * `idx`   Indices of the atoms in the [spinw.unit_cell] field stored in a
%           matrix with dimensions of $[1\times n_{atom}]$.
% * `mag`   Vector of logical variables, `true` if the spin of the atom is
%           non-zero, dimensions are $[1\times n_{atom}]$.
%
% ### See Also
%
% [spinw] \| [spinw.matom] \| [swsym.add] \| [spinw.genlattice] \| [spinw.addatom]
%
    """
    args = tuple(v for v in [obj] if v is not None)
    return m.atom(*args, **kwargs)


def structfact(obj=None, kGrid=None, *args, **kwargs):
    """
% calculates magnetic and nuclear structure factor
%
% ### Syntax
%
% `sFact   = structfact(obj, kGrid,Name,Value)`
%
% `sfTable = structfact(obj, kGrid,Name,Value)`
%
% ### Description
%
% `sFact   = structfact(obj, kGrid,Name,Value)` returns the calculated
% structure factors in units of barn. Magnetic structures (FM, AFM and
% helical) are checked against
% [FullProf](https://www.ill.eu/sites/fullprof/). The structure factor
% includes the site occupancy and Debye-Waller factors calculated from
% `obj.unit_cell.biso`, using the same definition as in FullProf.
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% `kGrid`
% : Defines the reciprocal lattice vectors where the structure
%      factor is to be calculated. For commensurate structures these
%      are the possible positions of the magnetic Bragg peaks. For
%      incommensurate helical/conical structures 3 Bragg peaks
%      positions are possible: $(\mathbf{k}-\mathbf{k}_m,\mathbf{k},\mathbf{k}+\mathbf{k}_m) around every reciprocal
%      lattice vector. In this case still the integer positions have
%      to be given and the code calculates the intensities at all
%      three points.
%
% ### Name-Value Pair Arguments
%
% `'mode'`
% : String, defines the type of calculation:
%   * `mag`     Magnetic structure factor and intensities for
%               unpolarised neutron scattering.
%   * `nucn`    Nuclear structure factor and neutron scattering
%               intensities.
%   * `nucx`    X-ray scattering structure factor and
%               intensities.
%
% `'sortq'`
% : Sorting the reflections according to increasing momentum
%   value if `true`. Default is `false`.
%
% `'formfact'`
% : If true, the magnetic form factor is included in the structure factor
%   calculation. The form factor coefficients are stored in
%   `obj.unit_cell.ff(1,:,atomIndex)`. Default value is `false`.
%
% `'formfactfun'`
% : Function that calculates the magnetic form factor for given $Q$ value.
%   value. Default value is `@sw_mff`, that uses a tabulated coefficients
%   for the form factor calculation. For anisotropic form factors a user
%   defined function can be written that has the following header:
%   ```
%   F = formfactfun(atomLabel,Q)
%   ```
%   where the parameters are:
%   * `F`           row vector containing the form factor for every input
%                   $Q$ value
%   * `atomLabel`   string, label of the selected magnetic atom
%   * `Q`           matrix with dimensions of $[3\times n_Q]$, where each
%                   column contains a $Q$ vector in $\\ang^{-1}$ units.
%
% `'gtensor'`
% : If true, the g-tensor will be included in the structure factor
%   calculation. Including anisotropic g-tensor or different
%   g-tensor for different ions is only possible here.
%
% `'lambda'`
% : Wavelength. If given, the $2\theta$ value for each reflection
%   is calculated.
%
% `'dmin'`
% : Minimum $d$-value of a reflection, all higher order
%   reflections will be removed from the results.
%
% `'output'`
% : String, defines the type of the output:
%   * `struct`  Results are returned in a struct type variable,
%               default.
%   * `table`   Results are returned in a table type output for
%               easy viewing and exporting.
%
% `'tol'`
% : Tolerance of the incommensurability of the magnetic
%   ordering wavevector. Deviations from integer values of the
%   ordering wavevector smaller than the tolerance are considered
%   to be commensurate. Default value is $10^{-4}$.
%
% `'fitmode'`
% : Speed up the calculation for fitting mode (omitting
%   cloning the [spinw] object into the output). Default is `false`.
%
% `'fid'`
% : Defines whether to provide text output. The default value is determined
%   by the `fid` preference stored in [swpref]. The possible values are:
%   * `0`   No text output is generated.
%   * `1`   Text output in the MATLAB Command Window.
%   * `fid` File ID provided by the `fopen` command, the output is written
%           into the opened file stream.
%
% ### Output Arguments
%
% `sFact`
% : Structure with the following fields:
%    * `F2`     Magnetic structure factor in a matrix with dimensions
%               $[3\times n_{hkl}]$.
%    * `Mk`     Square of the 3 dimensional magnetic structure factor,
%               dimensions are:
%               $[n_{ext}(1)\cdot f_{ext}(1)\times n_{ext}(2)\cdot f_{ext}(2)\times n_{ext}(3)\cdot f_{ext}(3)]$,
%               where $n_{ext}$ is the size of the extended unit cell.
%    * `hkl`    Contains the input $Q$ values in a matrix with dimensins of $[3\times n_{hkl}]$.
%    * `hklA`   Same as `hkl`, but in \\ang$^{-1}$ units in the
%               $xyz$ Cartesian coordinate system.
%    * `incomm` Whether the spectra calculated is incommensurate or not.
%    * `formfact` Cell containing the labels of the magnetic ions if form
%               factor in included in the spin-spin correlation function.
%    * `{tth}`  $2\theta$ value of the reflection for the given wavelength,
%               only given if a wavelength is provided.
%    * `obj`    Clone of the input `obj` object.
%
% `sfTable`
% : Table, optional output for quick viewing and saving the output into a
%   text file.
%
% ### See Also
%
% [sw_qgrid] \| [sw_plotsf] \| [sw_intsf] \| [spinw.anneal] \| [spinw.genmagstr]
%
    """
    args = tuple(v for v in [obj, kGrid] if v is not None) + args
    return m.structfact(*args, **kwargs)


def magtable(obj=None, **kwargs):
    """
% creates tabulated list of all magnetic moments stored in obj
%
% moments = MAGTABLE(obj)
%
% The function lists the APPROXIMATED moment directions (using the rotating
% coordinate system notation) in the magnetic supercell, whose size is
% defined by the obj.mag_str.nExt field. The positions of the magnetic
% atoms are in lattice units.
%
% Input:
%
% obj           spinw class object.
%
% Output:
%
% 'moments' is struct type data that contains the following fields:
%   M           Matrix, where every column defines a magnetic moment,
%               dimensions are [3 nMagExt].
%   e1,e2,e3    Unit vectors of the coordinate system used for the spin
%               wave calculation, the i-th column contains a normalized
%               vector for the i-th moment. e3 is parallel to the magnetic
%               moment, e1 and e2 span a right handed orthogonal coordinate
%               system.
%   R           Matrix, where every column defines the position of the
%               magnetic atom in lattice units.
%   atom        Pointer to the magnetic atom in the subfields of
%               spinw.unit_cell.
%
% See also SPINW.GENMAGSTR.
%
    """
    args = tuple(v for v in [obj] if v is not None)
    return m.magtable(*args, **kwargs)


def plot(obj=None, *args, **kwargs):
    """
% plots 3D model
%
% ### Syntax
%
% `plot(obj,Name,Value)`
% `hFigure = plot(obj,Name,Value)`
%
% ### Description
%
% `plot(obj,Name,Value)` plots the atoms and couplings stored in `obj` onto
% an [swplot] figure (see [swplot.figure]). The generated 3D plot can be
% rotated using the mouse and panning works by keeping the Ctrl/Control
% button pressed. There is information about every object on the figure
% (here called tooltips) that is shown when clicked on the object. The 3D
% view direction can be changed programatically using [swplot.view] while
% translations are controlled using the [swplot.translate]. Arbitrary
% transformation (combination of rotation and translation) can be
% introduced using the [swplot.transform]. All these transformation act as
% a global transformation, relative transformation of the 3D objects is
% only possible at creation by defining the transformed coordinates.
%
% The `spinw.plot` function calls several high level plot routines to draw
% the different types of objects: [swplot.plotatom] (atoms),
% [swplot.plotmag] (magnetic moments), [swplot.plotion] (single ion
% properties), [swplot.plotbond] (bonds), [swplot.plotbase] (basis vectors)
% and [swplot.plotcell] (unit cells).
%
% The high level `spinw.plot` function can send send parameters to any of
% the above plot group functions. The paramer name has to be of the format:
% `['plot group name' 'group option']`. For example to set the `color` option
% of the cell (change the color of the unit cell) use the option
% 'cellColor'. In this case `spinw.plot` will call the [swplot.plotcell]
% function with the `color` parameter set to the given value. For all the
% possible group plot function options see the corresponding help.
%
% It is possible to switch off calling any of the subfunctions by using the
% option `['plot group name' 'mode']` set to `'none'`. For example to skip
% plotting of the atoms set the `'atomMode'` parameter to `'none'`:
% `spinw.plot('atomMode','none')`.
%
% ### Name-Value Pair Arguments
%
% These are global options, that each plot group function recognizes, these global
% options can be added without the group name.
%
% `'range'`
% : Plotting range of the lattice parameters in lattice units,
%   in a matrix with dimensions of $[3\times 2]$. For example to plot the
%   first unit cell, use: `[0 1;0 1;0 1]`. Also the number unit cells can
%   be given along the $a$, $b$ and $c$ directions, e.g. `[2 1 2]`, this is
%   equivalent to `[0 2;0 1;0 2]`. Default value is the single unit cell.
%
% `'unit'`
% : Unit in which the range is defined. It can be the following
%   string:
%   * `'lu'`        Lattice units (default).
%   * `'xyz'`       Cartesian coordinate system in \\ang units.
%
% `'figure'`
% : Handle of the [swplot] figure. Default is the active figure.
%
% `'legend'`
% : Whether to add legend to the plot, default value is `true`, for details
%   see [swplot.legend].
%
% `'fontSize'`
% : Font size of the atom labels in pt units, default value is stored in
%   `swpref.getpref('fontsize')`.
%
% `'nMesh'`
% : Resolution of the ellipse surface mesh. Integer number that is
%   used to generate an icosahedron mesh with $n_{mesh}$ number of
%   additional triangulation, default value is stored in
%   `swpref.getpref('nmesh')`.
%
% `'nPatch'`
% : Number of points on the curve for the arrows and cylinders,
%   default value is stored in `swpref.getpref('npatch')`.
%
% `'tooltip'`
% : If `true`, the tooltips will be shown when clicking on the plot.
%   Default value is `true`.
%
% `'shift'`
% : Column vector with 3 elements, all objects will be shifted by
%   the given value. Default value is `[0;0;0]`.
%
% `'replace'`
% : Replace previous plot if `true`. Default value is `true`.
%
% `'translate'`
% : If `true`, all plot objects will be translated to the figure
%   center. Default is `true`.
%
% `'zoom'`
% : If `true`, figure will be automatically zoomed to the ideal scale.
%   Default value is `true`.
%
% ### See Also
%
% [swplot.plotatom] \| [swplot.plotmag] \| [swplot.plotion] \|
% [swplot.plotbond] \| [swplot.plotbase] \| [swplot.plotcell]
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.plot(*args, **kwargs)


def genmagstr(obj=None, *args, **kwargs):
    """
% generates magnetic structure
%
% ### Syntax
%
% `genmagstr(obj,Name,Value)`
%
% ### Description
%
% `genmagstr(obj,Name,Value)` is a Swiss knife for generating magnetic
% structures. It allows the definition of magnetic structures using several
% different ways, depending on the `mode` parameter. The generated magnetic
% structure is stored in the [obj.mag_str] field. The magetic structure is
% stored as Fourier components with arbitrary number of wave vectors in the
% [spinw] object. However spin waves can be only calculated if the magnetic
% structure has a single propagation vector (plus a k=0 ferromagnetic
% component perpendicular to the incommensurate magnetization), we simply
% call it single-k magnetic structure. Thus `genmagstr` enables to input
% magnetic structures that comply with this restriction by defining a
% magnetic structure by the moment directions (`S`) in the crystallographic
% cell, a propagation vector (`km`) and a vector that defines the normal of
% the rotation of the spin spiral (`n`). The function converts these values
% into Fourier components to store. To solve spin wave dispersion of
% magnetic structures with multiple propagation vectors, a magnetic
% supercell has to be defined where the propagation vector can be
% approximated to zero.
%
% ### Examples
%
% The example creates the multi-k magnetic structure of USb given by the
% `FQ` Fourier components and plots the magnetic structure:
%
% ```
% >>USb = spinw
% >>USb.genlattice('lat_const',[6.203 6.203 6.203],'sym','F m -3 m')
% >>USb.addatom('r',[0 0 0],'S',1)
% >>FQ = cat(3,[0;0;1+1i],[0;1+1i;0],[1+1i;0;0])>>
% >>k  = [0 0 1;0 1 0;1 0 0];
% >>USb.genmagstr('mode','fourier','S',FQ,'nExt',[1 1 1],'k',k)
% >>plot(USb,'range',[1 1 1])
% >>snapnow
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% `'mode'`
% : Mode that determines how the magnetic structure is generated:
%   * `'random'` (optionally reads `k`, `n`, `nExt`)
%           generates a random structure in the structural cell if no other
%           arguments are specified here or previously in this spinw
%           object. If `nExt` is specified all spins in the supercell are
%           randomised. If `k` is specified a random helical structure with
%           moments perpendicular to `n` (default value: `[0 0 1]`) with
%           the specified `k` propagation vector is generated. (`n` is not
%           otherwise used).
%   * `'direct'` (reads `S`, optionally reads `k`, `nExt`)
%           direct input of the magnetic structure using the
%           parameters of the single-k magnetic structure.
%   * `'tile'` (reads `S`, optionally reads `nExt`)
%           Simply extends the existing or input structure
%           (`S`) into a magnetic supercell by replicating it.
%           If no structure is stored in the [spinw] object a random
%           structure is generated automatically. If defined,
%           `S` is used as starting structure for extension
%           overwriting the stored structure. If the original
%           structure is already extended with other size, only the
%           moments in the crystallographic cell wil be replicated.
%           Magnetic ordering wavevector `k` will be set to zero. To
%           generate structure with non-zero k, use the `'helical'` or
%           `'direct'` option.
%   * `'helical'` (reads `S`, optionally reads `n`, `k`, `r0`, `nExt`, `epsilon`)
%           generates helical structure in a single cell or in a
%           supercell. In contrary to the `'extend'` option the
%           magnetic structure is not generated by replication but
%           by rotation of the moments using the following formula:
%
%     $\mathbf{S}^{gen}_i(\mathbf{r}) = R(2 \pi \mathbf{k_m} \cdot \mathbf{r})\cdot \mathbf{S}_i$
%
%     where $S_i$ has either a single moment or as many moments
%           as the number of magnetic atoms in the crystallographic
%           cell. In the first case $r$ denotes the atomic
%           positions, while for the second case $r$ denotes the
%           position of the origin of the cell.
%   * `'rotate'` (optionally reads `S`, `phi`, `phid`, `n`, `nExt`)
%           uniform rotation of all magnetic moments with a
%           `phi` angle around the given `n` vector. If
%           `phi=0`, all moments are rotated so, that the first
%           moment is parallel to `n` vector in case of
%           collinear structure or in case of planar structure
%           `n` defines the normal of the plane of the magnetic
%           moments.
%   * `'func'` (reads `func`, `x0`)
%           function that defines the parameters of the single-k
%           magnetic structure: moment vectors, propagation vector
%           and normal vector from arbitrary parameters in the
%           following form:
%     ```
%     [S, k, n] = @(x)func(S0, x)
%     ```
%     where `S` is matrix with dimensions of $[3\times n_{magExt}]$. `k` is
%           the propagation vector in a 3-element row vector. `n` is the
%           normal vector of the spin rotation plane also 3-element row
%           vector. The default value for `func` is `@gm_spherical3d`. For planar
%           magnetic structure use `@gm_planar`. Only `func` and `x`
%           have to be defined for this mode.
%  * `'fourier'` (reads `S`, optionally reads `k`, `r0`, `nExt`, `epsilon`)
%           same as `'helical'`, except the `S` option is taken as the
%           Fourier components, thus if it contains real numbers, it will
%           generate a sinusoidally modulated structure instead of
%           a spiral.
%
% `'phi'`
% : Angle of rotation of the magnetic moments in radian. Default
%   value is 0.
%
% `'phid'`
% : Angle of rotation of the magnetic moments in \\deg. Default
%   value is 0.
%
% `'nExt'`
% : Size of the magnetic supercell in multiples of the
%   crystallographic cell, dimensions are $[1\times 3]$. Default value is
%   stored in `obj`. If `nExt` is a single number, then the size of the
%   extended unit cell is automatically determined from the first
%   magnetic ordering wavevector. E.g. if `nExt = 0.01`, then the number
%   of unit cells is determined so, that in the extended unit cell,
%   the magnetic ordering wave vector is `[0 0 0]`, within the given
%   0.01 rlu tolerance.
%
% `'k'`
% : Magnetic ordering wavevector in rlu, dimensions are $[n_K\times 3]$.
%   Default value is defined in `obj`.
%
% `'n'`
% : Normal vector to the spin rotation plane for single-k magnetic
%   structures, stored in a 3-element row vector, is automatically
%   normalised to a unit vector. Default value `[0 0 1]`. The coordinate
%   system of the vector is determined by `unit`.
%
% `'S'`
% : Vector values of the spins (expectation value), dimensions are $[3\times n_{spin} n_K]$.
%   Every column defines the three $(S_x, S_y, S_z)$ components of
%   the spin (magnetic moment) in the $xyz$ Descartes coodinate system or
%   in lu. Default value is stored in `obj`.
%
% `'unit'`
% : Determines the coordinate system for `S` and `n` vectors using a
%   string:
%   * `'xyz'`   Cartesian coordinate system, fixed to the lattice.
%               Default value.
%   * `'lu'`	Lattice coordinate system (not necessarily
%               Cartesian. The three coordinate vectors are
%               parallel to the lattice vectors but normalized to
%               unity.
%
% `'epsilon'`
% : The smalles value of incommensurability that is
%   tolerated without warning in lattice units. Default is $10^{-5}$.
%
% `'func'`
% : Function handle that produces the magnetic moments, ordering wave
%   vector and normal vector from the `x` parameters in the
%   following form:
%   ```
%   [M, k, n] = @(x)func(M0,x)
%   ```
%   where `M` is a matrix with dimensions of $[3\times n_{magExt}]$, `k` is
%   the propagation vector, `n` is the normal vector of the spin rotation
%   plane. The default function is [gm_spherical3d]. For planar magnetic
%   structure use [gm_planar].
%
% `'x0'`
% : Input parameters for `func` function, row vector with $n_X$ number of
%   elements.
%
% `'norm'`
% : Set the length of the generated magnetic moments to be equal to
%   the spin of the magnetic atoms. Default is `true`.
%
% `'r0'`
% : If `true` and only a single spin direction is given, the spin
%   phases are determined by atomic position times k-vector, while
%   if it is `false`, the first spin will have 0 phase. Default is
%   `true`.
%
% ### Output Arguments
%
% The [obj.mag_str] field will contain the new magnetic structure.
%
% ### See Also
%
% [spinw] \| [spinw.anneal] \| [spinw.optmagstr] \| [gm_spherical3d] \| [gm_planar]
%
% *[rlu]: Reciprocal Lattice Units
% *[lu]: Lattice Units
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.genmagstr(*args, **kwargs)


def intmatrix(obj=None, *args, **kwargs):
    """
% generates interaction matrix
%
% ### Syntax
%
% `[SS, SI, RR] = intmatrix(obj,Name,Value)`
%
% ### Description
%
% `[SS, SI, RR] = intmatrix(obj,Name,Value)` lists the bonds and generates
% the corresponding exchange matrices by applying the bond symmetry
% operators on the stored matrices. Also applies symmetry on the single ion
% anisotropies and can generate the representation of bonds, anistropies
% and atomic positions in an arbitrary supercell. The output argument `SS`
% contains the different types of exchange interactions separated into
% different fields, such as `SS.DM` for the Dzyaloshinskii-Moriya
% interaction, `SS.iso` for Heisenberg exchange, `SS.all` for general
% exchange etc.
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% `'fitmode'`
% : Can be used to speed up calculation, modes:
%   * `true`    No speedup (default).
%   * `false`   For the interactions stored in `SS`, only the
%               `SS.all` field is calculated.
%
% `'plotmode'`
% : If `true`, additional rows are added to `SS.all`, to identify
%   the couplings for plotting. Default is `false`.
%
% `'sortDM'`
% : If true each coupling is sorted for consistent plotting of
%   the DM interaction. Sorting is based on the `dR` bond vector that
%   points from `atom1` to `atom2`, for details see [spinw.coupling].
%   After sorting `dR` vector components fulfill the following rules in
%   hierarchical order:
%   1. `dR(x) > 0`
%   2. `dR(y) > 0`
%   3. `dR(z) > 0`.
%
%   Default is `false`.
%
% `'zeroC'`
% : Whether to output bonds with assigned matrices that have only
%   zero values. Default is `false`.
%
% `'extend'`
% : If `true`, all bonds in the magnetic supercell will be
%   generated, if `false`, only the bonds in the crystallographic
%   unit cell is calculated. Default is `true`.
%
% `'conjugate'`
% : Introduce the conjugate of the couplings (by exchanging the interacting
%   `atom1` and `atom2`). Default is `false`.
%
% ### Output Arguments
%
% `SS`
% : structure where every field is a matrix. Every column is a coupling
%   between two spins. The first 3 rows contain the unit cell translation
%   vector between the interacting spins, the 4th and 5th rows contain
%   the indices of the two interacting spins in the [spinw.matom] list.
%   Subsequent rows in the matrix depend on the field
%   SS will always have the following fields
%   * `all`
%   * `dip`
%   Subsequent rows in these matrices are the elements of the 3 x 3
%   exchange matrix `[Jxx; Jxy; Jxz; Jyx; Jyy; Jyz; Jzx; Jzy; Jzz]`
%   and the final row indicates whether the coupling is
%   bilinear (0) or biquadratic (1). The `dip` field contains the dipolar
%   interactions only that are not added to `SS.all.
%   If `plotmode` is `true`, two additional rows are added to `SS.all`,
%   that contains the `idx` indices of the `obj.matrix(:,:,idx)`
%   corresponding matrix for each coupling and the `idx` values of the
%   couplings (stored in `spinw.coupling.idx`).
%
%  If fitmode = false there are additional fields
%  * `iso` : One subsequent row which is the isotropic exchane
%  * `ani` : Subsequent rows contain anisotropic interaction `[Jxx; Jyy;
%               Jzz]`),
%  * `dm`  : Subsequent rows contain DM interaction `[DMx; DMy; DMz]`
%  * `gen` : Subsequent rows contain a general interaction
%            `[Jxx; Jxy; Jxz; Jyx; Jyy; Jyz; Jzx; Jzy; Jzz]`
%  * `bq`  : One subsequent row which is the isotropic exchagne as in
%            SS.iso but only the biquadratic couplings which are not
%            included in SS.iso
%
% `SI`
% : single ion properties stored in a structure with fields:
%
%   * `aniso`   Matrix with dimensions of $[3\times 3\times n_{magAtom}]$,
%               where the classical energy of the $i$-th spin is expressed
%               as `E_aniso = spin(:)*A(:,:,i)*spin(:)'`
% 	* `g`       g-tensor, with dimensions of $[3\times 3\times n_{magAtom}]$. It determines
%               the energy of the magnetic moment in external field:
%               `E_field = B(:)*g(:,:,i)*spin(:)'`
% 	* `field`   External magnetic field in a row vector with three elements $(B_x, B_y, B_z)$.
%
% `RR`
% : Positions of the atoms in lattice units in a matrix with dimensions of $[3\times n_{magExt}]$.
%
% ### See Also
%
% [spinw.table] \| [spinw.symop]
%
% *[DM]: Dzyaloshinskii-Moriya
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.intmatrix(*args, **kwargs)


def powspec(obj=None, hklA=None, *args, **kwargs):
    """
% calculates powder averaged spin wave spectra
%
% ### Syntax
%
% `spectra = powspec(obj,QA)`
%
% `spectra = powspec(___,Name,Value)`
%
% ### Description
%
% `spectra = powspec(obj,QA)` calculates powder averaged spin wave spectrum
% by averaging over spheres with different radius around origin in
% reciprocal space. This way the spin wave spectrum of polycrystalline
% samples can be calculated. This method is not efficient for low
% dimensional (2D, 1D) magnetic lattices. To speed up the calculation with
% mex files use the `swpref.setpref('usemex',true)` option.
%
% `spectra = powspec(___,Value,Name)` specifies additional parameters for
% the calculation. For example the function can calculate powder average of
% arbitrary spectral function, if it is specified using the `specfun`
% option.
%
% ### Example
%
% Using only a few lines of code one can calculate the powder spectrum of
% the triangular lattice antiferromagnet ($S=1$, $J=1$) between $Q=0$ and 3
% \\ang$^{-1}$ (the lattice parameter is 3 \\ang).
%
% ```
% >>tri = sw_model('triAF',1);
% >>E = linspace(0,4,100);
% >>Q = linspace(0,4,300);
% >>triSpec = tri.powspec(Q,'Evect',E,'nRand',1e3);
% >>sw_plotspec(triSpec);
% >>snapnow
% ```
%
% ### Input arguments
%
% `obj`
% : [spinw] object.
%
% `QA`
% : Vector containing the $Q$ values in units of the inverse of the length
% unit (see [spinw.unit]) with default unit being \\ang$^{-1}$. The
% value are stored in a row vector with $n_Q$ elements.
%
% ### Name-Value Pair Arguments
%
% `specfun`
% : Function handle of a solver. Default value is `@spinwave`. It is
%   currently tested with two functions:
%
%   * `spinw.spinwave` 	Powder average spin wave spectrum.
%   * `spinw.scga`      Powder averaged diffuse scattering spectrum.
%
% `nRand`
% : Number of random orientations per `QA` value, default value is 100.
%
% `Evect`
% : Row vector, defines the center/edge of the energy bins of the
%   calculated output, number of elements is $n_E$. The energy units are
%   defined by the `spinw.unit.kB` property. Default value is an edge bin
%   `linspace(0,1.1,101)`.
%
% `binType`
% : String, determines the type of bin, possible options:
%   * `'cbin'`    Center bin, the center of each energy bin is given.
%   * `'ebin'`    Edge bin, the edges of each bin is given.
%
%   Default value is `'ebin'`.
%
% `'T'`
% : Temperature to calculate the Bose factor in units
%   depending on the Boltzmann constant. Default value taken from
%   `obj.single_ion.T` value.
%
% `'title'`
% : Gives a title to the output of the simulation.
%
% `'extrap'`
% : If true, arbitrary additional parameters are passed over to
%   the spectrum calculation function.
%
% `'fibo'`
% : If true, instead of random sampling of the unit sphere the Fibonacci
%   numerical integration is implemented as described in
%   [J. Phys. A: Math. Gen. 37 (2004)
%   11591](http://iopscience.iop.org/article/10.1088/0305-4470/37/48/005/meta).
%   The number of points on the sphere is given by the largest
%   Fibonacci number below `nRand`. Default value is false.
%
% `'imagChk'`
% : Checks that the imaginary part of the spin wave dispersion is
%   smaller than the energy bin size. Default value is true.
%
% `'component'`
% : See [sw_egrid] for the description of this parameter.
%
% The function also accepts all parameters of [spinw.spinwave] with the
% most important parameters are:
%
% `'formfact'`
% : If true, the magnetic form factor is included in the spin-spin
%   correlation function calculation. The form factor coefficients are
%   stored in `obj.unit_cell.ff(1,:,atomIndex)`. Default value is `false`.
%
% `'formfactfun'`
% : Function that calculates the magnetic form factor for given $Q$ value.
%   value. Default value is `@sw_mff`, that uses a tabulated coefficients
%   for the form factor calculation. For anisotropic form factors a user
%   defined function can be written that has the following header:
%   ```
%   F = formfactfun(atomLabel,Q)
%   ```
%   where the parameters are:
%   * `F`           row vector containing the form factor for every input
%                   $Q$ value
%   * `atomLabel`   string, label of the selected magnetic atom
%   * `Q`           matrix with dimensions of $[3\times n_Q]$, where each
%                   column contains a $Q$ vector in $\\ang^{-1}$ units.
%
% `'gtensor'`
% : If true, the g-tensor will be included in the spin-spin correlation
%   function. Including anisotropic g-tensor or different
%   g-tensor for different ions is only possible here. Including a simple
%   isotropic g-tensor is possible afterwards using the [sw_instrument]
%   function.
%
% `'hermit'`
% : Method for matrix diagonalization with the following logical values:
%
%   * `true`    using Colpa's method (for details see [J.H.P. Colpa, Physica 93A (1978) 327](http://www.sciencedirect.com/science/article/pii/0378437178901607)),
%               the dynamical matrix is converted into another Hermitian
%               matrix, that will give the real eigenvalues.
%   * `false`   using the standard method (for details see [R.M. White, PR 139 (1965) A450](https://journals.aps.org/pr/abstract/10.1103/PhysRev.139.A450))
%               the non-Hermitian $\mathcal{g}\times \mathcal{H}$ matrix
%               will be diagonalised, which is computationally less
%               efficient. Default value is `true`.
%
% {{note Always use Colpa's method, except when imaginary eigenvalues are
%   expected. In this case only White's method work. The solution in this
%   case is wrong, however by examining the eigenvalues it can give a hint
%   where the problem is.}}
%
% `'fid'`
% : Defines whether to provide text output. The default value is determined
%   by the `fid` preference stored in [swpref]. The possible values are:
%   * `0`   No text output is generated.
%   * `1`   Text output in the MATLAB Command Window.
%   * `fid` File ID provided by the `fopen` command, the output is written
%           into the opened file stream.
%
% `'tid'`
% : Determines if the elapsed and required time for the calculation is
%   displayed. The default value is determined by the `tid` preference
%   stored in [swpref]. The following values are allowed (for more details
%   see [sw_timeit]):
%   * `0` No timing is executed.
%   * `1` Display the timing in the Command Window.
%   * `2` Show the timing in a separat pup-up window.
%
% `dE`
% : Energy resolution (FWHM) can be function, or a numeric matrix that
%   has length 1 or the number of energy bin centers.
%
% `'neutron_output'`
% : If `true`, the spinwave will output only `Sperp`, the S(q,w) component
%   perpendicular to Q that is measured by neutron scattering, and will
%   *not* output the  full Sab tensor. (Usually sw_neutron is used to
%   calculate `Sperp`.) Default value is `false`.
%
% `'fastmode'`
% : If `true`, will set `'neutron_output', true`, `'fitmode', true`,
%   `'sortMode', false`, and will only output intensity for positive energy
%   (neutron energy loss) modes. Default value is `false`.
%
% The function accepts some parameters of [spinw.scga] with the most important
% parameters are:
%
% `'nInt'`
% : Number of $Q$ points where the Brillouin zone is sampled for the
%   integration.
%
% ### Output Arguments
%
% `spectra`
% : structure with the following fields:
%
%   * `swConv` The spectra convoluted with the dispersion. The center
%     of the energy bins are stored in `spectra.Evect`. Dimensions are
%     $[n_E\times n_Q]$.
%   * `hklA` Same $Q$ values as the input `hklA`.
%   * `Evect` Contains the bins (edge values of the bins) of the energy transfer
%     values, dimensions are $[1\times n_E+1]$.
%   * `param` Contains all the input parameters.
%   * `obj` The clone of the input `obj` object, see [spinw.copy].
%
% ### See also
%
% [spinw] \| [spinw.spinwave] \| [spinw.optmagstr] \| [sw_egrid]
%
    """
    args = tuple(v for v in [obj, hklA] if v is not None) + args
    return m.powspec(*args, **kwargs)


def newcell(obj=None, *args, **kwargs):
    """
% transforms lattice
%
% ### Syntax
%
% `newcell(obj,Name,Value)`
%
% `T = newcell(obj,Name,Value)`
%
% ### Description
%
% `T = newcell(obj,Name,Value)` redefines the unit cell using new basis
% vectors. The input three basis vectors are in lattice units of the
% original cell and define a parallelepiped. The atoms from the original
% unit cell will fill the new unit cell and if the two cells are compatible
% the structure won't change. The magnetic structure, bonds and single ion
% property definitions will be erased. The new cell will have different
% reciprocal lattice, however the original reciprocal lattice units will be
% retained automatically. To use the new reciprocal lattice, set the
% `'keepq'` option to `false`. In the default case the [spinw.spinwave]
% function will calculate spin wave dispersion at reciprocal lattice points
% of the original lattice. The transformation between the two lattices is
% stored in `spinw.unit.qmat`.
%
% ### Examples
%
% In this example we generate the triangular lattice antiferromagnet and
% convert the hexagonal cell to orthorhombic. This doubles the number of
% magnetic atoms in the cell and changes the reciprocal lattice. However we
% set `'keepq'` parameter to `true` to able to index the reciprocal lattice
% of the orthorhombic cell with the reciprocal lattice of the original
% hexagonal cell. To show that the two models are equivalent, we calculate
% the spin wave spectrum on both model using the same rlu. On the
% orthorhombic cell, the $Q$ value will be converted automatically and the
% calculated spectrum will be the same for both cases.
%
% ```
% >>tri = sw_model('triAF',1)
% >>tri_orth = copy(tri)
% >>tri_orth.newcell('bvect',{[1 0 0] [1 2 0] [0 0 1]},'keepq',true)
% >>tri_orth.gencoupling
% >>tri_orth.addcoupling('bond',1,'mat','J_1')
% >>newk = ((tri_orth.unit.qmat)*tri.magstr.k')'
% >>tri_orth.genmagstr('mode','helical','k',newk,'S',[1 0 0]')
% >>plot(tri_orth)
% >>>swplot.zoom(1.5)
% >>snapnow
% >>>figure
% >>subplot(2,1,1)
% >>sw_plotspec(sw_egrid(tri.spinwave({[0 0 0] [1 1 0] 501})),'mode','color','dE',0.2)
% >>subplot(2,1,2)
% >>spec = tri_orth.spinwave({[0 0 0] [1 1 0] 501});
% >>sw_plotspec(sw_egrid(tri_orth.spinwave({[0 0 0] [1 1 0] 501})),'mode','color','dE',0.2)
% >>snapnow
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% `'bvect'`
% : Defines the new lattice vectors in the original lattice
%   coordinate system. Cell with the following elements
%   `{v1 v2 v3}` or a $[3\times 3]$ matrix with `v1`, `v2` and `v3` as column
%   vectors: `[v1 v2 v3]`. Default value is `eye(3)` for indentity
%   transformation.
%
% `'bshift'`
% : Row vector that defines a shift of the position of the unit cell.
%   Default value is `[0 0 0]`.
%
% `'keepq'`
% : If true, the reciprocal lattice units of the new model will be
%   the same as in the old model. This is achieved by storing the
%   transformation matrix between the new and the old coordinate system in
%   `spinw.unit.qmat` and applying it every time a reciprocal space
%   definition is invoked, such as in [spinw.spinwave]. Default value is
%   `false`.
%
% ### Output Arguments
%
% `T`
% : Transformation matrix that converts $Q$ points (in reciprocal
%       lattice units) from the old reciprocal lattice to the new
%       reciprocal lattice as follows:
%   ```
%   Qrlu_new = T * Qrlu_old
%   ```
%   where the $Q$ vectors are row vectors with 3 elements.
%
% ### See Also
%
% [spinw.genlattice] \| [spinw.gencoupling] \| [spinw.nosym]
%
% *[rlu]: reciprocal lattice unit
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.newcell(*args, **kwargs)


def fouriersym(obj=None, *args, **kwargs):
    """
% calculates the Fourier transformation of the symbolic Hamiltonian
%
% ### Syntax
%
% `res = fouriersym(obj,Name,Value)`
%
% ### Description
%
% `res = fouriersym(obj,Name,Value)` solves the symbolic Fourier transform
% problem.
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% `'hkl'`
% : Symbolic definition of positions in momentum space. Default value is
%   the general $Q$ point:
%   ```
%   hkl = [sym('h') sym('k') sym('l')]
%   ```
%
% ### See Also
%
% [spinw.fourier]
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.fouriersym(*args, **kwargs)


def moment(obj=None, *args, **kwargs):
    """
% calculates quantum correction on ordered moment
%
% ### Syntax
%
% `M = moment(obj,Name,Value)`
%
% ### Description
%
% `M = moment(obj,Name,Value)` calculates the spin expectation value
% including the leading quantum and thermal fluctuations ($S^{-1}$ terms).
% The magnon poulation is calculated at a given temperature $T$ integrated
% over the Brillouin zone. To calculate the numerical integral the
% Brillouin zone is sampled using Monte Carlo technique.
%
% ### Example
%
% #### Triangular lattice antiferromagnet
%
% The example calculates the spin expectation value at zero temperature on
% the triangular lattice Heisenberg antiferromagnet. The result can be
% compared with the following calculations: [A. V Chubukov, S. Sachdev,
% and T. Senthil, J. Phys. Condens. Matter 6, 8891 (1994)](http://iopscience.iop.org/article/10.1088/0953-8984/6/42/019/meta): $\langle S
% \rangle = S - 0.261$ and
% [S. J. Miyake, J. Phys. Soc. Japan 61, 983 (1992)](http://journals.jps.jp/doi/abs/10.1143/JPSJ.61.983): $\langle S \rangle = S - 0.2613 +
% 0.0055/S$ ($1/S$ is a higher order term neglected here).
%
% ```
% >>tri = sw_model('triAF',1)
% >>M = tri.moment('nRand',1e7)
% >>dS = 1-M.moment>>
% ```
%
% #### Square lattice antiferromagnet
%
% The reduced moment of the Heisenberg square lattice antiferromagnet at
% zero temperature can be compared to the published result of
% [D. A. Huse, Phys. Rev. B 37, 2380
% (1988)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.37.2380)
% $\langle S \rangle = S - 0.197$.
%
% ```
% >>sq = sw_model('squareAF',1)
% >>M = sq.moment('nRand',1e7)
% >>dS = 1-M.moment>>
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% `'nRand'`
% : The number of random $Q$ points in the Brillouin-zone,
%   default value is 1000.
%
% `'T'`
% : Temperature, default value is taken from `obj.single_ion.T` and the
%   unit is stored in [spinw.unit] with the default being K.
%
% `'tol'`
% : Tolerance of the incommensurability of the magnetic
%   propagation wavevector. Deviations from integer values of the
%   propagation vector smaller than the tolerance are
%   considered to be commensurate. Default value is $10^{-4}$.
%
% `'omega_tol'`
% : Tolerance on the energy difference of degenerate modes when
%   diagonalising the quadratic form, default value is $10^{-5}$.
%
% `'fid'`
% : Defines whether to provide text output. The default value is determined
%   by the `fid` preference stored in [swpref]. The possible values are:
%   * `0`   No text output is generated.
%   * `1`   Text output in the MATLAB Command Window.
%   * `fid` File ID provided by the `fopen` command, the output is written
%           into the opened file stream.
%
% ### Output Arguments
%
% `M`
% : structure, with the following fields:
%   * `moment`  Size of the reduced moments in a row vector with
%     $n_{magExt}$ number of elements.
%   * `T`       Temperature.
%   * `nRand`   Number of random $Q$ points.
%   * `obj`     The clone of the input `obj`.
%
% ### See Also
%
% [spinw] \| [spinw.spinwave] \| [spinw.genmagstr] \| [spinw.temperature]
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.moment(*args, **kwargs)


def copy(obj=None, **kwargs):
    """
% clones spinw object
%
% ### Syntax
%
% `newObj = copy(obj)`
%
% ### Description
%
% `newObj = copy(obj)` clones a SpinW object with all of its internal data.
% The `newObj` will be independent of the original `obj`. Since the [spinw]
% is a handle class, this command should be used to duplicate an object
% instead of the `=` operator. Using the `=` operator does not create a new
% object, but only a pointer that points to the original object:
% ```
% obj2 = obj
% ```
% Changing `obj` after the above command will also change `obj2`.
%
% ### Examples
%
% In this example $J_{1a}$ is a matrix with 1 in the diagonal, while
% $J_{1b}$ has 3.1415 in the diagonal. If `cryst` is changed, `cryst1` will
% be changed as well and viece versa, since they point to the
% same object. However `cryst2` is independent of `cryst`:
%
% ```
% >>cryst = spinw
% >>cryst.addmatrix('label','J1','value',3.1415)
% >>cryst1 = cryst
% >>cryst2 = cryst.copy
% >>cryst.addmatrix('label','J1','value',1)
% >>J1a = cryst1.matrix.mat>>
% >>J1b = cryst2.matrix.mat>>
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Output Arguments
%
% `newObj`
% : New [spinw] object that contains all the data of `obj`.
%
% ### See Also
%
% [spinw] \| [spinw.struct]
%
    """
    args = tuple(v for v in [obj] if v is not None)
    return m.copy(*args, **kwargs)


def validate(*args, **kwargs):
    """
% validates spinw object properties
%
% VALIDATE(obj, {fieldToValidate})
%
    """
    
    return m.validate(*args, **kwargs)


def matparser(obj=None, *args, **kwargs):
    """
% parses parameter vector into matrices
%
% ### Syntax
%
% `matparser(obj,Name,Value)`
%
% ### Description
%
% `matparser(obj,Name,Value)` modifies the `obj.matrix.mat` matrix,
% assigning new values from a given parmeter vector.
%
% ### Example
%
% To assign a Dzyaloshinskii-Moriya vector to the `'DM'` matrix, the
% following input would be sufficient:
%
% ```
% >>cryst = spinw
% >>cryst.addmatrix('label','DM','value',1)
% >>P = [0.2 0.35 3.14]
% >>M = {'DM' 'DM' 'DM'}
% >>S = cat(3,[0 0 0;0 0 1;0 -1 0],[0 0 -1;0 0 0;1 0 0],[0 1 0;-1 0 0;0 0 0])
% >>cryst.matparser('param',P,'mat',M,'selector',S)
% >>cryst.matrix.mat>>
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% `'param'`
% : Input row vector `P` with `nPar` elements that contains the
%   new values to be assignd to elements of `obj.matrix.mat`
%   matrix.
%
% `'mat'`
% : Identifies which matrices to be changed according to their
%   label or index. To select matrices with given labels use a
%   cell of strings with $n_{par}$ elements, for example
%   `M = {'J1','J2'}`. This will change the diagonal elements of
%   matrices $J_1$ and $J_2$ to a given value that is provided in the
%   `param` parameter vector. Alternatively the index of the matrices can
%   be given in a vector, such as `[1 2]` (index runs according
%   to the order of the previous creation of the matrices using
%   [spinw.addmatrix]).
%
%   To assign parameter value only to a selected element of a
%   $[3\times 3]$ matrix, a bracket notation can be used in any string,
%   such as `'D(3,3)'`, in this case only the $(3,3)$ element of
%   the $[3\times 3]$ matrix of `'D'` will be modified, the other elements
%   will be unchanged. To modify multiple elements of a matrix
%   at once, use the option `selector`.
%
% `'selector'`
% : Matrix with dimensions of $[3\times 3\times n_{par}]$. Each `S(:,:,i)`
%   submatrix can contain $\pm 1$ and 0. Where `S(:,:,i)` contains
%   1, the corresponding matrix elements of
%   `spinw.matrix.mat(:,:,M(i))` will be changed to the value
%   `P(i)*S(:,:,i)` where `P(i)` is the corresponding parameter
%   value.
%
% `'init'`
% : Initialize the matrices of `obj.matrix.mat` with zeros for all
%   selected labels before assigning parameter values. Default
%   is `false`.
%
% ### Output Arguments
%
% The [spinw] object will contain the modified `obj.matrix.mat` field.
%
% ### See Also
%
% [spinw] \| [spinw.horace] \| [spinw.addmatrix]
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.matparser(*args, **kwargs)


def addg(obj=None, matrixIdx=None, *args, **kwargs):
    """
% assigns g-tensor to magnetic atoms
%
% ### Syntax
%
% `addg(obj, matrixIdx, {atomTypeIdx}, {atomIdx})`
%
% ### Description
%
% `addg(obj, matrixIdx, {atomTypeIdx}, {atomIdx})` assigns the
% $[3\times 3]$ matrix selected by `matrixIdx` (using either the matrix
% label or matrix index) to the magnetic sites selected by `atomTypeIdx`
% that can contain a name of an atom or its atom index (see [spinw.atom]).
% If `atomTypeIdx` is not defined, g-tensor will be assigned to all
% magnetic atoms.
%
% ### Examples
%
% The following example will add the $g_1$ diagonal matrix to all magnetic
% atoms as anisotropic g-tensor and show the effect of a fourfold axis:
%
% ```
% >>cryst = spinw
% >>cryst.genlattice('lat_const',[4 4 3],'sym','P 4')
% >>cryst.addatom('r',[1/4 1/4 1/2],'S',1)
% >>cryst.addmatrix('label','g_1','value',diag([2 1 1]))
% >>cryst.gencoupling
% >>cryst.addg('g_1')
% >>cryst.plot('ionMode','g')
% >>snapnow
% ```
%
% ### Input Arguments
%
% `matrixIdx`
% : Either an integer, that selects the matrix
%   `obj.matrix.mat(:,:,matrixIdx)`, or a string identical to one
%   of the previously defined matrix labels, stored in
%   `obj.matrix.label`. Maximum value is $n_{mat}$.
%
% `atomTypeIdx`
% : String or cell of strings that select magnetic atoms by
%   their label. Also can be a vector that contains integers, the index of
%   the magnetic atoms in [spinw.unit_cell], this will assign the given
%   g-tensor to all symmetry equivalent atoms. Maximum value is $n_{atom}$.
%   If `atomTypeIdx` is not defined, the given g-tensor will be assigned to
%   all magnetic atoms. Optional.
%
% `atomIdx`
% : A vector that contains indices selecting some of the
%   symmetry equivalent atoms. Maximum value is the number of symmetry
%   equivalent atoms corresponding to `atomTypeIdx`. If the crystal
%   symmetry is higher than $P0$, `atomIdx` is not allowed, since the
%   g-tensor for equivalent atoms will be calculated using the symmetry
%   operators of the space group. Optional.
%
% ### Output Arguments
%
% The function adds extra entries to the `obj.single_ion.g` matrix.
%
% ### See Also
%
% [spinw] \| [spinw.addcoupling] \| [spinw.addaniso] \| [spinw.addmatrix]
%
    """
    args = tuple(v for v in [obj, matrixIdx] if v is not None) + args
    return m.addg(*args, **kwargs)


def fitspec(obj=None, *args, **kwargs):
    """
% fits experimental spin wave data
%
% ### Syntax
%
% `fitsp = fitspec(obj,Name,Value)`
%
% ### Description
% `fitsp = fitspec(obj,Name,Value)` uses a heuristic method to fit spin
% wave spectrum using a few simple rules to define the goodness (or
% R-value) of the fit:
% 1. All calculated spin wave modes that are outside of the measured
%    energy range will be omitted.
% 2. Spin wave modes that are closer to each other than the given energy
%    bin will be binned together and considered as one mode in the fit.
% 3. If the number of calculated spin wave modes after applying rule 1&2
%    is larger than the observed number, the weakes simulated modes will
%    be removed from the fit.
% 4. If the number of observed spin wave modes is larger than the observed
%    number, fake spin wave modes are added with energy equal to the
%    limits of the scan; at the upper or lower limit depending on which is
%    closer to the observed spin wave mode.
%
% After these rules the number of observed and simulated spin wave modes
% will be equal. The R-value is defined as:
%
% $R = \sqrt{ \frac{1}{n_E} \cdot \sum_{i,q} \frac{1}{\sigma_{i,q}^2}\left(E_{i,q}^{sim} - E_{i,q}^{meas}\right)^2},$
%
% where $(i,q)$ indexing the spin wave mode and momentum respectively.
% $E_{sim}$ and $E_{meas}$ are the simulated and measured spin wave
% energies, sigma is the standard deviation of the measured spin wave
% energy determined previously by fitting the inelastic peak. $n_E$ is the
% number of energies to fit.
%
% The R value is optimized using particle swarm algorithm to find the
% global minimum.
%
% ### Name-Value Pair Arguments
%
% `'func'`
% : Function to change the Hamiltonian in `obj`, it needs to have the
%   following header:
%   ```
%   obj = @func(obj, x)
%   ```
%
% `'datapath'`
% : Path to the file that stores the experimental data. For the
%   input data format see [sw_readspec].
%
% `'Evect'`
% : Column vector with $n_E$ elements that defines the energy binning of
%   the calculated dispersion. Larger binning steps solve the issue of
%   fitting unresolved modes.
%
% `'xmin'`
% : Lower limit of the optimisation parameters, optional.
%
% `'xmax'`
% : Upper limit of the optimisation parameters, optional.
%
% `'x0'`
% : Starting value of the optimisation parameters. If empty
%  or undefined, random values are used within the given limits.
%
% `'optimizer'`
% : String that determines the type of optimizer to use, possible values:
%   * `'pso'`       Particle-swarm optimizer, see [ndbase.pso],
%                   default.
%   * `'simplex'`   Matlab built-in simplex optimizer, see [fminsearch](www.mathworks.ch/help/matlab/ref/fminsearch.html).
%
% `'nRun'`
% : Number of consecutive fitting runs, each result is saved in the
%   output `fitsp.x` and `fitsp.R` arrays. If the Hamiltonian given by the
%   random `x` parameters is incompatible with the ground state,
%   those `x` values will be omitted and new random `x` values will be
%   generated instead. Default value is 1.
%
% `'nMax'`
% : Maximum number of runs, including the ones that produce error
%   (due to incompatible ground state). Default value is 1000.
%
% `'hermit'`
% : Method for matrix diagonalization, for details see [spinw.spinwave].
%
% `'epsilon'`
% : Small number that controls wether the magnetic structure is
%   incommensurate or commensurate, default value is $10^{-5}$.
%
% `'imagChk'`
% : Checks that the imaginary part of the spin wave dispersion is
%   smaller than the energy bin size.
%   If false, will not check
%   If 'penalize' will apply a penalty to iterations that yield imaginary modes
%   If true, will stop the fit if an iteration gives imaginary modes
%   Default is `penalize`.
%
% Parameters for visualizing the fit results:
%
% `'plot'`
% : If `true`, the measured dispersion is plotted together with the
%   fit. Default is `true`.
%
% `'iFact'`
% : Factor of the plotted simulated spin wave intensity (red
%   ellipsoids).
%
% `'lShift'`
% : Vertical shift of the `Q` point labels on the plot.
%
% Optimizer options:
%
% `'TolX'`
% : Minimum change of` x` when convergence reached, default
%   value is $10^{-4}$.
%
% `'TolFun'`
% : Minimum change of the R value when convergence reached,
%   default value is $10^{-5}$.
%
% `'MaxFunEvals'`
% : Maximum number of function evaluations, default value is
%   $10^7$.
%
% `'MaxIter'`
% : Maximum number of iterations for the [ndbse.pso] optimizer.
%   Default value is 20.
%
% ### Output Arguments
%
% Output `fitsp` is struct type with the following fields:
% * `obj`   Copy of the input `obj`, with the best fitted
%           Hamiltonian parameters.
% * `x`     Final values of the fitted parameters, dimensions are
%           $[n_{run}\times n_{par}]$. The rows of `x` are sorted according
%           to increasing R values.
% * `redX2` Reduced $\chi^2_\eta$ value, goodness of the fit stored in a column
%           vector with $n_{run}$ number of elements, sorted in increasing
%           order. $\chi^2_\eta$ is defined as:
%
%   $\begin{align}
%                   \chi^2_\eta &= \frac{\chi^2}{\eta},\\
%                   \eta        &= n-m+1,
%   \end{align}$
%   where \\eta is the degree of freedom, $n$ number of
%   observations and $m$ is the number of fitted parameters.
%
% * `exitflag`  Exit flag of the `fminsearch` command.
% * `output`    Output of the `fminsearch` command.
%
% {{note As a rule of thumb when the variance of the measurement error is
% known a priori, \\chi$^2_\eta$\\gg 1 indicates a poor model fit. A
% \\chi$^2_\eta$\\gg 1 indicates that the fit has not fully captured the
% data (or that the error variance has been underestimated). In principle,
% a value of \\chi$^2_\eta$= 1 indicates that the extent of the match
% between observations and estimates is in accord with the error variance.
% A \\chi$^2_\eta$ < 1 indicates that the model is 'over-fitting' the data:
% either the model is improperly fitting noise, or the error variance has
% been overestimated.}}
%
% Any other option used by [spinw.spinwave] function are also accepted.
%
% ### See Also
%
% [spinw.spinwave] \| [spinw.matparser] \| [sw_egrid] \| [sw_neutron] \| [sw_readspec]
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.fitspec(*args, **kwargs)


def optmagsteep(obj=None, *args, **kwargs):
    """
% quench optimization of magnetic structure
%
% ### Syntax
%
% `optm = optmagsteep(obj,Name,Value)`
%
% ### Description
%
% `optm = optmagsteep(obj,Name,Value)` determines the lowest energy
% magnetic configuration within a given magnetic supercell and previously
% fixed propagation (and normal) vector (see [spinw.optmagk]). It
% iteratively rotates each spin towards the local magnetic field thus
% achieving local energy minimum. Albeit not guaranteed this method often
% finds the global energy minimum. The methods works best for small
% magnetic cells and non-frustrated structures. Its execution is roughly
% equivalent to a thermal quenching from the paramagnetic state.
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% ### Name-Value Pair Arguments
%
% `'nRun'`
% : Number of iterations, default value is 100 (it is usually enough). Each
%   spin will be quenched `nRun` times or until convergence is reached.
%
% `'boundary'`
% : Boundary conditions of the magnetic cell, string with allowed values:
%   * `'free'`  Free, interactions between extedned unit cells are
%               omitted.
%   * `'per'`   Periodic, interactions between extended unit cells
%               are retained.
%
%   Default value is `{'per' 'per' 'per'}`.
%
% `'nExt'`
% : The size of the magnetic cell in number of crystal unit cells.
%   Default value is taken from `obj.mag_str.nExt`.
%
% `'fSub'`
% : Function that defines non-interacting sublattices for parallelization.
%   It has the following header:
%       `cGraph = fSub(conn,nExt)`, where `cGraph` is a row vector with
%       $n_{magExt}$ number of elements,
%   `conn` is a matrix with dimensions of $[2\times n_{conn}]$ size matrix and $n_{ext}$ is equal to
%   the `nExt` parameter. Default value is `@sw_fsub`.
%
% `'subLat'`
% : Vector that assigns all magnetic moments into non-interacting
%   sublattices, contains a single index $(1,2,3...)$ for every magnetic
%   moment in a row vector with $n_{magExt}$ number of elements. If
%   undefined, the function defined in `fSub` will be used to partition the
%   lattice.
%
% `'random'`
% : If `true` random initial spin orientations will be used (paramagnet),
%   if initial spin configuration is undefined (`obj.mag_str.F` is empty)
%   the initial configuration will be always random. Default value is
%   `false`.
%
% `'TolX'`
% : Minimum change of the magnetic moment necessary to reach convergence.
%
% `'saveAll'`
% : Save moment directions for every loop, default value is `false`.
%
% `'Hmin'`
% : Minimum field value on the spin that moves the spin. If the
%   molecular field absolute value is below this, the spin won't be
%   turned. Default is 0.
%
% `'plot'`
% : If true, the magnetic structure in plotted in real time. Default value
%   is `false`.
%
% `'pause'`
% : Time in second to pause after every optimization loop to slow down plot
%   movie. Default value is 0.
%
% `'fid'`
% : Defines whether to provide text output. The default value is determined
%   by the `fid` preference stored in [swpref]. The possible values are:
%   * `0`   No text output is generated.
%   * `1`   Text output in the MATLAB Command Window.
%   * `fid` File ID provided by the `fopen` command, the output is written
%           into the opened file stream.
%
% ### Output Arguments
%
% `optm`
% : Struct type variable with the following fields:
%   * `obj`         spinw object that contains the optimised magnetic structure.
%   * `M`           Magnetic moment directions with dimensions $[3\times n_{magExt}]$, if
%                   `saveAll` parameter is `true`, it contains the magnetic structure
%                   after every loop in a matrix with dimensions $[3\times n{magExt}\times n_{loop}]$.
%   * `dM`          The change of magnetic moment vector averaged over all moments
%                   in the last loop.
%   * `e`           Energy per spin in the optimised structure.
%   * `param`       Input parameters, stored in a struct.
%   * `nRun`        Number of loops executed.
%   * `datestart`   Starting time of the function.
%   * `dateend`     End time of the function.
%   * `title`       Title of the simulation, given in the input.
%
% ### See Also
%
% [spinw] \| [spinw.anneal] \| [sw_fsub] \| [sw_fstat]
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.optmagsteep(*args, **kwargs)


def spinwave(obj=None, hkl=None, *args, **kwargs):
    """
% calculates spin correlation function using linear spin wave theory
%
% ### Syntax
%
% `spectra = spinwave(obj,Q)`
%
% `spectra = spinwave(___,Name,Value)`
%
% ### Description
%
% `spinwave(obj,Q,Name,Value)` calculates spin wave dispersion and
% spin-spin correlation function at the reciprocal space points $Q$. The
% function can solve any single-k magnetic structure exactly and any
% multi-k magnetic structure appoximately and quadratic spinw-spin
% interactions as well as single ion anisotropy and magnetic field.
% Biquadratic exchange interactions are also implemented, however only for
% $k_m=0$ magnetic structures.
%
% If the magnetic ordering wavevector is non-integer, the dispersion is
% calculated using a coordinate system rotating from unit cell to unit
% cell. In this case the spin Hamiltonian has to fulfill this extra
% rotational symmetry which is not checked programatically.
%
% Some of the code of the function can run faster if mex files are used. To
% switch on mex files, use the `swpref.setpref('usemex',true)` command. For
% details see the [sw_mex] and [swpref.setpref] functions.
%
% ### Examples
%
% To calculate and plot the spin wave dispersion of the
% triangular lattice antiferromagnet ($S=1$, $J=1$) along the $(h,h,0)$
% direction in reciprocal space we create the built in triangular lattice
% model using `sw_model`.
%
% ```
% >>tri = sw_model('triAF',1)
% >>spec = tri.spinwave({[0 0 0] [1 1 0]})
% >>sw_plotspec(spec)
% >>snapnow
% ```
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% `Q`
% : Defines the $Q$ points where the spectra is calculated, in reciprocal
%   lattice units, size is $[3\times n_{Q}]$. $Q$ can be also defined by
%   several linear scan in reciprocal space. In this case `Q` is cell type,
%   where each element of the cell defines a point in $Q$ space. Linear scans
%   are assumed between consecutive points. Also the number of $Q$ points can
%   be specified as a last element, it is 100 by defaults.
%
%   For example to define a scan along $(h,0,0)$ from $h=0$ to $h=1$ using
%   200 $Q$ points the following input should be used:
%   ```
%   Q = {[0 0 0] [1 0 0]  200}
%   ```
%
%   For symbolic calculation at a general reciprocal space point use `sym`
%   type input.
%
%   For example to calculate the spectrum along $(h,0,0)$ use:
%   ```
%   Q = [sym('h') 0 0]
%   ```
%   To calculate spectrum at a specific $Q$ point symbolically, e.g. at
%   $(0,1,0)$ use:
%   ```
%   Q = sym([0 1 0])
%   ```
%
% ### Name-Value Pair Arguments
%
% `'formfact'`
% : If true, the magnetic form factor is included in the spin-spin
%   correlation function calculation. The form factor coefficients are
%   stored in `obj.unit_cell.ff(1,:,atomIndex)`. Default value is `false`.
%
% `'formfactfun'`
% : Function that calculates the magnetic form factor for given $Q$ value.
%   value. Default value is `@sw_mff`, that uses a tabulated coefficients
%   for the form factor calculation. For anisotropic form factors a user
%   defined function can be written that has the following header:
%   ```
%   F = formfactfun(atomLabel,Q)
%   ```
%   where the parameters are:
%   * `F`           row vector containing the form factor for every input
%                   $Q$ value
%   * `atomLabel`   string, label of the selected magnetic atom
%   * `Q`           matrix with dimensions of $[3\times n_Q]$, where each
%                   column contains a $Q$ vector in $\\ang^{-1}$ units.
%
% `'cmplxBase'`
% : If `true`, we use a local coordinate system fixed by the
%   complex magnetisation vectors:
%   $\begin{align}  e_1 &= \Im(\hat{M})\\
%                   e_3 &= Re(\hat{M})\\
%                   e_2 &= e_3\times e_1
%    \end{align}$
%   If `false`, we use a coordinate system fixed to the moments:
%   $\begin{align}  e_3 \parallel S_i\\
%                   e_2 &= \S_i \times [1, 0, 0]\\
%                   e_1 &= e_2 \times e_3
%   \end{align}$
%   Except if $S_i \parallel [1, 0, 0], e_2 = [0, 0, 1]$. The default is
%  `false`.
%
% `'gtensor'`
% : If true, the g-tensor will be included in the spin-spin correlation
%   function. Including anisotropic g-tensor or different
%   g-tensor for different ions is only possible here. Including a simple
%   isotropic g-tensor is possible afterwards using the [sw_instrument]
%   function.
%
% `'neutron_output'`
% : If `true`, will output only `Sperp`, the S(q,w) component perpendicular
%   to Q that is measured by neutron scattering, and will *not* output the
%   full Sab tensor. (Usually sw_neutron is used to calculate `Sperp`.)
%   Default value is `false`.
%
% `'fitmode'`
% : If `true`, function is optimized for multiple consecutive calls (e.g.
%   the output spectrum won't contain the copy of `obj`), default is
%   `false`.
%
% `'fastmode'`
% : If `true`, will set `'neutron_output', true`, `'fitmode', true`,
%   `'sortMode', false`, and will only output intensity for positive energy
%   (neutron energy loss) modes. Default value is `false`.
%
% `'notwin'`
% : If `true`, the spectra of the twins won't be calculated. Default is
%   `false`.
%
% `'sortMode'`
% : If `true`, the spin wave modes will be sorted by continuity. Default is
%   `true`.
%
% `'optmem'`
% : Parameter to optimise memory usage. The list of Q values will be cut
%   into `optmem` number of pieces and will be calculated piece by piece to
%   decrease peak memory usage. Default value is 0, when the number
%   of slices are determined automatically from the available free memory.
%
% `'tol'`
% : Tolerance of the incommensurability of the magnetic ordering wavevector.
%   Deviations from integer values of the ordering wavevector smaller than
%   the tolerance are considered to be commensurate. Default value is
%   $10^{-4}$.
%
% `'omega_tol'`
% : Tolerance on the energy difference of degenerate modes when
%   diagonalising the quadratic form, default value is $10^{-5}$.
%
% `'hermit'`
% : Method for matrix diagonalization with the following logical values:
%
%   * `true`    using Colpa's method (for details see [J.H.P. Colpa, Physica 93A (1978) 327](http://www.sciencedirect.com/science/article/pii/0378437178901607)),
%               the dynamical matrix is converted into another Hermitian
%               matrix, that will give the real eigenvalues.
%   * `false`   using the standard method (for details see [R.M. White, PR 139 (1965) A450](https://journals.aps.org/pr/abstract/10.1103/PhysRev.139.A450))
%               the non-Hermitian $\mathcal{g}\times \mathcal{H}$ matrix
%               will be diagonalised, which is computationally less
%               efficient. Default value is `true`.
%
% {{note Always use Colpa's method, except when imaginary eigenvalues are
%   expected. In this case only White's method work. The solution in this
%   case is wrong, however by examining the eigenvalues it can give a hint
%   where the problem is.}}
%
% `'saveH'`
% : If true, the quadratic form of the Hamiltonian is also saved in the
%   output. Be carefull, it can take up lots of memory. Default value is
%   `false`.
%
% `'saveV'`
% : If true, the matrices that transform the normal magnon modes into the
%   magnon modes localized on the spins are also saved into the output. Be
%   carefull, it can take up lots of memory. Default value is `false`.
%
% `'saveSabp'`
% : If true, the dynamical structure factor in the rotating frame
%   $S'(k,\omega)$ is saved. For incommensurate structures only. Default
%   value is `false`.
%
% `'title'`
% : Gives a title string to the simulation that is saved in the output.
%
% `'fid'`
% : Defines whether to provide text output. The default value is determined
%   by the `fid` preference stored in [swpref]. The possible values are:
%   * `0`   No text output is generated.
%   * `1`   Text output in the MATLAB Command Window.
%   * `fid` File ID provided by the `fopen` command, the output is written
%           into the opened file stream.
%
% `'tid'`
% : Determines if the elapsed and required time for the calculation is
%   displayed. The default value is determined by the `tid` preference
%   stored in [swpref]. The following values are allowed (for more details
%   see [sw_timeit]):
%   * `0` No timing is executed.
%   * `1` Display the timing in the Command Window.
%   * `2` Show the timing in a separat pup-up window.
%
% ### Output Arguments
%
% `spectra`
% : structure, with the following fields:
%   * `omega`   Calculated spin wave dispersion with dimensions of
%               $[n_{mode}\times n_{Q}]$.
%   * `Sab`     Dynamical structure factor with dimensins of
%               $[3\times 3\times n_{mode}\times n_{Q}]$. Each
%               `(:,:,i,j)` submatrix contains the 9 correlation functions
%               $S^{xx}$, $S^{xy}$, $S^{xz}$, etc. If given, magnetic form
%               factor is included. Intensity is in \\hbar units, normalized
%               to the crystallographic unit cell.
%   * `Sperp`   The component of `Sab` perpendicular to $Q$, which neutron
%               scattering measures. This is outputed *instead* of `Sab`
%               if the `'neutron_output', true` is specified.
%   * `H`       Quadratic form of the Hamiltonian. Only saved if `saveH` is
%               true.
%   * `V`       Transformation matrix from the normal magnon modes to the
%               magnons localized on spins using the following:
%               $x_i = \sum_j V_{ij} \times x_j'$
%               Only saved if `saveV` is true.
%   * `Sabp`    Dynamical structure factor in the rotating frame,
%               dimensions are $[3\times 3\times n_{mode}\times n_{Q}]$,
%               but the number of modes are equal to twice the number of
%               magnetic atoms.
%   * `hkl`     Contains the input $Q$ values, dimensions are $[3\times n_{Q}]$.
%   * `hklA`    Same $Q$ values, but in $\\ang^{-1}$ unit, in the
%               lab coordinate system, dimensins are $[3\times n_{Q}]$.
%   * `formfact`Logical value, whether the form factor has been included in
%               the spin-spin correlation function.
%   * `incomm`  Logical value, tells whether the calculated spectra is
%               incommensurate or not.
%   * `helical` Logical value, whether the magnetic structure is a helix
%               i.e. whether 2*k is non-integer.
%   * `norm`    Logical value, is always false.
%   * `nformula`Number of formula units in the unit cell that have been
%               used to scale Sab, as given in spinw.unit.nformula.
%   * `param`   Struct containing input parameters, each corresponds to the
%               input parameter of the same name:
%               * `notwin`
%               * `sortMode`
%               * `tol`
%               * `omega_tol`
%               * `hermit`
%   * `title`   Character array, the title for the output spinwave, default
%               is 'Numerical LSWT spectrum'
%   * `gtensor` Logical value, whether a g-tensor has been included in the
%               calculation.
%   * `obj`     The copy (clone) of the input `obj`, see [spinw.copy].
%   * `datestart`Character array, start date and time of the calculation
%   * `dateend` Character array, end date and time of the calculation
%
% The number of magnetic modes (labeled by `nMode`) for commensurate
% structures is double the number of magnetic atoms in the magnetic cell.
% For incommensurate structures this number is tripled due to the
% appearance of the $(Q\pm k_m)$ Fourier components in the correlation
% functions. For every $Q$ points in the following order:
% $(Q-k_m,Q,Q+k_m)$.
%
% If several twins exist in the sample, `omega` and `Sab` are packaged into
% a cell, that contains $n_{twin}$ number of matrices.
%
% ### See Also
%
% [spinw] \| [spinw.spinwavesym] \| [sw_mex] \| [spinw.powspec] \| [sortmode]
%
    """
    args = tuple(v for v in [obj, hkl] if v is not None) + args
    return m.spinwave(*args, **kwargs)


def version(obj=None, **kwargs):
    """
% returns the version of SpinW
%
% ### Syntax
%
% `verInfo = version(obj)`
%
    """
    args = tuple(v for v in [obj] if v is not None)
    return m.version(*args, **kwargs)


def datastruct(**kwargs):
    """
% DATASTRUCT defines the data structure used in spinw object It defines the
% data structure with initial values all are necessary for valid data
% structure.
%
    """
    args = []
    return m.datastruct(*args, **kwargs)


def vararginnames(*args, **kwargs):
    """
% Given varargin, returns a list of the given
% argument names (so we know which arguments a user has passed to a function).
% Note that inputs to SpinW functions can either be name-value pairs or a
% struct
%
% Input:
%
% varargin    Variable-length argument list (name value pairs) or struct
    """
    
    return m.vararginnames(*args, **kwargs)


def softparamcheck(params_to_check=None, func_name=None, param=None, *args, **kwargs):
    """
% Checks if any parameters have been provided in varargin, but set to
% empty, and raises an error if so. This function is needed because by
% default 'soft' params will silently be set to empty if their shape is
% incorrect, causing unexpected behaviour for users.
%
% Input:
%
% params_to_check    A list of strings of the parameters to check e.g.
%                    ["S", "k"]
% func_name          The name of the function this is being called from
%                    to be used in the error identifier text
% param              The output of sw_readparam. If an argument exists in
%                    varargin, but has been set to empty in param, we know
%                    it has been silently ignored so raise an error
% varargin           Varargin that was used as input to sw_readparam to
%                    create param, this should be name-value pairs or a
%                    struct
%
    """
    args = tuple(v for v in [params_to_check, func_name, param] if v is not None) + args
    return m.softparamcheck(*args, **kwargs)


def initfield(obj=None, *args, **kwargs):
    """
% initializes all subfields of the obj structure to the default values
%
% SPINW.INITFIELD(objS, {field})
%
% Input:
%
% objS      Structure to initialize.
% field     String or cell of strings that contains specific fields to
%           initialize.
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.initfield(*args, **kwargs)


def export(obj=None, location=None, **kwargs):
    """
% saves swpref object into a file
%
% ### Syntax
%
% `success = export(obj,location)`
%
% `success = export(obj)`
%
% ### Description
%
% `success = export(obj,location)` writes the preferences given in `obj` to
% a file location given by `location`. The file is in a basic `.json`
% format.
%
% `success = export(obj)` writes the preferences given in `obj` to
% the users home folder as `swprefs.json`. The file is in a basic `.json`
% format.
%
% ### See Also
%
% [swpref.import]
%
    """
    args = tuple(v for v in [obj, location] if v is not None)
    return m.export(*args, **kwargs)


def import_(obj=None, location=None, **kwargs):
    """
% imports swpref object from file
%
% ### Syntax
%
%
% `obj = import(obj)`
%
% `obj = import(obj,location)`
%
% ### Description
%
% `obj = import(obj)` loads the preferences given in by the file
% `swprefs.json` in the users home folder. It sets the preferences and
% returns a new preference object.
%
% `obj = import(obj,location)` loads the preferences given in by the file
% specified by `location`, sets the preferences and returns a new
% preference object.
%
% ### See Also
%
% [swpref.export]
%
    """
    args = tuple(v for v in [obj, location] if v is not None)
    return m.import_(*args, **kwargs)


def datastruct(**kwargs):
    """
% Function called to create a default preference object.
%
%  {{warning Internal function for the Spin preferences.}}
%
% ### Syntax
%
% 'prefs = datastruct()'
%
% ### Description
%
% 'prefs = datastruct()' creates a structure with the following fields:
%
% 'Name' a cell array giving the name of each dynamic property.
%
% 'Validation' a cell array with functions to evaluate when a
% property is set.
%
% 'Value' a cell array giving the default value of a dynamic property
%
% 'Label' a cell array giving a short description on the dynamic
% property.
%
    """
    args = []
    return m.datastruct(*args, **kwargs)


def importcif(_=None, dataStr=None, **kwargs):
    """
% imports .cif data from file, web or string
    """
    args = tuple(v for v in [dataStr] if v is not None)
    return m.importcif(*args, **kwargs)


def symbol(sName=None, noError=None, **kwargs):
    """
% returns the character corresponding to the given symbol name
%
% S = SYMBOL(sName)
%
% Input:
%
% sName     String, name of the symbol. For example: 'alpha', 'Angstrom',
%           etc. The input is case sensitive. Alternatively it can be a
%           text that contains name of symbols with \\ before them, for
%           example: "The length of the bond is 3.2 \\a.".
%
% Output:
%
% S         A char type variable containing the symbol.
%
    """
    args = tuple(v for v in [sName, noError] if v is not None)
    return m.symbol(*args, **kwargs)


def sumsym(A=None, *args, **kwargs):
    """
% sums up matrices containing symbolic variables
%
% sumA = SUMSYM(A,dim)
%
% The function sums up matrices containing symbolic variables in arbitrary
% dimensions, for any other input type it calls the standard sum function.
%
% See also sym, syms.
%
    """
    args = tuple(v for v in [A] if v is not None) + args
    return m.sumsym(*args, **kwargs)


def makecolormap(*args, **kwargs):
    """
%% MAKECOLORMAP makes smoothly varying colormaps
% a = makeColorMap(beginColor, middleColor, endColor, numSteps);
% a = makeColorMap(beginColor, endColor, numSteps);
% a = makeColorMap(beginColor, middleColor, endColor);
% a = makeColorMap(beginColor, endColor);
%
% all colors are specified as RGB triples
% numSteps is a scalar saying howmany points are in the colormap
%
% Examples:
%
% peaks;
% a = makeColorMap([1 0 0],[1 1 1],[0 0 1],40);
% colormap(a)
% colorbar
%
% peaks;
% a = makeColorMap([1 0 0],[0 0 1],40);
% colormap(a)
% colorbar
%
% peaks;
% a = makeColorMap([1 0 0],[1 1 1],[0 0 1]);
% colormap(a)
% colorbar
%
% peaks;
% a = makeColorMap([1 0 0],[0 0 1]);
% colormap(a)
% colorbar
%
% Reference:
% A. Light & P.J. Bartlein, "The End of the Rainbow? Color Schemes for
% Improved Data Graphics," Eos,Vol. 85, No. 40, 5 October 2004.
% http://geography.uoregon.edu/datagraphics/EOS/Light&Bartlein_EOS2004.pdf
%
    """
    
    return m.makecolormap(*args, **kwargs)


def gcdv(v=None, **kwargs):
    """
% calculates the greates common divisor of a set of numbers
%
% G = VECGCD(V)
%
% is the greatest common divisor of the elements of the integer vector V. V
% must be a row or a column vector of integers. We define gcd([]) = 1 and
% gcd([0 0 ... 0]) = 0.
%
    """
    args = tuple(v for v in [v] if v is not None)
    return m.gcdv(*args, **kwargs)


def grabxy(fName=None, ax=None, logax=None, **kwargs):
    """
% reads coordinates from raster image or image on the clipboard
%
% pts = GRABXY(fName, ax, {logax})
%
% Input:
%
% fName         String, path to the image file. If empty, the image is read
%               from the clipboard.
% ax            (x,y) coordinates of the three axis points, with dimensions
%               of 2x3. If ax is omitted or empty, GRABXY just shows the
%               image.
% logax         Optional input string, cn be used if the axis is in
%               logaritmic units, possible options:
%                   'logx'
%                   'logy'
%                   'logxy'
%
% Output:
%
% pts           Matrix, where the first row are the x coordinates the
%               second row is the y coordinates.
%
% How to use the function?
%
% You need an image where you know the coordinates of three points. These
% coordinates has to be given as the ax input to the grabxy() function.
% After calling the function, it shows the image file and the first three
% mouse clicks on the figure will determine the position of the three
% predefined points (shown as red circles) given in ax. Any other click
% afterwards will grab coordinates (shown as green circles). The coordinates
% of the green circles will be returned. If you don't want to grab more
% points, just right click anywhere on the figure.
%
    """
    args = tuple(v for v in [fName, ax, logax] if v is not None)
    return m.grabxy(*args, **kwargs)


def tensordot(A=None, B=None, dim1=None, dim2=None, **kwargs):
    """
% Tensor product of arbitrary dimensional matrices.
%
% C = tensorprod(A,B,dimA,{dimB})
%
% Input:
% A, B      Multidimensional input arrays.
% dim       Contains two number, that selects two dimensions.
%
% The multiplication is a standard matrix multiplication. The two matrices
% are selected by dim:
%   AB = A(... dim(1) ... dim(2) ...) * B(... dim(1) ... dim(2) ...)
% The necessary condition that the multiplication can be performed:
%   size(A,dim(2)) = size(B,dim(1))
%
% Singleton dimensions in both A and B matrices are supported.
%
% The default value for dim is dim = [1 2].
%
% Examples:
% For 2D matrices mmat is identical to the Matlab built-in multiplication:
% A = [1 2 3 4];
% B = [1;2;3;4];
% C = mmat(A,B)
%
% C will be 30.
%
% For multidimensional arrays:
% A = repmat([1 2 3 4],[1 1 5]);
% B = [1 2 3 4]';
% C = mmat(A,B)
% C will be an array with dimensions of 1x1x5 and every element is 30.
%
    """
    args = tuple(v for v in [A, B, dim1, dim2] if v is not None)
    return m.tensordot(*args, **kwargs)


def changem(A=None, newval=None, oldval=None, **kwargs):
    """
% vectorized version of changem
%
% B = CHANGEM(A,newval,oldval)
%
% The function changes the old values in A to the new values pair wise.
%
    """
    args = tuple(v for v in [A, newval, oldval] if v is not None)
    return m.changem(*args, **kwargs)


def sw_fminsearchbnd(fun=None, x0=None, LB=None, UB=None, options=None, *args, **kwargs):
    """
% FMINSEARCHBND: FMINSEARCH, but with bound constraints by transformation
% usage: x=FMINSEARCHBND(fun,x0)
% usage: x=FMINSEARCHBND(fun,x0,LB)
% usage: x=FMINSEARCHBND(fun,x0,LB,UB)
% usage: x=FMINSEARCHBND(fun,x0,LB,UB,options)
% usage: x=FMINSEARCHBND(fun,x0,LB,UB,options,p1,p2,...)
% usage: [x,fval,exitflag,output]=FMINSEARCHBND(fun,x0,...)
%
% arguments:
%  fun, x0, options - see the help for FMINSEARCH
%
%  LB - lower bound vector or array, must be the same size as x0
%
%       If no lower bounds exist for one of the variables, then
%       supply -inf for that variable.
%
%       If no lower bounds at all, then LB may be left empty.
%
%       Variables may be fixed in value by setting the corresponding
%       lower and upper bounds to exactly the same value.
%
%  UB - upper bound vector or array, must be the same size as x0
%
%       If no upper bounds exist for one of the variables, then
%       supply +inf for that variable.
%
%       If no upper bounds at all, then UB may be left empty.
%
%       Variables may be fixed in value by setting the corresponding
%       lower and upper bounds to exactly the same value.
%
% Notes:
%
%  If options is supplied, then TolX will apply to the transformed
%  variables. All other FMINSEARCH parameters should be unaffected.
%
%  Variables which are constrained by both a lower and an upper
%  bound will use a sin transformation. Those constrained by
%  only a lower or an upper bound will use a quadratic
%  transformation, and unconstrained variables will be left alone.
%
%  Variables may be fixed by setting their respective bounds equal.
%  In this case, the problem will be reduced in size for FMINSEARCH.
%
%  The bounds are inclusive inequalities, which admit the
%  boundary values themselves, but will not permit ANY function
%  evaluations outside the bounds. These constraints are strictly
%  followed.
%
%  If your problem has an EXCLUSIVE (strict) constraint which will
%  not admit evaluation at the bound itself, then you must provide
%  a slightly offset bound. An example of this is a function which
%  contains the log of one of its parameters. If you constrain the
%  variable to have a lower bound of zero, then FMINSEARCHBND may
%  try to evaluate the function exactly at zero.
%
%
% Example usage:
% rosen = @(x) (1-x(1)).^2 + 105*(x(2)-x(1).^2).^2;
%
% fminsearch(rosen,[3 3])     % unconstrained
% ans =
%    1.0000    1.0000
%
% fminsearchbnd(rosen,[3 3],[2 2],[])     % constrained
% ans =
%    2.0000    4.0000
%
% See test_main.m for other examples of use.
%
%
% See also: fminsearch, fminspleas
%
%
% Author: John D'Errico
% E-mail: woodchips@rochester.rr.com
% Release: 4
% Release date: 7/23/06
    """
    args = tuple(v for v in [fun, x0, LB, UB, options] if v is not None) + args
    return m.sw_fminsearchbnd(*args, **kwargs)


def bsxfunsym(op=None, A=None, B=None, **kwargs):
    """
% C = BSXFUNSYM(@op,A,B) extends the bsxfun to sym class variables, for any
% other input type it calls the standrd bsxfun function.
%
% See also sym, syms.
%
    """
    args = tuple(v for v in [op, A, B] if v is not None)
    return m.bsxfunsym(*args, **kwargs)


def pmat(M=None, dims=None, pVal=None, **kwargs):
    """
% pads matrix to the required dimensions with a given value
%
% Mpad = PMAT(M,dims,{pVal})
%
% The output M is padded with zeros or the value given by pVal. If dims
% define a smaller dimension than the input matrix, the matrix gets cutted.
%
% Input:
%
% M         Input matrix with arbitrary dimensions.
% dims      Row vector, gives the dimensions of the output matrix.
% pVal      Value that is used for padding, default is 0.
%
% Output:
%
% Mpad      Output matrix with the padded values.
%
    """
    args = tuple(v for v in [M, dims, pVal] if v is not None)
    return m.pmat(*args, **kwargs)


def sortmode(Dseq=None, Vseq=None, deg=None, **kwargs):
    """
% sort eigenvalues and eigenvectors
%
% ### Syntax
%
% `[Dseq,Vseq] = sortmode(Dseq,Vseq)`
%
% `[Dseq,Vseq] = sortmode(___,deg)`
%
% ### Description
%
% `[Dseq,Vseq] = sortmode(Dseq,Vseq)` sorts the eigenvalues and
% eigenvectors stored in `Dseq` and `Vseq` matrices. The code tries to find
% continuous dispersion lines first based on smoothness (by fitting
% dispersion up to 4th degree polynomial) and at the crossing points of
% multiple dispersion lines it tries to minimize the variation of the
% eigenvectors.
%
% {{note If the dispersion is extensively degenerate, the modes are sorted
% only according to the smoothness of the dispersion.}}
%
% {{warning The code assumes that the input dispersion matrix is sorted in
% energy.}}
%
% `[Dseq,Vseq] = sortmode(___,deg)` control wether the spectrum is
% extensively degenerate or not by setting `deg` `true` or `false`
% respectively.
%
% ### Input Arguments
%
% `Desq`
% : Dispersion stored in a matrix with dimensions of $[n_{mode}\times
%   n_{point}]$.
%
% `Vseq`
% : Eigenvectors or any other value corresponding to the eigenvalues stored
%   in matrix with dimensions of $[n_{vec}\times n_{mode}\times
%   n_{point}]$, where $v_{vec}=n_{mode}$ if `Vseq` stores the
%   eigenvectors, otherwise it can be of arbitrary size.
%
% ### Output Arguments
%
% `Dseq`, `Vseq`
% : Same as the input matrices except that they are sorted along the
%   $n_{mode}$ dimension.
%
    """
    args = tuple(v for v in [Dseq, Vseq, deg] if v is not None)
    return m.sortmode(*args, **kwargs)


def tensordotWM(tensor1=None, ind1=None, legdimensions1=None, tensor2=None, ind2=None, legdimensions2=None, **kwargs):
    """
%TENSORDOT Summary of this function goes here
%   Detailed explanation goes here
    """
    args = tuple(v for v in [tensor1, ind1, legdimensions1, tensor2, ind2, legdimensions2] if v is not None)
    return m.tensordotWM(*args, **kwargs)


def gobjects0(*args, **kwargs):
    """
% use double insted of graphics handle class for Matlab prior 8.1
    """
    
    return m.gobjects0(*args, **kwargs)


def eigorth(M=None, tol=None, useMex=None, **kwargs):
    """
% orthogonal eigenvectors of defective eigenvalues
%
% [V, D, {Idx}] = EIGORTH(M, tol, useMex)
%
% Input:
%
% M         Stack of square matrices, dimensions are [nMat nMat nStack].
% tol       Tolerance, within two eigenvalue are regarded equal:
%               abs(real(diff(D))) < max([real(D) 1e-5])*tol
%           Default is 1e-5.
% useMex    If true a mex file will be used to speed up the calculation.
%           Default is false.
%
% Output:
%
% V         Matrix stack, every column contains an eigenvector of M in
%           every stack, dimensions are the same as M.
% D         Stack of vectors, that contains the eigenvalues of M,
%           dimensions are [nMat nStack].
% idx       Permutation indices of the eigenvalues and eigenvectors for
%           every stack, dimensions are [nMat nStack].
%
% See also eig, sortmode.
%
    """
    args = tuple(v for v in [M, tol, useMex] if v is not None)
    return m.eigorth(*args, **kwargs)


def ksearch(obj=None, k=None, N=None, kR=None, kD=None, **kwargs):
    """
% search for best magnetic k-vector
%
% [km, R2] = KSEARCH(obj, km, Ngrid, kmRange, kmNum)
%
% Input:
%
% abc   Vector defining the crystal lattice with the following numbers:
%           [a b c alpha beta gamma], angles are in degree. If the crystal
%           is defined in SpinW, just use the obj.abc command.
% km    List of magnetic Bragg peak positions in A-1.
% Ngrid Vector with 3 numbers or scalar, the number of reciprocal lattice
%       points along H, K and L to test. If a single number is given, the
%       same number of points will be tested along all three dimensions.
%       The HKL grid will be: -Ngrid:Ngrid.
% kmRange   Either a vector with 3 elements or a scalar, defines the range
%       of magnetic ordering wave vectors to be tested. For example:
%           kmRange = 0.3, then ordering wave vectors will be search
%           between 0 and 0.3.
% kmNum The number of ordering wave vectors between 0 and kmRange.
%
% Output:
%
% km    Matrix with dimensions 10x3, returns the best 10 magnetic ordering
%       wave vectors.
% R2    Column vector containing the R^2 values for the best 10 fits.
%
    """
    args = tuple(v for v in [obj, k, N, kR, kD] if v is not None)
    return m.ksearch(*args, **kwargs)


def iindex(x=None, *args, **kwargs):
    """
% inline indexing using parenthesis or braces
    """
    args = tuple(v for v in [x] if v is not None) + args
    return m.iindex(*args, **kwargs)


def munkres(costMat=None, **kwargs):
    """
% MUNKRES   Munkres (Hungarian) Algorithm for Linear Assignment Problem.
%
% [ASSIGN,COST] = munkres(COSTMAT) returns the optimal column indices,
% ASSIGN assigned to each row and the minimum COST based on the assignment
% problem represented by the COSTMAT, where the (i,j)th element represents the cost to assign the jth
% job to the ith worker.
%
    """
    args = tuple(v for v in [costMat] if v is not None)
    return m.munkres(*args, **kwargs)


def clipboardimage(**kwargs):
    """
% returns the RGB image from clipboard
%
% rgbData = CLIPBOARDIMAGE()
%
% The function at the moment works with print screen images on OXS and
% Windows.
%
% Output:
%
% rgbData   Matrix with dimensions W x H x 3, containing the RGB values
%           from the clipboard. Empty matrix if the clipboard doesn't
%           contain image data.
%
% Example:
%
% figure
% imshow(clipboardimage)
%
    """
    args = []
    return m.clipboardimage(*args, **kwargs)


def mmat(A=None, B=None, dim=None, **kwargs):
    """
% Simple matrix multiplication of multidimensional arrays.
%
% Input:
% A, B      Multidimensional input arrays.
% dim       Contains two number, that selects two dimensions.
%
% The multiplication is a standard matrix multiplication. The two matrices
% are selected by dim:
%   AB = A(... dim(1) ... dim(2) ...) * B(... dim(1) ... dim(2) ...)
% The necessary condition that the multiplication can be performed:
%   size(A,dim(2)) = size(B,dim(1))
%
% Singleton dimensions in both A and B matrices are supported.
%
% The default value for dim is dim = [1 2].
%
% Examples:
% For 2D matrices mmat is identical to the Matlab built-in multiplication:
% A = [1 2 3 4];
% B = [1;2;3;4];
% C = mmat(A,B)
%
% C will be 30.
%
% For multidimensional arrays:
% A = repmat([1 2 3 4],[1 1 5]);
% B = [1 2 3 4]';
% C = mmat(A,B)
% C will be an array with dimensions of 1x1x5 and every element is 30.
%
    """
    args = tuple(v for v in [A, B, dim] if v is not None)
    return m.mmat(*args, **kwargs)


def fprintf0(fid=None, *args, **kwargs):
    """
% same as fprintf, expect if fid is zero, will not produce output.
    """
    args = tuple(v for v in [fid] if v is not None) + args
    return m.fprintf0(*args, **kwargs)


def strsplit0(s=None, delimiter=None, **kwargs):
    """
% splits a string into multiple terms
%
% terms = STRSPLIT(str, delimiter)
%
%   terms = strsplit(s)
%       splits the string s into multiple terms that are separated by
%       white spaces (white spaces also include tab and newline).
%
%       The extracted terms are returned in form of a cell array of
%       strings.
%
%   terms = strsplit(s, delimiter)
%       splits the string s into multiple terms that are separated by
%       the specified delimiter.
%
%   Remarks
%   -------
%       - Note that the spaces surrounding the delimiter are considered
%         part of the delimiter, and thus removed from the extracted
%         terms.
%
%       - If there are two consecutive non-whitespace delimiters, it is
%         regarded that there is an empty-string term between them.
%
%   Examples
%   --------
%       % extract the words delimited by white spaces
%       ts = strsplit('I am using MATLAB');
%       ts <- {'I', 'am', 'using', 'MATLAB'}
%
%       % split operands delimited by '+'
%       ts = strsplit('1+2+3+4', '+');
%       ts <- {'1', '2', '3', '4'}
%
%       % It still works if there are spaces surrounding the delimiter
%       ts = strsplit('1 + 2 + 3 + 4', '+');
%       ts <- {'1', '2', '3', '4'}
%
%       % Consecutive delimiters results in empty terms
%       ts = strsplit('C,Java, C++ ,, Python, MATLAB', ',');
%       ts <- {'C', 'Java', 'C++', '', 'Python', 'MATLAB'}
%
%       % When no delimiter is presented, the entire string is considered
%       % as a single term
%       ts = strsplit('YouAndMe');
%       ts <- {'YouAndMe'}
%
    """
    args = tuple(v for v in [s, delimiter] if v is not None)
    return m.strsplit0(*args, **kwargs)


def sumargs(*args, **kwargs):
    """
% sums up all arguments
    """
    
    return m.sumargs(*args, **kwargs)


def mdiagonal(A=None, dim=None, **kwargs):
    """
% Returns the diagonal elements along two selected dimensions.
%
% Input:
% A         Multidimensional input array.
% dim       Contains two number, that selects two dimensions.
%
% The diagonal is the diagonal of every A(... dim(1)...dim(2)...) matrix.
% The result is contracted along dim(2).
%
% The default value for dim is dim = [1 2].
%
% Examples:
% For 2D matrices mmat is identical to the Matlab built-in diag:
% A = [1 2; 3 4];
% C = mdiag(A)
%
% C will be [1;4].
%
% For multidimensional arrays:
% A = repmat([1 2; 3 4],[1 1 3]);
% B = mdiag(A,[1 2])
% B will be an array with dimensions of 2x3: [1 1 1;4 4 4].
%
    """
    args = tuple(v for v in [A, dim] if v is not None)
    return m.mdiagonal(*args, **kwargs)


def err2str(num0=None, err=None, **kwargs):
    """
% converts value and standard deviation into a string
%
% sOut = ERR2STR(num,{err})
%
% The result is a number with error in brackets in the end. All standard
% deviation is given with the 2 leading digits if the 2 leading digits of
% the standard deviation is smaller than 20. Otherwise the first leading
% digit of the s.d. is given. Function also removes trailing zero to
% improve the quality of the string.
%
% Input:
%
% num   Single number of a 2 element vector, where the second element is
%       the standard deviation.
% err   Standard deviation. If given, this will be used instead of num(2).
%       Optional.
%
% WARNING it gives sometimes wrong results, e.g. err2str([100.1 1])
%
    """
    args = tuple(v for v in [num0, err] if v is not None)
    return m.err2str(*args, **kwargs)


def findmax(X=None, *args, **kwargs):
    """
% find the maximum valued element in a vector
%
% I = FINDMAX(X,val)
% I = FINDMAX(X,val,k)
% I = FINDMAX(X,val,k,direction)
%
% [row,col] = FINDMAX(___)
% [row,col,v] = FINDMAX(___)
%
% It has the same parameters and output as find().
%
% See also find.
    """
    args = tuple(v for v in [X] if v is not None) + args
    return m.findmax(*args, **kwargs)


def sw_cbrewer(cName=None, nCol=None, **kwargs):
    """
% creates nice colormaps based on the original cbrewer() function
%
% cMap = SW_CBREWER(colorName, nColors)
%
% This function produces nice colormaps, for more information on the colors
% please visit http://colorbrewer2.org/
%
% Input:
%
% colorName Name of the colormap in a string, for the possible names, call
%           sw_cbrewer without input and the possible colormaps will be
%           shown.
% nColors   Number of colors in the colormap. The colors will be
%           interpolated from the few predefined base colors.
%
%  This function includes color specifications and designs developed by
%  Cynthia Brewer (http://colorbrewer.org/).
%
    """
    args = tuple(v for v in [cName, nCol] if v is not None)
    return m.sw_cbrewer(*args, **kwargs)


def uiopen(type=None, direct=None, **kwargs):
    """
% Overloaded UIOPEN to enable drag&drop for .cif files via SpinW and to
% show images in Matlab.
%
%You can drag&drop .cif files into the Matlab Command Window and
%they will be plotted automatically. For any other input, the function
%calls the original Matlab function, see it's help below.
%
%UIOPEN Present file selection dialog with appropriate file filters.
%
%   UIOPEN presents a file selection dialog.  The user can either choose a
%   file to open or click cancel.  No further action is taken if the user
%   clicks on cancel.  Otherwise the OPEN command is evaluated in the base
%   workspace with the user specified filename.
%
%   These are the file filters presented using UIOPEN.
%
%   1st input argument   Filter List
%   <no input args>      *.m, *.fig, *.mat,
%                        *.mdl, *.slx  (if Simulink is installed),
%                        *.cdr         (if Stateflow is installed),
%                        *.rtw, *.tmf, *.tlc, *.c, *.h, *.ads, *.adb
%                                      (if Simulink Coder is installed),
%                        *.*
%   MATLAB               *.m, *.fig, *.*
%   LOAD                 *.mat, *.*
%   FIGURE               *.fig, *.*
%   SIMULINK             *.mdl, *.slx, *.*
%   EDITOR               *.m, *.mdl, *.cdr, *.rtw, *.tmf, *.tlc, *.c, *.h, *.ads, *.adb, *.*
%
%   If the first input argument is unrecognized, it is treated as a file
%   filter and passed directly to the UIGETFILE command.
%
%   If the second input argument is true, the first input argument is
%   treated as a filename.
%
%   Examples:
%       uiopen % displays the dialog with the file filter set to all MATLAB
%              %files.
%
%       uiopen('matlab') %displays the dialog with the file
%                         %filter set to all MATLAB files.
%
%       uiopen('load') %displays the dialog with the file filter set to
%                      %MAT-files (*.mat).
%
%       uiopen('figure') %displays the dialog with the file filter set to
%                        %figure files (*.fig).
%
%       uiopen('simulink') %displays the dialog with the file filter set to
%                          %model files (*.mdl,*.slx).
%
%       uiopen('editor') %displays the dialog with the file filter set to
%                        %"All MATLAB files". This filters out binary
%                        %formats: .mat, .fig, .slx.
%                        %All files are opened in the MATLAB Editor.
%
%   See also UIGETFILE, UIPUTFILE, OPEN, UIIMPORT.
    """
    args = tuple(v for v in [type, direct] if v is not None)
    return m.uiopen(*args, **kwargs)


def findmin(X=None, *args, **kwargs):
    """
% find the minimum valued element in a vector
%
% I = FINDMIN(X,val)
% I = FINDMIN(X,val,k)
% I = FINDMIN(X,val,k,direction)
%
% [row,col] = FINDMIN(___)
% [row,col,v] = FINDMIN(___)
%
% It has the same parameters and output as find().
%
% See also find.
    """
    args = tuple(v for v in [X] if v is not None) + args
    return m.findmin(*args, **kwargs)


def findval(X=None, val=None, *args, **kwargs):
    """
% find the an element in a vector that is closest to a given value
%
% I = FINDVAL(X,val)
% I = FINDVAL(X,val,k)
% I = FINDVAL(X,val,k,direction)
%
% [row,col] = FINDVAL(___)
% [row,col,v] = FINDVAL(___)
%
% It has the same parameters and output as find() plus the extra val value.
%
% See also find.
    """
    args = tuple(v for v in [X, val] if v is not None) + args
    return m.findval(*args, **kwargs)


def strword(str=None, idx=None, last=None, **kwargs):
    """
% extract words separated by whitespace from string
%
% out = strword(str, idx, {last})
%
% Input:
%
% str       String input.
% idx       indexes of the words to be extracted.
% last      If true, the last word is given if idx contains an element
%           larger than the word count, if flase an empty string.
%           Default is false.
%
% Output:
%
% out       Cell contains the extracted words in the order idx is give.
%
% Example:
%
% strword(' one two three four',[4 1])
% the output will be: {'four' 'one'}.
%
    """
    args = tuple(v for v in [str, idx, last] if v is not None)
    return m.strword(*args, **kwargs)


def sumn(A=None, dim=None, *args, **kwargs):
    """
% sum of array elements along multiple dimensions
%
% S = SUMN(A,dim,...)
%
% Works the same way as the Matlab built-in sum() function, but it can do
% summation along multiple dimensions with a single call.
%
% See also SUM.
%
    """
    args = tuple(v for v in [A, dim] if v is not None) + args
    return m.sumn(*args, **kwargs)


def strjoin0(input=None, separator=None, **kwargs):
    """
%STRJOIN Concatenate an array into a single string.
%
%     S = strjoin(C)
%     S = strjoin(C, separator)
%
% Description
%
% S = strjoin(C) takes an array C and returns a string S which concatenates
% array elements with comma. C can be a cell array of strings, a character
% array, a numeric array, or a logical array. If C is a matrix, it is first
% flattened to get an array and concateneted. S = strjoin(C, separator)
% also specifies separator for string concatenation. The default separator
% is whitespace: ' '.
%
% Examples
%
%     >> str = strjoin({'this','is','a','cell','array'})
%     str =
%     this is a cell array
%
%     >> str = strjoin([1,2,2],'_')
%     str =
%     1_2_2
%
%     >> str = strjoin({1,2,2,'string'},'\t')
%     str =
%     1 2 2 string
%
% Default separator modified by S.T. 30.07.2014
%
    """
    args = tuple(v for v in [input, separator] if v is not None)
    return m.strjoin0(*args, **kwargs)


def invfast(M=None, opt=None, **kwargs):
    """
% fast calculation of the matrix inverse of stacked matrices
%
% I = INVFAST(M,{opt})
%
% The function is vectorised and efficient for very large number of small
% matrices (1x1, 2x2 and 3x3). For larger matrices the code calls the
% built-in inv() function. If opt is 'diag', only the diagonal of the
% inverse matrices are calculated.
%
% Input:
%
% M         Matrix with dimensions of [D,D,N1,N2,...], where D can be
%           1, 2 or 3.
% opt       String, with possile values:
%               'full'  Calculate the inverse matrices, the output matrix
%                       will have the same dimensions as the input matrix.
%                       Default option.
%               'diag'  Calculate only the diagonal elements of the inverse
%                       matrix, the output matrix will have dimensions of
%                       [D,N1,N2,...].
%               'sum'   Calculate only the sum of the elements of the
%                       inverse matrix, the output will have dimensions of
%                       [1,N1,N2,...].
%           Default value is 'full'.
%
% Output:
%
% I         Matrix with dimensions determined by opt.
%
    """
    args = tuple(v for v in [M, opt] if v is not None)
    return m.invfast(*args, **kwargs)


def cm_inferno(nCol=None, **kwargs):
    """
% inferno colormap with added white
%
% CM_INFERNO(nCol)
%
% This is a honest colormap, unlike the Matlab default parula(). This means
% this colormap is perceptionally uniform, thus it will not emphasize any
% value on the plot. It is also compatible with black and white output. The
% colormap is copied from the Python package Matplotlib
% (https://bids.github.io/colormap/).
%
% Input:
%
% nCol      Number of colors, default value is 256.
%
    """
    args = tuple(v for v in [nCol] if v is not None)
    return m.cm_inferno(*args, **kwargs)


def cm_viridis(nCol=None, white=None, **kwargs):
    """
% viridis colormap with added white
%
% CM_VIRIDIS(nCol,{white})
%
% This is a honest colormap, unlike the Matlab default parula(). This means
% this colormap is perceptionally uniform, thus it will not emphasize any
% value on the plot. It is also compatible with black and white output. The
% colormap is copied from the Python package Matplotlib
% (https://bids.github.io/colormap).
%
% Input:
%
% nCol      Number of colors, default value is 256.
% white     String that determine if white should added to the colormap:
%               'off'       default hevaiour,
%               'top'       white is added to the end of the colormap
%               'bottom'    white is added to the beginning of the colormap
%
    """
    args = tuple(v for v in [nCol, white] if v is not None)
    return m.cm_viridis(*args, **kwargs)


def cm_tasty(n=None, method=None, **kwargs):
    """
% custom colormap with (some) tasty colors
%
% cmap = tasty({n},{method})
%
% Colormap made of black, violet, strawberry, pumpkin, royal yellow and
% white.
%
% Input:
%
% n         Number of colors, default is 121.
% method    Interpolation method, allowed values are:
%               'pchip'     Default, cubic interpolation.
%               'linear'    Linear interpolation between the given colors.
%
% Composed by Sandor Toth, 4.05.2016
%
    """
    args = tuple(v for v in [n, method] if v is not None)
    return m.cm_tasty(*args, **kwargs)


def cm_magma(nCol=None, **kwargs):
    """
% magma colormap with added white
%
% CM_MAGMA(nCol)
%
% This is a honest colormap, unlike the Matlab default parula(). This means
% this colormap is perceptionally uniform, thus it will not emphasize any
% value on the plot. It is also compatible with black and white output. The
% colormap is copied from the Python package Matplotlib
% (https://bids.github.io/colormap/).
%
% Input:
%
% nCol      Number of colors, default value is 256.
%
    """
    args = tuple(v for v in [nCol] if v is not None)
    return m.cm_magma(*args, **kwargs)


def cm_fireprint(n=None, *args, **kwargs):
    """
% colormap that increases linearly in lightness (with colors)
%
%   Colormap that increases linearly in lightness (such as a pure black to white
%   map) but incorporates additional colors that help to emphasize the
%   transitions and hence enhance the perception of the data.
%   This colormap is designed to be printer-friendly both for color printers as
%   as well as B&W printers.
%
%	Written by Matthias & Stefan Geissbuehler - matthias.geissbuehler@a3.epfl.ch
%	June 2011
%
%   Credit: The idea of the passages over blue&red stems from ImageJ's LUT 'Fire'
%   Our colormap corrects the color-printout-problems as well as the
%   non-linearity in the fire-colormap which would make it incompatible
%   with a B&W printing.
%
%
%
%   Usage:
%   cmap = fireprint(n)
%
%   All arguments are optional:
%
%   n           The number of elements (256)
%
%   Further on, the following options can be applied
%     'minColor' The absolute minimum value can have a different color
%                ('none'), 'white','black','lightgray', 'darkgray'
%                or any RGB value ex: [0 1 0]
%     'maxColor' The absolute maximum value can have a different color
%     'invert'   (0), 1=invert the whole colormap
%
%
%   Examples:
%     figure; imagesc(peaks(200));
%     colormap(fireprint)
%     colorbar
%
%     figure; imagesc(peaks(200));
%     colormap(fireprint(256,'minColor','black','maxColor',[0 1 0]))
%     colorbar
%
%     figure; imagesc(peaks(200));
%     colormap(fireprint(256,'invert',1,'minColor','darkgray'))
%     colorbar
%
    """
    args = tuple(v for v in [n] if v is not None) + args
    return m.cm_fireprint(*args, **kwargs)


def cm_plasma(nCol=None, **kwargs):
    """
% magma colormap with added white
%
% CM_PLASMA(nCol)
%
% This is a honest colormap, unlike the Matlab default parula(). This means
% this colormap is perceptionally uniform, thus it will not emphasize any
% value on the plot. It is also compatible with black and white output. The
% colormap is copied from the Python package Matplotlib
% (https://bids.github.io/colormap).
%
% Input:
%
% nCol      Number of colors, default value is 256.
%
    """
    args = tuple(v for v in [nCol] if v is not None)
    return m.cm_plasma(*args, **kwargs)


def rdir(rootdir=None, *args, **kwargs):
    """
% Lists the files in a directory and its sub directories.
%
% function [D] = rdir(ROOT,TEST)
%
% Recursive directory listing.
%
% ROOT is the directory starting point and includes the
% wildcard specification.
% The function returns a structure D similar to the one
% returned by the built-in dir command.
% There is one exception, the name field will include
% the relative path as well as the name to the file that
% was found.
% Pathnames and wildcards may be used. Wild cards can exist
% in the pathname too. A special case is the double * that
% will match multiple directory levels, e.g. c:\**\*.m.
% Otherwise a single * will only match one directory level.
% e.g. C:\Program Files\Windows *\
%
% TEST is an optional test that can be performed on the
% files. Two variables are supported, datenum & bytes.
% Tests are strings similar to what one would use in a
% if statement. e.g. 'bytes>1024 & datenum>now-7'
%
% If not output variables are specified then the output is
% sent to the screen.
%
% See also DIR
%
% examples:
%   D = rdir('*.m');
%     for ii=1:length(D), disp(D(ii).name); end;
%
%   % to find all files in the current directory and sub directories
%   D = rdir('**\*')
%
%   % If no output is specified then the files are sent to
%   % the screen.
%   rdir('c:\program files\windows *\*.exe');
%   rdir('c:\program files\windows *\**\*.dll');
%
%   % Using the test function to find files modified today
%   rdir('c:\win*\*','datenum>floor(now)');
%   % Using the test function to find files of a certain size
%   rdir('c:\program files\win*\*.exe','bytes>1024 & bytes<1048576');
%
    """
    args = tuple(v for v in [rootdir] if v is not None) + args
    return m.rdir(*args, **kwargs)


