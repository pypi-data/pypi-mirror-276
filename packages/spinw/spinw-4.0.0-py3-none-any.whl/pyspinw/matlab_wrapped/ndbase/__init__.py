import pyspinw
m = pyspinw.Matlab()


def pso(dat=None, func=None, p0=None, *args, **kwargs):
    """
% particle swarm optimisation
%
% [pOpt,fVal,stat] = NDBASE.PSO([],func,p0,'Option1','Value1',...)
%
% [pOpt,fVal,stat] = NDBASE.PSO(dat,func,p0,'Option1','Value1',...)
%
%
% PSO finds a minimum of a function of several variables using the particle
% swarm optimization (PSO) algorithm originally introduced in 1995 by
% Kennedy and Eberhart. This algorithm was extended by Shi and Eberhart in
% 1998 through the introduction of inertia factors to dampen the velocities
% of the particles. In 2002, Clerc and Kennedy introduced a constriction
% factor in PSO, which was later on shown to be superior to the inertia
% factors. Therefore, the algorithm using a constriction factor was
% implemented here.
%
% The function has two different modes, depending on the first input
% argument. If dat is empty, pso minimizes the cost function func, that has
% the following header:
%                           R2 = func(p)
%
% If dat is a struct, the function optimizes the model defined by func via
% least squares to the data stored in dat. In this case func has the
% following header:
%                           yModel = func(x,p)
% And the least square deviation is defined by:
%                       R2 = sum((yData-yModel).^2/errorData.^2)
%
%
% Input:
%
% dat       Either empty or contains data to be fitted stored in a
%           structure with fields:
%               dat.x   vector of N independent variables,
%               dat.y   vector of N data values to be fitted,
%               dat.e   vector of N standard deviation (positive numbers)
%                       used to weight the fit. If zero or missing
%                       1./dat.y^2 will be assigned to each point.
% func      Function handle with one of the following definition:
%               R2 = func(p)        if dat is empty,
%               y  = func(x,p)      if dat is a struct.
%           Here x is a vector of N independent variables, p are the
%           M parameters to be optimized and y is the simulated model, R2
%           is the value to minimize.
% p0        Vector of M initial parameters.
%
% Options:
%
% lb        Vector with N elements, lower boundary of the parameters.
%           Default value is -1e5.
% ub        Vector with N elements, upper boundary of the parameters.
%           Default value is 1e5.
% MaxIter   Maximum number of iterations, default value is 100*M.
% MaxFunEvals Maximum number of function evaluations, default value is
%           1000*M. NOT IMPLEMENTED!
% TolX      Convergence tolerance for parameters, default value is 1e-3.
% Display   Level of information to print onto the Command Line during
%           optimisation. Possible values are 'off', 'notify' and 'iter'.
%           Default is 'off'.
% TolFun    Convergence tolerance on the R2 value (return value of func or
%           the weighted least square deviation from data). Default value
%           is 1e-3.
% SwarmC1   Swarm parameter, also called phi_p in the literature. Default
%           value is 2.8.
% SwarmC2   Swarm parameter, also called phi_g in the literature. Default
%           value is 1.3.
% k0        Swarm paramter, it can take values between 0 and 1, but is
%           usually set to one (Montes de Oca et al., 2006). Default value
%           is 1.
% seed      Seed number for the random number generator, by default it is
%           seeded from the system clock every time the function is called.
% PopulationSize Size of the swarm, default value is 25.
% autoTune  Determine the size of the swarm based on the number of free
%           parameters (number of parameters that are not fixed by setting
%           lb(i)==ub(i)). Default is false. The optimal swarm size is:
%               PopulationSize = 25 + 1.4*Nf
%           This value is based on the technical report:
%               Good Parameters for Particle Swarm Optimization By Magnus Erik Hvass Pedersen Hvass Laboratories
%               Technical Report no. HL1001
%               http://www.hvass-labs.org/people/magnus/publications/pedersen10good-pso.pdf
% tid       Setup time estimation with the following values:
%               0   Do nothing (default).
%               1   Text output to the Command Window. Default.
%               2   Graphical output, using the waitbar() function.
%              -1   Set the value from the SpinW preferences (needs SpinW
%                   installed).
%
% See also NDBASE.LM.
%
    """
    args = tuple(v for v in [dat, func, p0] if v is not None) + args
    return m.ndbase.pso(*args, **kwargs)


