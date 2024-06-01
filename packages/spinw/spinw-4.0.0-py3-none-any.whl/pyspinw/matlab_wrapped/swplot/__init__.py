import pyspinw
m = pyspinw.Matlab()


def tooltipcallback(obj=None, hit=None, hFigure=None, hTransform=None, **kwargs):
    """
% callback for displaying tooltip
%
% ### Syntax
%
% `swplot.tooltipcallback(obj,hit,hFigure,hTransform)`
%
% ### Description
%
% `swplot.tooltipcallback(obj,hit,hFigure,hTransform)` is the callback
% function that is automatically added to any object on an [swplot] figure
% that is created using one of the `swplot.plot...` commands with `tooltip`
% parameter set to `true`.
%
% ### Input Arguments
%
% `obj`
% : [spinw] object.
%
% `hit`
% :  Hit object, defines the point where the mouse clicked.
%
% `hFigure`
% : Handle of parent swplot figure.
%
% `hTransform`
% : Parent [matlab.hgtransform] object if exists.
%
% ### See Also
%
% [swplot.tooltip]
%
    """
    args = tuple(v for v in [obj, hit, hFigure, hTransform] if v is not None)
    return m.swplot.tooltipcallback(*args, **kwargs)


def legend(switch0=None, hFigure=None, **kwargs):
    """
% adds legend to the swplot figure
%
% ### Syntax
%
% `swplot.legend`
%
% `swplot.legend(switch, hFigure)`
%
% `status = swplot.legend`
%
% ### Description
%
% `swplot.legend` adds legend to the active swplot figure.
%
% `swplot.legend(switch, hFigure)` adds/removes/refreshes the legend on the
% swplot figure referenced by the `hFigure` handle depending on the
% `switch` string.
%
% ### Examples
%
% This example shows how the default legend for arrow and circle objects
% looks like.
%
% ```
% >>swplot.plot('type','arrow','position',rand(3,10,2)*10-5,'legend',1,'color','gold')
% >>swplot.plot('type','circle','position',rand(3,10,2)*10-5,'R',1,'legend',1,'color','purple')
% >>swplot.zoom
% >>swplot.legend
% >>snapnow
% ```
%
% ### Input Arguments
%
% `switch`
% : One of the following string:
%   * `'on'`                show legend,
%   * `'off'`               hide legend,
%   * `'refresh'`           redraw legend,
%   * `'-'`\|`'--'`\|`'none'` change the linestyle of the legend frame.
%
%   Default value is `'on'`.
%
% `hFigure`
% : Handle of the swplot figure, default value is the handle of the active
%   figure.
%
    """
    args = tuple(v for v in [switch0, hFigure] if v is not None)
    return m.swplot.legend(*args, **kwargs)


def base(*args, **kwargs):
    """
% sets the basis vectors of an swplot figure
%
% ### Syntax
%
% `swplot.base(BV)`
%
% `swplot.base(obj)`
%
% `BV = swplot.base`
%
% ### Description
%
% `swplot.base(BV)` sets the basis vector for an swplot figure. The basis
% vectors can be used to define a non-orthogonal coordinate system for
% graphic objects.
%
% `swplot.base(obj)` sets the basis vectors to the lattice units of a given
% [spinw] object `obj`.
%
% `BV = swplot.base` returns the basis vectors stored in the swplot figure.
%
%
% ### Input Arguments
%
% `BV`
% : Either a $[3\times 3]$ matrix of the new basis vectors or a [spinw]
%   object where the new basis vectors will be the lattice
%   units and the basis vectors are generated via [spinw.basisvector].
%
% `hFigure`
% : Handle of the [swplot] figure. Default is the active
%   figure.
%
% ### See Also
%
% [swplot.plot]
%
    """
    
    return m.swplot.base(*args, **kwargs)


def line(*args, **kwargs):
    """
% creates 3D line patch
%
% ### Syntax
%
% `hLine = swplot.line(rStart, rEnd)`
%
% `hLine = swplot.line(r,[])`
%
% `hLine = swplot.line(rStart, rEnd, lineStyle, lineWidth, multiPatch)`
%
% ### Description
%
% `hLine = swplot.line(rStart, rEnd)` creates disconnected line segments
% between multiple `rStart(:,i)` `rEnd(:,i)` pairs of 3D coordinates. The
% lines are shown as patch faces.
%
% `hLine = swplot.line(r,[])` creates connected line segments  between
% the consicutive points `r(:,i)`.
%
% `hPatch = swplot.line(handle, ...)` adds the generated patch object to a
% given axis if `handle` is an axis handle or adds the lines to an
% existing [matlab.patch] object, if the given `handle` points to a patch
% object.
%
% ### Input Arguments
%
% `handle`
% : Handle of an axis or triangulated patch object. In case of patch
%   object, the constructed faces will be added to the existing object.
%
% `rStart`
% : Coordinate(s) of the starting point, either a 3 element vector or
%   a matrix with dimensions of $[3\times n_{lineSegment}] to plot multiple line
%   segments.
%
% `rEnd`
% : Coordinate(s) of the end point, either a 3 element vector or
%   a matrix with dimensions of $[3\times n_{lineSegment}]$ to plot multiple line
%   segments.
%
% `r`
% : Matrix with dimensions of $[3\times n_{obj}\times n_{lineSegment}]$. The function
%   will plot $n_{obj}$ number of disconnected curves. The $i$th
%   curve will follow the `x=r(1,i,:)`, `y=r(2,i,:)`, `z=r(3,i,:)`
%   (parameteric) segmented curve.
%
% `lineStyle`
% : Line style, default value is `'-'` for continuous line. Any other
%   Matlab line style string is accepted: `'--'`\|`':'`\|`'-.'`\|`'none'`.
%
% `lineWidth`
% : Line width in pt, default value is 0.5.
%
% `mPatch`
% : If `true`, a separate patch object will be created per line
%   segment. Default is `false`, a single patch object will store all
%   line segments.
%
% ### See Also
%
% [matlab.line]
%
    """
    
    return m.swplot.line(*args, **kwargs)


def ishg(hFigure=None, **kwargs):
    """
% does the swplot figure uses hgtransform
%
% ### Syntax
%
% `ishg = swplot.ishg`
%
% `ishg = swplot.ishg(hFigure)`
%
% ### Description
%
% `ishg = swplot.ishg` `true` if the active swplot figure uses
% [matlab.hgtransfrom], otherwise `false`.
%
% `ishg = swplot.ishg(hFigure)` applies to the swplot figure referenced by
% the `hFigure` handle.
%
% ### See Also
%
% [swplot.figure]
%
    """
    args = tuple(v for v in [hFigure] if v is not None)
    return m.swplot.ishg(*args, **kwargs)


def getdata(*args, **kwargs):
    """
% gets the data stored in an swplot figure
%
% ### Syntax
%
% `data = swplot.getdata`
%
% `data = swplot.getdata(hFigure)`
%
% `data = swplot.getdata(field)`
%
% ### Description
%
% `data = swplot.getdata` gets all the object data stored in the active
% swplot figure.
%
% `data = swplot.getdata(hFigure)` get all object data stored in the swplot
% figure identified by the `hFigure` handle.
%
% `data = swplot.getdata(field)` loads only the given field of the data
% structure.
%
% ### Examples
%
% This example shows how the data of all objects on a 3D SpinW plot can be
% retrieved.
%
% ```
% >>model = sw_model('triAF',1)
% >>plot(model)
% >>swplot.getdata>>
% ```
%
% ### Input Arguments
%
% `hFigure`
% : Handle of the swplot figure, default value is the active figure.
%
% `field`
% : String, determines the requested field name. If omitted, all
%   stored fields are returned.
%
% ### See Also
%
% [matlab.getappdata]
%
    """
    
    return m.swplot.getdata(*args, **kwargs)


def cylinder(*args, **kwargs):
    """
% creates a closed/open 3D cylinder patch
%
% ### Syntax
%
% `hPatch = swplot.cylinder(rStart, rEnd, R)`
%
% `hPatch = swplot.cylinder(rStart, rEnd, R, nPatch, close)`
%
% `hPatch = swplot.cylinder(handle, ...)`
%
% ### Description
%
% `hPatch = swplot.cylinder(rStart, rEnd, R)` generates multiple cylinders
% with a single triangular patch command. The cylinders are defined by
% start and end positions and their radii.
%
% `hPatch = swplot.cylinder(rStart, rEnd, R, nPatch, close)` creates
% cylinders with $4 n_{patch}$ number of patch faces per arrow.
%
% Handle can be the handle of an axes object or a patch object. It either
% selects an axis to plot or a patch object (triangulated) to add vertices
% and faces.
%
% ### Examples
%
% Draw 100 random cylinders within the $(\pm 1,\pm 1,\pm 1)$ cube:
%
% ```
% >>swplot.figure
% >>N = 100;
% >>swplot.cylinder(2*rand(3,N)-1,2*rand(3,N)-1,0.1,100,true)
% >>swplot.zoom(30)
% >>snapnow
% ```
%
% ### Input Arguments
%
% `handle`
% : Handle of an axis or patch object. In case of [matlab.patch] object,
%   the constructed faces will be added to the existing object instead of
%   creating a new one.
%
% `rStart`
% : Coordinate of the starting point or multiple starting points in a
%   matrix with dimensions $[3\times n_{obj}]$.
%
% `rEnd`
% : Coordinate of the end point or multiple end points in a
%   matrix with dimensions $[3\times n_{obj}]$.
%
% `R`
% : Radius of the arrow body, scalar.
%
% `nPatch`
% : Number of points on the circle of the body, default value is stored in
%   `swpref.getpref('npatch')`. The final patch object will have
%   $4n_{patch}$ number of faces and $2n_{patch}$ number of vertices.
%
% `close`
% : If `true` the cylinder is closed at both ends. Default is `true`.
%
% ### See Also
%
% [swplot.arrow]
%
    """
    
    return m.swplot.cylinder(*args, **kwargs)


def export(*args, **kwargs):
    """
% exports swplot figure into raster/vector image
%
% ### Syntax
%
% `swplot.export(Name,Value)`
%
% ### Description
%
% `swplot.export(Name,Value)` exports an swplot figure into a raster/vector
% image. The function will remove the tooltip before exporting to raster
% image. For vector graphics, also the legend will be removed as it causes
% a bug in the Matlab [matlab.print] command. Also, vector graphics export
% does not support transparency, thus all transparency will be removed from
% the figure. Be careful, the vector image filesize can be quite large if
% there are many object on the figure. To reduce the file size, try
% reducing the $n_{patch}$ and $n_{mesh}$ values to reduce the number of
% faces per object. The function uses the Matlab built-in [matlab.print]
% command after preparing the figure. All figure property restored after
% export.
%
% ### Name-Value Pair Arguments
%
% `'figure'`
% : Handle of the swplot figure. Default value is the active figure.
%
% `'filename'`
% : String, name of the image file. Image type will be determined
%   based on the extension. Supported graphics formats:
%   * `png`    Raster image.
%   * `eps`    Vector image.
%
%   If no filename provided, the function returns without printing.
%
% `'res'`
% : Resolution for raster images in dpi, default value is 300. Set
%   it to 0, to save the image with the screen resolution.
%
% ### See Also
%
% [matlab.print]
%
    """
    
    return m.swplot.export(*args, **kwargs)


