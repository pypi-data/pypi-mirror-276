import pyspinw
m = pyspinw.Matlab()

from libpymcr import MatlabProxyObject
from libpymcr.utils import get_nlhs

class swpref(MatlabProxyObject):
    """
  class to store and retrieve persistent settings
 
  ### Syntax
 
  `pref = swpref`
 
  `pref = swpref('default')`
 
  ### Description
 
  `pref = swpref` retrieves and creates a preference object.
 
  `pref = swpref('default')` resets all preferences to default values.
 
  The settings sotred in the `swpref` class for spinw objects will
  persist during a single Matlab session. It is different from the
  Matlab built-in preferences, as swpref resets all settings to factory
  default after every restart of Matlab.
 
  ### Examples
 
  We change the fontsize value and show that it is retained even when a
  new instance of the object is created:
 
  ```
  >>pref = swpref
  >>pref.fontsize>>
  >>pref.fontsize = 18
  >>pref2 = swpref
  >>pref.fontsize>>
  >>pref2.fontsize>>
  ```
 
  ### Properties
 
  Properties can be changed by directly assigning a new value to them.
  Once a new value to a given property is assigned, it will be retained
  until the end of a MATLAB session, even if a new class instance is
  created.
 
  ### Methods
 
  Methods are the different commands that require an `swpref` object as
  a first input, thus they can be called as `method1(obj,...)`,
  alternatively the equivalent command is `obj.method1(...)`.
 
  swpref.get
  swpref.set
  swpref.export
  swpref.import
 
  Commands are methods which can be called without first creating a
  preference object `swpref.command(....)`.
 
  swpref.getpref
  swpref.setpref

    <a href="matlab:doc swpref">Documentation for swpref</a>


    """
    def __init__(self, opt=None, **kwargs):
        """
  Spin preference constructor.
 
  ### Syntax
 
  `pref = swpref`
 
  `pref = swpref('default')`
 
 
  ### Description
 
  `pref = swpref` retrieves and creates a preference object.
 
  `pref = swpref('default')` resets all preferences to default values.
 
 
  {{note The preferences are reset after every restart of Matlab, unlike the
  Matlab built-in preferences that are persistent between Matlab sessions.
  If you want certain preferences to keep after closing matlab, use the
  'pref.export(fileLocation)' and 'pref.import(fileLocation)' functions.
  These can be added to your startup file.}}
 
  ### See Also
 
  [swpref.get], [swpref.set]

    <a href="matlab:doc swpref">Documentation for swpref/swpref</a>


        """
        self.__dict__['interface'] = m._interface
        self.__dict__['_methods'] = []
        self.__dict__['__name__'] = 'swpref'
        self.__dict__['__origin__'] = swpref
        args = tuple(v for v in [opt] if v is not None)
        args += sum(kwargs.items(), ())
        self.__dict__['handle'] = self.interface.call('swpref', *args, nargout=1)

    def addprop(self, object=None, propname=None, **kwargs):
        """
 <strong>addprop</strong>   Add dynamic property to MATLAB object.
    D = <strong>addprop</strong>(H,DynamicPropName) adds a dynamic property to the MATLAB 
    objects in array H. DynamicPropName can be a string scalar or character 
    vector.  The added property is associated only with the objects of H.  
    There is no effect on the class of H.  <strong>addprop</strong> returns a 
    META.DYNAMICPROPERTY object, which can be modified to change property 
    attributes or add property set and get methods.  
 
    A dynamic property can be removed from an object by calling DELETE on
    the META.DYNAMICPROPERTY object.
 
    See also <a href="matlab:help swpref -displayBanner">swpref</a>, <a href="matlab:help handle -displayBanner">handle</a>, <a href="matlab:help meta.DynamicProperty -displayBanner">meta.DynamicProperty</a>

Help for <strong>swpref/addprop</strong> is inherited from superclass <a href="matlab:help dynamicprops -displayBanner">dynamicprops</a>

    <a href="matlab:doc dynamicprops/addprop">Documentation for swpref/addprop</a>


        """
        args = tuple(v for v in [object, propname] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('addprop')), 1)
        return m.addprop(self.handle, *args, nargout=nout)

    def check_names(self, obj=None, name=None, **kwargs):
        """
  Checking to see if a get/set name is valid.
 
   {{warning Internal function for the Spin preferences.}}
 
  ### Syntax
 
  'logical = obj.<strong>check_names</strong>(name)'
 
  ### Description
 
  'logical = obj.<strong>check_names</strong>(name)' returns true if 'name' is a
  valid field of 'obj' and false otherwise.


        """
        args = tuple(v for v in [obj, name] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('check_names')), 1)
        return m.check_names(self.handle, *args, nargout=nout)

    def datastruct(self, *args, **kwargs):
        """
SWPREF/<strong>datastruct</strong> is an undocumented builtin function.


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('datastruct')), 1)
        return m.datastruct(self.handle, *args, nargout=nout)

    def disp(self, obj=None, **kwargs):
        """
  function called when a preference is displayed.
 
  ### Syntax
 
  `disp(obj)`
 
  `obj.disp`
 
  ### Description
 
  `disp(obj)` shows a table of all dynamic properties including
  name, value and description. If a table is not supported only
  `name: value` is displayed for all properties.


        """
        args = tuple(v for v in [obj] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('disp')), 1)
        return m.disp(self.handle, *args, nargout=nout)

    def export(self, *args, **kwargs):
        """
  saves swpref object into a file
 
  ### Syntax
 
  `success = export(obj,location)`
 
  `success = export(obj)`
 
  ### Description
 
  `success = export(obj,location)` writes the preferences given in `obj` to
  a file location given by `location`. The file is in a basic `.json`
  format.
 
  `success = export(obj)` writes the preferences given in `obj` to
  the users home folder as `swprefs.json`. The file is in a basic `.json`
  format.
 
  ### See Also
 
  [swpref.import]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('export')), 1)
        return m.export(self.handle, *args, nargout=nout)

    def export_prefs(self, *args, **kwargs):
        """
  saves swpref object into a file
 
  ### Syntax
 
  `success = <strong>swpref.export_prefs</strong>(location)`
 
  `success = <strong>swpref.export_prefs</strong>`
 
  ### Description
 
  `success = <strong>swpref.export_prefs</strong>(location)` writes the preferences given by swpref to
  a file location given by `location`. The file is in a basic `.json`
  format.
 
  `success = <strong>swpref.export_prefs</strong>` writes the preferences given in `obj` to
  the users home folder as `swprefs.json`. The file is in a basic `.json`
  format.
 
  ### See Also
 
  [swpref.import_prefs]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('export_prefs')), 1)
        return m.export_prefs(self.handle, *args, nargout=nout)

    def get(self, obj=None, names=None, **kwargs):
        """
  retrieves a preference value
 
  ### Syntax
 
  `value = get(obj, name)`
 
  `value = obj.get(name)`
 
  ### Description
 
  `value = get(obj, name)` gets the preference `name`.
 
  `value = obj.get(name)` gets the preference `name`.
 
  ### See Also
 
  [swpref.set]


        """
        args = tuple(v for v in [obj, names] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('get')), 1)
        return m.get(self.handle, *args, nargout=nout)

    def get_data(self, obj=None, name=None, **kwargs):
        """
  Function called when a vairable is retrieved.
 
   {{warning Internal function for the Spin preferences.}}
 
  ### Syntax
 
  'value = <strong>get_data</strong>(obj, name)'
 
  ### Description
 
  'value = <strong>get_data</strong>(obj, name)' returns the value of parameter
  'name' from persistent storage.
 
  ### See Also
 
  [swpref.setpref], [swpref.set_data]


        """
        args = tuple(v for v in [obj, name] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('get_data')), 1)
        return m.get_data(self.handle, *args, nargout=nout)

    def get_set_static(self, name=None, value=None, **kwargs):
        """
  The internal session persistent storage of vairables.
 
   {{warning Internal function for the Spin preferences.}}
 
  ### Syntax
 
  'values = <strong>get_set_static</strong>()'
 
  'value' = <strong>get_set_static</strong>(name)'
 
  '<strong>get_set_static</strong>(name, value)'
 
  ### Description
 
  'values = <strong>get_set_static</strong>()' retrieves all the preferences in
  the storage.
 
  'value' = <strong>get_set_static</strong>(name)' returns the value of
  preference given by 'name'.
 
  '<strong>get_set_static</strong>(name, value)' sets the preference given
  by 'name' to value 'value'
 
  ### See Also
 
  [swpref.check_names], [swpref.get_data], [swpref.set_data]


        """
        args = tuple(v for v in [name, value] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('get_set_static')), 1)
        return m.get_set_static(self.handle, *args, nargout=nout)

    def getpref(self, name=None, *args, **kwargs):
        """
  retrieves a preference value
 
  ### Syntax
 
  `allPref = <strong>swpref.getpref</strong>`
 
  `selPref = <strong>swpref.getpref</strong>(name)`
 
  `val = <strong>swpref.getpref</strong>(name,[])`
 
  ### Description
 
  `allPref = <strong>swpref.getpref</strong>` returns all preference in a struct where each
  field-value pair corresponds to a prefernce name-value pair.
 
  `selPref = <strong>swpref.getpref</strong>(name)` returns a struct that contains the
  value, name and label of the selected preference.
 
  `val = <strong>swpref.getpref</strong>(name,[])` just returns the stored value
  corresponding to `name` preference.
 
  {{note The preferences are reset after every restart of Matlab, unlike the
  Matlab built-in preferences that are persistent between Matlab sessions.
  If you want certain preferences to keep after closing matlab, define them
  in the `startup.m` file.}}
 
  {{warning This is a legacy function. It is better to use `pref = swpref` and then
  use regular `pref.name = value` or `set(pref, name, value)` syntax.}}
 
  ### See Also
 
  [swpref.setpref]


        """
        args = tuple(v for v in [name] if v is not None) + args
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('getpref')), 1)
        return m.getpref(self.handle, *args, nargout=nout)

    def import_(self, *args, **kwargs):
        """
  imports swpref object from file
 
  ### Syntax
 
  
  `obj = import(obj)`
 
  `obj = import(obj,location)`
 
  ### Description
 
  `obj = import(obj)` loads the preferences given in by the file
  `swprefs.json` in the users home folder. It sets the preferences and
  returns a new preference object.
 
  `obj = import(obj,location)` loads the preferences given in by the file 
  specified by `location`, sets the preferences and returns a new
  preference object.
 
  ### See Also
 
  [swpref.export]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('import_')), 1)
        return m.import_(self.handle, *args, nargout=nout)

    def import_prefs(self, *args, **kwargs):
        """
  imports swpref object from file
 
  ### Syntax
 
 
  `obj = <strong>swpref.import_prefs</strong>`
 
  `obj = <strong>swpref.import_prefs</strong>(location)`
 
  ### Description
 
  `obj = <strong>swpref.import_prefs</strong>` loads the preferences given in by the file
  `swprefs.json` in the users home folder. It sets the preferences and
  returns a new preference object.
 
  `obj = <strong>swpref.import_prefs</strong>(location)` loads the preferences given in by the file
  specified by `location`, sets the preferences and returns a new
  preference object.
 
  ### See Also
 
  [swpref.export_prefs]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('import_prefs')), 1)
        return m.import_prefs(self.handle, *args, nargout=nout)

    def set(self, obj=None, names=None, values=None, **kwargs):
        """
  sets a preference value
 
  ### Syntax
 
  `set(obj, name, value)`
 
  `obj.set(name, value)`
 
  ### Description
 
  `set(obj, name, value)` sets the preference `name` to the
  value given by `value`
 
  `obj.set(name, value)` sets the preference `name` to the
  value given by `value`
 
  ### See Also
 
  [swpref.get]


        """
        args = tuple(v for v in [obj, names, values] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('set')), 1)
        return m.set(self.handle, *args, nargout=nout)

    def set_data(self, obj=None, name=None, val=None, **kwargs):
        """
  Function called when a vairable is set.
 
   {{warning Internal function for the Spin preferences.}}
 
  ### Syntax
 
  '<strong>set_data</strong>(obj, name, value)'
 
  ### Description
 
  '<strong>set_data</strong>(obj, name, value)' sets the 'value' of parameter
  'name' which is stored in persistent storage.
 
  ### See Also
 
  [swpref.setpref], [swpref.get_data]


        """
        args = tuple(v for v in [obj, name, val] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('set_data')), 1)
        return m.set_data(self.handle, *args, nargout=nout)

    def setpref(self, *args, **kwargs):
        """
  sets a preference value
 
  ### Syntax
 
  `<strong>swpref.setpref</strong>(name, value)`
 
  ### Description
 
  `<strong>swpref.setpref</strong>(name, value)` sets the value of `name`
  preferences.
 
  {{note The preferences are reset after every restart of Matlab, unlike the
  Matlab built-in preferences that are persistent between Matlab sessions.
  If you want certain preferences to keep after closing matlab, define them
  in the `startup.m` file.}}
 
  {{warning This is a legacy function. It is better to use 'pref = swpref' and then
  use regular 'value = pref.name' or 'get(pref, name)' syntax.}}
 
  ### See Also
 
  [swpref.getpref]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('setpref')), 1)
        return m.setpref(self.handle, *args, nargout=nout)