def getdata(obj=None, *args, **kwargs):
    """
% extract data from different type of objects
%
% dat = NDBASE.GETDATA(dndobj, 'option1',value1,...)
%
% Currently works with dnd objects.
%
%
% Input:
%
% dndobj        Object of dnd type.
%
% Options:
%
% binType       Type of the output bin:
%                   'center'    Center bin, default.
%                   'edge'      Edge bin (storing edge value of each bin).
% axUnit        Unit of the axis:
%                   'default'   Units as it is given in the dnd object,
%                               default.
%                   'A-1'       Units of A^-1.
% emptyval      Value for empty pixels. Default is nan.
%
% Output:
%
% dat           Structure with the following fields:
%                   sig     Storing the signal in a matrix with dimensions
%                           [nAx1 nAx2 ...].
%                   err     Standard deviation of the signal stored in a
%                           matrix with same dimensions.
%                   ax      Axes stored in a cell: {ax1 ax2 ...}. Each axn
%                           is a column vector with nAxn or nAxn+1 number
%                           of elements for center and edge bins
%                           respectively.
%
    """
    args = tuple(v for v in [obj] if v is not None) + args
    return m.ndbase.getdata(*args, **kwargs)


def corrphon(d2ddat=None, *args, **kwargs):
    """
% subtract incoherent phonons from magnetic data in d2d object
%
% NDBASE.CORRPHON(d2d,'option1',value1,...)
%
% Options:
%
% qphon         Q-range where the phonon background is to be fitted in
%               units of A^-1. Recommended range is above 4 A^-1, where the
%               magnetic signal is negligible due to the form factor. It is
%               also possible to given an upper value. For no upper limit,
%               use inf. Default value is [4 5].
%
    """
    args = tuple(v for v in [d2ddat] if v is not None) + args
    return m.ndbase.corrphon(*args, **kwargs)