def logo(*args, **kwargs):
    """
% creates the SpinW logo
%
% ### Syntax
%
% `swplot.logo`
%
% `swplot.logo(fName)`
%
% ### Description
%
% `swplot.logo` creates and displays the SpinW logo with credentials. The
% logo is using an honest colormap [cm_inferno] and removed the tiles of
% the sine wave to symbolize the increase of quality of code (measured as a
% number of eliminated for loops) :D The logo is used for SpinW 3.0.
% Colormap is expected to change for every major version jump.
%
% ### Examples
%
% This is the logo:
%
% ```
% >>swplot.logo
% >>snapnow
% ```
%
% ### Input Arguments
%
% `fName`
% : File name to save the logo. Optional, if not given the logo
%   will be shown in a new figure.
%
% ### See Also
%
% [spinw]
%
    """
    
    return m.swplot.logo(*args, **kwargs)


def subfigure(m=None, n=None, p=None, hFigure=None, **kwargs):
    """
% changes position of figure window on the screen
%
% ### Syntax
%
% `swplot.subfigure(m,n,p)`
%
% `swplot.subfigure(m,n,p,hFigure)`
%
% ### Description
%
% `swplot.subfigure(m,n,p)` changes the position of the current figure
% window on the screen, the position is determined similarly to the Matlab
% function [matlab.subplot]. Here the screen is the canvas where the figure
% window is positioned.
%
% The function divides the display into an $m$-by-$n$ grid and moves the
% figure window in the position specified by $p$. It numbers the figures by
% row major, such that the first figure is the first column of the first
% row, the second figure is the second column of the first row, and so on.
%
% `swplot.subfigure(m,n,p,hFigure)` repositions the figure related to
% `hFigure` handle.
%
% ### Input Arguments
%
% `m,n,p`
% : Integer numbers that define the figure window position.
%
% `hFigure`
% : Handle of the figure window, optional. Default value is [matlab.gcf].
%
    """
    args = tuple(v for v in [m, n, p, hFigure] if v is not None)
    return m.swplot.subfigure(*args, **kwargs)


def delete(*args, **kwargs):
    """
% deletes objects and corresponding data from swplot figure
%
% ### Syntax
%
% `swplot.delete(objID)`
%
% `swplot.delete(hFigure,objID)`
%
% ### Description
%
% `swplot.delete(objID)` deletes objects and their data that corresponds to
% the given unique `objID` (integer number) on the active swplot figure.
%
% `swplot.delete(hFigure,objID)` deletes objects from the swplot figure
% corresponding to `hFigure` handle.
%
% If `objID` equals to 0, all objects will be deleted from the swplot
% figure.
%
% ### See Also
%
% [swplot.figure] \| [swplot.add]
%
    """
    
    return m.swplot.delete(*args, **kwargs)


def zoom(mode=None, hFigure=None, **kwargs):
    """
% zooms to objects
%
% ### Syntax
%
% `swplot.zoom(mode)`
%
% `swplot.zoom(mode, hFigure)`
%
% ### Description
%
% `swplot.zoom(mode)` controls the zoom (angle of view of the virtual
% camera) level on the active [swplot] figure.
%
% `swplot.zoom(mode, hFigure)` controls the zoom on the swplot figure
% referenced by the `hFigure` handle.
%
% ### Input Arguments
%
% `mode`
% : Either a number determining the relative zoom value, or `'auto'`
%   that zooms to fit every object into the figure.
%
% `hFigure`
% : Handle of the swplot figure, default value is the active swplot figure.
%
% ### See Also
%
% [swplot.figure]
%
    """
    args = tuple(v for v in [mode, hFigure] if v is not None)
    return m.swplot.zoom(*args, **kwargs)


def tooltipstring(swObject=None, obj=None, **kwargs):
    """
% generates tooltip text
%
% ### Syntax
%
% `swplot.tooltipstring(swObject,[])`
%
% `swplot.tooltipstring(swObject,obj)`
%
% ### Description
%
% `swplot.tooltipstring(swObject)` generates tooltip string from the data
% of a graphical object.
%
% ### Input Arguments
%
% `swObject`
% : Struct, that contains the object data that is clicked on.
%
% `obj`
% : [spinw] object that provides data to the tooltip text, optional.
%
    """
    args = tuple(v for v in [swObject, obj] if v is not None)
    return m.swplot.tooltipstring(*args, **kwargs)


def translate(mode=None, hFigure=None, **kwargs):
    """
% translates objects on swplot figure
%
% ### Syntax
%
% `swplot.translate(mode)`
%
% `swplot.translate(mode, hFigure)`
%
% ### Description
%
% `swplot.translate(mode)` translates the objects of an active swplot
% figure, where the coordinate system is defined by the plane of the figure
% with horizontal $x$-axis, vertical $y$-axis and out-of-plane $z$-axis.
%
% `swplot.translate(mode, hFigure)` acts on the figure referenced by the
% `hFigure` handle.
%
% ### Input Arguments
%
% `mode`
% : Either a vector with three numbers that determine the translation
%   vector in the figure plane coordinate system, or `'auto'` that
%   centers figure to the middle of the objects. Default value is `'auto'`.
%
% `hFigure`
% : Handle of the swplot figure, default value is the active figure.
%
% ### See Also
%
% [swplot.zoom]
%
    """
    args = tuple(v for v in [mode, hFigure] if v is not None)
    return m.swplot.translate(*args, **kwargs)


def plotion(*args, **kwargs):
    """
% plots magnetic ion properties
%
% ### Syntax
%
% `swplot.plotion(Name,Value)`
%
% `hFigure = swplot.plotion(Name,Value)`
%
% ### Description
%
% `swplot.plotion(Name,Value)` visualizes selected properties of magnetic
% ions stored in a [spinw] object onto an swplot figure. The supported
% properties are the g-tensor and single ion anisotropy.
%
% ### Name-Value Pair Arguments
%
% `'mode'`
% : String that defines the type of property that is visualized:
%   * `'aniso'`     ellipsoid is plotted to visualize single ion anisotropy,
%   * `'g'`     	ellipsoid is plotted to visualize g-tensor.
%
% `'scale'`
% : Scaling factor for the size of the ellipsoid relative to the
%   shortest bond length. Default value is 1/3.
%
% `'alpha'`
% : Transparency (alpha value) of the ellipsoid (1 for opaque, 0 for
%   transparent), default value is 0.3.
%
% `'radius1'`
% : Minimum radius of the ellipsoid, default value is 0.08 \\ang.
%
% `'lineWidth'`
% : Line width in pt of the main circles surrounding the ellipsoid,
%   if zero no circles are drawn. Default is 0.5 pt.
%
% `'color'`
% : Color of the ellipsoid, one of the following values:
%   * `'auto'`      all ellipsoids get the color of the central atom,
%   * `'colorname'` all ellipsoids will have the same color defined by the
%                   string, e.g. `'red'`,
%   * `[R G B]`     all ellipsoids will have the same color defined by the RGB
%                   code.
% `'color2'`
% : Color of the lines of the main circles, default value is `'auto'` when
%   the ellipses will have the same color as the ellipsoids. Can be either
%   a row vector of RGB code or string of a color name, see the `color`
%   parameter.
%
% #### General paraters
%
% These parameters have the same effect on any of the `swplot.plot...`
% functions.
%
% `'obj'`
% : [spinw] object.
%
% `'unit'`
% : Unit in which the plotting range is defined. It can be one of the
%   following strings:
%   * `'lu'`        plot range is defined in lattice units (default),
%   * `'xyz'`       plot range is defined in the $xyz$ Cartesian coordinate
%                   system in \\ang units.
%
% `'range'`
% : Defines the plotting range. Depending on the `unit` parameter, the
%   given range can be in lattice units or in units of the $xyz$ Cartesian
%   coordinate system. It is either a matrix with dimensions of $[3\times
%   2]$ where the first and second columns define the lower and upper plot
%   limits respectively. It can be alternatively a vector with three
%   elements `[a,b,c]` which is equivalent to `[0 a;0 b;0 c]`. Default
%   value is `[0 1;0 1;0 1]` to show a single cell.
%
% `'figure'`
% : Handle of the swplot figure. Default value is the active figure handle.
%
% `'legend'`
% : Whether to show the plot on the legend, default value is `true`.
%
% `'tooltip'`
% : If `true`, the tooltips will be shown when clicking on the plot
%   objects. Default value is `true`.
%
% `'shift'`
% : Column vector with 3 elements, all object positions will be
%   shifted by the given value in \\ang units. Default value is
%   `[0;0;0]`.
%
% `'replace'`
% : If `true` the plot will replace the previous plot of the same type.
%   Default value is `true`.
%
% `'translate'`
% : If `true`, the plot will be centered, independent of the range. Default
%   value is `false`.
%
% `'zoom'`
% : If `true`, the swplot figure will be zoomed to make the plot objects
%   cover the full figure. Default is `true`.
%
% `'copy'`
% : If `true`, a clone of the [spinw] object will be saved in the
%   swplot figure data which can be retwrived using
%   `swplot.getdata('obj')`. If `false`, the handle of the original [spinw]
%   object is saved which is linked to the input `obj` and so it changes
%   when `obj` is changed. Default value is `false`.
%
% `nMesh`
% : Mesh of the ellipse surface, a triangulation class object or an
%   integer that used to generate an icosahedron mesh with $n_{mesh}$
%   number of additional subdivision into triangles. Default value is
%   stored in `swpref.getpref('nmesh')`, see also [swplot.icomesh].
%
% `nPatch`
% : Number of vertices on any patch object that is not the icosahedron,
%   default value is stored in `swpref.getpref('npatch')`.
%
% ### Output Arguments
%
% `hFigure`
% : Handle of the swplot figure.
%
% The name of the objects that are created are `'ion'` and `'ion_edge'`.
% To find the handles and the corresponding data on these objects, use e.g.
% sObject = swplot.findobj(hFigure,'name','ion')`.
%
    """
    
    return m.swplot.plotion(*args, **kwargs)


