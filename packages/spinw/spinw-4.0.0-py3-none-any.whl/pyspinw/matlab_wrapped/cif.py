import pyspinw
m = pyspinw.Matlab()

from libpymcr import MatlabProxyObject
from libpymcr.utils import get_nlhs

class cif(MatlabProxyObject):
    """
  class handling cif data
 
  ### Syntax
 
  `obj = cif(source)`
 
  ### Description
 
  `obj = cif(source)` generates a cif class object. The object returns
  any field value corresponding to an existing field value in the
  imported .cif file. Use `cif.('field-name')` for field names that are
  not valid Matlab variable names. If a cif files contains multiple
  crystal structure, only the first one will be imported.
 
  ### Examples
 
  To test loading a .cif file from the internet use:
 
  cryst = cif('<a href="matlab:web https://goo.gl/Bncwcn">https://goo.gl/Bncwcn</a>');
 
  ### Input Arguments
 
  `source`
  : Location of the .cif file. It can be a filename, internet
    link or a string containing the content of a .cif file.
 
  ### See Also
 
  [cif.fieldnames]

    <a href="matlab:doc cif">Documentation for cif</a>


    """
    def __init__(self, path=None, **kwargs):
        """
  class handling cif data
 
  ### Syntax
 
  `obj = cif(source)`
 
  ### Description
 
  `obj = cif(source)` generates a cif class object. The object returns
  any field value corresponding to an existing field value in the
  imported .cif file. Use `cif.('field-name')` for field names that are
  not valid Matlab variable names. If a cif files contains multiple
  crystal structure, only the first one will be imported.
 
  ### Examples
 
  To test loading a .cif file from the internet use:
 
  cryst = cif('<a href="matlab:web https://goo.gl/Bncwcn">https://goo.gl/Bncwcn</a>');
 
  ### Input Arguments
 
  `source`
  : Location of the .cif file. It can be a filename, internet
    link or a string containing the content of a .cif file.
 
  ### See Also
 
  [cif.fieldnames]

    <a href="matlab:doc cif">Documentation for cif/cif</a>


        """
        self.__dict__['interface'] = m._interface
        self.__dict__['_methods'] = []
        self.__dict__['__name__'] = 'cif'
        self.__dict__['__origin__'] = cif
        args = tuple(v for v in [path] if v is not None)
        args += sum(kwargs.items(), ())
        self.__dict__['handle'] = self.interface.call('cif', *args, nargout=1)

    @property
    def cifdat(self):
        """
<strong>cif/cifdat</strong> is a property.


        """
        return self.__getattr__('cifdat')

    @cifdat.setter
    def cifdat(self, val):
        self.__setattr__('cifdat', val)

    @property
    def source(self):
        """
<strong>cif/source</strong> is a property.


        """
        return self.__getattr__('source')

    @source.setter
    def source(self, val):
        self.__setattr__('source', val)

    @property
    def isfile(self):
        """
<strong>cif/isfile</strong> is a property.


        """
        return self.__getattr__('isfile')

    @isfile.setter
    def isfile(self, val):
        self.__setattr__('isfile', val)

    def disp(self, obj=None, **kwargs):
        """
 <strong>disp</strong> Display array.
    <strong>disp</strong>(X) displays array X without printing the array name or 
    additional description information such as the size and class name.
    In all other ways it is the same as leaving the semicolon off an
    expression except that nothing is shown for empty arrays.
 
    If X is a string or character array, the text is displayed.
 
    See also <a href="matlab:help formattedDisplayText -displayBanner">formattedDisplayText</a>, <a href="matlab:help sprintf -displayBanner">sprintf</a>, <a href="matlab:help num2str -displayBanner">num2str</a>, <a href="matlab:help format -displayBanner">format</a>, <a href="matlab:help details -displayBanner">details</a>.


        """
        args = tuple(v for v in [obj] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('disp')), 1)
        return m.disp(self.handle, *args, nargout=nout)

    def fieldnames(self, obj=None, **kwargs):
        """
  returns all the field names of the cif object


        """
        args = tuple(v for v in [obj] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('fieldnames')), 1)
        return m.fieldnames(self.handle, *args, nargout=nout)

    def fields(self, obj=None, **kwargs):
        """
  returns all the field names of the cif object


        """
        args = tuple(v for v in [obj] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('fields')), 1)
        return m.fields(self.handle, *args, nargout=nout)

    def importcif(self, *args, **kwargs):
        """
  imports .cif data from file, web or string


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('importcif')), 1)
        return m.importcif(self.handle, *args, nargout=nout)

    def subsref(self, obj=None, S=None, **kwargs):
        """
 <strong>subsref</strong> Subscripted reference.
    A(I) is an array formed from the elements of A specified by the
    subscript vector I.  The resulting array is the same size as I except
    for the special case where A and I are both vectors.  In this case,
    A(I) has the same number of elements as I but has the orientation of A.
 
    A(I,J) is an array formed from the elements of the rectangular
    submatrix of A specified by the subscript vectors I and J.  The
    resulting array has LENGTH(I) rows and LENGTH(J) columns.  A colon used
    as a subscript, as in A(I,:), indicates all columns of those rows
    indicated by vector I. Similarly, A(:,J) = B means all rows of columns
    J.
 
    For multi-dimensional arrays, A(I,J,K,...) is the subarray specified by
    the subscripts.  The result is LENGTH(I)-by-LENGTH(J)-by-LENGTH(K)-...
 
    A{I} when A is a cell array and I is a scalar is a copy of the array in
    the specified cell of A.  If I has more than one element, this
    expression is a comma separated list (see LISTS). Multiple subscripts
    that specify a scalar element, as in A{3,4}, also work.
 
    A(I).label when A is a structure or object array and I is a scalar is a
    copy of the array in the field or property with the name 'label'. If I
    has more than one element, this expression is a comma separated list.
    If A is a 1-by-1 array, then the subscript can be dropped. In this
    case, A.label is the same as A(1).label.
 
    When var is a variable containing 'label', A(I).(var) is a copy of the
    array in the field or property with the name 'label'. If I has more
    than one element, this expression is a comma separated list.
 
    A class can implement a method named <strong>subsref</strong> to overload indexed
    reference. When a class has a <strong>subsref</strong> method, B = <strong>subsref</strong>(A,S) is
    called for the syntax A(I), A{I}, A.I, or A.(I) whenever A is an
    instance of the class. The argument S is a structure array with the
    fields:
        type -- character vector or string containing '()', '{}', or '.' 
                specifying the subscript type.
        subs -- cell array, character vector, or string containing the 
                actual subscripts.
 
    Subscripting expressions can use more than one level to form more
    complicated expressions, for example A{1}.field(3:5). For an expression
    with N subscripting levels, S is a 1-by-N structure array.
    
    Instead of implementing <strong>subsref</strong>, class authors can use the mixins in
    the matlab.mixin.indexing package to overload indexing. See the
    documentation for more information.
 
    See also <a href="matlab:help subsasgn -displayBanner">subsasgn</a>, <a href="matlab:help substruct -displayBanner">substruct</a>, <a href="matlab:help numArgumentsFromSubscript -displayBanner">numArgumentsFromSubscript</a>, <a href="matlab:help subsindex -displayBanner">subsindex</a>,
             <a href="matlab:help paren -displayBanner">paren</a>, <a href="matlab:help lists -displayBanner">lists</a>, <a href="matlab:help matlab.mixin.indexing -displayBanner">matlab.mixin.indexing</a>


        """
        args = tuple(v for v in [obj, S] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('subsref')), 1)
        return m.subsref(self.handle, *args, nargout=nout)