def lm3(dat=None, func0=None, p0=None, *args, **kwargs):
    """
% least square refinement of parameters using Levenberg Marquardt method
%
% [pOpt,fVal,stat] = NDBASE.LM(dat,func,p0,'Option1','Value1',...)
%
% Levenberg Marquardt curve-fitting function, minimizes sum of weighted
% squared residuals.
%
% Input:
%
% dat       Data to be fitted stored in a structure with fields:
%               dat.x   vector of N independent variables,
%               dat.y   vector of N data values to be fitted,
%               dat.e   vector of N standard deviation (positive numbers)
%                       used to weight the fit. If zero or missing
%                       1./dat.y^2 will be assigned to each point, however
%                       in this case the refinement is reduced to an
%                       optimisation problem.
% func      Function handle with the following definition:
%               y = func(x,p)
%           where x is a vector of N independent variables, p are the
%           M parameters to be optimized and y is the simulated model.
% p0        Row vector of M initial parameters.
%
% Options:
%
% Options can be given using the modified output of optimset() or as option
% name string option value pairs.
%
% dp        Vector with N or 1 element, defines the fractional increment of
%           'p' when calculating the Jacobian matrix dFunc(x,p)/dp:
%               dp(j)>0     central differences calculated,
%               dp(j)<0     one sided 'backwards' differences calculated,
%               dp(j)=0     sets corresponding partials to zero, i.e. holds
%                           p(j) fixed.
%           Default value if 1e-3.
% vary      Vector with N elements, if an element is false, the
%           corresponding parameter will be fixed. Default value is
%           false(1,N).
% win       Limits for the independent variabel values where the function
%           is fitted. Default is [-inf inf].
% lb        Vector with N elements, lower boundary of the parameters.
%           Default value is -inf.
% ub        Vector with N elements, upper boundary of the parameters.
%           Default value is inf.
% MaxIter   Maximum number of iterations, default value is 10*M.
% MaxFunEvals Maximum number of function evaluations, default value is
%           100*M.
% TolX      Convergence tolerance for parameters, defines the maximum of
%           the relative chande of any parameter value. Default value is
%           1e-3.
% eps1      Convergence tolerance for gradient, default value is 1e-3.
% eps2      Convergence tolerance for reduced Chi-square, default value is
%           1e-2.
% eps3      Determines acceptance of a L-M step, default value is 0.1.
% lambda0   Initial value of L-M paramter, default value is 1e-2.
% nu0       Value that determines the speed of convergence. Default value
%           is 10. It should be larger than 1.
% lUp       Factor for increasing lambda, default value is 30.
% lDown     Factor for decreasing lambda, default value is 7.
% update    Type of parameter update:
%                   'lm'        Levenberg-Marquardt lambda update,
%                   'quadratic' Quadratic update,
%                   'nielsen'   Nielsen's lambda update equations (default).
% extraStat Calculates extra statistics: covariance matrix of parameters,
%           cofficient of multiple determination, asymptotic standard
%           error of the curve-fit and convergence history.
% confLev   Confidence level, where the error of the curve fit (sigY) is
%           calculated. Default is erf(1/sqrt(2))~0.6827 for standard
%           deviation (+/- 1 sigma).
%
% Output:
%
% pOpt      Value of the M optimal parameters.
% fVal      Value of the model function calculated with the optimal
%           parameters at the N independent values of x.
%
% stat      Structure, storing the detailed output of the calculation with
%           the following fields:
%               p       Least-squares optimal estimate of the parameter
%                       values.
%               redX2   Reduced Chi squared error criteria, its value
%                       should be close to 1. If the value is larger, the
%                       model is not a good description of the data. If the
%                       value is smaller, the model is overparameterized
%                       and fitting the statistical error of the data.
%               sigP    Asymptotic standard error of the parameters.
%               sigY    Asymptotic standard error of the curve-fit.
%               corrP   Correlation matrix of the parameters.
%               Rsq     R-squared cofficient of multiple determination.
%               cvgHst  Convergence history.
%               exitFlag The reason, why the code stopped:
%                           1       convergence in r.h.s. ("JtWdy"),
%                           2       convergence in parameters,
%                           3       convergence in reduced Chi-square,
%                           4       maximum Number of iterations reached
%                                   without convergence
%               message String, one of the above messages.
%               nIter   The number of iterations executed during the fit.
%               nFunEvals The number of function evaluations executed
%                       during the fit.
%
% See also NDBASE.PSO.
%
    """
    args = tuple(v for v in [dat, func0, p0] if v is not None) + args
    return m.ndbase.lm3(*args, **kwargs)