def plotbond(*args, **kwargs):
    """
% plots bonds
%
% ### Syntax
%
% `swplot.plotbond(Name,Value)`
%
% `hFigure = swplot.plotbond(Name,Value)`
%
% ### Description
%
% `swplot.plotbond(Name,Value)` plots the magnetic bonds stored in
% [spinw.coupling]. It can plot bonds using different styles, such as
% arrows, lines or cylinders and allows controlling the the line style,
% cylinder radius, color, etc. The command can also plot cylinders with
% radii that are dependent on the strength of the exchange interaction
% assigned to the particular bond.
%
% ### Name-Value Pair Arguments
%
% `'mode'`
% : String that defines the style of the bond:
%   * `'cylinder'`   bonds are plotted as cylinders connecting the two atoms
%                   (default),
%   * `'arrow'`      bonds are plotted as arrows (default if DM
%                   interactions are present),
%   * `'line'`       bonds are plotted as lines,
%   * `'empty'`      no bonds are plotted.
%
% `'mode2'`
% : String that defines what object is plotted on the middle of the bond:
%   * `'none'`      don't plot anything on the bond (default),
%   * `'antisym'`   plot the antisymmetric part (DM vector) of the
%                   exchange on the middle point of the bond
%                   (default if DM vectors are non-zero),
%   * `'sym'`       plot an ellipsoid (corresponding to the symmetric
%                   exchange) on the middle of the bond.
%
% `'sign'`
% : String that defines how the ellipsoids are generated for exchange
%   matrices that contain both negative and positive eigenvalues.
%   Possible values are:
%   * `'abs'`       The absolute value of the eigenvalues is used,
%                   this works nicely except that AFM and FM values
%                   will have the same radius (default).
%   * `'min'`       If there is a negative eigenvalue, it is
%                   shifted to zero with all other egeinvalues
%                   equally. This works nicely to emphasize AFM
%                   type values in the exchange matrix. Problem is
%                   that 0 exchange values can be assigned non-zero
%                   radius.
%   * `'max'`       Same as `'min'`, except the positive eigenvalues are
%                   shifted to zero. This works nicely to emphasize
%                   FM type exchange values, has the same problem
%                   as the `'min'` option.
%
% `'linewidth'`
% : Defines the bond radius if `mode` is set to `line`, one of the folling
%   strings:
%   * `'fix'`       All lines will have a width defined by the `linewidth0`
%                   parameter (default).
%   * `'lin'`       Lines will have a width that is depending
%                   linearly on the exchange matrix on the bond:
%                          `~Width ~ sum(abs(J))`,
%                   where the largest line width on
%                   the strongest bond is given by `linewidth0`.
%   * `'pow'`       Same as `'auto'`, but the line width is a
%                   power function of the exchange value:
%                   `W~(sum(abs(J))).^widthpow`.
%
% `'widthpow'`
% : Defines the power that determines the linewidth if `linewidth`
%   parameter is set to `'pow'`.
%
% `'linewidth0'`
% : Line width in pt used to draw the bond if `mode` parameter is `'line'`.
%   Default value is 0.5.
%
% `'lineStyle'`
% : Determines the line style when `mode` parameter is `'line'`. Possible
%   values are:
%   * `'auto'`      Bonds are plotted as continuous/dashed lines
%                   depending on the label of the corresponding
%                   matrix (dashed line is used if the matrix
%                   label ends with `'-'`, otherwise continuous) (default).
%   * `'--'`        Bonds are plotted as dashed lines.
%   * `'-'`         Bonds are plotted as lines.
%   * `':'`         Bonds are plotted using dotted lines.
%   * `'-.'`        Bonds are plotted using dash-dotted lines.
%
% `'zero'`
% : If `true`, bonds with zero exchange matrix will be plotted as
%   well. Default value is `true`.
%
% `'radius0'`
% : Radius of the cylinder when `mode` parameter is set to `'cylinder'`.
%   Default value is 0.05 \\ang.
%
% `'radius1'`
% : Radius of the DM vector and the minimum radius of the
%   ellipsoid, default value is 0.08 \\ang.
%
% `'radius2'`
% : Constant atom radius, default value is 0.3 \\ang.
%
% `'radius'`
% : Defines the atom radius (important for arrow bonds, to avoid
%   overlap with the spheres of the atoms), see [swplot.plotatom]:
%   * `'fix'`       Sets the radius of all atoms to the value
%                   given by the `radius2` parameter.
%   * `'auto'`      use radius data from database based on the atom
%                   label multiplied by the `radius2` option value.
%
% `'ang'`
% : Angle of the arrow head in degree units, default value is 30\\deg.
%
% `'lHead'`
% : Length of the arrow head, default value is 0.3 \\ang.
%
% `'scale'`
% : Scaling factor for the length of the DM vector or the size of
%   the ellipsoid relative to the shortest bond length. Default
%   value is 1/3.
%
% `'color'`
% : Color of the bonds, one of the following values:
%   * `'auto'`      all bonds gets the color stored in [spinw.matrix],
%   * `'colorname'` all bonds will have the same color defined by the
%                   string, e.g. `'red'`,
%   * `[R G B]`     all bonds will have the same color defined by the given
%                   RGB code.
%
% `'color2'`
% : Color of the ellipse or DM vector on the bond:
%   * `'auto'`      all object get the color of the bond,
%   * `'colorname'` all object will have the same color defined by the
%                   string, e.g. `'red'`,
%   * `[R G B]`     all objects will have the same color defined by the
%                   given RGB code.
%
% #### General paraters
%
% These parameters have the same effect on any of the `swplot.plot...`
% functions.
%
% `'obj'`
% : [spinw] object.
%
% `'unit'`
% : Unit in which the plotting range is defined. It can be one of the
%   following strings:
%   * `'lu'`        plot range is defined in lattice units (default),
%   * `'xyz'`       plot range is defined in the $xyz$ Cartesian coordinate
%                   system in \\ang units.
%
% `'range'`
% : Defines the plotting range. Depending on the `unit` parameter, the
%   given range can be in lattice units or in units of the $xyz$ Cartesian
%   coordinate system. It is either a matrix with dimensions of $[3\times
%   2]$ where the first and second columns define the lower and upper plot
%   limits respectively. It can be alternatively a vector with three
%   elements `[a,b,c]` which is equivalent to `[0 a;0 b;0 c]`. Default
%   value is `[0 1;0 1;0 1]` to show a single cell.
%
% `'figure'`
% : Handle of the swplot figure. Default value is the active figure handle.
%
% `'legend'`
% : Whether to show the plot on the legend, default value is `true`.
%
% `'tooltip'`
% : If `true`, the tooltips will be shown when clicking on the plot
%   objects. Default value is `true`.
%
% `'shift'`
% : Column vector with 3 elements, all object positions will be
%   shifted by the given value in \\ang units. Default value is
%   `[0;0;0]`.
%
% `'replace'`
% : If `true` the plot will replace the previous plot of the same type.
%   Default value is `true`.
%
% `'translate'`
% : If `true`, the plot will be centered, independent of the range. Default
%   value is `false`.
%
% `'zoom'`
% : If `true`, the swplot figure will be zoomed to make the plot objects
%   cover the full figure. Default is `true`.
%
% `'copy'`
% : If `true`, a clone of the [spinw] object will be saved in the
%   swplot figure data which can be retwrived using
%   `swplot.getdata('obj')`. If `false`, the handle of the original [spinw]
%   object is saved which is linked to the input `obj` and so it changes
%   when `obj` is changed. Default value is `false`.
%
% `nMesh`
% : Mesh of the ellipse surface, a triangulation class object or an
%   integer that used to generate an icosahedron mesh with $n_{mesh}$
%   number of additional subdivision into triangles. Default value is
%   stored in `swpref.getpref('nmesh')`, see also [swplot.icomesh].
%
% `nPatch`
% : Number of vertices on any patch object that is not the icosahedron,
%   default value is stored in `swpref.getpref('npatch')`.
%
% ### Output Arguments
%
% `hFigure`
% : Handle of the swplot figure.
%
% The name of the objects that are created are `'bond'`.
% To find the handles and the corresponding data on these objects, use e.g.
% sObject = swplot.findobj(hFigure,'name','bond')`.
%
% *[DM]: Dzyaloshinskii-Moriya
% *[FM]: FerroMagnet
% *[AFM]: AntiFerromagnet
%
    """
    
    return m.swplot.plotbond(*args, **kwargs)


def mouse(hFigure=None, perspective=None, **kwargs):
    """
% adds mouse callbacks to swplot figure
%
% ### Syntax
%
% `swplot.mouse`
%
% `swplot.mouse(hFigure, perspective)`
%
% ### Description
%
% `swplot.mouse` adds rotation and zoom functionality to the active swplot
% figure. The following mouse actions are supported:
% * `mouse-drag`        Rotation of objects.
% * `ctrl+mouse-drag`   Shift of objects (pan).
% * `mouse-wheel`       Zoom of objects.
% * `ctrl+mouse-wheel`  Change perspective and switch to perspective
%                       projection.
%
% ### Input Arguments
%
% `hFigure`
% : Handle of the swplot figure. Default is the active figure.
%
% `perspective`
% : String determines whether camera projection mode is changed
%   automatically between orthographic (zooming withouth ctrl
%   key pressed) and perspective (zooming with ctrl key
%   pressed):
%   * `'auto'`      Automatic switching (default).
%   * `'fix'`       No switching.
%
% ### See Also
%
% [matlab.camproj]
%
    """
    args = tuple(v for v in [hFigure, perspective] if v is not None)
    return m.swplot.mouse(*args, **kwargs)


def add(hAdd=None, hFigure=None, showtooltip=None, **kwargs):
    """
% adds a graphical object to an swplot figure
%
% ### Syntax
%
% `swplot.add(hAdd)`
%
% `swplot.add(hAdd,hFigure)`
%
% ### Description
%
% `swplot.add(hAdd)` adds a graphical object to the active swplot figure to
% enable continuous rotation with the mouse. The function adds the
% graphical objects to as a children to the [matlab.hgtransform].
%
% `swplot.add(hAdd,hFigure)` adds the graphical objects to the figure of
% the figure handle `hFigure`.
%
% ### Input Arguments
%
% `hAdd`
% : Either vector of the handles of the graphical objects, or
%   struct with $n_{obj}$ number of elements with a `handle` field each
%   containing a graphical object handle. The struct can contain any subset
%   of the following fields as well:
%   * `name`      Default value is `'general'` if not given. The
%                 name identifies groups of objects.
%   * `text`      Text that is shown in the tooltip when clicking
%                 on the object.
%   * `position`  Position of the object, see [swplot.plot] for
%                 details.
%    * `label`    Label that is shown in the legend.
%    * `legend`   Type of legend, see [swplot.legend] for details.
%    * `type`     Type of graphical object, see [swplot.plot].
%    * `data`     Arbitrary data assigned to the object.
%
% `hFigure`
% : The handle of the figure or number in the figure title. The
%   default value is the active swplot figure if `hFigure` is not given or
%   empty matrix.
%
% ### See Also
%
% [swplot] \| [swplot.figure] \| [matlab.hgtransform] \| [swplot.delete]
%
    """
    args = tuple(v for v in [hAdd, hFigure, showtooltip] if v is not None)
    return m.swplot.add(*args, **kwargs)


