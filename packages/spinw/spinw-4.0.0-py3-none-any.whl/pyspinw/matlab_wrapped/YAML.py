import pyspinw
m = pyspinw.Matlab()

from libpymcr import MatlabProxyObject
from libpymcr.utils import get_nlhs

class YAML(MatlabProxyObject):
    """
 <strong>YAML</strong>  Serialize a matlab variable to yaml format
 
   [ X ] = <strong>YAML</strong>.load( S )
   [ S ] = <strong>YAML</strong>.dump( X )
 
   [ X ] = <strong>YAML</strong>.read( filepath )
   <strong>YAML</strong>.write( filepath, X )
 
  <strong>YAML</strong>.LOAD takes <strong>YAML</strong> string S and returns matlab variable X.
  <strong>YAML</strong>.DUMP takes matlab variable X and converts to <strong>YAML</strong> string S.
  <strong>YAML</strong>.READ and <strong>YAML</strong>.WRITE are convenient methods to load and dump
  <strong>YAML</strong> format directly from a file.
 
  Examples:
  To serialize matlab object
 
    >> X = struct('matrix', rand(3,4), 'char', 'hello');
    >> S = <strong>YAML</strong>.dump(X);
    >> disp(S);
    matrix:
    - [0.9571669482429456, 0.14188633862721534]
    - [0.4853756487228412, 0.421761282626275]
    - [0.8002804688888001, 0.9157355251890671]
    char: hello
 
  To decode yaml string
 
    >> X = <strong>YAML</strong>.load(S);
    >> disp(X)
      matrix: [3x2 double]
        char: 'hello'
 
  See also: <a href="matlab:help xmlread -displayBanner">xmlread</a> <a href="matlab:help xmlwrite -displayBanner">xmlwrite</a>

    <a href="matlab:doc YAML">Documentation for YAML</a>


    """
    def __init__(self, **kwargs):
        """
 <strong>YAML</strong>  Serialize a matlab variable to yaml format
 
   [ X ] = <strong>YAML</strong>.load( S )
   [ S ] = <strong>YAML</strong>.dump( X )
 
   [ X ] = <strong>YAML</strong>.read( filepath )
   <strong>YAML</strong>.write( filepath, X )
 
  <strong>YAML</strong>.LOAD takes <strong>YAML</strong> string S and returns matlab variable X.
  <strong>YAML</strong>.DUMP takes matlab variable X and converts to <strong>YAML</strong> string S.
  <strong>YAML</strong>.READ and <strong>YAML</strong>.WRITE are convenient methods to load and dump
  <strong>YAML</strong> format directly from a file.
 
  Examples:
  To serialize matlab object
 
    >> X = struct('matrix', rand(3,4), 'char', 'hello');
    >> S = <strong>YAML</strong>.dump(X);
    >> disp(S);
    matrix:
    - [0.9571669482429456, 0.14188633862721534]
    - [0.4853756487228412, 0.421761282626275]
    - [0.8002804688888001, 0.9157355251890671]
    char: hello
 
  To decode yaml string
 
    >> X = <strong>YAML</strong>.load(S);
    >> disp(X)
      matrix: [3x2 double]
        char: 'hello'
 
  See also: <a href="matlab:help xmlread -displayBanner">xmlread</a> <a href="matlab:help xmlwrite -displayBanner">xmlwrite</a>

    <a href="matlab:doc YAML">Documentation for YAML/YAML</a>


        """
        self.__dict__['interface'] = m._interface
        self.__dict__['_methods'] = []
        self.__dict__['__name__'] = 'YAML'
        self.__dict__['__origin__'] = YAML
        args = tuple(v for v in [] if v is not None)
        args += sum(kwargs.items(), ())
        self.__dict__['handle'] = self.interface.call('YAML', *args, nargout=1)

    @property
    def JARFILE(self):
        """
<strong>YAML.JARFILE</strong> is a property.


        """
        return self.__getattr__('JARFILE')

    @JARFILE.setter
    def JARFILE(self, val):
        self.__setattr__('JARFILE', val)

    def dump(self, X=None, **kwargs):
        """
 <strong>dump</strong> serialize matlab object into yaml string


        """
        args = tuple(v for v in [X] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('dump')), 1)
        return m.dump(self.handle, *args, nargout=nout)

    def dump_data(self, r=None, **kwargs):
        """
 <strong>dump_data</strong> convert


        """
        args = tuple(v for v in [r] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('dump_data')), 1)
        return m.dump_data(self.handle, *args, nargout=nout)

    def jarfile(self, **kwargs):
        """
 <strong>jarfile</strong> path to the SnakeYAML jar file


        """
        args = tuple(v for v in [] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('jarfile')), 1)
        return m.jarfile(self.handle, *args, nargout=nout)

    def load(self, S=None, **kwargs):
        """
 <strong>load</strong> load matlab object from yaml string


        """
        args = tuple(v for v in [S] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('load')), 1)
        return m.load(self.handle, *args, nargout=nout)

    def load_data(self, r=None, **kwargs):
        """
 <strong>load_data</strong> recursively convert java objects


        """
        args = tuple(v for v in [r] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('load_data')), 1)
        return m.load_data(self.handle, *args, nargout=nout)

    def merge_cell(self, r=None, **kwargs):
        """
 <strong>merge_cell</strong> convert cell array to native matrix


        """
        args = tuple(v for v in [r] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('merge_cell')), 1)
        return m.merge_cell(self.handle, *args, nargout=nout)

    def read(self, filepath=None, **kwargs):
        """
 <strong>read</strong> read and decode yaml data from file


        """
        args = tuple(v for v in [filepath] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('read')), 1)
        return m.read(self.handle, *args, nargout=nout)

    def write(self, filepath=None, X=None, **kwargs):
        """
 <strong>write</strong> serialize and write yaml data to file


        """
        args = tuple(v for v in [filepath, X] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('write')), 1)
        return m.write(self.handle, *args, nargout=nout)