def lm(dat=None, func0=None, p0=None, *args, **kwargs):
    """
% least square refinement of parameters using Levenberg Marquardt method
%
% [pOpt,fVal,stat] = NDBASE.LM(dat,func,p0,'Option1','Value1',...)
%
% Levenberg Marquardt curve-fitting function, minimizes sum of weighted
% squared residuals.
%
% Input:
%
% dat       Data to be fitted stored in a structure with fields:
%               dat.x   vector of N independent variables,
%               dat.y   vector of N data values to be fitted,
%               dat.e   vector of N standard deviation (positive numbers)
%                       used to weight the fit. If zero or missing
%                       1./dat.y^2 will be assigned to each point, however
%                       in this case the refinement is reduced to an
%                       optimisation problem.
% func      Function handle with the following definition:
%               y = func(x,p)
%           where x is a vector of N independent variables, p are the
%           M parameters to be optimized and y is the simulated model.
% p0        Vector of M initial parameters.
%
% Options:
%
% Options can be given using the modified output of optimset() or as option
% name string option value pairs.
%
% dp        Vector with N or 1 element, defines the fractional increment of
%           'p' when calculating the Jacobian matrix dFunc(x,p)/dp:
%               dp(j)>0     central differences calculated,
%               dp(j)<0     one sided 'backwards' differences calculated,
%               dp(j)=0     sets corresponding partials to zero, i.e. holds
%                           p(j) fixed.
%           Default value if 1e-3.
% vary      Vector with N elements, if an element is false, the
%           corresponding parameter will be fixed. Default value is
%           false(1,N).
% win       Limits for the independent variabel values where the function
%           is fitted. Default is [-inf inf].
% lb        Vector with N elements, lower boundary of the parameters.
%           Default value is -inf.
% ub        Vector with N elements, upper boundary of the parameters.
%           Default value is inf.
% MaxIter   Maximum number of iterations, default value is 10*M.
% MaxFunEvals Maximum number of function evaluations, default value is
%           100*M.
% TolX      Convergence tolerance for parameters, defines the maximum of
%           the relative chande of any parameter value. Default value is
%           1e-3.
% eps1      Convergence tolerance for gradient, default value is 1e-3.
% eps2      Convergence tolerance for reduced Chi-square, default value is
%           1e-2.
% eps3      Determines acceptance of a L-M step, default value is 0.1.
% lambda0   Initial value of L-M paramter, default value is 1e-2.
% nu0       Value that determines the speed of convergence. Default value
%           is 10. It should be larger than 1.
% lUp       Factor for increasing lambda, default value is 30.
% lDown     Factor for decreasing lambda, default value is 7.
% update    Type of parameter update:
%                   'lm'        Levenberg-Marquardt lambda update,
%                   'quadratic' Quadratic update,
%                   'nielsen'   Nielsen's lambda update equations (default).
% extraStat Calculates extra statistics: covariance matrix of parameters,
%           cofficient of multiple determination, asymptotic standard
%           error of the curve-fit and convergence history.
% confLev   Confidence level, where the error of the curve fit (sigY) is
%           calculated. Default is erf(1/sqrt(2))~0.6827 for standard
%           deviation (+/- 1 sigma).
%
% Output:
%
% pOpt      Value of the M optimal parameters.
% fVal      Value of the model function calculated with the optimal
%           parameters at the N independent values of x.
%
% stat      Structure, storing the detailed output of the calculation with
%           the following fields:
%               p       Least-squares optimal estimate of the parameter
%                       values.
%               redX2   Reduced Chi squared error criteria, its value
%                       should be close to 1. If the value is larger, the
%                       model is not a good description of the data. If the
%                       value is smaller, the model is overparameterized
%                       and fitting the statistical error of the data.
%               sigP    Asymptotic standard error of the parameters.
%               sigY    Asymptotic standard error of the curve-fit.
%               corrP   Correlation matrix of the parameters.
%               Rsq     R-squared cofficient of multiple determination.
%               cvgHst  Convergence history.
%               exitFlag The reason, why the code stopped:
%                           1       convergence in r.h.s. ("JtWdy"),
%                           2       convergence in parameters,
%                           3       convergence in reduced Chi-square,
%                           4       maximum Number of iterations reached
%                                   without convergence
%               message String, one of the above messages.
%               nIter   The number of iterations executed during the fit.
%               nFunEvals The number of function evaluations executed
%                       during the fit.
%
% See also NDBASE.PSO.
%
    """
    args = tuple(v for v in [dat, func0, p0] if v is not None) + args
    return m.ndbase.lm(*args, **kwargs)