def figure(mode=None, **kwargs):
    """
% creates swplot figure
%
% ### Syntax
%
% `hFigure = swplot.figure`
%
% `hFigure = swplot.figure(mode)`
%
% ### Description
%
% `hFigure = swplot.figure` creates an empty figure with all the controls
% for modifying the plot and the 3D roation engine initialized that rotates
% the objects on the figure instead of the viewport. To plot anything onto
% the figure, the handle of the graphics object (after creating it using
% [matlab.surf], [matlab.patch], etc.) has to be added to the figure using
% the function [swplot.add].
%
% `hFigure = swplot.figure(mode)` defines settings for the figure.
%
% ### Input Arguments
%
% `mode`
% : Optional string. If `'nohg'`, then no hgtransform object will be
%   used for fine object rotation. Can be usefull for certain
%   export functions, that are incompatible with [matlab.hgtransform]
%   objects. Default value is `'hg'` to use hgtransform.
%
% ### See Also
%
% [swplot.add] \| [matlab.hgtransform]
%
    """
    args = tuple(v for v in [mode] if v is not None)
    return m.swplot.figure(*args, **kwargs)


def findobj(*args, **kwargs):
    """
% finds object data on swplot figure
%
% ### Syntax
%
% `sObj = swplot.findobj(Name,Value)`
%
% `sObj = swplot.findobj(hFigure,Name,Value)`
%
% ### Description
%
% `sObj = swplot.findobj(Name,Value)` finds graphical objects on the active
% swplot figure hFigure which have the given property name-value pairs. The
% possible property names are:
% * `handle`    Handle of the graphical object.
% * `objID`     Unique number of the object (increasing integer numbers).
% * `name`      Name of the object, identifies groups, such as `'atom'` for
%               all atoms.
% * `label`     Label of the objects, can identify types of atoms, etc.
%               it will accept sub strings, e.g. `'Cr'` parameter would
%               match both `'Cr1 Cr3+'` and `'Cr2 Cr3+'` labels.
%
% `sObj = swplot.findobj(hFigure,Name,Value)` search for objects on the
% swplot figure identified by the `hFigure` handle.
%
% ### Output Arguments
%
% `sObj`
% : Struct that contains all the data of the found objects.
%
% ### See Also
%
% [swplot.delete]
%
    """
    
    return m.swplot.findobj(*args, **kwargs)


def plotcell(*args, **kwargs):
    """
% plots unit cell
%
% ### Syntax
%
% `swplot.plotcell(Name,Value)`
%
% `hFigure = swplot.plotcell(Name,Value)`
%
% ### Description
%
% `swplot.plotcell(Name,Value)` plots the edges of the unit cell or
% multiple unit cells.
%
% ### Name-Value Pair Arguments
%
% `'mode'`
% : String that determines how the cells are plotted:
%   * `'inside'`    unit cells are plotted inside the volume defined by the
%                   given `range` parameter (default),
%   * `'single'`    a single unit cell is plotted at the origin,
%   * `'outside'`   unit cells are plotted inclusive the volume defined
%                   by the `range` parameter.
%
% `'color'`
% : Color of the edges of the cells, one of the following values:
%   * `'auto'`      all edges will be black,
%   * `'colorname'` all edges will have the same color defined by the
%                   string, e.g. `'red'`,
%   * `[R G B]`     all edges will have the same color defined by the RGB
%                   code.
%
% `'lineStyle'`
% : Determines the line style of the edges. Possible values are:
%   * `'--'`        dahsed edges (default),
%   * `'-'`         edges as continuous lines,
%   * `':'`         edges as dotted lines,
%   * `'-.'`        edges as dash-dotted lines.
%
% `'lineWdith'`
% : Line width of the edges, default value is 1 pt.
%
% #### General paraters
%
% These parameters have the same effect on any of the `swplot.plot...`
% functions.
%
% `'obj'`
% : [spinw] object.
%
% `'unit'`
% : Unit in which the plotting range is defined. It can be one of the
%   following strings:
%   * `'lu'`        plot range is defined in lattice units (default),
%   * `'xyz'`       plot range is defined in the $xyz$ Cartesian coordinate
%                   system in \\ang units.
%
% `'range'`
% : Defines the plotting range. Depending on the `unit` parameter, the
%   given range can be in lattice units or in units of the $xyz$ Cartesian
%   coordinate system. It is either a matrix with dimensions of $[3\times
%   2]$ where the first and second columns define the lower and upper plot
%   limits respectively. It can be alternatively a vector with three
%   elements `[a,b,c]` which is equivalent to `[0 a;0 b;0 c]`. Default
%   value is `[0 1;0 1;0 1]` to show a single cell.
%
% `'figure'`
% : Handle of the swplot figure. Default value is the active figure handle.
%
% `'legend'`
% : Whether to show the plot on the legend, default value is `true`.
%
% `'tooltip'`
% : If `true`, the tooltips will be shown when clicking on the plot
%   objects. Default value is `true`.
%
% `'shift'`
% : Column vector with 3 elements, all object positions will be
%   shifted by the given value in \\ang units. Default value is
%   `[0;0;0]`.
%
% `'replace'`
% : If `true` the plot will replace the previous plot of the same type.
%   Default value is `true`.
%
% `'translate'`
% : If `true`, the plot will be centered, independent of the range. Default
%   value is `false`.
%
% `'zoom'`
% : If `true`, the swplot figure will be zoomed to make the plot objects
%   cover the full figure. Default is `true`.
%
% `'copy'`
% : If `true`, a clone of the [spinw] object will be saved in the
%   swplot figure data which can be retwrived using
%   `swplot.getdata('obj')`. If `false`, the handle of the original [spinw]
%   object is saved which is linked to the input `obj` and so it changes
%   when `obj` is changed. Default value is `false`.
%
% `nMesh`
% : Mesh of the ellipse surface, a triangulation class object or an
%   integer that used to generate an icosahedron mesh with $n_{mesh}$
%   number of additional subdivision into triangles. Default value is
%   stored in `swpref.getpref('nmesh')`, see also [swplot.icomesh].
%
% `nPatch`
% : Number of vertices on any patch object that is not the icosahedron,
%   default value is stored in `swpref.getpref('npatch')`.
%
% ### Output Arguments
%
% `hFigure`
% : Handle of the swplot figure.
%
% The name of the objects `'cell'`.
% To find the handles and the corresponding data on these objects, use e.g.
% sObject = swplot.findobj(hFigure,'name','cell')`.
%
    """
    
    return m.swplot.plotcell(*args, **kwargs)


def tooltip(text0=None, hFigure=None, win=None, **kwargs):
    """
% creates tooltip
%
% ### Syntax
%
% `swplot.tooltip(switch)`
%
% `swplot.tooltip(switch,hFigure)`
%
% `swplot.tooltip(switch,hFigure,window)`
%
% `status = swplot.tooltip`
%
% ### Description
%
% `swplot.tooltip(switch)` creates/deletes the tooltip axis on the active
% swplot figure.
%
% `swplot.tooltip(switch,hFigure)` controls the tooltip on the swplot
% figure referenced by `hFigure` handle.
%
% `swplot.tooltip(switch,hFigure,window)` the `window` argument controls
% whether the tooltip is shown in a separate window of not.
%
% `status = swplot.tooltip` returns the tooltip status, one of the strings
% `'on'`\|`'off'`.
%
% ### Examples
%
% Add the tooltip to an [swplot] figure:
%
% ```
% swplot.figure
% swplot.addcircle([0 0 0],[0 0 1],1)
% swplot.tooltip
% ```
%
% ### Input Arguments
%
% `switch`
% : String, with recognised values of `'on'`\|`'off'` which switches the
%   tooltip on/off respectively. If it is any other string, the text will
%   be shown in the tooltip. Default value is 'on'.
%
% `hFigure`
% : Handle of the [swplot] figure. Default value is the active figure.
%
% `window`
% : If `true`, the tooltips will be shown in a separate window.
%   Default value is `false`.
%
% ### Output Arguments
%
% `status`
% : String, one of the `'on'`\|`'off'` values depending on the status of
%   the tooltip axis.
%
    """
    args = tuple(v for v in [text0, hFigure, win] if v is not None)
    return m.swplot.tooltip(*args, **kwargs)


def plot(*args, **kwargs):
    """
% plots objects to swplot figure
%
% ### Syntax
%
% `swplot.plot(Name,Value)`
%
% `hFigure = swplot.plot(Name,Value)`
%
% ### Description
%
% `swplot.plot(Name,Value)` plots objects to the swplot figure and adds the
% objects to the [matlab.hgtransform] object. This command enables the
% plotting of multiple objects simultaneously while enabling fine control
% of color, legend test, tooltip text etc. This commands is used by the
% [spinw.plot] high level plot command.
%
% ### Name-Value Pair Arguments
%
% `'type'`
% : Type of object to plot in a string. Possible options are:
%   * `'arrow'`         position specifies start and end points,
%   * `'ellipsoid'`     position specifies center,
%   * `'cylinder'`      position specifies start and end points,
%   * `'polyhedron'`    position specifies the vertices of the
%                       convex polyhedron or polygon,
%   * `'circle'`        position specifies center and normal vector,
%   * `'line'`          position specifies start and end points (or
%                       any number of points per curve),
%   * `'text'`          position specifies the center of the text.
%
% `'position'`
% : Position of the object/objects in a matrix with dimensions of
%   $[3\times n_{obj}\times 2]$ or $[3\times n_{obj}]$ or $[3\times
%   n_{obj}\times n_{point}]$ depending on the type of object. The unit of
%   the positions is determined by the `unit` parameter.
%
% `'name'`
% : String, the name of the object. It can be used for grouping the
%   object handles to enable easier search, see [swplot.findobj] for
%   details.
%
% `'text'`
% : Text to appear in the tooltip of the swplot figure after
%   clicking on the object. Can be a string that will be the same
%   for all objects, or a cell of strings for different text per
%   object. Default value is taken from the label option.
%
% `'label'`
% : Text to appear in the legend in a string for the same text of
%   all objects or strings in a cell with $n_{obj}$ number of elements for
%   multiple objects. Default value is taken from the `name` parameter.
%
% `'legend'`
% : Type of legend to show the object:
%   * `0`       do not show in legend,
%   * `1`       colored box in legend,
%   * `2`       dashed box in legend,
%   * `3`       colored sphere in legend.
%
% `'color'`
% : Color of objects, either a single color or as many colors as
%   many objects are given in a matrix with dimensions of $[3\times 1]$ or
%   $[3\times n_{obj}]$. Colors are RGB triplets with values between 0 and
%   255. Can be also string or cell of strings with the name of the colors,
%   for possible color names see [swplot.color]. Default value is `'red'`.
%
% `'alpha'`
% : Transparency of objects (1: non-transparent, 0: transparent)
%   defined as a single number for uniform transparency or as a
%   row vector with $n_{obj}$ number of elements to set transparency per object.
%   Default value is 1.
%
% `'unit'`
% : String that determines the coordinate system where position vectors are
%   defined:
%   * `'lu'`    Lattice units are used where the lattice is defined
%               by the stored basis (default).
%   * `'xyz'`   Use the original Matlab units.
%
% `'figure'`
% : Handle of the swplot figure, default is the active figure.
%
% `'R'`
% : Radius value of cylinder, sphere (if no `'T'` parameter is given) and
%   arrow, default value is 0.06.
%
% `'ang'`
% : Angle for arrow head in degree, default value is 15\\deg.
%
% `'lHead'`
% : Length of the arrow head, default value is 0.5.
%
% `'T'`
% : Transformation matrix that transforms a unit sphere to the
%   ellipse via: `R' = T(:,:,i)*R`, stored in a matrix with
%   dimensions of $[3\times 3\times n_{obj}]$.
%
% `'lineStyle'`
% : Line style, default value is `'-'` for continuous lines. It can
%   be also a vector with as many elements as many line segments.
%   In this case the numbers are equivalent to the following style
%   format string:
%   * `1`   `'-'`,
%   * `2`   `'--'`,
%   * `3`   `'-.'`,
%   * `4`   `':'`,
%   * `5`   `'none'`.
%
% `'lineWidth'`
% : Line width, default value is 0.5, can be a vector with $n_{obj}$
%   columns for different width per line segment.
%
% `'fontSize'`
% : Font size of text in pt when `type` parameter is set to `'text'`.
%   Default value is stored in `swpref.getpref('fontsize')`.
%
% `'nMesh'`
% : Resolution of the ellipse surface mesh. Integer number that is
%   used to generate an icosahedron mesh with `nMesh` number of
%   additional subdivision of triangular surfaces. Default value is stored in
%   `swpref.getpref('nmesh')`.
%
% `'nPatch'`
% : Number of points on the curve for arrow and cylinder, default
%   value is stored in `swpref.getpref('npatch')`.
%
% `'tooltip'`
% : If `true`, the tooltip will be switched on after the
%   plot. Default is `true`.
%
% `'replace'`
% : If `true`, all objects with the same name as the new plot will be
%   deleted before plotting. Default is `false`.
%
% `'data'`
% : User supplied data per object that will be stored in the swplot
%   figure and can be retrieved using [swplot.getdata]. It is stored in a
%   cell with $n_{obj}$ number of elements.
%
% `'translate'`
% : If `true`, the average center of the plot objects will be translated to
%   the figure center. Default is `true`.
%
% `'zoom'`
% : If `true`, the swplot figure will be zoomed to make the plot objects
%   cover the full figure. Default is `true`.
%
% ### See Also
%
% [swplot.color] \| [swplot.add]
%
    """
    
    return m.swplot.plot(*args, **kwargs)


def activefigure(*args, **kwargs):
    """
% returns the handle of the active swplot figure
%
% ### Syntax
%
% `hFigure = swplot.activefigure`
%
% `swplot.activefigure(hFigure)`
%
% ### Description
%
% `hfigure = swplot.activefigure` returns the handle of the active swplot
% figure and makes it selected. If no swplot figure exists, the function
% throws an error.
%
% `swplot.activefigure(hFigure)` makes the figure of `hFigure` handle the
% active figure.
%
% ### Input Arguments
%
% `hFigure`
% : Figure handle or figure number.
%
% ### Output Arguments
%
% `hFigure`
% : Handle of the active swplot figure.
%
% ### See Also
%
% [swplot.figure]
%
    """
    
    return m.swplot.activefigure(*args, **kwargs)


def view(ax=None, hFigure=None, **kwargs):
    """
% controls the 3D view direction
%
% ### Syntax
%
% `swplot.view(ax)`
%
% `swplot.view(ax, hFigure)`
%
% ### Description
%
% `swplot.view(ax)` controls the plane that the camera sees. The
% preconfigured options are pairs of $abc$ axes or $hkl$ reciprocal lattice
% axes.
%
% ### Input Arguments
%
% `ax`
% : String that controls the view plane, recognised values are:
%   * `'ab'`\|`'bc'`\|`'ac'`  the two axes define the view plane,
%   * `'hk'`\|`'kl'`\|`'hl'`  the two reciprocal lattice vectors define
%                             the view plane.
%
% `hFigure`
% : Handle of the swplot figure window, default value is the active swplot
%   figure.
%
    """
    args = tuple(v for v in [ax, hFigure] if v is not None)
    return m.swplot.view(*args, **kwargs)


def text(*args, **kwargs):
    """
% creates text at a 3D position
%
% ### Syntax
%
% `hText = swplot.text(r, string)`
%
% `hText = swplot.text(r, string, fontSize)`
%
% `hText = swplot.text(handle, ...)`
%
% ### Description
%
% `hText = swplot.text(r, string)` creates single or multiple text in 3D
% space.
%
% `hPatch = swplot.text(handle, ...)` adds the generated text object to a
% given axis referenced by `handle`.
%
% ### Input Arguments
%
% `handle`
% : Handle of an axis object, default value is [matlab.gca].
%
% `r`
% : Coordinate of the center of the text for a single text or
%   matrix with dimensions $[3\times n_{obj}]$ for multiple text.
%
% `string`
% : String that contains the text or cell of strings when multiple
%   text is drawn.
%
% `fontSize`
% : Font size in pt, default value is stored in `swpref.getpref('fontsize')`.
%
% ### See Also
%
% [matlab.text]
%
    """
    
    return m.swplot.text(*args, **kwargs)


def plotatom(*args, **kwargs):
    """
% plots crystal structure
%
% ### Syntax
%
% `swplot.plotatom(Name,Value)`
%
% `hFigure = swplot.plotatom(Name,Value)`
%
% ### Description
%
% `swplot.plotatom(Name,Value)` plots the crystal structure of a SpinW
% object onto an swplot figure where each atom is shown as a sphere. It can
% display text labels, control the radius and color of the spheres.
%
% `hFigure = swplot.plotatom(Name,Value)` returns the handle of the swplot
% figure.
%
% ### Name-Value Pair Arguments
%
% `'mode'`
% : String that defines the types of atoms to plot:
%   * `'all'`       plot all atoms (default),
%   * `'mag'`       plot magnetic atoms only,
%   * `'nonmag'`    plot non-magnetic atoms only.
%
% `'label'`
% : Whether to plot the labels of the atoms, default value is `false`.
%
% `'dText'`
% : Distance between the atom and its text label, default value is 0.1
%   \\ang.
%
% `'fontSize'`
% : Font size of the atom labels in pt, default value is read using
%   `swpref.getpref('fontsize')`.
%
% `'radius'`
% : Defines the atom radius, one of the following strings:
%   * `'fix'`       Sets the radius of all atoms to the value
%                   of the `radius0` parameter,
%   * `'auto'`      determine the atom radius based on the atom
%                   label (e.g. the radius of Cr atom is
%                   `sw_atomdata('Cr','radius')`) and multiply the value by
%                   the `radius0` parameter.
%
% `'radius0'`
% : Constant atom radius, default value is 0.3 \\ang.
%
% `'color'`
% : Color of the atoms, one of the following values:
%   * `'auto'`      all atom gets the color stored in [spinw.unit_cell],
%   * `'colorname'` all atoms will have the same color defined by the
%                   string, e.g. `'red'`,
%   * `[R G B]`     all atoms will have the same color defined by the RGB
%                   code.
%
% #### General paraters
%
% These parameters have the same effect on any of the `swplot.plot...`
% functions.
%
% `'obj'`
% : [spinw] object.
%
% `'unit'`
% : Unit in which the plotting range is defined. It can be one of the
%   following strings:
%   * `'lu'`        plot range is defined in lattice units (default),
%   * `'xyz'`       plot range is defined in the $xyz$ Cartesian coordinate
%                   system in \\ang units.
%
% `'range'`
% : Defines the plotting range. Depending on the `unit` parameter, the
%   given range can be in lattice units or in units of the $xyz$ Cartesian
%   coordinate system. It is either a matrix with dimensions of $[3\times
%   2]$ where the first and second columns define the lower and upper plot
%   limits respectively. It can be alternatively a vector with three
%   elements `[a,b,c]` which is equivalent to `[0 a;0 b;0 c]`. Default
%   value is `[0 1;0 1;0 1]` to show a single cell.
%
% `'figure'`
% : Handle of the swplot figure. Default value is the active figure handle.
%
% `'legend'`
% : Whether to show the plot on the legend, default value is `true`.
%
% `'tooltip'`
% : If `true`, the tooltips will be shown when clicking on the plot
%   objects. Default value is `true`.
%
% `'shift'`
% : Column vector with 3 elements, all object positions will be
%   shifted by the given value in \\ang units. Default value is
%   `[0;0;0]`.
%
% `'replace'`
% : If `true` the plot will replace the previous plot of the same type.
%   Default value is `true`.
%
% `'translate'`
% : If `true`, the plot will be centered, independent of the range. Default
%   value is `false`.
%
% `'zoom'`
% : If `true`, the swplot figure will be zoomed to make the plot objects
%   cover the full figure. Default is `true`.
%
% `'copy'`
% : If `true`, a clone of the [spinw] object will be saved in the
%   swplot figure data which can be retwrived using
%   `swplot.getdata('obj')`. If `false`, the handle of the original [spinw]
%   object is saved which is linked to the input `obj` and so it changes
%   when `obj` is changed. Default value is `false`.
%
% `nMesh`
% : Mesh of the ellipse surface, a triangulation class object or an
%   integer that used to generate an icosahedron mesh with $n_{mesh}$
%   number of additional subdivision into triangles. Default value is
%   stored in `swpref.getpref('nmesh')`, see also [swplot.icomesh].
%
% `nPatch`
% : Number of vertices on any patch object that is not the icosahedron,
%   default value is stored in `swpref.getpref('npatch')`.
%
% ### Output Arguments
%
% `hFigure`
% : Handle of the swplot figure.
%
% The name of the objects that are created are `'atom'` and `'atom_label'`.
% To find the handles and the corresponding data on these objects, use e.g.
% sObject = swplot.findobj(hFigure,'name','atom')`.
%
    """
    
    return m.swplot.plotatom(*args, **kwargs)