def histn(X=None, Y=None, *args, **kwargs):
    """
% calculates histogram of arbitrary dimensional data
%
% function [Ysum, Nsum, Cbin] = NDBASE.HISTN(X,Y,bin1,bin2,...,'option1',value1)
%
% Any data point with NaN X or Y value is omitted from the binning. Works
% for non-uniform bins and also optimised for uniform bins with significant
% speedup.
%
% Input:
%
% X         Array with size of [nPoint nDim], that represents
%           positions in the nDim dimensional space (R^nDim).
% Y         Column vector with nPoint element, that represents values at
%           the points defined in X. {X,Y} defines a scalar field in the
%           nDim dimensional space. If Y contains multiple columns, each
%           column will be binned independently and saved into Ysum in
%           separate columns, this can represent vector field at X. The
%           dimensions of the vector field is nField, if the size of Y is
%           [nPoint nField].
% binI      Row vectors that define BIN EDGES along the I-th dimension.
%           It goes from 1 to nDim. Each vector has to have at least two
%           elements. The number of bins along the I-th dimension is equal
%           to the number of elements in the binI vector minus one. Thus:
%               nBinI = numel(binI)-1
%
% Options:
%
% emptyval  Value for empty bins in Ysum and Nsum:
%               emptyval = [emptyY emptyN]
%           Default value is [NaN 0].
%
% Output:
%
% Ysum      Array with size of [nBin1 nBin2 nBin3 ... nField]. Each pixel
%           contains the sum of the elements of Y that are within the
%           given bin boundaries:
%               bin1(i1) <= X(:,i1) < bin1(i1+1) and
%               	...
%               binN(iN) <= X(:,iN) < binN(iN+1)
%           Points of X, that are outside of the bin boundaries are
%           omitted. Empty pixels will contain NaN by default.
% Nsum      Column vector with the same number of rows as Ysum, contains
%           the number of points that are contributing to the pixel. Only
%           calculated if two output is expected. Empty pixels will contain
%           the value 0 by default. To make it possible to calculate the
%           average value of each pixel, set the default value to 1, then
%           devide Ysum with Nsum element vise:
%               Yavg = bsxfun(@rdivide,Ysum,Nsum);
% Cbin      Center bin positions, if nDim=1 the values are stored in a row
%           vector. If nDim>1 the center bin vectors are packed into a
%           cell.
%
% Example:
%
% Random points in 2D.
%
% nPoint = 1e3;
% nDim   = 2;
% bin = linspace(0,1,101);
%
% X = rand(nPoint,nDim);
% Y = sin(X(:,1)*2*pi);
% [Ysum,Nsum] = ndbase.histn(X,Y,bin,bin);
% figure
% imagesc(Ysum./Nsum);
%
%
% Create points on a square lattice.
%
% [xx,yy] = ndgrid(1:0.5:10,1:0.5:10);
%
% bin = linspace(0,11,101);
%
% [Ysum,Nsum] = ndbase.histn([xx(:) yy(:)],sin(xx(:)),bin,bin);
% figure
% imagesc(Ysum./Nsum);
%
% Oversample the sine function defined on a finite point.
% xx = 0:0.5:10;
% bin = linspace(0,11,101);
%
% Ysum = ndbase.histn([xx(:)],sin(xx(:)),bin);
% figure
% plot(Ysum,'o-');
%
% See also accumarray, interp1.
    """
    args = tuple(v for v in [X, Y] if v is not None) + args
    return m.ndbase.histn(*args, **kwargs)


def source(dataSource=None, type=None, **kwargs):
    """
% reads text data from multiple sources
%
% [dataStr, {info}] = SOURCE(dataSource, {type})
%
% The function can read text data from the following sources:
%   - local files, where the file location is specified in dataSource
%   - download an url content, when dataSource begins with 'http'
%
% Input:
%
% dataSource    String, can be file name or url (starting with 'http').
% {type}        Forces to treat data source as a certain type, optional.
%               Possible values:
%                   'auto'      Determine automatically whether file or
%                               url, (default).
%                   'file'      Local file.
%                   'url'       Url adress.
%
% Output:
%
% dataStr       String in a char type row vector.
% {info}        Additional information stored in a struct with fields:
%   source      Data source (empty if string data was given).
%   isfile      Logical variable, true if the source is a local file.
%
    """
    args = tuple(v for v in [dataSource, type] if v is not None)
    return m.ndbase.source(*args, **kwargs)