def plotbase(*args, **kwargs):
    """
% plots basis vectors
%
% ### Syntax
%
% `swplot.plotbase(Name,Value)`
%
% `hFigure = swplot.plotbase(Name,Value)`
%
% ### Description
%
% `swplot.plotbase(Name,Value)` plots the three basis vectors that define
% the coordinate system of the plot, either the $abc$ lattice vectors,
% $xyz$ Descartes coodinate system or the $hkl$ reciprocal lattice vectors.
%
% ### Name-Value Pair Arguments
%
% `'mode'`
% : String that determines the type of basis vectors to plot. Possible
%   values are:
%   * `abc`     plots the lattice vectors (default),
%   * `hkl`     plots the reciprocal lattice vectors,
%   * `xyz`     plots the $xyz$ Descartes coordinate system.
%
% `'length'`
% : Determines the length of the 3 basis vectors. If 0, the
%   length won't be rescaled. If non-zero, the `length` parameter
%   determines the length of the plotted vectors in \\ang. Default value is
%   2 \\ang.
%
% `'label'`
% : Logical variable, plots the vector labels if `true`. Default value is
%   `true`.
%
% `'color'`
% : Color of the arrows, either a cell of three color name strings or a
%   matrix with dimensions of ${3\times 3]$ where each column defines the
%   RGB values of a color. Default value is `{'red' 'green' 'blue'}`.
%
% `'R'`
% : Radius of the arrow body, default value is 0.06 \\ang.
%
% `'alpha'`
% : Head angle of the arrow in degree units, default value is 30\\deg.
%
% `'lHead'`
% : Length of the arrow head, default value is 0.5 \\ang.
%
% `'d'`
% : Distance from origin in $xyz$ units, default value is `[1 1 1]`.
%
% `'dtext'` : Distance of the label from the arrow in xyz units, default
%   value is 0.5 \\ang.
%
% #### General paraters
%
% These parameters have the same effect on any of the `swplot.plot...`
% functions.
%
% `'obj'`
% : [spinw] object.
%
% `'figure'`
% : Handle of the swplot figure. Default value is the active figure handle.
%
% `'tooltip'`
% : If `true`, the tooltips will be shown when clicking on the plot
%   objects. Default value is `true`.
%
% `'shift'`
% : Column vector with 3 elements, all object positions will be
%   shifted by the given value in \\ang units. Default value is
%   `[0;0;0]`.
%
% `'replace'`
% : If `true` the plot will replace the previous plot of the same type.
%   Default value is `true`.
%
% `'translate'`
% : If `true`, the plot will be centered, independent of the range. Default
%   value is `false`.
%
% `'zoom'`
% : If `true`, the swplot figure will be zoomed to make the plot objects
%   cover the full figure. Default is `true`.
%
% `'copy'`
% : If `true`, a clone of the [spinw] object will be saved in the
%   swplot figure data which can be retwrived using
%   `swplot.getdata('obj')`. If `false`, the handle of the original [spinw]
%   object is saved which is linked to the input `obj` and so it changes
%   when `obj` is changed. Default value is `false`.
%
% `nPatch`
% : Number of vertices on any patch object that is not the icosahedron,
%   default value is stored in `swpref.getpref('npatch')`.
%
    """
    
    return m.swplot.plotbase(*args, **kwargs)


def circle(*args, **kwargs):
    """
% creates a 3D circle surface patch
%
% ### Syntax
%
% `hPatch = swplot.circle(r0, n, R)`
%
% `hPatch = swplot.circle(r0, n, R, nPatch)`
%
% `hPatch = swplot.circle(handle, ...)`
%
% ### Description
%
% `hPatch = swplot.circle(r0, n, R)` creates a triangulated patch of a
% surface of a circle in 3D, defined by the center position, normal vector
% and radius.
%
% `hPatch = swplot.circle(handle, ...)` adds the patch object to a given axis
% if `handle` is an axis handle or adds the arrow to an existing
% [matlab.patch] object, if the given `handle` points to a patch object.
%
%
% ### Examples
%
% Draw 100 random unit circle surfaces with center at $(0,0,0)$ and random
% normal vector.
%
% ```
% >>swplot.figure
% >>N = 100
% >>swplot.circle(zeros(3,N),2*rand(3,N)-1,1)
% >>swplot.zoom(30)%
% >>snapnow
% ```
%
% ### Input Arguments
%
% `handle`
% : Handle of an axis or triangulated patch object. In case of patch
%   object, the constructed faces will be added to the existing object.
%
% `r0`
% : Center position of the circle in a column vector. Multiple circles can
%   be defined using a matrix with dimensions of $[3\times n_{obj}]$ where
%   each column defines a circle center.
%
% `n`
% : Column vector with 3 elements, normal to the circle surface. Multiple
%   circles can be defined using a matrix with the same dimensions as `r0`
%   parameter.
%
% `R`
% : Radius of the circle, scalar or row vector with $n_{obj}$ number of
%   elements.
%
% `nPatch`
% : Number of points on the circle circumference, default value is stored in
%   `swpref.getpref('npatch')`. The generated patch will contain
%   $n_{patch}$ number of faces and vertices.
%
% ### See Also
%
% [swplot.cylinder]
%
    """
    
    return m.swplot.circle(*args, **kwargs)


def plotmag(*args, **kwargs):
    """
% plots magnetic structure
%
% ### Syntax
%
% `swplot.plotmag(Name,Value)`
%
% `hFigure = swplot.plotmag(Name,Value)`
% ### Description
%
% `swplot.plotmag(Name,Value)` plots the magnetic structure stored in a
% [spinw] object onto an swplot figure. The magnetic structure is
% represented by arrows on the magnetic atoms.
%
% ### Name-Value Pair Arguments
%
% `'mode'`
% : String that defines the way the magnetic moments are plotted:
%   * `'all'`       Plot both the rotation plane of single-k incommensurate
%                   magnetic structures and the moment directions.
%   * `'circle'`    Plot only the rotation plane of incommensurate
%                   magnetic structures.
%   * `'arrow'`     Plots only the moment directions.
%
% `'label'`
% : Whether to plot labels for magnetic atoms, default value is `true`.
%
% `'dText'`
% : Distance between atom and its text label, default value is 0.1
%   \\ang.
%
% `'fontSize'`
% : Font size of the text labels in pt, default value is stored in
%   `swpref.getpref('fontsize')`.
%
% `'color'`
% : Color of the magnetic moment vectors, one of the following values:
%   * `'auto'`      all moments get the color of the magnetic atom,
%   * `'colorname'` all moments will have the same color defined by the
%                   string, e.g. `'red'`,
%   * `[R G B]`     all moments will have the same color defined by the RGB
%                   code.
%
% `'scale'`
% : Scaling factor for the lenght of the magnetic moments relative
%   to the length of the shortest bond (if there are no bonds, 3 \\ang
%   is taken as bond length). Default value is 0.4.
%
% `'normalize'`
% : If `true`, all moment length will be normalized to the scale
%   factor, default value is `false`.
%
% `'radius0'`
% : Radius value of arrow body, default value is 0.06 \\ang.
%
% `'ang'`
% : Angle of the arrow head in degree units, default value is 30 \\deg.
%
% `'lHead'`
% : Length of the arrow head, default value is 0.5 \\ang.
%
% `'alpha'`
% : Transparency (alpha value) of the circle, representing the
%   rotation plane of the moments, default value is 0.07.
%
% #### General paraters
%
% These parameters have the same effect on any of the `swplot.plot...`
% functions.
%
% `'obj'`
% : [spinw] object.
%
% `'unit'`
% : Unit in which the plotting range is defined. It can be one of the
%   following strings:
%   * `'lu'`        plot range is defined in lattice units (default),
%   * `'xyz'`       plot range is defined in the $xyz$ Cartesian coordinate
%                   system in \\ang units.
%
% `'range'`
% : Defines the plotting range. Depending on the `unit` parameter, the
%   given range can be in lattice units or in units of the $xyz$ Cartesian
%   coordinate system. It is either a matrix with dimensions of $[3\times
%   2]$ where the first and second columns define the lower and upper plot
%   limits respectively. It can be alternatively a vector with three
%   elements `[a,b,c]` which is equivalent to `[0 a;0 b;0 c]`. Default
%   value is `[0 1;0 1;0 1]` to show a single cell.
%
% `'figure'`
% : Handle of the swplot figure. Default value is the active figure handle.
%
% `'legend'`
% : Whether to show the plot on the legend, default value is `true`.
%
% `'tooltip'`
% : If `true`, the tooltips will be shown when clicking on the plot
%   objects. Default value is `true`.
%
% `'shift'`
% : Column vector with 3 elements, all object positions will be
%   shifted by the given value in \\ang units. Default value is
%   `[0;0;0]`.
%
% `'replace'`
% : If `true` the plot will replace the previous plot of the same type.
%   Default value is `true`.
%
% `'translate'`
% : If `true`, the plot will be centered, independent of the range. Default
%   value is `false`.
%
% `'zoom'`
% : If `true`, the swplot figure will be zoomed to make the plot objects
%   cover the full figure. Default is `true`.
%
% `'copy'`
% : If `true`, a clone of the [spinw] object will be saved in the
%   swplot figure data which can be retwrived using
%   `swplot.getdata('obj')`. If `false`, the handle of the original [spinw]
%   object is saved which is linked to the input `obj` and so it changes
%   when `obj` is changed. Default value is `false`.
%
% `nMesh`
% : Mesh of the ellipse surface, a triangulation class object or an
%   integer that used to generate an icosahedron mesh with $n_{mesh}$
%   number of additional subdivision into triangles. Default value is
%   stored in `swpref.getpref('nmesh')`, see also [swplot.icomesh].
%
% `nPatch`
% : Number of vertices on any patch object that is not the icosahedron,
%   default value is stored in `swpref.getpref('npatch')`.
%
% ### Output Arguments
%
% `hFigure`
% : Handle of the swplot figure.
%
% The name of the objects are `'mag'`.
% To find the handles and the corresponding data on these objects, use e.g.
% sObject = swplot.findobj(hFigure,'name','mag')`.
%
    """
    
    return m.swplot.plotmag(*args, **kwargs)


def transform(*args, **kwargs):
    """
% transforms objects on swplot figure
%
% ### Syntax
%
% `swplot.transform(T)`
%
% `swplot.transform(T, hFigure)`
%
% `T = swplot.transform'
%
% ### Description
%
% `swplot.transform(T)` transforms the objects on the active [swplot] figure
% using the transformation matrix `T`.
%
% `swplot.transform(T, hFigure)` transforms objects on the [swplot] figure
% referenced by the `hFigure` handle.
%
% `T = swplot.transform' returns the transfomation matrix of the active
% [swplot] figure.
%
% {{note If the figure is created without the `hgtransform` object, the
%   transformation matrix moves the camera.}}
%
% ### Input Arguments
%
% `M`
% : Transformation matrix with the following dimensions:
%   * $[4\times4]$      This follows the Matlab standard definition of coordinate transformations used by [matlab.hgtransform].
%   * $[3\times 4]$     This is the SpinW format for space group
%                       transformations, see [swsym.str].
%   * $[3\times 3]$     This defines a rotation matrix only.
%
%   Setting `M` to 0 returns the plot to the original orientation
%   (equivalent to `M=eye(4)`).
%
% `hFigure`
% : Handle of the swplot figure window, default value if the handle of the
%   active figure.
%
% ### Output Arguments
%
% `T`
% : Transformation matrix of the figure with dimensions of $[4\times 4]$.
%
% ### See Also
%
% [swplot.figure] \| [matlab.hgtransform]
%
    """
    
    return m.swplot.transform(*args, **kwargs)


def patchfacefcn(obj=None, hit=None, fun=None, selection=None, dLim=None, hTransform=None, **kwargs):
    """
% callback function for patch face selection
%
% ### Syntax
%
% `patchfacefcn(hPatch, hit, callbackFun, selection)`
%
% `patchfacefcn(hPatch, hit, callbackFun, selection, dLim)`
%
% ### Description
%
% `patchfacefcn(hPatch, hit, callbackFun, selection)` finds the index of the
% face in a patch object which was clicked on by the mouse. The function
% should be used as a callback function for the `ButtonDownFcn` event of
% the patch object and it will call a user defined function with the same
% arguments as the `ButtonDownFcn` call, plus adding an extra argument, the
% face index. Thus the user defined callback function needs to have the
% following header:
% ```
% callbackFun(hPatch,hit,faceIndex)
% ```
%
% The function can detect if the mouse click was on a face or on an edge of
% the patch object.
%
% `patchfacefcn(hPatch, hit, callbackFun, selection, dLim)` adds optional
% control on the selectivity whether the click was on a face of a patch
% object.
%
% ### Examples
%
% The color of any face of the red triangulated icosahedron will be
% changed from red to green if clicked on with the mouse.
%
% ```
% >>mesh = swplot.icomesh(1)
% >>V = mesh.X
% >>F = mesh.Triangulation
% >>hPatch = patch('Faces',F,'Vertices',V,'FaceColor','r','EdgeColor','none')
% >>axis equal
% >>axis off
% >>box on
% >>view(3)
% >>camlight('right')
% >>hPatch.FaceColor = 'flat'
% >>hPatch.FaceVertexCData = repmat([1 0 0],[size(F,1) 1])
% >>fun = @(hPatch,hif,face)set(hPatch,'FaceVertexCData',[hPatch.FaceVertexCData(1:(face-1),:); [0 1 0]; hPatch.FaceVertexCData((face+1):end,:)])
% >>hPatch.ButtonDownFcn = @(hPatch,hit)swplot.patchfacefcn(hPatch,hit,fun,'face')
% ```
%
% ### Input Arguments
%
% `hPatch`
% : Handle of the patch object.
%
% `hit`
% : Hit object that contains the point where the object was hit.
%
% `callbackFun`
% : User function that will be called in case of a click event
%     on `hPatch` object. It should have the following header:
%         `callbackFun(hPatch,hit,faceIndex)`
%     where `faceIndex` contains the index of the face that was
%     clicked on, it can contain a single index or more depending
%     on the selection type.
%
% `selection`
% : String, that defines three diferent selection criteria when the
%   `callbackfun()` function will be called:
%   * `'face'`  The `callbackFun()` will be triggered if a face
%               was clicked (`numel(faceIndex)==1`).
%   * `'edge'`  The `callbackfun()` will be triggered if an edge
%               is clicked (`numel(faceIndex)==2`).
%   * `'all'`   The `callbackfun()` will be triggered for both
%               faces and edges.
%
% `dLim`
% : Upper limit of the absolute value of the determinant that
%   determines whether a point is on a plane spanned by the two
%   edges of a triangle. Default value is $10^{-7}$ (tested).
%
% ### See Also
%
% [matlab.patch]
%
    """
    args = tuple(v for v in [obj, hit, fun, selection, dLim, hTransform] if v is not None)
    return m.swplot.patchfacefcn(*args, **kwargs)


def plotchem(*args, **kwargs):
    """
% plots polyhedra or chemical bonds
%
% ### Syntax
%
% `swplot.plotchem(Name,Value)`
%
% `hFigure = swplot.plotchem(Name,Value)`
%
% ### Description
%
% `swplot.plotchem(Name,Value)` plots polyhedra around selected atoms, or
% chemical bonds between atoms on an swplot figure.
%
% ### Name-Value Pair Arguments
%
% `'mode'`
% : String that selects the type of the plot, one of the following:
%   * `'poly'`      draws polyhedra around the center atoms
%                   (default),
%   * `'bond'`      draws bonds between the given atoms.
%
% `'atom1'`
% : Indices of atoms stored in [spinw.unit_cell] for the center atom
%   of the polyhedra or the first atom of the bonds. Can be also a
%   string that identifies the atoms by their labels.
%
% `'atom2'`
% : Indices or label of the atoms stored in [spinw.unit_cell]. It
%   determines the vertices of the polyhedra or gives the second
%   atom of a bond.
%
% `'extend'`
% : If `true`, the starting of the bonds or center of polyhedra will be
%   restricted within the given `range`, while the surrounding atoms or end
%   of bonds (defined by `atom2`) are not restricted. if `extend` is set to
%   `false`, only those bonds/polyhedra will be plotted that are completely
%   inside the volume defined by the `range` parameter.
%
% `'limit'`
% : Can be a single number, which defines the number vertices of the
%   polyhedra (`mode` set to `'poly'`) or the number of neighboring atoms
%   (identified by`atom2`) that will be connected to `atom1`. If can be
%   also a row vector with 2 elements `[dmin dmax]` that defines the
%   neighbors of `atom1` via a minimum and maxium distance in \\ang units.
%   Default value is 6 to plot octahedra around `atom1` type atoms (when
%   `mode` is set to `poly`).
%
% `'alpha'`
% : Transparency of the plotted surfaces, value between 0 and 1 (1 for
%   opaque, 0 for transparent). Default value is 1 for bonds and
%   0.3 for polyhedron.
%
% `'color'`
% : Color of the objects, one of the following values:
%   * `'auto'`      the color of all objects will be set to the color of
%                   `atom1`,
%   * `'colorname'` all objects will have the same color defined by the
%                   string, e.g. `'red'`,
%   * `[R G B]`     all objects will have the same color defined by the RGB
%                   code.
%   * `'none'`      no faces will be shown.
%
% `'color2'`
% : Color of the edges of the polyhedra (unused for bonds), default
%   value is `'auto'` when the edge will have the same color as the faces,
%   see the `color` parameter, using `'none'` will remove the edges.
%
% `'radius0'`
% : Radius of the bond cylinder, default value is 0.03 \\ang.
%
% #### General paraters
%
% These parameters have the same effect on any of the `swplot.plot...`
% functions.
%
% `'obj'`
% : [spinw] object.
%
% `'unit'`
% : Unit in which the plotting range is defined. It can be one of the
%   following strings:
%   * `'lu'`        plot range is defined in lattice units (default),
%   * `'xyz'`       plot range is defined in the $xyz$ Cartesian coordinate
%                   system in \\ang units.
%
% `'range'`
% : Defines the plotting range. Depending on the `unit` parameter, the
%   given range can be in lattice units or in units of the $xyz$ Cartesian
%   coordinate system. It is either a matrix with dimensions of $[3\times
%   2]$ where the first and second columns define the lower and upper plot
%   limits respectively. It can be alternatively a vector with three
%   elements `[a,b,c]` which is equivalent to `[0 a;0 b;0 c]`. Default
%   value is `[0 1;0 1;0 1]` to show a single cell.
%
% `'figure'`
% : Handle of the swplot figure. Default value is the active figure handle.
%
% `'legend'`
% : Whether to show the plot on the legend, default value is `true`.
%
% `'tooltip'`
% : If `true`, the tooltips will be shown when clicking on the plot
%   objects. Default value is `true`.
%
% `'shift'`
% : Column vector with 3 elements, all object positions will be
%   shifted by the given value in \\ang units. Default value is
%   `[0;0;0]`.
%
% `'replace'`
% : If `true` the plot will replace the previous plot of the same type.
%   Default value is `true`.
%
% `'translate'`
% : If `true`, the plot will be centered, independent of the range. Default
%   value is `false`.
%
% `'zoom'`
% : If `true`, the swplot figure will be zoomed to make the plot objects
%   cover the full figure. Default is `true`.
%
% `'copy'`
% : If `true`, a clone of the [spinw] object will be saved in the
%   swplot figure data which can be retwrived using
%   `swplot.getdata('obj')`. If `false`, the handle of the original [spinw]
%   object is saved which is linked to the input `obj` and so it changes
%   when `obj` is changed. Default value is `false`.
%
% `nMesh`
% : Mesh of the ellipse surface, a triangulation class object or an
%   integer that used to generate an icosahedron mesh with $n_{mesh}$
%   number of additional subdivision into triangles. Default value is
%   stored in `swpref.getpref('nmesh')`, see also [swplot.icomesh].
%
% `nPatch`
% : Number of vertices on any patch object that is not the icosahedron,
%   default value is stored in `swpref.getpref('npatch')`.
%
% ### Output Arguments
%
% `hFigure`
% : Handle of the swplot figure.
%
% The name of the objects is `'chem'`.
% To find the handles and the corresponding data on these objects, use e.g.
% sObject = swplot.findobj(hFigure,'name','chem')`.
%
    """
    
    return m.swplot.plotchem(*args, **kwargs)


def color(cName=None, index=None, **kwargs):
    """
% generates RGB code from color name
%
% ### Syntax
%
% `RGB = swplot.color(cName)`
%
% `RGB = swplot.color(cName,index)`
%
% ### Description
%
% `RGB = swplot.color(cName)` reads the color RGB values from the
% [color.dat] file corresponding to the given color name `cName`. The
% color name can be either a single character (see [matlab.colorspec]) or
% any [HTML color name](https://www.w3schools.com/colors/colors_names.asp)
% that is stored in the [color.dat] file.
%
% `RGB = swplot.color(cName,index)` if `index` is true, RGB code
% corresponding to the `cName` color index is read.
%
% ### Examples
%
% Read the RGB code corresponding to light gray:
% ```
% >>RGB = swplot.color('LightGray')>>
% ```
%
% ### Input Arguments
%
% `cName`
% : String of a color name. For multiple colors, use a cell of strings.
%
% `index`
% : If `true`, instead of the color name, `cName` means the index of the
%   color in the [color.dat] file. index 1 corresponds to the 9th entry
%   (the first 8 entry are standard Matlab color names), default value is
%   `false`.
%
% ### Output Arguments
%
% `RGB`
% : RGB color codes in a matrix with dimensions of $[3\times n_{color}]$, where
%   every value is an integer between 0 and 255.
%
    """
    args = tuple(v for v in [cName, index] if v is not None)
    return m.swplot.color(*args, **kwargs)