def cplot(dat=None, *args, **kwargs):
    """
% produces interplolated color plot of scattered data
%
% hPlot = NDBASE.CPLOT(dat, 'option1', value1, ...)
%
% Input:
%
% dat       Data, either array of spec1d type or struct with fields x, y
%           and z.
%
% Options:
%
% x         X-values for spec1d data.
% scale     Scalar, determines the scaling between the x- and y-axis for
%           the interpolation. Default is 'auto'.
% npix      Number of pixels either scalar or 2 element vector
%           [npixx npixy].
% plot      Logical, if true a plot will be produced.
% scatter   If true, dots are plotted at the position of the given data
%           points. Default is true.
% convhull  If true, the color map is shown only between the given data
%           points (within the convex hull of the points), this is achieved
%           by giving nan value for all interpolated points outside of the
%           convex hull. Default is true.
% log       Plot natural logarithm of the values.
%
% Output
%
% hPlot     Handle of the plot object.
%
    """
    args = tuple(v for v in [dat] if v is not None) + args
    return m.ndbase.cplot(*args, **kwargs)


def spaghetti(dat=None, *args, **kwargs):
    """
% creates spaghetti plot from d2d objects
%
% udat = NDBASE.SPAGHETTI(dat, 'option1', value1, ...)
%
% Input:
%
% dat       Array of d2d class objects with nDat member. Typically Horace
%           cuts.
%
% Options:
%
% flip      Vector of nDat logical values, if any value is true the
%           corresponding data is flipped along the horizontal axis.
%           Default is false(1,nDat).
% label     Cell of strings for the x-axis label. There has to be nDat+1
%           strings.
% dashed    If true, black dashed line is drawn between cuts. Default is
%           true.
% ylim      If true, the upper limit of the vertical axis is automatically
%           determined. Default is true.
% plot      If true, plot is created. Default is true.
% pad       If true, the output data is padded with nans on the top and
%           right side. Then it can be plotted directly using surf():
%               udat = ndbase.spaghetti(dat,'pad',true);
%               coo = cell(1,2);
%               [coo{:}] = ndgrid(udat.x,udat.y);
%               surf(coo{:},udat.sig);
% axscale   Scale of the unit on the x-axis. Defines what A^-1 value
%           corresponds to unit 1. Default value is 1.
%
% Output:
%
% udat      United data in simple struct with the following fields:
%               x       Column vector of x-coordinate edge bins (nX+1).
%               y       Column vector of y-coordinate edge bins (nY+1).
%               sig     Signal matrix with dimensions [nX nY].
%               err     Error matrix with dimensions [nX nY].
%               ylabel  Label of the y-axis, string.
%               xlim    Limits of the x-axis, row vector with 2 elements.
%               ylim    Limits of the y-axis, row vector with 2 elements.
%               clim    Limits of the c-axis, row vector with 2 elements.
%
    """
    args = tuple(v for v in [dat] if v is not None) + args
    return m.ndbase.spaghetti(*args, **kwargs)


def simplex(dat=None, func=None, p0=None, *args, **kwargs):
    """
% simplex optimisation
%
% ### Syntax
%
% `[pOpt,fVal,stat] = ndbase.simplex([],func,p0,Name,Value)`
%
% `[pOpt,fVal,stat] = ndbase.simplex(dat,func,p0,Name,Value)`
%
% ### Description
%
% `[pOpt,fVal,stat] = ndbase.simplex([],func,p0,Name,Value)` finds a
% minimum of a function of several parameters using the constrained simplex
% optimization algorithm by calling the unconstrained Matlab built-in
% algorithm [matlab.fminsearch].
%
% The function has two different modes, depending on the first input
% argument. If `dat` is empty, `simplex` minimizes the cost function func,
% that has the following header:
% ```
% R2 = func(p)
% ```
%
% If `dat` is a struct, `simplex` optimizes the model defined by `func` via
% least squares to the data stored in `dat`. In this case `func` has the
% following header:
% ```
% yModel = func(x,p)
% ```
%
% And the least square deviation is defined by:
%
% $R^2 = \sum \frac{(y_{dat}-y_{fit})^2}{\sigma_{dat}^2}$
%
%  {{note If options is supplied, then TolX will apply to the transformed
%  variables. All other [matlab.fminsearch] parameters should be unaffected.
%
%  Variables which are constrained by both a lower and an upper
%  bound will use a $\sin(x)$ transformation. Those constrained by
%  only a lower or an upper bound will use a quadratic
%  transformation, and unconstrained variables will be left alone.
%
%  Variables may be fixed by setting their respective bounds equal.
%  In this case, the problem will be reduced in size for [matlab.fminsearch].
%
%  The bounds are inclusive inequalities, which admit the
%  boundary values themselves, but will not permit any function
%  evaluations outside the bounds. These constraints are strictly
%  followed.
%
%  If your problem has an exclusive (strict) constraint which will
%  not admit evaluation at the bound itself, then you must provide
%  a slightly offset bound. An example of this is a function which
%  contains the log of one of its parameters. If you constrain the
%  variable to have a lower bound of zero, then `simplex` may
%  try to evaluate the function exactly at zero.}}
%
% ### Examples
%
% Example usage on the rosen function.
%
% ```
% >>rosen = @(x) (1-x(1)).^2 + 105*(x(2)-x(1).^2).^2
% ```
%
% Unconstrained optimisation:
%
% ```
% >>>rosen = @(x) (1-x(1)).^2 + 105*(x(2)-x(1).^2).^2
% >>fminsearch(rosen,[3 3])>>
% ```
%
% Constrained optimisation:
%
% ```
% >>>rosen = @(x) (1-x(1)).^2 + 105*(x(2)-x(1).^2).^2
% >>ndbase.simplex([],rosen,[3 3],'lb',[2 2],'ub',[])>>
% ```
%
% ### Input Arguments
%
% `dat`
% : Either empty or contains data to be fitted stored in a structure with
%   fields:
%   * `dat.x`   vector of $N$ independent variables,
%   * `dat.y`   vector of $N$ data values to be fitted,
%   * `dat.e`   vector of $N$ standard deviation (positive numbers)
%               used to weight the fit. If zero or missing
%               `1/dat.y^2` will be assigned to each point.
%
% `func`
% : Function handle with one of the following definition:
%   * `R2 = func(p)`        if `dat` is empty,
%   * `y  = func(x,p)`      if `dat` is a struct.
%   Here `x` is a vector of $N$ independent variables, `p` are the
%   $M$ parameters to be optimized and `y` is the simulated model, `R2`
%   is the value to minimize.
%
% ### Name-Value Pair Arguments
%
% `'lb'`
% : Vector with $N$ elements, lower boundary of the parameters. Default
%   value is -inf.
%
% `'ub'`
% : Vector with $N$ elements, upper boundary of the parameters. Default
%   value is inf.
%
% `'MaxIter'`
% : Maximum number of iterations, default value is $100M$.
%
% `'MaxFunEvals'`
% : Maximum number of function evaluations, default value is
%   $1000M$. NOT IMPLEMENTED!
%
% `'TolX'`
% : Convergence tolerance for parameters, default value is $10^{-3}$.
%
% `'Display'`
% : Level of information to print onto the Command Line during
%   optimisation. Possible values are `'off'`, `'notify'` and `'iter'`.
%   Default value is `'off'`.
%
% `'TolFun'`
% : Convergence tolerance on the `R2` value (return value of `func` or
%   the weighted least square deviation from data). Default value is
%   $10^{-3}$.
%
%
% ### See Also
%
% [ndbase.lm] \| [ndbase.pso]
    """
    args = tuple(v for v in [dat, func, p0] if v is not None) + args
    return m.ndbase.simplex(*args, **kwargs)