def arrow(*args, **kwargs):
    """
% creates a 3D arrow patch
%
% ### Syntax
%
% `hPatch = swplot.arrow(rStart, rEnd, R, alpha, lHead)`
%
% `hPatch = swplot.arrow(rStart, rEnd, R, alpha, lHead, nPatch)`
%
% `hPatch = swplot.arrow(handle, ...)`
%
% ### Description
%
% `hPatch = swplot.arrow(rStart, rEnd, R, alpha, lHead)` draws 3D arrows
% between a given start and end position. The arrows will be a triangulated
% [matlab.patch] object.
%
% `hPatch = swplot.arrow(rStart, rEnd, R, alpha, lHead, nPatch)` creates
% arrows with $5 n_{patch}$ number of patch faces per arrow.
%
% `hPatch = swplot.arrow(handle, ...)` adds the generated patch object to a
% given axis if `handle` is an axis handle or adds the arrows to an
% existing [matlab.patch] object, if the given `handle` points to a patch
% object.
%
% ### Examples
%
% Draw a 100 random arrows in the $(\pm 1,\pm 1,\pm 1)$ cube:
%
% ```
% >>swplot.figure
% >>N = 100
% >>swplot.arrow(2*rand(3,N)-1,2*rand(3,N)-1,0.01,30,0.05)
% >>swplot.zoom(40)
% >>snapnow
% ```
%
% ### Input Arguments
%
% `handle`
% : Handle of an axis or triangulated patch object. In case of patch
%   object, the constructed faces will be added to the existing object.
%
% `rStart`
% : Coordinates of the arrow starting point, one vector per arrow in a
%   matrix with dimensions of $[3\times n_{obj}]$.
%
% `rEnd`
% : Coordinates of the arrow end point, one vector per arrow in a
%   matrix with dimensions of $[3\times n_{obj}]$.
%
% `R`
% : Radius of the arrow body, scalar.
%
% `alpha`
% : Angle of the head in degree.
%
% `lHead`
% : Length of the head.
%
% `nPatch`
% : Number of points on the circle of the body, default value is stored in
%   `swpref.getpref('npatch')`. The final patch object will have
%   $5n_{patch}$ number of faces and $3n_{patch}$ number of vertices.
%
% ### See Also
%
% [swplot.cylinder]
%
    """
    
    return m.swplot.arrow(*args, **kwargs)


def polyhedron(*args, **kwargs):
    """
% creates convex polyhedra or polygon from vertex list
%
% ### Syntax
%
% `hPatch = swplot.polyhedron(vertices)`
%
% `hPatch = swplot.polyhedron(handle, ...)`
%
% ### Description
%
% `hPatch = swplot.polyhedron(vertices)` creates convex polyhedra or
% polygon from a given vertex list (unordered list of 3D coordinates). To
% draw the polyhedron the convex hull of the given point cloud is
% calculated using [matlab.convhulln]. It is automatically detected if the
% given vertex points lie on a plane in which case the convex polygon is
% drawn.
%
% `hPatch = swplot.polyhedron(handle, ...)` adds the generated patch object
% to a given axis if `handle` is an axis handle or adds the polyhedron to
% an existing [matlab.patch] object, if the given `handle` points to a
% patch object.
%
% ### Input Arguments
%
% `vertices`
% : Matrix with dimensions of $[3\times n_{obj}\times n_{point}]$, where
%   $n_{obj}$ is the number of polyhedra to draw, $n_{point}$ is the number
%   of vertices per polyhedron.
%
% ### See Also
%
% [matlab.convhulln]
%
    """
    
    return m.swplot.polyhedron(*args, **kwargs)


def setrangegui(*args, **kwargs):
    """
% GUI to change the plotting range
%
% ### Syntax
%
% `swplot.setrangegui`
%
% `swplot.setrangegui(hFigure)`
%
% `swplot.setrangegui(~,~,hfigure)`
%
% ### Description
%
% `swplot.setrangegui` produces a window that enables changing
% the limits of the active swplot figure. After changing the range, every
% object that is created with the `swplot.plot...` commands will be
% replotted using the new `range` parameter.
%
% `swplot.setrangegui(hFigure)` chow the gui for the swplot figure related
% the `hFigure` handle.
%
% `swplot.setrangegui(~,~,hfigure)` can be used in figure callbacks, for
% example by assigning it to `'ClickedCallback'` property of a button.
%
% ### Input Arguments
%
% `hFigure`
% : Handle of the swplot figure. Default value is the active figure.
%
    """
    
    return m.swplot.setrangegui(*args, **kwargs)


def close(*args, **kwargs):
    """
% closes swplot figure
%
% ### Syntax
%
% `swplot.close`
%
% `swplot.close('all')`
%
% `swplot.close(hFigure)`
%
% ### Description
%
% `swplot.close` closes the active swplot figure.
%
% `swplot.close('all')` closes all swplot figure.
%
% `swplot.close(hFigure)` closes the swplot figure corresponding to
% `hFigure` handle.
%
% ### See Also
%
% [swplot.figure]
%
    """
    
    return m.swplot.close(*args, **kwargs)


def ellipsoid(*args, **kwargs):
    """
% creates a 3D ellipsoid patch
%
% ### Syntax
%
% `hPatch = swplot.ellipsoid(R0, T)`
%
% `hPatch = swplot.ellipsoid(R0, T, nMesh)`
%
% `hPatch = swplot.ellipsoid(handle, ...)`
%
% ### Description
%
% `hPatch = swplot.ellipsoid(R0,T)` creates multiple ellipsoids with a
% single [matlab.patch] command. The ellipsoids are defined by the position
% of the center and a $[3\times 3]$ matrix, a qudratic form.
%
% Significant speedup can be achieved using a single patch command to
% generate many ellipsoids compared to drawing single ellipse per patch.
%
% `hPatch = swplot.ellipsoid(R0, T, nMesh)` defines the size of the mesh
% that defines the surface.
%
% `hPatch = swplot.ellipsoid(handle, ...)` adds the generated patch object
% to a given axis if `handle` is an axis handle or adds the ellipsoids to
% an existing [matlab.patch] object, if the given `handle` points to a
% patch object.
%
% ### Input Arguments
%
% `handle`
% : Handle of an axis or triangulated patch object. In case of patch
%   object, the constructed faces will be added to the existing object.
%
% `R0`
% : Center of the ellipsoids stored in a column vector with 3 elements or a
%   matrix with dimensions of $[3\times n_{obj}]$ when multiple ellipsoids
%   are defined at once.
%
% `T`
% : Transformation matrix that transforms a unit sphere to the desired
%   ellipsoid by applying: `R' = T(:,:,i)*R`. In case of multiple
%   ellipsoids the parameter is stored in a matrix with dimensions of
%   $[3\times 3\times n_{obj}]$.
%
% `nMesh`
% : Mesh of the ellipse surface, a triangulation class object or an
%   integer that used to generate an icosahedron mesh with $n_{mesh}$
%   number of additional subdivision into triangles. Default value is stored in
%   `swpref.getpref('nmesh')`, see also [swplot.icomesh].
%
% ### See Also
%
% [matlab.triangulation] \| [swplot.icomesh]
%
    """
    
    return m.swplot.ellipsoid(*args, **kwargs)


def raytriangle(V=None, F=None, ray=None, **kwargs):
    """
% finds if a ray crosses a triangle
%
% ### Syntax
%
% `swplot.raytriangle(V,F,ray)`
%
% ### Description
%
% `swplot.raytriangle(V,F,ray)` determines if a given ray crosses within a
% triangle defined by its vertex coordinates. The code is optimised for
% a single ray and multiple triangles.
%
% ### Input Arguments
%
% `V`
% : Vertex positions in a matrix with dimensions $[n_{vertex}\times 3]$.
%
% `F`
% : Faces in a matrix with dimensions $[n_{face}\times 3]$, where
%       $max(F) = n_{vertex}$.
%
% `ray`
% : Definition of the ray via 2 points in space, stored in a matrix with
%   dimensions of $[2\times 3]$. The two points of the ray, $P_1$ and
%   $P_2$, are stored in the first and second rows respectively. The ray
%   points from $P_1$ to $P_2$.
%
    """
    args = tuple(v for v in [V, F, ray] if v is not None)
    return m.swplot.raytriangle(*args, **kwargs)


def clear(*args, **kwargs):
    """
% clears swplot figure
%
% ### Syntax
%
% `swplot.clear`
%
% `swplot.clear(hFigure)`
%
% ### Description
%
% `swplot.clear` clears the active swplot figure.
%
% `swplot.clear(hFigure)` clears the swplot figure correspondign to
% `hFigure` handle
%
% ### See Also
%
% [swplot.figure]
%
    """
    
    return m.swplot.clear(*args, **kwargs)


def subplot(*args, **kwargs):
    """
% create subplots with variable gaps between axes
%
% ### Syntax
%
% `swplot.subplot(m,n,p,space)`
%
% `swplot.subplot([m,n,p],space)`
%
% ### Description
%
% `swplot.subplot(m,n,p,space)` is equivalent to the [matlab.subplot]
% command, except that the space between axes can be controlled.
%
% ### Input Arguments
%
% `m,n,p`
% : Three integer that defines subplot, for details see the
%   built-in [matlab.subplot] command.
%
% `space`
% : Vector with elements: `[margin hgap vgap]`, where:
%   * `margin`  Top and right margin at the figure edge.
%   * `hgap`    Left margin and horizontal gap between axes.
%   * `vgap`    Bottom margin and vertical gap between axes.
%
% ### See Also
%
% [matlab.subplot]
%
    """
    
    return m.swplot.subplot(*args, **kwargs)


def icomesh(nSub=None, **kwargs):
    """
% creates mesh by subdividing icosahedron faces
%
% ### Syntax
%
% `TR = swplot.icomesh(nMesh)`
%
% ### Description
%
% `TR = swplot.icomesh(nMesh)` outputs a triangulation that is generated by
% subdividing icosahedron faces. The triangulation will contain $20\cdot 4^n$
% (where $n=n_{mesh}$) triangular faces. The output can be plotted using the
% [matlab.trimesh] function.
%
% ### Examples
%
% This example shows how to create and plot the icosahedron.
%
% ```
% >>TR = swplot.icomesh
% >>>figure
% >>trimesh(TR)
% >>>axis('equal')
% >>>axis('off')
% >>snapnow
% ```
%
% ### Input Arguments
%
% `nMesh`
% : Number of subdivisions. Default value is 0, when the function returns
%   the icosahedron.
%
% ### Output Arguments
%
% `TR`
% : Triangulation class object for plotting with [matlab.trimesh].
%
% ### See Also
%
% [matlab.triangulation]
%
    """
    args = tuple(v for v in [nSub] if v is not None)
    return m.swplot.icomesh(*args, **kwargs)