def lm2(dat=None, func0=None, p0=None, *args, **kwargs):
    """
% optimization of parameters using the Levenberg Marquardt method
%
% [pOpt,fVal,stat] = NDBASE.LM([],func,p0,'Option1','Value1',...)
%
% Levenberg Marquardt curve-fitting function, minimizes the return value of
% a given function.
%
% Input:
%
% func      Function handle with the following definition:
%               R = func(p)
%           where p are the M parameters to be optimized.
% p0        Vector of M initial parameters.
%
% Options:
%
% Options can be given using the modified output of optimset() or as option
% name string option value pairs.
%
% dp        Vector with N or 1 element, defines the fractional increment of
%           'p' when calculating the Jacobian matrix dFunc(x,p)/dp:
%               dp(j)>0     central differences calculated,
%               dp(j)<0     one sided 'backwards' differences calculated,
%               dp(j)=0     sets corresponding partials to zero, i.e. holds
%                           p(j) fixed.
%           Default value if 1e-3.
% vary      Vector with N elements, if an element is false, the
%           corresponding parameter will be fixed. Default value is
%           false(1,N).
% lb        Vector with N elements, lower boundary of the parameters.
%           Default value is -inf.
% ub        Vector with N elements, upper boundary of the parameters.
%           Default value is inf.
% MaxIter   Maximum number of iterations, default value is 10*M.
% MaxFunEvals Maximum number of function evaluations, default value is
%           100*M.
% TolX      Convergence tolerance for parameters, defines the maximum of
%           the relative chande of any parameter value. Default value is
%           1e-3.
% eps1      Convergence tolerance for gradient, default value is 1e-3.
% eps2      Convergence tolerance for reduced Chi-square, default value is
%           1e-2.
% eps3      Determines acceptance of a L-M step, default value is 0.1.
% lambda0   Initial value of L-M paramter, default value is 1e-2.
% nu0       Value that determines the speed of convergence. Default value
%           is 10. It should be larger than 1.
%
% Output:
%
% pOpt      Value of the M optimal parameters.
% fVal      Value of the model function calculated with the optimal
%           parameters at the N independent values of x.
%
% stat      Structure, storing the detailed output of the calculation with
%           the following fields:
%               p       Least-squares optimal estimate of the parameter
%                       values.
%               redX2   Reduced Chi squared error criteria, its value
%                       should be close to 1. If the value is larger, the
%                       model is not a good description of the data. If the
%                       value is smaller, the model is overparameterized
%                       and fitting the statistical error of the data.
%               sigP    Asymptotic standard error of the parameters.
%               sigY    Asymptotic standard error of the curve-fit.
%               corrP   Correlation matrix of the parameters.
%               Rsq     R-squared cofficient of multiple determination.
%               cvgHst  Convergence history.
%               exitFlag The reason, why the code stopped:
%                           1       convergence in r.h.s. ("JtWdy"),
%                           2       convergence in parameters,
%                           3       convergence in reduced Chi-square,
%                           4       maximum Number of iterations reached
%                                   without convergence
%               message String, one of the above messages.
%               nIter   The number of iterations executed during the fit.
%               nFunEvals The number of function evaluations executed
%                       during the fit.
%
% See also NDBASE.PSO.
%
    """
    args = tuple(v for v in [dat, func0, p0] if v is not None) + args
    return m.ndbase.lm2(*args, **kwargs)


