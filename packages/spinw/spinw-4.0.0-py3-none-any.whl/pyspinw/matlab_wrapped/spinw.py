import pyspinw
m = pyspinw.Matlab()

from libpymcr import MatlabProxyObject
from libpymcr.utils import get_nlhs

class spinw(MatlabProxyObject):
    """
  SpinW
  Version 3.1 (unreleased) 29-Nov-2017


spinw is both a directory and a function.

  class to store and solve magnetic Hamiltonians
 
  ### Syntax
 
  `obj = spinw`
 
  `obj = spinw(obj)`
 
  `obj = spinw(source)`
 
  `obj = spinw(figure_handle)`
 
  ### Description
 
  `obj = spinw` constructs an empty spinw class object.
 
  `obj = spinw(obj)` constructs a spinw class object from the
  parameters defined in `obj`. If `obj` is spinw class, it only checks
  the integrity of its internal data structure. If `obj` is struct
  type, it creates new spinw object and checks data integrity.
 
  `obj = spinw(source)` construct new spinw class object, where
  `source` is either a file path pointing to a local `cif` or `fst`
  file or a link to an online file.
 
  `obj = spinw(figure_handle)` copy the spinw object stored in a
  previous structural 3D plot figure, referenced by `figure_handle`.
 
 
  The data structure within the spinw object can be accessed by using
  [spinw.struct] method. All fields of the struct type data behind the
  spinw object are accessible through the main field names of the `obj`
  object. For example the lattice parameters can be accessed using:
 
  ```
  abc = obj.unit_cell.lat_const
  ```
 
  spinw is a handle class, which means that only the handle of the
  object is copied in an assinment command `swobj1 = swobj2`. To create
  a copy (clone) of an spinw object use:
 
  ```
  swobj1 = swobj2.copy
  ```
 
  ### Properties
 
  The data within the `spinw` object is organized into a tree structure
  with the main groups and the type of data they store are the
  following:
 
  * [spinw.lattice] unit cell parameters
  * [spinw.unit_cell] atoms in the crystallographic unit cell
  * [spinw.twin] crystal twin parameters
  * [spinw.matrix] 3x3 matrices for using them in the Hailtonian
  * [spinw.single_ion] single ion terms of the Hamiltonian
  * [spinw.coupling] list of bonds
  * [spinw.mag_str] magnetic structure
  * [spinw.unit] physical units for the Hamiltonian
  * [spinw.cache] temporary values
 
  ### Methods
 
  Methods are the different commands that require a `spinw` object as a
  first input, thus they can be called as `method1(obj,...)`,
  alternatively the equivalent command is `obj.method1(...)`. The list
  of public methods is below.
 
  #### Lattice operations
 
    spinw.genlattice
    spinw.basisvector
    spinw.rl
    spinw.nosym
    spinw.newcell
    spinw.addatom
    spinw.unitcell
    spinw.abc
    spinw.atom
    spinw.matom
    spinw.natom
    spinw.formula
    spinw.disp
    spinw.symmetry
    
  #### Plotting
 
    spinw.plot
 
  #### Crystallographic twin operations
 
    spinw.addtwin
    spinw.twinq
    spinw.notwin
 
  #### Magnetic structure operations
 
    spinw.genmagstr
    spinw.magstr
    spinw.magtable
    spinw.nmagext
    spinw.optmagstr
    spinw.optmagk
    spinw.optmagsteep
    spinw.anneal
    spinw.annealloop
    spinw.structfact
    
  #### Matrix operations
 
    spinw.addmatrix
    spinw.getmatrix
    spinw.setmatrix
    
  #### Spin Hamiltonian generations
 
    spinw.quickham
    spinw.gencoupling
    spinw.addcoupling
    spinw.addaniso
    spinw.addg
    spinw.field
    spinw.temperature
    spinw.intmatrix
    spinw.symop
    spinw.setunit
    
  #### Solvers
 
    spinw.spinwave
    spinw.powspec
    spinw.energy
    spinw.moment
    spinw.spinwavesym
    spinw.symbolic
    spinw.fourier
    spinw.fouriersym
 
  #### Fitting spin wave spectrum
 
    spinw.fitspec
    spinw.matparser
    spinw.horace
    
  #### Miscellaneous
 
    spinw.copy
    spinw.export
    spinw.table
    spinw.validate
    spinw.version
    spinw.struct
    spinw.clearcache
    spinw.spinw
 
  ### See also
 
  [spinw.copy], [spinw.struct], [Comparing handle and value classes](<a href="matlab:web https://www.mathworks.com/help/matlab/matlab_oop/comparing-handle-and-value-classes.html">https://www.mathworks.com/help/matlab/matlab_oop/comparing-handle-and-value-classes.html</a>)

    <a href="matlab:doc spinw">Documentation for spinw</a>


    """
    def __init__(self, *args, **kwargs):
        """
  spinw constructor
 
  ### Syntax
 
  `obj = spinw`
 
  `obj = spinw(struct)` 
 
  `obj = spinw(hFigure)`
 
  `obj = spinw(fName)`
 
  `obj = spinw(obj)`
 
  ### Description
 
  `obj = spinw` creates an empty SpinW object with default
  values.
 
  `obj = spinw(struct)` creates a SpinW object from a structure
  which has fields that are compatible with the SpinW property
  structure.
 
  `obj = spinw(hFigure)` clones SpinW object from an swplot
  figure or spectral plot figure.
 
  `obj = spinw(fName)` imports the file referenced by `fName`.
  SpinW is able to import .cif/.fts files for crystal or
  magnetic structure from a local file or a web address.
 
  `obj = spinw(obj)` checks the input SpinW object for
  consistency.

    <a href="matlab:doc spinw">Documentation for spinw/spinw</a>


        """
        self.__dict__['interface'] = m._interface
        self.__dict__['_methods'] = []
        self.__dict__['__name__'] = 'spinw'
        self.__dict__['__origin__'] = spinw
        
        args += sum(kwargs.items(), ())
        self.__dict__['handle'] = self.interface.call('spinw', *args, nargout=1)

    @property
    def lattice(self):
        """
  stores the unit cell parameters
 
  ### Sub fields
 
  `lat_const`
  : Lattice constants in a $[1\times 3]$ vector in units defined in
    [spinw.unit] (default value is \\ang).
 
  `angle`
  : `[\\alpha,\\beta,\\gamma]` angles in a $[1\times 3]$ vector in
    radian units.
 
  `sym`
  : Symmetry operators stored in matrix with dimensions of
    $[3\times 4 \times n_{op}]$.
 
  `origin`
  : Origin of the cell in lattice units.
  
  `label`
  : Label of the space group.
 


        """
        return self.__getattr__('lattice')

    @lattice.setter
    def lattice(self, val):
        self.__setattr__('lattice', val)

    @property
    def unit_cell(self):
        """
  stores the atoms in the crystallographic unit cell
 
  ### Sub fields
 
  `r`
  : Positions of the atoms in the unit cell, stored in a
    matrix with dimensions of $[3\times n_{atom}]$, values are
    in lattice units.
 
  `S`
  : Spin quantum number of the atoms, stored in a row vector with
    $n_{atom}$ number of elements, non-magnetic atoms have `S=0`.
 
  `label`
  : Label of the atom, strings stored in a $[1\times n_{atom}]$
    cell.
 
  `color`
  : Color of the atom stored in a matrix with dimensions of $[3\times n_{atom}]$, where every
    column defines an RGB color with values between 0 and 255.
 
  `ox`
  : Oxidation number of the atom, stored in a $[1\times n_{atom}]$
    matrix.
 
  `occ`
  : Site occupancy in a $[1\times n_{atom}]$ matrix.
 
  `b`
  : Scattering length of the atoms for neutron and x-ray
    stored in a $[2\times n_{atom}]$ matrix, first row is neutron,
    second row is for x-ray.
 
  `ff`
  : Form factor of the site stored in a $[2\times 9\times
    n_{atom}]$ matrix, first row is the magnetic form factor for
    neutrons, the second row is the charge form factor for x-ray
    cross section.
 
  `Z`
  : Atomic number in a row vector.
 
  `A`
  : Atomic mass (N+Z) for isotopes and -1 for natural
    distribution of isotopes stored in a row vector.
 
  `biso`
  : Isotropic displacement factors in units of \\ang$^2$.
    Definition is the same as in
    [FullProf](<a href="matlab:web https://www.ill.eu/sites/fullprof/">https://www.ill.eu/sites/fullprof/</a>), defining the
    Debye-Waller factor as $W(d) = 1/8*b_{iso}/d^2$ which is
    included in the structure factor as $\exp(-2W(d))$.
 


        """
        return self.__getattr__('unit_cell')

    @unit_cell.setter
    def unit_cell(self, val):
        self.__setattr__('unit_cell', val)

    @property
    def twin(self):
        """
  stores the crystal twin parameters
 
  ### Sub fields
 
  `rotc`
  : Rotation matrices in the $xyz$ coordinate system for
    every twin, stored in a matrix with dimensions of $[3\times
    3\times n_{twin}]$.
 
  `vol`
  : Volume ratio of the different twins, stored in a
     row vector with $n_{twin}$ elements.
 


        """
        return self.__getattr__('twin')

    @twin.setter
    def twin(self, val):
        self.__setattr__('twin', val)

    @property
    def matrix(self):
        """
  stores 3x3 matrices for using them in the Hailtonian
 
  ### Sub fields
 
  `mat`
  : Stores the actual values of 3x3 matrices, in a matrix with
  dimensions of $[3\times 3\times n_{matrix}]$, if assigned for a 
  bond, the unit of energy is stored in [spinw.unit] (default value 
  is meV).
 
  `color`
  : Color assigned for every matrix, stored in a
    matrix with dimensions of $[3\times n_{matrix}]$, with each
    column defining an RGB value.
 
  `label`
  : Label for every matrix, stored as string in a cell with
    dimensions of $[1\times n_{matrix}]$.
 


        """
        return self.__getattr__('matrix')

    @matrix.setter
    def matrix(self, val):
        self.__setattr__('matrix', val)

    @property
    def single_ion(self):
        """
  stores single ion terms of the Hamiltonian
 
  ### Sub fields
 
  `aniso`
  : Row vector that contains $n_{magatom}$ integers, each integer
    assignes one of the matrices from the [spinw.matrix] property
    to a magnetic atom in the generated [spinw.matom] list as a single
    ion anisotropy. Zero value of `aniso` means no single ion
    anisotropy for the corresponding magnetic atom.
 
  `g`
  : Row vector with $n_{magatom}$ integers, each integer
    assignes one of the matrices from the [spinw.matrix] property
    to a magnetic atom in the spinw.matom list as a
    g-tensor. Zero value of `g` means a default g-value of 2 for
    the corresponding atoms.
 
  `field`
  : External magnetic field stored in a row vector with 3 elements,
    unit is defined in [spinw.unit] (default unit is Tesla).
 
  `T`
  : Temperature, scalar, unit is defined in [spinw.unit] (default
    unit is Kelvin).
 


        """
        return self.__getattr__('single_ion')

    @single_ion.setter
    def single_ion(self, val):
        self.__setattr__('single_ion', val)

    @property
    def coupling(self):
        """
  stores the list of bonds
 
  ### Sub fields
 
  `dl`
  : Distance between the unit cells of two interacting
    spins, stored in a $[3\times n_{coupling}]$ matrix.
 
  `atom1`
  : First magnetic atom, pointing to the list of
    magnetic atoms in the list generated by `spinw.matom`, stored in a
    row vector with $n_{coupling}$ element.
 
  `atom2`
  : Second magnetic atom, same as `atom1`.
 
  `mat_idx`
  : Stores pointers to matrices for every coupling in a
    $[3\times n_{coupling}]$ matrix, maximum three matrix per
    coupling (zeros for no coupling) is allowed.
 
  `idx`
  : Neighbor index, increasing indices for the equivalent
    couplings, starting with 1,2,... which means first and second
    neighbor bonds, respectively.
 
  `type`
  : Type of coupling corresponding to `mat_idx` matrices.
    Default is 0 for quadratic exchange, `type = 1` for
    biquadratic exchange.
  
  `sym`
  : If `true` the bond symmetry operators will be applied
    on the assigned matrix.
  
  `rdip`
  : Maximum distance until the dipolar interaction is
    calculated. Zero value means no dipolar interactions
    are considered.
  
  `nsym`
  : The largest bond `idx` value that is generated
    using the space group operators. Typically very long bonds for
    dipolar interactions won't be calculated using space group
    symmetry.
 


        """
        return self.__getattr__('coupling')

    @coupling.setter
    def coupling(self, val):
        self.__setattr__('coupling', val)

    @property
    def mag_str(self):
        """
  stores the magnetic structure
 
  ### Sub fields
 
  `F`
  : Complex magnetization (strictly speaking complex
    spin expectation value) for every spin in the magnetic
    cell, represented by a matrix with dimensions of $[3\times
    n_{magext}\times n_k]$,
    where `nMagExt = nMagAtom*prod(N_ext)` and $n_k$ is the number
    of the magnetic propagation vectors.
 
  `k`
  : Magnetic propagation vectors stored in a matrix with dimensions
    of $[3\times n_k]$.
 
  `N_ext`
  : Size of the magnetic supercell in lattice units, default value
    is `[1 1 1]` emaning that the magnetic cell is identical to the
    crystallographic cell. The $[1\times 3]$ vector extends the cell
    along the $a$, $b$ and $c$ axes.
 


        """
        return self.__getattr__('mag_str')

    @mag_str.setter
    def mag_str(self, val):
        self.__setattr__('mag_str', val)

    @property
    def unit(self):
        """
  stores the physical units for the Hamiltonian
 
  Default values are meV, T, \\ang and K for energy, magnetic
  field, length and temperature, respectively.
 
  ### Sub fields
 
  `kB`
  : Boltzmann constant, default value is 0.0862 meV/K.
 
  `muB`
  : Bohr magneton, default values is 0.0579 meV/T.
 
  `mu0`
  : Vacuum permeability, default value is 201.335431 T$^2$\\ang$^3$/meV.
 
  `label`
  : Labels for distance, energy, magnetic field and temperature
  stored in a cell with dimensions $[1\times 4]$.
 
  `nformula`
  : Number of formula units in the unit cell.
 
  `qmat`
  : Transformation matrix that converts the given $Q$ values into
  the internal reciprocal lattice. The matrix has dimensions of
  $[3\times 3]$.
 


        """
        return self.__getattr__('unit')

    @unit.setter
    def unit(self, val):
        self.__setattr__('unit', val)

    @property
    def cache(self):
        """
  stores temporary values
 
  This property should be only used to check consistency of the code.
 
  {% include warning.html content="Changing these values is strongly 
  discouraged as it can break the code!" %}
  
  ### Sub fields
 
  `matom`
  : Generated data of the magnetic unit cell.
 
  `symop`
  : Generated symmetry operators for each bond.
 


        """
        return self.__getattr__('cache')

    @cache.setter
    def cache(self, val):
        self.__setattr__('cache', val)

    @property
    def propl(self):
        """
  stores the property change listener handles


        """
        return self.__getattr__('propl')

    @propl.setter
    def propl(self, val):
        self.__setattr__('propl', val)

    @property
    def sym(self):
        """
  stores whether the couplings are generated under symmetry constraints


        """
        return self.__getattr__('sym')

    @sym.setter
    def sym(self, val):
        self.__setattr__('sym', val)

    @property
    def symb(self):
        """
  stores whether the calculation are done symbolically


        """
        return self.__getattr__('symb')

    @symb.setter
    def symb(self, val):
        self.__setattr__('symb', val)

    @property
    def ver(self):
        """
  use the version property as contant, this will be executed only
  once


        """
        return self.__getattr__('ver')

    @ver.setter
    def ver(self, val):
        self.__setattr__('ver', val)

    def abc(self, *args, **kwargs):
        """
  returns lattice parameters and angles
  
  ### Syntax
  
  `latvect = abc(obj)`
  
  ### Description
  
  `latvect = abc(obj)` extracts the lattice vectors and angles from a
  [spinw] object.
  
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  ### Output Arguments
  
  `latVect`
  : Vector with elements `[a, b, c, \\alpha, \\beta, \\gamma]`,
    contains the lattice parameters and angles by default in \\ang and
    degree units respectively (see [spinw.unit] for details).
  
  ### See Also
  
  [spinw.horace]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('abc')), 1)
        return m.abc(self.handle, *args, nargout=nout)

    def addaniso(self, *args, **kwargs):
        """
  assigns anisotropy to magnetic sites
  
  ### Syntax
  
  `addaniso(obj, matrixIdx, {atomTypeIdx}, {atomIdx})`
  
  ### Description
  
  `addaniso(obj, matrixIdx, {atomTypeIdx}, {atomIdx})` assigns the
  $[3\times 3]$ matrix selected by `matrixIdx` (using either the matrix
  label or matrix index) to the magnetic sites selected by `atomTypeIdx`
  that can contain a name of an atom or its atom index (see [spinw.atom]).
  If `atomTypeIdx` is not defined, anisotropy will be assigned to all
  magnetic atoms.
  
  ### Examples
  
  To show the effect of a fourfold axis on anisotropy, we add $A_1$
  easy-axis anisotropy to atoms at $(1/4,1/4,1/2)$ and plot the result. The
  3D plot shows anistropy using ellipsoid around the magnetic atoms.
 
  ```
  >>cryst = spinw
  >>cryst.genlattice('lat_const',[4 4 3],'sym','P 4')
  >>cryst.addatom('r',[1/4 1/4 1/2],'S',1)
  >>cryst.addmatrix('label','A1','value',diag([-0.1 0 0]))
  >>cryst.gencoupling
  >>cryst.addaniso('A1')
  >>plot(cryst)
  >>snapnow
  ```
  
  ### Input arguments
 
  `obj`
  : [spinw] object.
 
  ### Name-Value Pair Arguments
  
  `matrixIdx`
  : Either an integer, that selects the matrix according to
    `obj.matrix.mat(:,:,matrixIdx)`, or a string identical to one
    of the previously defined matrix labels, stored in
    `obj.matrix.label`.
  
  `atomTypeIdx`
  : String or cell of strings that select magnetic atoms by
    their label. Also can be a vector that contains integers, the index of
    the magnetic atoms in `obj.unit_cell`, with all symmetry equivalent
    atoms. Maximum value is $n_{atom}$, if undefined anisotropy is assigned to
    all magnetic atoms. Optional.
 
  `atomIdx`
  : A vector that contains indices selecting some of the
    symmetry equivalent atoms. Maximum value is the number of symmetry
    equivalent atoms generated corresponding to `atomTypeIdx` site. If
    crystal symmetry is not 0, `atomIdx` is not allowed, since the
    anisotropy matrix for equivalent atoms will be calculated using the
    symmetry operators of the space group. Optional.
  
  ### Output Arguments
  
  The function adds extra entries in the `obj.single_ion.aniso` field of the
  obj [spinw] object.
  
  ### See Also
  
  [spinw], [spinw.single_ion], [spinw.addcoupling], [spinw.addg] and [spinw.addmatrix]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('addaniso')), 1)
        return m.addaniso(self.handle, *args, nargout=nout)

    def addatom(self, *args, **kwargs):
        """
  adds new atom
  
  ### Syntax
  
  `addatom(obj,Name,Value)`
  
  ### Description
  
  `addatom(obj,Name,Value)` adds a new atom to the list of symmetry
  inequivalent sites together with its properties, such as position, spin
  quantum number, form factor, etc.
  
  ### Examples
  
  To add a magnetic atom with $S=1$ at position $r=(0,0,0)$ and a
  non-magnetic one at $r=(1/2,0,0)$ with red and blue color respectively
  use the following command
 
  ```
  >>crystal = spinw;
  >>crystal.genlattice('lat_const',[4 3 3])
  >>crystal.addatom('r',[0 1/2; 0 0; 0 0],'S',[1 0],'color',{'red' 'blue'})
  >>crystal.plot
  ```
  
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  ### Name-Value Pair Arguments
  
  `r`
  : Atomic positions stored in a matrix with dimensions of $[3\times
    n_{atom}]$.
  
  `label`
  : Names of the atoms in a cell for plotting and form factor
    calculations (see [magion.dat]), e.g. `label={'atom1' 'atom2'
    'atom3'}`.
    Default value is `atomi`, where `i` is the atom index.
  
  `S`
  : Spin quantum number stored in a row vector with $n_{atom}$ elements,
    for non-magnetic atoms set S to zero. If not given the spin quantum
    number is guessed from the given label of the atom. For example if
    `label` is `MCr3+` or `Cr3+` then the $S=3/2$ high spin state is
    assumed for Cr$^{3+}$. The spin values for every ion is stored in the
    [magion.dat] file. If the atom type is unknown $S=0$ is assumed. Only
    positive S are allowed.
  
  `color`
  : RGB color of the atoms for plotting stored in a matrix with dimensions
    of $[3\times n_{atom}]$, where each column describes an RGB color. Each
    value is between 0 and 255. Default value is the color stored in the
    [atom.dat] file. Alternatively a name of the color can be given as a
    string, for example `'White'`, for multiple atoms package it into a
    cell. For the list of colors, see [swplot.color] or the [color.dat]
    file.
  
  `ox`
  : Oxidation number given as a double or it will be determined
    automatically from label. Default value is 0.
  
  `occ`
  : Occupancy, given as double. Default value is 1.
  
  `formfact`
  : Neutron scattering form factor, given as a row vector with 9 numbers,
    for details see [sw_mff]. Also string labels can be used from the
    [magion.dat] file.
  
  `formfactn`
  : Same as the `formfact` option.
  
  `formfactx`
  : X-ray scattering form factor, given as 9 numbers, for details
    see [sw_cff], also labels can be used from the [xrayion.dat] file.
  
  `Z`
  : Atomic number, given as integer or determined from the atom label
    automatically. Default value is 113 (Unobtanium).
  
  `A`
  : Atomic mass, given as integer. Default is -1 for the natural
    mixture of isotopes.
  
  `bn`
  : Neutron scattering length, given as double.
  
  `bx`
  : X-ray scattering length, given as double. Not yet implmented, this
    input will be ignored.
  
  `biso`
  : Isotropic displacement factors in units of \\ang$^2$.
    Definition is the same as in
    [FullProf](<a href="matlab:web https://www.ill.eu/sites/fullprof/">https://www.ill.eu/sites/fullprof/</a>), defining the
    Debye-Waller factor as $W(d) = 1/8*b_{iso}/d^2$, which is included in
    the structure factor as $exp(-2W(d))$.
  
  `update`
  : If `true`, existing atom with the same label and position as a
    new one will be updated. Default is `true`.
  
  ### Output Arguments
  
  The function modifies the [spinw.unit_cell] property of the obj
  [spinw] object.
  
  ### See Also
  
  [spinw.genlattice] \| [spinw.addmatrix] \| [swplot.color] \| [sw_mff] \| [sw_cff]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('addatom')), 1)
        return m.addatom(self.handle, *args, nargout=nout)

    def addcoupling(self, *args, **kwargs):
        """
  assigns an exchange matrix to a bond
  
  ### Syntax
  
  `addcoupling(obj,Name,Value)`
  
  ### Description
  
  `addcoupling(obj,Name,Value)` assigns a matrix (will be used as exchange
  matrix) to a given bond after bonds are generated using
  [spinw.gencoupling].
  
  ### Examples
  
  To add the $J_1$ diagonal matrix to all second neighbor bonds
  between magnetic atoms use the following:
 
  ```
  >>cryst = sw_model('squareAF',1)
  >>cryst.addmatrix('label','J1','value',diag([1 0.1 0.1]))
  >>cryst.gencoupling
  >>cryst.addcoupling('mat','J1','bond',2)
  >>plot(cryst,'range',[2 2 1])
  >>snapnow
  ```
  
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  ### Name-Value Pair Arguments
  
  `'mat'`
  : Label (string) or index (integer) of the matrix that will be assigned to
    selected bonds, e.g. `'J1'`.
  
  `'bond'`
  : Integer that selects bonds, e.g. 1 for first neighbor, 2 for second
    neighbor, etc. The given value is compared to the `obj.coupling.idx`
    vector and the exchange matrix will be assigned to matching bonds.
    `'bond'` can be also a row vector to assign matrices to multiple bonds.
  
  `'atom'`
  : Contains labels of atoms (string) or index of atoms (integer) that is
    compared to [spinw.unit_cell] where all symmetry inequivalent atoms are
    stored. If a single string label or number is given, e.g. `'Cr1'` only
    Cr1-Cr1 bonds will be assigned. If a cell with 2 strings, e.g. `{'Cr1'
    'Cr2'}` only Cr1-Cr2 bonds will be assigned. Default value is `[]`.
  
  `'subIdx'`
  : If the above options are not enough to select the desired
    bonds, using `subIdx` bonds can be selected one-by-one from
    the list of bonds that fulfill the constraint of `atom` and `bond`.
  
  `'type'`
  : Type of the coupling with possible values of:
    * `'quadratic'`     Quadratic exchange, default.
    * `'biquadratic'`   Biquadratic exchange.
  
  `'sym'`
  : If `true`, symmetry operators will be applied on the exchange
    matrices to generate the coupling on symmetry equivalent
    bonds, if `false` all symmetry equivalent bonds will have the
    same exhcange matrix.
  
  {{warning Setting `atom` or `subIdx` parameters will remove the symmetry
  operations on the selected bonds. This means that assigning any
  non-Heisenberg exchange matrix will break the space group defined in
  `obj.lattice.sym`. Effectively reducing the symmetry of the given bond to
  `P0`}}
 
  ### Output Arguments
  
  The function adds extra entries to the [spinw.coupling] property of
  `obj`. Specifically it will modify `obj.coupling.mat_idx`,
  `obj.coupling.type` and `obj.coupling.sym` matrices.
  
  ### See Also
  
  [spinw] \| [spinw.gencoupling] \| [spinw.addmatrix]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('addcoupling')), 1)
        return m.addcoupling(self.handle, *args, nargout=nout)

    def addg(self, *args, **kwargs):
        """
  assigns g-tensor to magnetic atoms
  
  ### Syntax
  
  `addg(obj, matrixIdx, {atomTypeIdx}, {atomIdx})`
  
  ### Description
  
  `addg(obj, matrixIdx, {atomTypeIdx}, {atomIdx})` assigns the
  $[3\times 3]$ matrix selected by `matrixIdx` (using either the matrix
  label or matrix index) to the magnetic sites selected by `atomTypeIdx`
  that can contain a name of an atom or its atom index (see [spinw.atom]).
  If `atomTypeIdx` is not defined, g-tensor will be assigned to all
  magnetic atoms.
  
  ### Examples
  
  The following example will add the $g_1$ diagonal matrix to all magnetic
  atoms as anisotropic g-tensor and show the effect of a fourfold axis:
  
  ```
  >>cryst = spinw
  >>cryst.genlattice('lat_const',[4 4 3],'sym','P 4')
  >>cryst.addatom('r',[1/4 1/4 1/2],'S',1)
  >>cryst.addmatrix('label','g_1','value',diag([2 1 1]))
  >>cryst.gencoupling
  >>cryst.addg('g_1')
  >>cryst.plot('ionMode','g')
  >>snapnow
  ```
  
  ### Input Arguments
  
  `matrixIdx`
  : Either an integer, that selects the matrix
    `obj.matrix.mat(:,:,matrixIdx)`, or a string identical to one
    of the previously defined matrix labels, stored in
    `obj.matrix.label`. Maximum value is $n_{mat}$.
  
  `atomTypeIdx`
  : String or cell of strings that select magnetic atoms by
    their label. Also can be a vector that contains integers, the index of
    the magnetic atoms in [spinw.unit_cell], this will assign the given
    g-tensor to all symmetry equivalent atoms. Maximum value is $n_{atom}$.
    If `atomTypeIdx` is not defined, the given g-tensor will be assigned to
    all magnetic atoms. Optional.
 
  `atomIdx`
  : A vector that contains indices selecting some of the
    symmetry equivalent atoms. Maximum value is the number of symmetry
    equivalent atoms corresponding to `atomTypeIdx`. If the crystal
    symmetry is higher than $P0$, `atomIdx` is not allowed, since the
    g-tensor for equivalent atoms will be calculated using the symmetry
    operators of the space group. Optional.
  
  ### Output Arguments
  
  The function adds extra entries to the `obj.single_ion.g` matrix.
  
  ### See Also
  
  [spinw] \| [spinw.addcoupling] \| [spinw.addaniso] \| [spinw.addmatrix]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('addg')), 1)
        return m.addg(self.handle, *args, nargout=nout)

    def addlistenermulti(self, obj=None, chgField=None, **kwargs):
        """
  create the corresponding listeners to each cache subfield


        """
        args = tuple(v for v in [obj, chgField] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('addlistenermulti')), 1)
        return m.addlistenermulti(self.handle, *args, nargout=nout)

    def addmatrix(self, *args, **kwargs):
        """
  adds new 3x3 matrix
  
  ### Syntax
  
  `addmatrix(obj,Name,Value)`
  
  ### Description
  
  `addmatrix(obj,Name,Value)` adds a new $[3\times 3]$ matrix to the
  [spinw.matrix] field of `obj`. The added matrices can be later assigned
  to bonds, single ion anisotropy terms or g-tensors of magnetic atoms. If
  the given matrix label already exists in `obj`, instead of adding new
  matrix the existing one will be overwritten.
  
  ### Examples
  
  The first example adds a diagonal matrix `eye(3)`, that can describe
  Heisenberg interaction if assigned to a bond. The second example adds an
  ansisymmetric matrix that can decribe Dzyaloshinskii-Moriya (DM)
  interaction if assigned to a bond.
 
  ```
  >>crystal = spinw
  >>crystal.addmatrix('value',1,'label','J_1')
  >>crystal.matrix.mat>>
  >>crystal.addmatrix('value',[1 0 0],'label','J_1')
  >>crystal.matrix.mat>>
  ```
  
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  ### Name-Value Pair Arguments
  
  `'value'`
  : The actual numerical values to be added as a matrix. It can have the
    following shapes:
    * $[3\times 3]$ the given values will be stored in [spinw.matrix] as
      they are given.
    * $[1\times 1]$ the given value will be multiplied with `eye(3)`.
    * `[Mx My Mz]` the given triplet will be used to define an
      antisymmetric matrix `M = [0 M3 -M2;-M3 0 M1;M2 -M1 0]`. 
  
  `'label'`
  : Label string for plotting default value is `'matI'`, where $I$ is the index
    of the matrix. Add '-' to the end of the label to plot bond as dashed
    line/cylinder.
  
  `'color'`
  : Color for plotting, either row vector
    that contains color RGB codes (values of 0-255), or a string with the
    name of the color, for possible colors names [swplot.color]. Default
    color is a random color.
  
  ### Output Arguments
  
  The `obj` output will contain the additional matrix in the [spinw.matrix]
  field.
  
  ### See Also
  
  [spinw] \| [swplot.color]
 
  *[DM]: Dzyaloshinski-Moriya
  *[RGB]: Red-Green-Blue


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('addmatrix')), 1)
        return m.addmatrix(self.handle, *args, nargout=nout)

    def addtwin(self, *args, **kwargs):
        """
  adds crystallographic twins
  
  ### Syntax
  
  `addtwin(obj,Name,Value)`
  
  ### Description
  
  `addtwin(obj,Name,Value)` adds crystallographic twins defined by a
  rotation matrix and its volume fraction. Using crystallographic twins,
  SpinW can simulate imperfect samples and if the relative orientation of
  the crystallographic twins are knows, SpinW simulations can be directly
  compared to the expeiments on the inperfect sample.
  
  ### Examples
  
  This example shows how to add two extra crystallographic twins to the
  crystal.  Together with the original orientation there will be three
  twins with equal volumes.
 
  ```
  cryst.addtwin('axis',[0 0 1],'phid',[60 120],'vol',[1 1])
  ```
  
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  ### Name-Value Pair Arguments
  
  `'axis'`
  : Defines the axis of rotation to generate twins in the xyz
    coordinate system, dimensions are $[1\times 3]$.
  
  `'phi'`
  : Defines the angle of rotation to generate twins in radian
    units. Several twins can be defined parallel if `phi` is a
    row vector. Dimensions are $[1\times n_{twin}]$.
  
  `'phid'`
  : Alternative to `phi` but the unit is \\deg.
  
  `'rotC'`
  : Rotation matrices, that define crystallographic twins. This is an
    alternative to the `axis`-`phi` parameter pair. Matrix dimensions are 
    $[3\times 3\times n_{twin}]$.
  
  `'vol'`
  : Volume fractions of the twins stored in a row vector with $n_{twin}$
    elements. Default value is `ones(1,nTwin)`.
  
  `'overwrite'`
  : If `true`, the last twin will be overwritten, instead of adding a
    new one. Default is `false`.
  
  ### Output Arguments
  
  The function adds extra entries to the [spinw.twin] property.
  
  ### See Also
  
  [spinw] \| [spinw.twinq]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('addtwin')), 1)
        return m.addtwin(self.handle, *args, nargout=nout)

    def anneal(self, *args, **kwargs):
        """
  performs simulated annealing of spins
 
  ### Syntax
 
  `stat = anneal(obj,Name,Value)`
 
  ### Description
 
  `stat = anneal(obj,Name,Value)` performs simulated annealing on the spin
  Hamiltonian defined in `obj`. It assumes a classical spin system and
  employs the [Metropolis–Hastings
  algorithm](<a href="matlab:web https://en.wikipedia.org/wiki/Metropolis–Hastings_algorithm">https://en.wikipedia.org/wiki/Metropolis–Hastings_algorithm</a>)
  for state updates. The annealing is performed from a given initial
  temperature down to final temperature with user defined steps and number
  of Monte-Carlo cycles per temperature. The `<strong>spinw/anneal</strong>` can also
  measure different thermodynamic quantities, such as heat capacity. The
  function can deal with single ion anisotropy and arbitrary exchange
  interactions. It can also restrict the spin degrees of freedom from 3
  (default) to 2 or 1 to speed up simulation on xy and Ising systems. For
  these restricted dimensions only isotropic exchange interactions are
  allowed. Also the g-tensor is assumed to be 2.
 
  {{warning The calculated energies does not contain the self energy (spin
  coupled to itself), thus the energies calculated here can differ from the
  output of [spinw.energy].}}
 
 
  ### Input Arguments
 
  `obj`
  : [spinw] object.
 
  ### Name-Value Pair Arguments
 
  `'spinDim'`
  : Dimensionality of the spins:
    * **1**     Ising spins.
    * **2**     XY spins.
    * **3**     Heisenberg spins, default.
 
    For Ising (spinDim=1) and XY (spinDim=2) models only isotropic
    exchange interaction and magnetic field can be used. For Ising
    the direction of the spins are along x-axis, for XY model the
    the xy-plane. Magnetic fields perpendicular to these directions
    are omitted.
 
  `'initT'`
  : The initial temperature, can be any positive number
    in units of Kelvin. Default value is 1.
 
  `'endT'`
  : Temperature at which the annealing will stop, can be any positive number
    smaller than `initT`, unit is Kelvin.
    Default value is $10^{-3}$.
 
  `'cool'`
  : Defines how the following temperature value is calculated from the
    previous one using a user function. Any function that takes a scalar as input and
    returns a smaller but positive scalar as output. Default is `@(T)(0.92*T)`.
 
  `'random'`
  : If `true` the initial spin orientation will be random, which is
    effectively a $T=\infty$ paramagnet. If the initial spin configuration
    is undefined (`obj.magstr.S` is empty) the initial configuration
    is always random independently of this parameter.
    Default value is `false`.
 
  `'nMC'`
  : Number of Monte-Carlo steps per spin at each temperature
    step  which includes thermalization and the sampling for the extracted
    TD properties at the last temperature). Default is 100.
 
  `'nORel'`
  : Number of over-relaxation steps after every Monte-Carlo
    steps. It rotates the spins around the direction of the local field by
    180\\deg. It is reversible and microcanonical if the single ion
    anisotropy is 0. Default value is 0, to omit over-relaxation.
 
  `'nStat'`
  : Number of cycles at the last temperature to calculate
    statistical averages. It has to be smaller or equal $n_{MC}$.
    Default value is 100.
 
  `'boundary'`
  : Boundary conditions of the extended unit cell:
    * **free**  Free, interactions between extedned unit cells are
                omitted.
    * **per**   Periodic, interactions between extended unit cells
                are retained.
    Default value is `{'per' 'per' 'per'}`.
 
  `'verbosity'`
  : Controls the amount of output to the Command Window:
    * **0**   Suppresses all output.
    * **1**   Gives final report only.
    * **2**   Plots temperature changes and final report, default value.
 
  `'nExt'`
  : The size of the magnetic cell in number of unit cells that can override
    the value stored in `obj.magstr.N_ext`, given by a row vector with
    three integers
 
  `'fStat'`
  : Function handle to measure TD quantities at the final temperature
    for `nStat` Monte-Carlo steps. The function returns a single structure
    and takes fixed input parameters:
    ```
    parOut = fStat(state, parIn, T, E, M, nExt).
    ```
    The function is called once before the annealing process
    when `state=1` to initialise the parameters. The function is called
    after every Monte-Carlo cycle with `state=2` and the output of the
    previous function call is assigned to the input struct. `fStat` is called
    once again in the end with `state=3` to calculate final parameters (in
    the last run, input `parIn.param` contains all the annealing
    parameters). For comparison see the defaul function [sw_fstat].
    Default value is `@sw_fstat`.
 
  `'fSub'`
  : Function to define sublattices for Monte-Carlo speedup. Function handle
    with the following header:
    ```
    cGraph = fSub(conn,nExt)
    ```
    where `cGraph` is a row vector with $n_{magExt}$ number of elements
    `conn` is a matrix with dimensions of $[2\times n_{conn}]$ $n_{ext}$ is
    equal to `nExt`. For the SpinW implementation see [sw_fsub]. Default
    value is `@sw_fsub`.
 
  `'subLat'`
  : Vector that assigns all magnetic moments into non-interacting
    sublattices, contains a single index $(1,2,3...)$ for every
    magnetic moment, row vector with $n_{magExt}$ number of elements. If
    undefined, the function defined in `fSub` parameter will be used to
    partition the lattice.
 
  `'title'`
  : Gives a title string to the simulation that is saved in the
    output.
 
  `'autoK'`
  : Bin length of the autocorrelation vector. Should be a few times
    smaller than `nMC`. Default value is 0 when no autocorrelation function
    is calculated.
 
  ### Output Arguments
 
  `stat` struct that contains the calculated TD averages and the parameters
  of the simulation with the following fields:
 
  `param`
  : All input parameter values of the anneal function.
 
  `obj`
  : The clone of the input `obj` updated with the final magnetic
    structure.
 
  `M`
  : Components of the magnetisation after the last annealing
    run stored in a matrix with dimensions of $[3\times n_{magExt}]$.
 
  `E`
  : Energy of the system after the last annealing run, excluding the self
    energy.
 
  `T`
  : Final temperature of the sample.
 
  Depending on the `fStat` parameter, additional fields are included. Using
  the default function [sw_fstat] the following parameters are also
  calculated:
 
  `avgM`
  : Average value of the magnetisation vector sampled over `nStat` runs,
    stored in a matrix with dimensions of $[3\times n_{magExt}]$.
 
  `stdM`
  : Standard deviation of the mgnetisation vector sampled over
    `nStat` runs, stored in a matrix with dimensions of $[3\times
    n_{magExt}]$.
 
  `avgE`
  : Average system energy per spin averaged over `nStat` runs, scalar.
 
  `stdE`
  : Standard deviation of the system energy per spin over
    `nStat` runs, scalar.
 
  `Cp`
  : Heat capacity of the sample, calculated using the formula $(\langle E^2\rangle-\langle E\rangle^2)/k_B/T^2$.
 
  `Chi`
  : Magnetic susceptibility of the sample calculated using the formula $(\langle M^2\rangle-\langle M\rangle^2)/k_B/T$.
 
 
  ### Reference
 
     Kirkpatrick, S., Gelatt, C.D., & Vecchi, M.P. (1983). Optimization by
     Simulated Annealing. _Science, 220_, 671-680.
 
  ### See Also
 
  [spinw] \| [spinw.optmagstr] \| [sw_fsub] \| [sw_fstat]
 
  *[TD]: Thermodynamic


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('anneal')), 1)
        return m.anneal(self.handle, *args, nargout=nout)

    def annealloop(self, *args, **kwargs):
        """
  parameter sweep for simulated annealing
  
  ### Syntax
  
  `stat = anneal(obj,Name,Value)`
  
  ### Description
  
  `stat = annealloop(obj,Name,Value)` performs simulated annealing while
  stepwise changing a selected parameter such as temperature or magnetic
  field while measuring thermodynamic properties. The function has the same
  parameters as [spinw.anneal] plus an additional
   
  
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  ### Name-Value Pair Arguments
  
  `'func'`
  : Function that changes the parameters in the spinw object in every
    loop. Default function is to change the temperature:
    ```
    @temperature(obj,x)
    ```
    The function takes two inputs a [spinw] object and a parameter value
    (ir values in a vector) and changes the correspondign property inside
    the object.
  
  `'x'`
  : Matrix of values of the loop parameter, with dimensions of
    $[n_{par}\times n_{loop}]$. Default value is 1. In the i-th loop the
    loop function is called as:
    ```
    func(obj,x(:,i));
    ```
  
  `'saveObj'`
  : If `true`, the spinw object is saved after every annealing step for
    debugging purposes. Default is `false`.
 
  `'tid'`
  : Determines if the elapsed and required time for the calculation is
    displayed. The default value is determined by the `tid` preference
    stored in [swpref]. The following values are allowed (for more details
    seee [sw_timeit]):
    * `0` No timing is executed.
    * `1` Display the timing in the Command Window.
    * `2` Show the timing in a separat pup-up window.
  
  ### Output Arguments
  
  Same output as of [spinw.anneal], just the struct is packaged into a cell
  with $n_{loop}$ number of elements.
 
  ### Reference
 
     Kirkpatrick, S., Gelatt, C.D., & Vecchi, M.P. (1983). Optimization by
     Simulated Annealing. _Science, 220_, 671-680.
  
  ### See Also
  
  [spinw] \| [spinw.anneal] \| [sw_fsub] \| [sw_fstat]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('annealloop')), 1)
        return m.annealloop(self.handle, *args, nargout=nout)

    def atom(self, *args, **kwargs):
        """
  generates symmetry equivalent atomic positions
  
  ### Syntax
  
  `atomList = atom(obj)`
  
  ### Description
  
  `atomList = atom(obj)` generates all atomic positions using the symmetry
  operators stored in `obj.lattice.sym` and the symmetry inequivalent
  atomic positions in `obj.unit_cell.r`. If no symmetry is defined (denoted
  $P0$ symmetry) or the symmetry is $P1$ the function returns simply the
  positions stored in `obj.unit_cell.r`.
  
  ### Examples
  
  Here we create a new space group, that contains all the translations of
  the FCC lattice. Then create a crystal with an atom at `[0 0 0]` position.
  The `cryst.atom` lists all 4 symmetry equivalent positions generated using
  the FCC symmetry operators:
 
  ```
  >>cryst = spinw
  >>opStr = 'x+1/2,y+1/2,z;x+1/2,y,z+1/2;x,y+1/2,z+1/2';
  >>cryst.genlattice('lat_const',[8 8 8],'sym',opStr,'label','FCC')
  >>cryst.addatom('r',[0 0 0],'label','Atom1')
  >>atomList = cryst.atom
  >>atomList.r>>
  ```
 
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  ### Output Arguments
  
  `atomList` is a structure with the following fields:
  * `r`     Positions of the atoms in lattice units stored in matrix with
            dimensions of $[3\times n_{atom}]$. 
  * `idx`   Indices of the atoms in the [spinw.unit_cell] field stored in a
            matrix with dimensions of $[1\times n_{atom}]$.
  * `mag`   Vector of logical variables, `true` if the spin of the atom is
            non-zero, dimensions are $[1\times n_{atom}]$.
  
  ### See Also
  
  [spinw] \| [spinw.matom] \| [swsym.add] \| [spinw.genlattice] \| [spinw.addatom]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('atom')), 1)
        return m.atom(self.handle, *args, nargout=nout)

    def basisvector(self, *args, **kwargs):
        """
  generates lattice vectors
  
  ### Syntax
  
  `basisVec = basisvector(obj, {norm})`
  
  ### Description
  
  `basisVec = basisvector(obj, {norm})` returns the lattice vectors of the
  unit cell in a $[3\times 3]$ matrix, with the $a$, $b$ and $c$ vectors
  stored in columns. The vectors are normalized to the lattice parameters
  by default.
  
  ### Examples
  
  The `basisVec` matrix can be used to change coordinate system, converting
  between positions expressed in lattice units to positions expressed in
  \\ang, using `r_lu` for lattice unit coordinates and `r_xyz` for
  \\ang units (both stored in a column vector) the conversions are the
  following:
  ```
  r_xyz = basisVec * r_lu
  ```
  or
  ```
  r_lu = inv(basisVec)*r_xyz
  ```
 
  It is also possible to convert between momentum vector in reciprocal
  lattice units (rlu) into \\ang$^{-1}$ units. Assuming that momentum
  vectors are row vectors:
  ```
  Q_xyz =  Q_rlu * 2*pi*inv(basisVec)
  ```
  or
  ```
  Q_rlu = 1/(2*pi)*Q_xyz*basisVect
  ```
  
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  `norm`
  : If `true`, the basis vectors are normalized to 1, otherwise the
    length of the basis vectors are equal to the lattice constants. Default
    is `false`.
  
  ### Output Arguments
  
  `basisVec`
  : Stores the three lattice vectors in columns, dimensions are $[3\times 3]$.
  
  ### See Also
  
  [spinw] \| [spinw.abc] \| [spinw.rl]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('basisvector')), 1)
        return m.basisvector(self.handle, *args, nargout=nout)

    def clearcache(self, obj=None, chgField=None, **kwargs):
        """
  clears the cache
 
  ### Syntax
 
  `clearcache(obj)`
 
  ### Description
 
  `clearcache(obj)` clears the cache that contains
  precalculated magnetic structure and bond symmetry operators.
  It is not necessary to clear the cache at any point as SpinW
  clears it whenever necessary. 
 
  ### See Also
 
  [spinw.cache]


        """
        args = tuple(v for v in [obj, chgField] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('clearcache')), 1)
        return m.clearcache(self.handle, *args, nargout=nout)

    def copy(self, *args, **kwargs):
        """
  clones spinw object
  
  ### Syntax
  
  `newObj = copy(obj)`
  
  ### Description
  
  `newObj = copy(obj)` clones a SpinW object with all of its internal data.
  The `newObj` will be independent of the original `obj`. Since the [spinw]
  is a handle class, this command should be used to duplicate an object
  instead of the `=` operator. Using the `=` operator does not create a new
  object, but only a pointer that points to the original object:
  ```
  obj2 = obj
  ```
  Changing `obj` after the above command will also change `obj2`.
 
  ### Examples
  
  In this example $J_{1a}$ is a matrix with 1 in the diagonal, while
  $J_{1b}$ has 3.1415 in the diagonal. If `cryst` is changed, `cryst1` will
  be changed as well and viece versa, since they point to the
  same object. However `cryst2` is independent of `cryst`:
 
  ```
  >>cryst = spinw
  >>cryst.addmatrix('label','J1','value',3.1415)
  >>cryst1 = cryst
  >>cryst2 = cryst.copy
  >>cryst.addmatrix('label','J1','value',1)
  >>J1a = cryst1.matrix.mat>>
  >>J1b = cryst2.matrix.mat>>
  ```
 
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  ### Output Arguments
  
  `newObj`
  : New [spinw] object that contains all the data of `obj`.
  
  ### See Also
  
  [spinw] \| [spinw.struct]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('copy')), 1)
        return m.copy(self.handle, *args, nargout=nout)

    def couplingtable(self, *args, **kwargs):
        """
  creates tabulated list of all bonds as stored
 
  bonds = <strong>couplingtable</strong>(obj,{bondIdx})
 
  Input:
 
  obj       spinw class object. 
  bondIdx   List of bond indices, by default all bonds will be output.
            Optional. If a bond index is mutiplied by -1, the table output
            is a matlab built in table type, works only for Matlab R2013b
            or later versions.
 
  Output:
 
  bonds is a struct type data that contains the following fields:
    table   Matrix, where every column defines a bond. The rows are the
            following: (dl_x, dl_y, dl_z, atom1, atom2, idx, mat_idx1,
            mat_idx2, mat_idx3). Where (dl_x, dl_y, dl_z) defines the
            translation vector between the origin of the unit cells of the
            two interacting atom (if they are in the same unit cell, all
            three components are zero) from atom1 to atom2. atom1 and atom2
            are the indices of the atoms in the obj.matom list. idx is the
            index of the bond, where equivalent bonds have identical
            indices, typically index is increasing with bond length. The
            last 3 rows (mat_idx) contains pointers to matrices if they
            are defined, otherwise zeros.
    bondv   Additional information for every bond defined in the .table
            field. The first three rows define the vector pointing from
            atom1 to atom2 in lattice units. The last row define the bond
            length in Angstrom.
    matrix  Contains the coupling matrix for every bond, dimensions are
            [3 3 nCoupling].
 
  Example:
 
  ...
  crystal.gencoupling
  bonds = crystal.couplingtable(-[1 2 3]).table
 
  This will list only the 1st, 2nd and 3rd neighbour bonds in a formatted
  table.
 
  See also <a href="matlab:help spinw/matom -displayBanner">spinw/matom</a>, <a href="matlab:help spinw/intmatrix -displayBanner">spinw/intmatrix</a>, <a href="matlab:help spinw/addcoupling -displayBanner">spinw/addcoupling</a>, <a href="matlab:help spinw/gencoupling -displayBanner">spinw/gencoupling</a>.


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('couplingtable')), 1)
        return m.couplingtable(self.handle, *args, nargout=nout)

    def datastruct(self, *args, **kwargs):
        """
SPINW/<strong>datastruct</strong> is an undocumented builtin function.


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('datastruct')), 1)
        return m.datastruct(self.handle, *args, nargout=nout)

    def disp(self, *args, **kwargs):
        """
  prints information
 
  ### Syntax
 
  `{swdescr} = disp(obj)`
 
  ### Description
 
  `{swdescr} = disp(obj)` generates text summary of a [spinw] object.
  Calling it with output argument, it will generate a text version of the
  internal data structure giving also the dimensions of the different
  matrices.
 
  ### Examples
 
  Here the internal data structure is generated:
 
  ```
  >>crystal = spinw
  >>swFields = disp(crystal)>>
  ```
 
  ### Input Arguments
 
  `obj`
  : [spinw] object.
 
  ### Output Arguments
 
  `swdescr`
  : If output variable is given, the description of the `obj` object
    will be output into the `swdescr` variable, instead of being
    written onto the Command Window/file. Optional.
 
  ### See Also
 
  [spinw]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('disp')), 1)
        return m.disp(self.handle, *args, nargout=nout)

    def energy(self, *args, **kwargs):
        """
  calculates the ground state energy
 
  ### Syntax
 
  `E = energy(obj,Name,Value)`
 
  ### Description
 
  `E = energy(obj,Name,Value)` calculates the classical ground state energy
  per spin. The calculation correctly takes into account the magnetic
  supercell. The function gives correct results on single-k magnetic
  structures even defined on magnetic supercells. For multi-k magnetic
  structures first a definition of a larger supercell is necessary where an
  effective $k=0$ representation is possible.
 
  ### Examples
 
  After optimising the magnetic structure (by minimizing the ground state
  energy), the energy per spin is calculated. This can be compared to
  different ground state structures to decide which is the right classical
  ground state of the magnetic model in cryst. Here we use the triangular
  lattice antiferromagnet where we define the magnetic structure on a
  $[3\times 3]$ magnetic supercell where the optimal structure (120\\deg
  angle between neighboring spins) has a 0 propagation vector. In this case
  the exact energy is $3\cdot 1^2\cdot \cos(120^\circ) = -1.5$.
 
  ```
  >>cryst = sw_model('triAF',1)
  >>cryst.genmagstr('mode','random','nExt',[3 3 1])
  >>cryst.optmagsteep('nRun',10)
  >>cryst.energy>>
  ```
 
  ### Input Arguments
 
  `obj`
  : [spinw] object.
 
  ### Name-Value Pair Arguments
 
  `'epsilon'`
  : The smallest value of incommensurability that is tolerated
    without warning. Default is $10^{-5}$.
 
  ### Output Arguments
 
  `E`
  : Energy per moment (anisotropy + exchange + Zeeman energy).
 
  {{warning The calculated energy can be wrong for incommensurate
  structures. For example a structure where the spins are rotating in $XY$
  plane with an incommensurate wavevector of $(1/3,0,0)$. The function only
  calculates the anisotropy energy in the first unit cell, that is for
  single spin $E_{aniso} = A_{xx}\cdot S_{xx}^2+A_{yy}\cdot S_{yy}^2$.
  While the anisotropy energy in reality is independent of the spin
  orientation in the $XY$ plane $E_{aniso}=3S\cdot (A_{xx}+A_{yy})/2$. Thus
  using `<strong>spinw/energy</strong>` on incommensurate structures together with single
  ion anisotropy one has to be carefull! In the triangular case one has to
  extend the unit cell to `nExt = [3 3 1]` (in the hexagonal setting), in
  this case the energy will be correct.}}
 
  ### See Also
 
  [spinw] \| [spinw.anneal] \| [spinw.newcell]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('energy')), 1)
        return m.energy(self.handle, *args, nargout=nout)

    def export(self, *args, **kwargs):
        """
  export data into file
  
  ### Syntax
  
  `export(obj,Name,Value)`
  
  `outStr = export(obj,Name,Value)`
 
  ### Description
  
  `export(obj,Name,Value)` exports different types of spinw object data.
 
  `outStr = export(obj,Name,Value)` returns a string instead of writing the
  data into a file.
 
  ### Examples
  
  In this example the crystal structure is imported from the `test.cif`
  file, and the atomic positions are saved into the `test.pcr` file for
  FullProf refinement (the pcr file needs additional text to work with
  FullProf).
 
  ```
  cryst = sw('test.cif');
  cryst.export('format','pcr','path','test.pcr');
  ```
 
  ### Input arguments
 
  `obj`
  : [spinw] object.
 
  ### Name-Value Pair Arguments
 
  `'format'`
  : Determines the output data and file type. The supported file formats
    are:
    * `'pcr'`   Creates part of a .pcr file used by [FullProf](<a href="matlab:web https://www.ill.eu/sites/fullprof">https://www.ill.eu/sites/fullprof</a>). It exports the
      atomic positions.
    * `'MC'`    Exports data into a custom file format for Monte Carlo simulations.
 
  `'path'`
  : Path to a file into which the data will be exported, `out` will
    be `true` if the file succesfully saved, otherwise `false`.
 
  `'fileid'`
  : File identifier that is already opened in Matlab using the
    `fileid = fopen(...)` command. Don't forget to close the file
    afterwards.
   
  #### File format dependent options:
   
  `'perm'` (`pcr`)
  : Permutation of the $xyz$ atomic positions, default value is `[1 2 3]`.
   
  `'boundary'` (`MC`)
  : Boundary conditions of the extended unit cell. Default value is `{'per'
    'per' 'per'}`. The following strings are accepted:
    * `'free'`  Free, interactions between extedned unit cells are omitted.
    * `'per'`   Periodic, interactions between extended unit cells are
      retained.
   
  {{note If neither `path` nor `fileid` is given, the `outStr` will be a
  cell containing strings for each line of the text output.}}


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('export')), 1)
        return m.export(self.handle, *args, nargout=nout)

    def field(self, *args, **kwargs):
        """
  get/set magnetic field value
  
  ### Syntax
  
  `field(obj,B)`
  `B = field(obj)`
  
  ### Description
  
  `field(obj,B)` sets the magnetic field stored in `obj.single_ion.field`
  to `B`, where `B` is a $[1\times 3]$ vector.
   
  `B = field(obj)` returns the current value of the magnetic field value
  stored in `obj`.
   
  ### See Also
  
  [spinw] \| [spinw.temperature] \| [spinw.single_ion]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('field')), 1)
        return m.field(self.handle, *args, nargout=nout)

    def fitspec(self, *args, **kwargs):
        """
  fits experimental spin wave data
  
  ### Syntax
  
  `fitsp = fitspec(obj,Name,Value)`
  
  ### Description
  `fitsp = fitspec(obj,Name,Value)` uses a heuristic method to fit spin
  wave spectrum using a few simple rules to define the goodness (or
  R-value) of the fit:
  1. All calculated spin wave modes that are outside of the measured
     energy range will be omitted.
  2. Spin wave modes that are closer to each other than the given energy
     bin will be binned together and considered as one mode in the fit.
  3. If the number of calculated spin wave modes after applying rule 1&2 
     is larger than the observed number, the weakes simulated modes will
     be removed from the fit.
  4. If the number of observed spin wave modes is larger than the observed
     number, fake spin wave modes are added with energy equal to the
     limits of the scan; at the upper or lower limit depending on which is
     closer to the observed spin wave mode.
 
  After these rules the number of observed and simulated spin wave modes
  will be equal. The R-value is defined as:
 
  $R = \sqrt{ \frac{1}{n_E} \cdot \sum_{i,q} \frac{1}{\sigma_{i,q}^2}\left(E_{i,q}^{sim} - E_{i,q}^{meas}\right)^2},$
   
  where $(i,q)$ indexing the spin wave mode and momentum respectively.
  $E_{sim}$ and $E_{meas}$ are the simulated and measured spin wave
  energies, sigma is the standard deviation of the measured spin wave
  energy determined previously by fitting the inelastic peak. $n_E$ is the
  number of energies to fit.
   
  The R value is optimized using particle swarm algorithm to find the
  global minimum.
  
  ### Name-Value Pair Arguments
  
  `'func'`
  : Function to change the Hamiltonian in `obj`, it needs to have the
    following header:
    ```
    obj = @func(obj, x)
    ```
  
  `'datapath'`
  : Path to the file that stores the experimental data. For the
    input data format see [sw_readspec].
  
  `'Evect'`
  : Column vector with $n_E$ elements that defines the energy binning of
    the calculated dispersion. Larger binning steps solve the issue of
    fitting unresolved modes.
  
  `'xmin'`
  : Lower limit of the optimisation parameters, optional.
  
  `'xmax'`
  : Upper limit of the optimisation parameters, optional.
  
  `'x0'`
  : Starting value of the optimisation parameters. If empty
   or undefined, random values are used within the given limits.
  
  `'optimizer'`
  : String that determines the type of optimizer to use, possible values:
    * `'pso'`       Particle-swarm optimizer, see [ndbase.pso],
                    default.
    * `'simplex'`   Matlab built-in simplex optimizer, see [fminsearch](www.mathworks.ch/help/matlab/ref/fminsearch.html).
  
  `'nRun'`
  : Number of consecutive fitting runs, each result is saved in the
    output `fitsp.x` and `fitsp.R` arrays. If the Hamiltonian given by the
    random `x` parameters is incompatible with the ground state,
    those `x` values will be omitted and new random `x` values will be
    generated instead. Default value is 1.
  
  `'nMax'`
  : Maximum number of runs, including the ones that produce error
    (due to incompatible ground state). Default value is 1000.
  
  `'hermit'`
  : Method for matrix diagonalization, for details see [spinw.spinwave].
  
  `'epsilon'`
  : Small number that controls wether the magnetic structure is
    incommensurate or commensurate, default value is $10^{-5}$.
  
  `'imagChk'`
  : Checks that the imaginary part of the spin wave dispersion is
    smaller than the energy bin size. 
    If false, will not check
    If 'penalize' will apply a penalty to iterations that yield imaginary modes
    If true, will stop the fit if an iteration gives imaginary modes
    Default is `penalize`.
  
  Parameters for visualizing the fit results:
  
  `'plot'`
  : If `true`, the measured dispersion is plotted together with the
    fit. Default is `true`.
  
  `'iFact'`
  : Factor of the plotted simulated spin wave intensity (red
    ellipsoids).
  
  `'lShift'`
  : Vertical shift of the `Q` point labels on the plot.
  
  Optimizer options:
  
  `'TolX'`
  : Minimum change of` x` when convergence reached, default
    value is $10^{-4}$.
  
  `'TolFun'`
  : Minimum change of the R value when convergence reached,
    default value is $10^{-5}$.
  
  `'MaxFunEvals'`
  : Maximum number of function evaluations, default value is
    $10^7$.
  
  `'MaxIter'`
  : Maximum number of iterations for the [ndbse.pso] optimizer.
    Default value is 20.
  
  ### Output Arguments
  
  Output `fitsp` is struct type with the following fields:
  * `obj`   Copy of the input `obj`, with the best fitted
            Hamiltonian parameters.
  * `x`     Final values of the fitted parameters, dimensions are
            $[n_{run}\times n_{par}]$. The rows of `x` are sorted according 
            to increasing R values.
  * `redX2` Reduced $\chi^2_\eta$ value, goodness of the fit stored in a column 
            vector with $n_{run}$ number of elements, sorted in increasing 
            order. $\chi^2_\eta$ is defined as:
 
    $\begin{align}
                    \chi^2_\eta &= \frac{\chi^2}{\eta},\\
                    \eta        &= n-m+1,
    \end{align}$
    where \\eta is the degree of freedom, $n$ number of
    observations and $m$ is the number of fitted parameters.
 
  * `exitflag`  Exit flag of the `fminsearch` command.
  * `output`    Output of the `fminsearch` command.
  
  {{note As a rule of thumb when the variance of the measurement error is
  known a priori, \\chi$^2_\eta$\\gg 1 indicates a poor model fit. A
  \\chi$^2_\eta$\\gg 1 indicates that the fit has not fully captured the
  data (or that the error variance has been underestimated). In principle,
  a value of \\chi$^2_\eta$= 1 indicates that the extent of the match
  between observations and estimates is in accord with the error variance.
  A \\chi$^2_\eta$ < 1 indicates that the model is 'over-fitting' the data:
  either the model is improperly fitting noise, or the error variance has
  been overestimated.}}
 
  Any other option used by [spinw.spinwave] function are also accepted.
  
  ### See Also
  
  [spinw.spinwave] \| [spinw.matparser] \| [sw_egrid] \| [sw_neutron] \| [sw_readspec]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('fitspec')), 1)
        return m.fitspec(self.handle, *args, nargout=nout)

    def formula(self, *args, **kwargs):
        """
  returns basic physical properties
 
  ### Syntax
 
  `formula = formula(obj)`
 
  ### Description
 
  `result = formula(obj)` returns chemical mass, density, cellvolume etc.
  of `obj`.
 
  ### Examples
 
  The formula of the crystal stored in the
  [<a href="matlab:web https://raw.githubusercontent.com/SpinW/Models/master/cif/Ca2RuO4.cif](https://raw.githubusercontent.com/SpinW/Models/master/cif/Ca2RuO4.cif">https://raw.githubusercontent.com/SpinW/Models/master/cif/Ca2RuO4.cif](https://raw.githubusercontent.com/SpinW/Models/master/cif/Ca2RuO4.cif</a>) linked file will be
  printed onto the Command Window.
 
  ```
  >>cryst = spinw('<a href="matlab:web https://raw.githubusercontent.com/SpinW/Models/master/cif/Ca2RuO4.cif">https://raw.githubusercontent.com/SpinW/Models/master/cif/Ca2RuO4.cif</a>')
  >>cryst.formula>>
  ```
 
  ### Name-Value Pair Arguments
 
  `'obj'`
  : [spinw] object.
 
  ### Output Arguments
 
  `formula` struct variable with the following fields:
  * `m`         Mass of the unit cell in g/mol units.
  * `V`         Calculated volume of the unit cell in length units (defined in [spinw.unit]).
  * `rho`       Density in g/cm$^3$.
  * `chemlabel` List of the different elements.
  * `chemnum`   Number of the listed element names
  * `chemform`  Chemical formula string.


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('formula')), 1)
        return m.formula(self.handle, *args, nargout=nout)

    def fourier(self, *args, **kwargs):
        """
  calculates the Fourier transformation of the Hamiltonian
  
  ### Syntax
  
  `F = fourier(obj,Q,Name,Value)`
  
  ### Description
  
  `F = fourier(obj,hkl,Name,Value)` calculates the following Fourier sum:
 
  $J(\mathbf{k}) = \sum_{i,j} J_{i,j} * \exp(i \mathbf{k}\cdot \mathbf{d}_{i,j})$
 
  The code is optimised for calculating the sum for large number of wave
  vectors and alternatively for a large number of $d_{i,j}$ vectors (large
  system size). The single ion anisotropy is not included in the sum.
  
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  `Q`
  : Defines the $Q$ points where the spectra is calculated, in reciprocal
    lattice units, size is $[3\times n_{Q}]$. $Q$ can be also defined by
    several linear scan in reciprocal space. In this case `Q` is cell type,
    where each element of the cell defines a point in $Q$ space. Linear scans
    are assumed between consecutive points. Also the number of $Q$ points can
    be specified as a last element, it is 100 by defaults. 
    
    For example to define a scan along $(h,0,0)$ from $h=0$ to $h=1$ using
    200 $Q$ points the following input should be used:
    ```
    Q = {[0 0 0] [1 0 0]  50}
    ```
 
    For symbolic calculation at a general reciprocal space point use `sym`
    type input. 
 
    For example to calculate the spectrum along $(h,0,0)$ use:
    ```
    Q = [sym('h') 0 0]
    ```
    To calculate spectrum at a specific $Q$ point symbolically, e.g. at
    $(0,1,0)$ use:
    ```
    Q = sym([0 1 0])
    ```
  
  ### Name-Value Pair Arguments
  
  `'extend'`
  : If `true`, the Fourier transform will be calculated on the
    magnetic supercell, if `false` the crystallographic cell will
    be considered. Default is `true.`
  
  `'isomode'`
  : Defines how Heisenberg/non-Heisenberg Hamiltonians are
    treated. Can have the following values:
    * `'off'`   Always output the $[3\times 3]$ form of the
                Hamiltonian, (default).
    * `'auto'`  If the Hamiltonian is Heisenberg, only output
                one of the diagonal values from the $[3\times 3]$
                matrices to reduce memory consumption.
  
  `'fid'`
  : Defines whether to provide text output. The default value is determined
    by the `fid` preference stored in [swpref]. The possible values are:
    * `0`   No text output is generated.
    * `1`   Text output in the MATLAB Command Window.
    * `fid` File ID provided by the `fopen` command, the output is written
            into the opened file stream.
  
  ### Output Arguments
  
  `res` struct type with the following fields:
  * `ft`        contains the Fourier transform in a matrix with dimensions
                $[3\times 3\times n_{magExt}\times n_{magExt}\times
                n_{hkl}]$ or $[1\times 1\times n_{magExt}\times n_{magExt}\times n_{hkl}]$
                for Heisenberg and non-Heisenberg Hamiltonians respectively
                (if isomode is `'auto'`). Here $n_{magExt}$ is the number of
                magnetic atoms in the magnetic cell and $n_{hkl}$ is the number
                of reciprocal space points.
  * `hkl`       Matrix with the given reciprocal space points stored in a
                matrix with dimensions $[3\times n_{hkl}]$.
  * `isiso`     True is the output is in Heisenberg mode, when the `ft`
                matrix has dimensions of $[1\times 1\times n_{magExt}\times n_{magExt}\times n_{hkl}]$,
                otherwise it is `false`.
  
  ### See Also
  
  [spinw.optmagk]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('fourier')), 1)
        return m.fourier(self.handle, *args, nargout=nout)

    def fouriersym(self, *args, **kwargs):
        """
  calculates the Fourier transformation of the symbolic Hamiltonian
  
  ### Syntax
  
  `res = fouriersym(obj,Name,Value)`
  
  ### Description
  
  `res = fouriersym(obj,Name,Value)` solves the symbolic Fourier transform
  problem.
  
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  ### Name-Value Pair Arguments
  
  `'hkl'`
  : Symbolic definition of positions in momentum space. Default value is
    the general $Q$ point:
    ```
    hkl = [sym('h') sym('k') sym('l')]
    ```
  
  ### See Also
  
  [spinw.fourier]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('fouriersym')), 1)
        return m.fouriersym(self.handle, *args, nargout=nout)

    def gencoupling(self, *args, **kwargs):
        """
  generates bond list
 
  ### Syntax
 
  `gencoupling(obj,Name,Value)`
 
  ### Description
 
  `gencoupling(obj,Name,Value)` generates all bonds up to a certain length
  between magnetic atoms. It also groups bonds based either on crystal
  symmetry (is space group is not $P0$) or bond length (with `tolDist`
  tolerance) is space group is not defined. Sorting bonds based on length
  can be forced by setting the `forceNoSym` parameter to true. To check
  whether a space group is defined call the [spinw.symmetry] function.
 
  {{warning This function has to be used after the crystal structure is defined.
    The [spinw.addcoupling] function will only work afterwards. }}
 
  ### Examples
 
  A triangular lattice is generated using `<strong>spinw/gencoupling</strong>` and
  the [spinw.table] function lists the 1st, 2nd and 3rd neighbor bonds:
 
  ```
  >>cryst = spinw
  >>cryst.genlattice('lat_const',[3 3 5],'angled',[90 90 120])
  >>cryst.addatom('r',[0 0 0],'S',1)
  >>cryst.gencoupling
  >>cryst.table('bond',1:3)>>
  ```
 
  ### Input Arguments
 
  `obj`
  : [spinw] object.
 
  ### Name-Value Pair Arguments
 
  `'forceNoSym'`
  : If `true`, equivalent bonds are always generated based on
    bond length with `tolDist` length tolerance and effectively reducing
    the bond symmetry to `P0`. If `false` symmetry operators will be used
    if they are given ([spinw.symmetry] returns `true`).
 
  `'maxDistance'`
  : Maximum bond length that will be stored in the
    [spinw.coupling] property in units of \\ang. Default value is 8.
 
  `'maxSym'`
  : Maximum bond length until the symmetry equivalent bonds are
    generated. It is usefull if long bonds have to be generated for the
    dipolar interaction, but the symmetry analysis of them is not
    necessary. Default value is equal to `maxDistance`.
 
  `'tolDist'`
  : Tolerance of distance, within two bonds are considered
    equivalent, default value is $10^{-3}$\\ang. Only used, when no
    space group is defined.
 
  `'tolMaxDist'`
  : Tolerance added to maxDistance to ensure bonds between same atom in
    neighbouring unit cells are included when maxDistance is equal to a
    lattice parameter.
 
  `'dMin'`
  : Minimum bond length, below which an error is triggered.
    Default value is 0.5 \\ang.
 
  `'fid'`
  : Defines whether to provide text output. The default value is determined
    by the `fid` preference stored in [swpref]. The possible values are:
    * `0`   No text output is generated.
    * `1`   Text output in the MATLAB Command Window.
    * `fid` File ID provided by the `fopen` command, the output is written
            into the opened file stream.
 
  ### Output Arguments
 
  The [spinw.coupling] field of `obj` will store the new bond list, while
  overwriting previous bond list. This will also remove any previous
  assignment of exchange matrices to bonds.
 
  ### See Also
 
  [spinw] \| [spinw.symmetry] \| [spinw.nosym]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('gencoupling')), 1)
        return m.gencoupling(self.handle, *args, nargout=nout)

    def genlattice(self, *args, **kwargs):
        """
  generates crystal lattice
  
  ### Syntax
 
  `genlattice(obj,Name,Value)`
 
  `R = genlattice(___)`
 
  ### Description
 
  `genlattice(obj,Name,Value)` generates all necessary parameters to define
  a lattice including space group symmetry and store the result it in the
  [spinw.lattice] field.
 
  `R = genlattice(___)` also returns the rotation matrix that
  rotates the inpub basis vectors to the internal coordinate system.
 
  Alternatively the lattice parameters can be given directly when the
  [spinw] object is created using the `spinw(inpStr)` command, where struct
  contains the fields with initial parameters, e.g.:
  ```
  inpStr.lattice.lat_const = [3 3 4];
  ```
 
  ### Example
 
  ```
  crystal.genlattice('lat_const',[3 3 4],'angled',[90 90 120],'sym','P 6')
  crystal.genlattice('lat_const',[3 3 4],'angled',[90 90 120],'sym',168)
  crystal.genlattice('lat_const',[3 3 4],'angled',[90 90 120],'sym','-y,x-y,z; -x,-y,z','label','R -3 m')
  ```
 
  The three lines are equivalent, both will create hexagonal lattice, with
  $P6$ space group.
 
  ### Input
 
  `obj`
  : [spinw] object.
  
  ### Options
  
  `angled`
  : `[\\alpha, \\beta, \\gamma]` angles in \\deg, dimensions are $[1\times 3]$.
  
  `angle`
  : `[\\alpha, \\beta, \\gamma]` angles in radian, dimensions are $[1\times 3]$.
  
  `lat_const`
  : `[a, b, c]` lattice parameters in units defined in [spinw.unit] (with \\ang
    being the default), dimensions are $[1\times 3]$.
  
  `spgr` or 'sym'
  : Defines the space group. Can have the following values:
 
    * **space group label** string, name of the space group, can be any
      label defined in the [symmetry.dat] file.
    * **space group index** line number in the [symmetry.dat] file.
    * **space group operators** matrix with dimensions 
      $[3\times 4\times n_{op}]$.
    
    The [symmetry.dat] file stores definition of the 230 space groups in
    standard settings as it is in the [International Tables of Crystallography](<a href="matlab:web http://it.iucr.org/A/">http://it.iucr.org/A/</a>).
    Additional lines can be added to the [symmetry.dat] file using the
    [swsym.add] function which later can be used in the `spgr` option.
  
    If the `spgr` option is 0, no symmetry will be used. The
    [spinw.gencoupling] function will determine the equivalent bonds based on
    bond length.
    
    Can also provide spacegroup and label (see below) in a cell e.g.
    {'-x,y,-z', 'P 2'}
  
  `label`
  : Optional label for the space group if the generators are given in the
    `spgr` option.
 
  `bv`
  : Basis vectors given in a matrix with dimensions of $[3\times 3]$, where
    each column defines a basis vector.
  
  `origin`
  : Origin for the space group operators, default value is `[0 0 0]`.
  
  `perm`
  : Permutation of the abc axes of the space group operators.
  
  `nformula`
  : Gives the number of formula units in the unit cell. It is used
    to normalize cross section in absolute units. Default value is 0, when
    cross section is normalized per unit cell.
  
  ### Output
  
  `R`
  : Rotation matrix that brings the input basis vector to the SpinW
    compatible form:
    ```
    BVspinw = R*BV
    ```
  
  The result of the `<strong>spinw/genlattice</strong>` function is that `obj.lattice` field
  will be changed based on the input, the lattice parameters are stored
  directly and the optional space group string is converted into space
  group operator matrices.
 
  ### See also
 
  [spinw], [swsym.add], [swsym.operator], [spinw.gencoupling]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('genlattice')), 1)
        return m.genlattice(self.handle, *args, nargout=nout)

    def genmagstr(self, *args, **kwargs):
        """
  generates magnetic structure
  
  ### Syntax
  
  `genmagstr(obj,Name,Value)`
  
  ### Description
  
  `genmagstr(obj,Name,Value)` is a Swiss knife for generating magnetic
  structures. It allows the definition of magnetic structures using several
  different ways, depending on the `mode` parameter. The generated magnetic
  structure is stored in the [obj.mag_str] field. The magetic structure is
  stored as Fourier components with arbitrary number of wave vectors in the
  [spinw] object. However spin waves can be only calculated if the magnetic
  structure has a single propagation vector (plus a k=0 ferromagnetic
  component perpendicular to the incommensurate magnetization), we simply
  call it single-k magnetic structure. Thus `genmagstr` enables to input
  magnetic structures that comply with this restriction by defining a
  magnetic structure by the moment directions (`S`) in the crystallographic
  cell, a propagation vector (`km`) and a vector that defines the normal of
  the rotation of the spin spiral (`n`). The function converts these values
  into Fourier components to store. To solve spin wave dispersion of
  magnetic structures with multiple propagation vectors, a magnetic
  supercell has to be defined where the propagation vector can be
  approximated to zero.
  
  ### Examples
  
  The example creates the multi-k magnetic structure of USb given by the
  `FQ` Fourier components and plots the magnetic structure:
  
  ```
  >>USb = spinw
  >>USb.genlattice('lat_const',[6.203 6.203 6.203],'sym','F m -3 m')
  >>USb.addatom('r',[0 0 0],'S',1)
  >>FQ = cat(3,[0;0;1+1i],[0;1+1i;0],[1+1i;0;0])>>
  >>k  = [0 0 1;0 1 0;1 0 0];
  >>USb.genmagstr('mode','fourier','S',FQ,'nExt',[1 1 1],'k',k)
  >>plot(USb,'range',[1 1 1])
  >>snapnow
  ```
 
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  ### Name-Value Pair Arguments
  
  `'mode'`
  : Mode that determines how the magnetic structure is generated:
    * `'random'` (optionally reads `k`, `n`, `nExt`)
            generates a random structure in the structural cell if no other
            arguments are specified here or previously in this spinw
            object. If `nExt` is specified all spins in the supercell are
            randomised. If `k` is specified a random helical structure with
            moments perpendicular to `n` (default value: `[0 0 1]`) with
            the specified `k` propagation vector is generated. (`n` is not
            otherwise used).
    * `'direct'` (reads `S`, optionally reads `k`, `nExt`)
            direct input of the magnetic structure using the 
            parameters of the single-k magnetic structure.
    * `'tile'` (reads `S`, optionally reads `nExt`)
            Simply extends the existing or input structure
            (`S`) into a magnetic supercell by replicating it.
            If no structure is stored in the [spinw] object a random
            structure is generated automatically. If defined,
            `S` is used as starting structure for extension
            overwriting the stored structure. If the original
            structure is already extended with other size, only the
            moments in the crystallographic cell wil be replicated.
            Magnetic ordering wavevector `k` will be set to zero. To
            generate structure with non-zero k, use the `'helical'` or
            `'direct'` option.
    * `'helical'` (reads `S`, optionally reads `n`, `k`, `r0`, `nExt`, `epsilon`)
            generates helical structure in a single cell or in a
            supercell. In contrary to the `'extend'` option the
            magnetic structure is not generated by replication but
            by rotation of the moments using the following formula:
 
      $\mathbf{S}^{gen}_i(\mathbf{r}) = R(2 \pi \mathbf{k_m} \cdot \mathbf{r})\cdot \mathbf{S}_i$
 
      where $S_i$ has either a single moment or as many moments
            as the number of magnetic atoms in the crystallographic
            cell. In the first case $r$ denotes the atomic
            positions, while for the second case $r$ denotes the
            position of the origin of the cell.
    * `'rotate'` (optionally reads `S`, `phi`, `phid`, `n`, `nExt`)
            uniform rotation of all magnetic moments with a
            `phi` angle around the given `n` vector. If
            `phi=0`, all moments are rotated so, that the first
            moment is parallel to `n` vector in case of
            collinear structure or in case of planar structure
            `n` defines the normal of the plane of the magnetic
            moments.
    * `'func'` (reads `func`, `x0`)
            function that defines the parameters of the single-k
            magnetic structure: moment vectors, propagation vector
            and normal vector from arbitrary parameters in the
            following form:
      ```
      [S, k, n] = @(x)func(S0, x)
      ```  
      where `S` is matrix with dimensions of $[3\times n_{magExt}]$. `k` is
            the propagation vector in a 3-element row vector. `n` is the
            normal vector of the spin rotation plane also 3-element row
            vector. The default value for `func` is `@gm_spherical3d`. For planar
            magnetic structure use `@gm_planar`. Only `func` and `x`
            have to be defined for this mode.
   * `'fourier'` (reads `S`, optionally reads `k`, `r0`, `nExt`, `epsilon`)
            same as `'helical'`, except the `S` option is taken as the
            Fourier components, thus if it contains real numbers, it will
            generate a sinusoidally modulated structure instead of
            a spiral.
  
  `'phi'`
  : Angle of rotation of the magnetic moments in radian. Default
    value is 0.
  
  `'phid'`
  : Angle of rotation of the magnetic moments in \\deg. Default
    value is 0.
  
  `'nExt'`
  : Size of the magnetic supercell in multiples of the
    crystallographic cell, dimensions are $[1\times 3]$. Default value is
    stored in `obj`. If `nExt` is a single number, then the size of the
    extended unit cell is automatically determined from the first
    magnetic ordering wavevector. E.g. if `nExt = 0.01`, then the number
    of unit cells is determined so, that in the extended unit cell,
    the magnetic ordering wave vector is `[0 0 0]`, within the given
    0.01 rlu tolerance.
  
  `'k'`
  : Magnetic ordering wavevector in rlu, dimensions are $[n_K\times 3]$.
    Default value is defined in `obj`.
  
  `'n'`
  : Normal vector to the spin rotation plane for single-k magnetic
    structures, stored in a 3-element row vector, is automatically
    normalised to a unit vector. Default value `[0 0 1]`. The coordinate
    system of the vector is determined by `unit`.
  
  `'S'`
  : Vector values of the spins (expectation value), dimensions are $[3\times n_{spin} n_K]$.
    Every column defines the three $(S_x, S_y, S_z)$ components of
    the spin (magnetic moment) in the $xyz$ Descartes coodinate system or
    in lu. Default value is stored in `obj`.
  
  `'unit'`
  : Determines the coordinate system for `S` and `n` vectors using a
    string:
    * `'xyz'`   Cartesian coordinate system, fixed to the lattice.
                Default value.
    * `'lu'`	Lattice coordinate system (not necessarily
                Cartesian. The three coordinate vectors are
                parallel to the lattice vectors but normalized to
                unity.
  
  `'epsilon'`
  : The smalles value of incommensurability that is
    tolerated without warning in lattice units. Default is $10^{-5}$.
  
  `'func'`
  : Function handle that produces the magnetic moments, ordering wave
    vector and normal vector from the `x` parameters in the
    following form:
    ```
    [M, k, n] = @(x)func(M0,x)
    ```
    where `M` is a matrix with dimensions of $[3\times n_{magExt}]$, `k` is
    the propagation vector, `n` is the normal vector of the spin rotation
    plane. The default function is [gm_spherical3d]. For planar magnetic
    structure use [gm_planar].
  
  `'x0'`
  : Input parameters for `func` function, row vector with $n_X$ number of
    elements.
  
  `'norm'`
  : Set the length of the generated magnetic moments to be equal to
    the spin of the magnetic atoms. Default is `true`.
  
  `'r0'`
  : If `true` and only a single spin direction is given, the spin
    phases are determined by atomic position times k-vector, while
    if it is `false`, the first spin will have 0 phase. Default is
    `true`.
  
  ### Output Arguments
  
  The [obj.mag_str] field will contain the new magnetic structure.
  
  ### See Also
  
  [spinw] \| [spinw.anneal] \| [spinw.optmagstr] \| [gm_spherical3d] \| [gm_planar]
 
  *[rlu]: Reciprocal Lattice Units
  *[lu]: Lattice Units


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('genmagstr')), 1)
        return m.genmagstr(self.handle, *args, nargout=nout)

    def get(self, *args, **kwargs):
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
 
    See also <a href="matlab:help get -displayBanner">get</a>, <a href="matlab:help spinw -displayBanner">spinw</a>, <a href="matlab:help spinw/getdisp -displayBanner">spinw/getdisp</a>, <a href="matlab:help handle -displayBanner">handle</a>

Help for <strong>spinw/get</strong> is inherited from superclass <a href="matlab:help matlab.mixin.SetGet -displayBanner">matlab.mixin.SetGet</a>


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('get')), 1)
        return m.get(self.handle, *args, nargout=nout)

    def getdisp(self, *args, **kwargs):
        """
 <strong>getdisp</strong>    Specialized MATLAB object property display.
    <strong>getdisp</strong> is called by GET when GET is called with no output argument 
    and a single input parameter H an array of handles to MATLAB objects.  
    This method is designed to be overridden in situations where a
    special display format is desired to display the results returned by
    GET(H).  If not overridden, the default display format for the class
    is used.
 
    See also <a href="matlab:help spinw -displayBanner">spinw</a>, <a href="matlab:help spinw/get -displayBanner">spinw/get</a>, <a href="matlab:help handle -displayBanner">handle</a>

Help for <strong>spinw/getdisp</strong> is inherited from superclass <a href="matlab:help matlab.mixin.SetGet -displayBanner">matlab.mixin.SetGet</a>


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('getdisp')), 1)
        return m.getdisp(self.handle, *args, nargout=nout)

    def getmatrix(self, *args, **kwargs):
        """
  determines the symmetry allowed tensor elements
  
  ### Syntax
  
  `amat = getmatrix(obj,Name,Value)`
  
  ### Description
  
  `amat = getmatrix(obj,Name,Value)` determines the symmetry allowed
  elements of the exchange, single-ion anistropy and g-tensor. For bonds,
  the code first determines the point group symmetry on the center of the
  bond and calculates the allowed eelements of the exchange tensor
  accordingly. For anisotropy and g-tensor, the point group symmetry of the
  selected atom is considered. For example the code can correctly calculate
  the allowed Dzyaloshinskii-Moriya vectors.
  
  ### Examples
  
  To following code will determine the allowed anisotropy matrix elements
  in the $C4$ point group (the symmetry at the $(0,0,0)$ atomic position).
  The allowed matrix elements will be `diag([A A B])`:
 
  ```
  >>cryst = spinw
  >>cryst.genlattice('sym','P 4')
  >>cryst.addatom('r',[0 0 0],'label','MCu2')
  >>cryst.addmatrix('label','A','value',1)
  >>cryst.gencoupling
  >>cryst.addaniso('A')
  >>cryst.getmatrix('mat','A')>>
  ```
  
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  ### Name-Value Pair Arguments
 
  At least one of the following option has to be defined:
  
  `mat`
  : Label or index of a matrix that is already assigned to
    a bond, anisotropy or g-tensor, e.g. `J1`.
  
  `bond`
  : Index of the bond in `spinw.coupling.idx`, e.g. 1 for first neighbor
    bonds.
  
  `aniso`
  : Label or index of the magnetic atom that has a single ion
    anisotropy matrix is assigned, e.g. `Cr1` if `Cr1` is a magnetic atom.
  
  `gtensor`
  : Label or index of the magnetic atom that has a g-tensor is 
    assigned.
 
  Optional inputs:
  
  `subIdx`
  : Selects a certain bond, within equivalent bonds. Default value is 1.
 
  `tol`
  : Tolerance for printing the output for the smallest matrix
    element.
  
  `pref`
  : If defined `amat` will contain a single $[3\times 3]$ matrix by
    multuplying the calculated tensor components with the given prefactors.
    Thus `pref` should contain the same number of elements as the number of
    symmetry allowed tensor components. Alternatively, if only a few of the
    symmetry allowed matrices have non-zero prefactors, use e.g. 
    `{[6 0.1 5 0.25]}` which means, the 6th symmetry allowed matrix have
    prefactor 0.1, the 5th symmetry allowed matrix have prefactor 0.25.
    Since Heisenberg isotropic couplings are always allowed, a cell with a
    single element will create a Heisenberg coupling, e.g. `{0.1}`, which is
    identical to `obj.matrix.mat = eye(3)*0.1`. For Dzyaloshinskii-Moriya
    interactions (antisymmetric exchange matrices), use a three element
    vector in a cell, e.g. `pref = {[D1 D2 D3]}`. In this case, these will
    be the prefactors of the 3 antisymmetric allowed matrices. In
    case no crystal symmetry is defined, these will define directly the
    components of the  Dzyaloshinskii-Moriya interaction in the xyz
    coordinate system.
 
    {{note Be carefull with the sign of the Dzyaloshinskii-Moriya
    interaction, it depends on the counting order of the two interacting
    atoms! For single-ion anisotropy and g-tensor antisymmetric matrices
    are forbidden in any symmetry.}}
  
  `'fid'`
  : Defines whether to provide text output. The default value is determined
    by the `fid` preference stored in [swpref]. The possible values are:
    * `0`   No text output is generated.
    * `1`   Text output in the MATLAB Command Window.
    * `fid` File ID provided by the `fopen` command, the output is written
            into the opened file stream.
 
  ### Output Arguments
  
  `aMat`
  : If no prefactors are defined, `aMat` contains all symmetry
    allowed elements of the selected tensor, dimensions are $[3\times 3\times n_{symmat}]$.
    If a prefactor is defined, it is a single $[3\times 3]$ matrix, that is
    a sum of all symmetry allowed elemenets multiplied by the given
    prefactors.
  
  ### See Also
  
  [spinw.setmatrix]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('getmatrix')), 1)
        return m.getmatrix(self.handle, *args, nargout=nout)

    def horace(self, *args, **kwargs):
        """
  spin wave calculator with interface to Horace
 
  ### Syntax
 
  `[w, s] = horace(obj, qh, qk, ql,Name,Value)`
 
  ### Description
 
  `[w, s] = horace(obj, qh, qk, ql,Name,Value)` produces spin wave
  dispersion and intensity for [Horace](<a href="matlab:web http://horace.isis.rl.ac.uk">http://horace.isis.rl.ac.uk</a>).
 
  ### Examples
 
  This example creates a `d3d` object, a square in $(h,k,0)$ plane and in
  energy between 0 and 10 meV. Then calculates the inelastice neutron
  scattering intensity of the square lattice antiferromagnet stored in
  `cryst` and plots a cut between 4 and 5 meV using the Horace `plot`
  command.
  ```
  >>>horace on
  >>cryst = sw_model('squareAF',1)
  >>d3dobj = d3d(cryst.abc,[1 0 0 0],[0,0.02,2],[0 1 0 0],[0,0.02,2],[0 0 0 1],[0,0.1,10])
  >>d3dobj = disp2sqw_eval(d3dobj,@cryst.horace,{'component','Sperp'},0.1)
  >>plot(cut(d3dobj,[],[],[4 5]))
  >>>colorslider('delete')
  >>snapnow
  >>>horace off
  ```
 
  ### Input Arguments
 
  `obj`
  : [spinw] object.
 
  `qh`, `qk`, `ql`
  : Reciprocal lattice vectors in reciprocal lattice units.
 
  ### Name-Value Pair Arguments
 
  `'component'`
  : Selects the previously calculated intensity component to be
    convoluted. The possible options are:
    * `'Sperp'` convolutes the magnetic neutron scattering
                intensity ($\langle S_\perp \cdot S_\perp\rangle$ expectation value).
                Default value.
    * `'Sab'`   convolutes the selected components of the spin-spin
                correlation function.
    For details see [sw_egrid].
 
  `'norm'`
  : If `true` the spin wave intensity is normalized to mbarn/meV/(unit
    cell) units. Default is `false`.
 
  `'dE'`
  : Energy bin size, for intensity normalization. Use 1 for no
    division by `dE` in the intensity.
 
  `'param'`
  : Input parameters (can be used also within Tobyfit). Additional
    parameters (`'mat'`,`'selector'`) might be necessary, for details see
    [spinw.matparser]. All extra parameters of `<strong>spinw/horace</strong>`
    will be forwarded to the [spinw.matparser] function before
    calculating the spin wave spectrum (or any user written parser
    function). For user written functions defined with the
    following header:
    ```
    func(obj,param)
    ```
    the value of the param option will be forwarded. For user
    functions with variable number of arguments, all input options
    of `<strong>spinw/horace</strong>` will be forwarded. In this case it is recommended
    to use [sw_readparam] function to handle the variable number
    arguments within `func()`.
 
  `'parfunc'`
  : Parser function of the `param` input. Default value is
    `@spinw.matparser` which can be used directly by Tobyfit. For user
    defined functions the minimum header has to be:
    ```
    func(obj,param)
    ```
    where obj is an spinw type object, param is the parameter
    values forwarded from` <strong>spinw/horace</strong>` directly.
 
  `'func'`
  : User function that will be called after the parameters set on
    the [spinw] object. It can be used to optimize magnetic
    structure for the new parameters, etc. The input should be a
    function handle of a function with a header:
    ```
    fun(obj)
    ```
 
  `'fid'`
  : Defines whether to provide text output. The default value is determined
    by the `fid` preference stored in [swpref]. The possible values are:
    * `0`   No text output is generated.
    * `1`   Text output in the MATLAB Command Window.
    * `fid` File ID provided by the `fopen` command, the output is written
            into the opened file stream.
 
  `'useFast'`
  : whether to use the 'fastmode' option in spinwave() or not. This method
            calculates only the unpolarised neutron cross-section and
            *ignores all negative energy branches*. In general it produces
            the same spectra as spinw.spinwave, with some rounding errors,
            but can be 2-3 times faster and uses less memory.
 
  ### Output Arguments
 
  `w`
  : Cell that contains the spin wave energies. Every cell elements
            contains a vector of spin wave energies for the corresponding
            input $Q$ vector.
 
  `s`
  : Cell that contains the calculated element of the spin-spin
            correlation function. Every cell element contains a vector of
            intensities in the same order as the spin wave energies in `w`.
 
  ### See Also
 
  [spinw] \| [spinw.spinwave] \| [spinw.matparser] \| [sw_readparam]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('horace')), 1)
        return m.horace(self.handle, *args, nargout=nout)

    def horace_sqw(self, *args, **kwargs):
        """
  Calculate spectral weight from a spinW model for Horace. Uses disp2sqw
  as the back-end function to calculate the convolution.
 
    >> weight = swobj.<strong>horace_sqw</strong>(qh,qk,ql,en,pars,swobj,pars,kwpars)
 
  Input:
  ------
    qh,qk,ql,en Arrays containing points at which to evaluate sqw from the
                broadened dispersion
 
    pars        Arguments needed by the function.
                - pars = [model_pars scale_factor resolution_pars]
                - Should be a vector of parameters
                - The first N parameters relate to the spin wave dispersion
                  and correspond to spinW matrices in the order defined by
                  the 'mat' option [N=numel(mat)]
                - The next M parameters relate to the convolution parameters
                  corresponding to the convolution function defined by the
                  'resfun' option (either one or two parameters depending
                  on function type.
                - The last parameter is a scale factor for the intensity
                  If this is omitted, a scale factor of 1 is used;
 
    kwpars      - A series of 'keywords' and parameters. Specific to this
                  function is:
 
                - 'resfun' - determines the convolution / resolution 
                     function to get S(q,w). It can be either a string: 
                       'gauss' - gaussian with single fixed (fittable) FWHM
                       'lor' - lorentzian with single fixed (fittable) FWHM
                       'voigt' - pseudo-voigt with single fixed (fittable) FWHM
                       @fun - a function handle satisfying the requirements of
                              the 'fwhm' parameter of disp2sqw.
                     NB. For 'gauss' and 'lor' only one fwhm parameter may be
                     specified. For 'voigt', fwhm = [width lorz_frac]
                     contains two parameters - the fwhm and lorentzian fraction  
                     [default: 'gauss']
                - 'partrans' - a function to transform the fit parameters
                     This transformation will be applied before each iteration
                     and the transformed input parameter vector passed to
                     spinW and the convolution function.
                     [default: @(y)y  % identity operation]
                - 'coordtrans' - a matrix to transform the input coordinates
                     (qh,qk,ql,en) before being sent to SpinW. 
                     [default: eye(4) % identity]
 
                In addition, the following parameters are used by this function                         
                     and will also be passed on to spinw.matparser which will
                     do the actual modification of spinW model parameters:
                   
                - 'mat' - A cell array of labels of spinW named 'matrix' or
                     matrix elements. E.g. {'J1', 'J2', 'D(3,3)'}. These will
                     be the model parameters to be varied in a fit, their
                     order in this cell array will be the same as in the
                     fit parameters vector.
                     [default: [] % empty matrix - no model parameters] 
 
                  All other parameters will be passed to spinW. See the help
                     for spinw/spinwave, spinw/matparser and spinw/sw_neutron
                     for more information.
 
    swobj       The spinwave object which defines the magnetic system to be
                calculated.
 
  Output:
  -------
    weight      Array with spectral weight at the q,e points
                If q and en given:  weight is an nq x ne array, where nq
                                    is the number of q points, and ne the
                                    number of energy points
                If qw given together: weight has the same size and dimensions
                                      as q{1} i.e. qh
 
  Example:
  --------
 
  tri = sw_model('triAF',[5 1]);                         % J1=5, J2=1 (AFM)
  spinw_pars = {'mat', {'J1', 'J2'}, 'hermit', true, ...
                'useMex', true, 'optmem', 100};
  [wf,fp] = fit_sqw(w1, @tri.<strong>horace_sqw</strong>, {[J1 J2 fwhm] spinw_pars});


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('horace_sqw')), 1)
        return m.horace_sqw(self.handle, *args, nargout=nout)

    def initfield(self, *args, **kwargs):
        """
SPINW/<strong>initfield</strong> is an undocumented builtin function.


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('initfield')), 1)
        return m.initfield(self.handle, *args, nargout=nout)

    def intmatrix(self, *args, **kwargs):
        """
  generates interaction matrix
  
  ### Syntax
  
  `[SS, SI, RR] = intmatrix(obj,Name,Value)`
  
  ### Description
  
  `[SS, SI, RR] = intmatrix(obj,Name,Value)` lists the bonds and generates
  the corresponding exchange matrices by applying the bond symmetry
  operators on the stored matrices. Also applies symmetry on the single ion
  anisotropies and can generate the representation of bonds, anistropies
  and atomic positions in an arbitrary supercell. The output argument `SS`
  contains the different types of exchange interactions separated into
  different fields, such as `SS.DM` for the Dzyaloshinskii-Moriya
  interaction, `SS.iso` for Heisenberg exchange, `SS.all` for general
  exchange etc.
  
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  ### Name-Value Pair Arguments
  
  `'fitmode'`
  : Can be used to speed up calculation, modes:
    * `true`    No speedup (default).
    * `false`   For the interactions stored in `SS`, only the
                `SS.all` field is calculated.
  
  `'plotmode'`
  : If `true`, additional rows are added to `SS.all`, to identify
    the couplings for plotting. Default is `false`.
  
  `'sortDM'`
  : If true each coupling is sorted for consistent plotting of
    the DM interaction. Sorting is based on the `dR` bond vector that
    points from `atom1` to `atom2`, for details see [spinw.coupling].
    After sorting `dR` vector components fulfill the following rules in
    hierarchical order:
    1. `dR(x) > 0`
    2. `dR(y) > 0`
    3. `dR(z) > 0`.
 
    Default is `false`.
  
  `'zeroC'`
  : Whether to output bonds with assigned matrices that have only
    zero values. Default is `false`.
  
  `'extend'`
  : If `true`, all bonds in the magnetic supercell will be
    generated, if `false`, only the bonds in the crystallographic
    unit cell is calculated. Default is `true`.
  
  `'conjugate'`
  : Introduce the conjugate of the couplings (by exchanging the interacting
    `atom1` and `atom2`). Default is `false`.
  
  ### Output Arguments
  
  `SS`
  : structure where every field is a matrix. Every column is a coupling 
    between two spins. The first 3 rows contain the unit cell translation 
    vector between the interacting spins, the 4th and 5th rows contain
    the indices of the two interacting spins in the [spinw.matom] list. 
    Subsequent rows in the matrix depend on the field
    SS will always have the following fields
    * `all`
    * `dip`
    Subsequent rows in these matrices are the elements of the 3 x 3 
    exchange matrix `[Jxx; Jxy; Jxz; Jyx; Jyy; Jyz; Jzx; Jzy; Jzz]`
    and the final row indicates whether the coupling is
    bilinear (0) or biquadratic (1). The `dip` field contains the dipolar
    interactions only that are not added to `SS.all.
    If `plotmode` is `true`, two additional rows are added to `SS.all`,
    that contains the `idx` indices of the `obj.matrix(:,:,idx)`
    corresponding matrix for each coupling and the `idx` values of the 
    couplings (stored in `spinw.coupling.idx`).
 
   If fitmode = false there are additional fields
   * `iso` : One subsequent row which is the isotropic exchane
   * `ani` : Subsequent rows contain anisotropic interaction `[Jxx; Jyy;
                Jzz]`), 
   * `dm`  : Subsequent rows contain DM interaction `[DMx; DMy; DMz]`
   * `gen` : Subsequent rows contain a general interaction 
             `[Jxx; Jxy; Jxz; Jyx; Jyy; Jyz; Jzx; Jzy; Jzz]`
   * `bq`  : One subsequent row which is the isotropic exchagne as in 
             SS.iso but only the biquadratic couplings which are not 
             included in SS.iso
 
  `SI`
  : single ion properties stored in a structure with fields:
 
    * `aniso`   Matrix with dimensions of $[3\times 3\times n_{magAtom}]$,
                where the classical energy of the $i$-th spin is expressed
                as `E_aniso = spin(:)*A(:,:,i)*spin(:)'`
  	* `g`       g-tensor, with dimensions of $[3\times 3\times n_{magAtom}]$. It determines
                the energy of the magnetic moment in external field:
                `E_field = B(:)*g(:,:,i)*spin(:)'`
  	* `field`   External magnetic field in a row vector with three elements $(B_x, B_y, B_z)$.
 
  `RR`
  : Positions of the atoms in lattice units in a matrix with dimensions of $[3\times n_{magExt}]$.
  
  ### See Also
  
  [spinw.table] \| [spinw.symop]
 
  *[DM]: Dzyaloshinskii-Moriya


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('intmatrix')), 1)
        return m.intmatrix(self.handle, *args, nargout=nout)

    def loadobj(self, obj=None, **kwargs):
        """
  restore property listeners
  add new listeners to the new object


        """
        args = tuple(v for v in [obj] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('loadobj')), 1)
        return m.loadobj(self.handle, *args, nargout=nout)

    def magstr(self, *args, **kwargs):
        """
  returns single-k magnetic structure representation
  
  ### Syntax
  
  `magout = magstr(obj,Name,Value)`
  
  ### Description
  
  `magout = magstr(obj,Name,Value)` converts the internally stored magnetic
  structure (general Fourier representation) into a rotating frame
  representation with a single propagation vector, real magnetisation
  vectors and the normal axis of the rotation. The conversion is not always
  possible, in that case the best possible approximation is used, that
  might lead sometimes to unexpected magnetic structures. In this case a
  warning is triggered.
  
  ### Example
 
  The example shows the equivalent represenation of a simple spin helix in
  the $ab$-plane using Fourier components of the magnetization and using
  the rotating frame. The complex magnetization in the Fourier
  representation is converted into a real spin vector and a normal vector
  that defines the axis of rotation.
 
  ```
  >>model = spinw
  >>model.addatom('r',[0 0 0],'S',1)
  >>model.genmagstr('mode','fourier','S',[1i 1 0]','k',[1/3 0 0])
  >>model.mag_str.F>>
  >>model.magstr>>
  >>model.magstr.S>>
  ```
 
  ### Name-Value Pair Arguments
  
  `'exact'`
  : If `true`, a warning appears in case the conversion is not exact.
    Default is `true`.
  
  `'nExt'`
  : Size of the magnetic supercell, default value is the value stored in
    the [spinw] object (on which the Fourier expansion is defined).
  
  `'origin'`
  : Origin in lattice units, the magnetic structure will be
    calculated relative to this point. Default value is `[0 0 0]`.
    Shifting the origin introduces an overall phase factor.
  
  ### See Also
  
  [spinw.genmagstr]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('magstr')), 1)
        return m.magstr(self.handle, *args, nargout=nout)

    def magtable(self, *args, **kwargs):
        """
  creates tabulated list of all magnetic moments stored in obj
 
  moments = <strong>magtable</strong>(obj)
 
  The function lists the APPROXIMATED moment directions (using the rotating
  coordinate system notation) in the magnetic supercell, whose size is
  defined by the obj.mag_str.nExt field. The positions of the magnetic
  atoms are in lattice units.
 
  Input:
 
  obj           spinw class object.
 
  Output:
 
  'moments' is struct type data that contains the following fields:
    M           Matrix, where every column defines a magnetic moment,
                dimensions are [3 nMagExt].
    e1,e2,e3    Unit vectors of the coordinate system used for the spin
                wave calculation, the i-th column contains a normalized
                vector for the i-th moment. e3 is parallel to the magnetic
                moment, e1 and e2 span a right handed orthogonal coordinate
                system.
    R           Matrix, where every column defines the position of the
                magnetic atom in lattice units.
    atom        Pointer to the magnetic atom in the subfields of
                spinw.unit_cell.
 
  See also <a href="matlab:help spinw/genmagstr -displayBanner">spinw/genmagstr</a>.


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('magtable')), 1)
        return m.magtable(self.handle, *args, nargout=nout)

    def matom(self, *args, **kwargs):
        """
  generates magnetic lattice
  
  ### Syntax
  
  `mAtomList = matom(obj)`
  
  ### Description
  
  `mAtomList = matom(obj)` is the same as [spinw.atom], but only lists the
  magnetic atoms, which have non-zero spin. Also this function stores the
  generated list in [spinw.cache].
  
  ### Output Arguments
  
  `mAtomList`
  : structure with the following fields:
    * `r`   Position of the magnetic atoms in a matrix with dimensions of 
      $[3\times n_{magAtom}]$.
    * `idx` Index in the symmetry inequivalent atom list [spinw.unit_cell] 
      stored in a row vector with $n_{magAtom}]$ number of elements.
    * `S`   Spin of the magnetic atoms stored in a row vectorwith
      $n_{magAtom}]$ number of elements.
  
  ### See Also
  
  [spinw.atom]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('matom')), 1)
        return m.matom(self.handle, *args, nargout=nout)

    def matparser(self, *args, **kwargs):
        """
  parses parameter vector into matrices
  
  ### Syntax
  
  `matparser(obj,Name,Value)`
  
  ### Description
  
  `matparser(obj,Name,Value)` modifies the `obj.matrix.mat` matrix,
  assigning new values from a given parmeter vector.  
  
  ### Example
 
  To assign a Dzyaloshinskii-Moriya vector to the `'DM'` matrix, the
  following input would be sufficient:
 
  ```
  >>cryst = spinw
  >>cryst.addmatrix('label','DM','value',1)
  >>P = [0.2 0.35 3.14]
  >>M = {'DM' 'DM' 'DM'}
  >>S = cat(3,[0 0 0;0 0 1;0 -1 0],[0 0 -1;0 0 0;1 0 0],[0 1 0;-1 0 0;0 0 0])
  >>cryst.matparser('param',P,'mat',M,'selector',S)
  >>cryst.matrix.mat>>
  ```
 
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  ### Name-Value Pair Arguments
  
  `'param'`
  : Input row vector `P` with `nPar` elements that contains the
    new values to be assignd to elements of `obj.matrix.mat`
    matrix.
  
  `'mat'`
  : Identifies which matrices to be changed according to their
    label or index. To select matrices with given labels use a
    cell of strings with $n_{par}$ elements, for example
    `M = {'J1','J2'}`. This will change the diagonal elements of
    matrices $J_1$ and $J_2$ to a given value that is provided in the
    `param` parameter vector. Alternatively the index of the matrices can
    be given in a vector, such as `[1 2]` (index runs according
    to the order of the previous creation of the matrices using
    [spinw.addmatrix]).
 
    To assign parameter value only to a selected element of a
    $[3\times 3]$ matrix, a bracket notation can be used in any string,
    such as `'D(3,3)'`, in this case only the $(3,3)$ element of
    the $[3\times 3]$ matrix of `'D'` will be modified, the other elements
    will be unchanged. To modify multiple elements of a matrix
    at once, use the option `selector`.
  
  `'selector'`
  : Matrix with dimensions of $[3\times 3\times n_{par}]$. Each `S(:,:,i)`
    submatrix can contain $\pm 1$ and 0. Where `S(:,:,i)` contains
    1, the corresponding matrix elements of
    `spinw.matrix.mat(:,:,M(i))` will be changed to the value
    `P(i)*S(:,:,i)` where `P(i)` is the corresponding parameter
    value. 
  
  `'init'`
  : Initialize the matrices of `obj.matrix.mat` with zeros for all
    selected labels before assigning parameter values. Default
    is `false`.
  
  ### Output Arguments
  
  The [spinw] object will contain the modified `obj.matrix.mat` field.
  
  ### See Also
  
  [spinw] \| [spinw.horace] \| [spinw.addmatrix]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('matparser')), 1)
        return m.matparser(self.handle, *args, nargout=nout)

    def moment(self, *args, **kwargs):
        """
  calculates quantum correction on ordered moment
  
  ### Syntax
  
  `M = moment(obj,Name,Value)`
  
  ### Description
  
  `M = moment(obj,Name,Value)` calculates the spin expectation value
  including the leading quantum and thermal fluctuations ($S^{-1}$ terms).
  The magnon poulation is calculated at a given temperature $T$ integrated
  over the Brillouin zone. To calculate the numerical integral the
  Brillouin zone is sampled using Monte Carlo technique.
  
  ### Example
 
  #### Triangular lattice antiferromagnet
 
  The example calculates the spin expectation value at zero temperature on
  the triangular lattice Heisenberg antiferromagnet. The result can be
  compared with the following calculations: [A. V Chubukov, S. Sachdev,
  and T. Senthil, J. Phys. Condens. Matter 6, 8891 (1994)](<a href="matlab:web http://iopscience.iop.org/article/10.1088/0953-8984/6/42/019/meta">http://iopscience.iop.org/article/10.1088/0953-8984/6/42/019/meta</a>): $\langle S
  \rangle = S - 0.261$ and 
  [S. J. Miyake, J. Phys. Soc. Japan 61, 983 (1992)](<a href="matlab:web http://journals.jps.jp/doi/abs/10.1143/JPSJ.61.983">http://journals.jps.jp/doi/abs/10.1143/JPSJ.61.983</a>): $\langle S \rangle = S - 0.2613 +
  0.0055/S$ ($1/S$ is a higher order term neglected here).
 
  ```
  >>tri = sw_model('triAF',1)
  >>M = tri.moment('nRand',1e7)
  >>dS = 1-M.moment>>
  ```
 
  #### Square lattice antiferromagnet
 
  The reduced moment of the Heisenberg square lattice antiferromagnet at
  zero temperature can be compared to the published result of 
  [D. A. Huse, Phys. Rev. B 37, 2380
  (1988)](<a href="matlab:web https://journals.aps.org/prb/abstract/10.1103/PhysRevB.37.2380">https://journals.aps.org/prb/abstract/10.1103/PhysRevB.37.2380</a>)
  $\langle S \rangle = S - 0.197$.
 
  ```
  >>sq = sw_model('squareAF',1)
  >>M = sq.moment('nRand',1e7)
  >>dS = 1-M.moment>>
  ```
 
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  ### Name-Value Pair Arguments
  
  `'nRand'`
  : The number of random $Q$ points in the Brillouin-zone,
    default value is 1000.
  
  `'T'`
  : Temperature, default value is taken from `obj.single_ion.T` and the
    unit is stored in [spinw.unit] with the default being K.
  
  `'tol'`
  : Tolerance of the incommensurability of the magnetic
    propagation wavevector. Deviations from integer values of the
    propagation vector smaller than the tolerance are
    considered to be commensurate. Default value is $10^{-4}$.
  
  `'omega_tol'`
  : Tolerance on the energy difference of degenerate modes when
    diagonalising the quadratic form, default value is $10^{-5}$.
 
  `'fid'`
  : Defines whether to provide text output. The default value is determined
    by the `fid` preference stored in [swpref]. The possible values are:
    * `0`   No text output is generated.
    * `1`   Text output in the MATLAB Command Window.
    * `fid` File ID provided by the `fopen` command, the output is written
            into the opened file stream.
  
  ### Output Arguments
  
  `M`
  : structure, with the following fields:
    * `moment`  Size of the reduced moments in a row vector with
      $n_{magExt}$ number of elements.
    * `T`       Temperature.
    * `nRand`   Number of random $Q$ points.
    * `obj`     The clone of the input `obj`.
 
  ### See Also
  
  [spinw] \| [spinw.spinwave] \| [spinw.genmagstr] \| [spinw.temperature]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('moment')), 1)
        return m.moment(self.handle, *args, nargout=nout)

    def natom(self, obj=None, **kwargs):
        """
  number of symmetry unrelated atoms
 
  ### Syntax
 
  `nAtom = natom(obj)`
 
  ### Description
 
  `nAtom = natom(obj)` return the number of symmetry unrelated
  atoms stored in `obj`.
 
  ### See Also
 
  [spinw.nmagext] \| [spinw.atom]


        """
        args = tuple(v for v in [obj] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('natom')), 1)
        return m.natom(self.handle, *args, nargout=nout)

    def newcell(self, *args, **kwargs):
        """
  transforms lattice
  
  ### Syntax
  
  `newcell(obj,Name,Value)`
 
  `T = newcell(obj,Name,Value)`
  
  ### Description
  
  `T = newcell(obj,Name,Value)` redefines the unit cell using new basis
  vectors. The input three basis vectors are in lattice units of the
  original cell and define a parallelepiped. The atoms from the original
  unit cell will fill the new unit cell and if the two cells are compatible
  the structure won't change. The magnetic structure, bonds and single ion
  property definitions will be erased. The new cell will have different
  reciprocal lattice, however the original reciprocal lattice units will be
  retained automatically. To use the new reciprocal lattice, set the
  `'keepq'` option to `false`. In the default case the [spinw.spinwave]
  function will calculate spin wave dispersion at reciprocal lattice points
  of the original lattice. The transformation between the two lattices is
  stored in `spinw.unit.qmat`.
  
  ### Examples
  
  In this example we generate the triangular lattice antiferromagnet and
  convert the hexagonal cell to orthorhombic. This doubles the number of
  magnetic atoms in the cell and changes the reciprocal lattice. However we
  set `'keepq'` parameter to `true` to able to index the reciprocal lattice
  of the orthorhombic cell with the reciprocal lattice of the original
  hexagonal cell. To show that the two models are equivalent, we calculate
  the spin wave spectrum on both model using the same rlu. On the
  orthorhombic cell, the $Q$ value will be converted automatically and the
  calculated spectrum will be the same for both cases.
 
  ```
  >>tri = sw_model('triAF',1)
  >>tri_orth = copy(tri)
  >>tri_orth.newcell('bvect',{[1 0 0] [1 2 0] [0 0 1]},'keepq',true)
  >>tri_orth.gencoupling
  >>tri_orth.addcoupling('bond',1,'mat','J_1')
  >>newk = ((tri_orth.unit.qmat)*tri.magstr.k')'
  >>tri_orth.genmagstr('mode','helical','k',newk,'S',[1 0 0]')
  >>plot(tri_orth)
  >>>swplot.zoom(1.5)
  >>snapnow
  >>>figure
  >>subplot(2,1,1)
  >>sw_plotspec(sw_egrid(tri.spinwave({[0 0 0] [1 1 0] 501})),'mode','color','dE',0.2)
  >>subplot(2,1,2)
  >>spec = tri_orth.spinwave({[0 0 0] [1 1 0] 501});
  >>sw_plotspec(sw_egrid(tri_orth.spinwave({[0 0 0] [1 1 0] 501})),'mode','color','dE',0.2)
  >>snapnow
  ```
  
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  ### Name-Value Pair Arguments
  
  `'bvect'`
  : Defines the new lattice vectors in the original lattice
    coordinate system. Cell with the following elements
    `{v1 v2 v3}` or a $[3\times 3]$ matrix with `v1`, `v2` and `v3` as column
    vectors: `[v1 v2 v3]`. Default value is `eye(3)` for indentity
    transformation.
  
  `'bshift'`
  : Row vector that defines a shift of the position of the unit cell.
    Default value is `[0 0 0]`.
  
  `'keepq'`
  : If true, the reciprocal lattice units of the new model will be
    the same as in the old model. This is achieved by storing the
    transformation matrix between the new and the old coordinate system in
    `spinw.unit.qmat` and applying it every time a reciprocal space
    definition is invoked, such as in [spinw.spinwave]. Default value is
    `false`.
  
  ### Output Arguments
  
  `T`
  : Transformation matrix that converts $Q$ points (in reciprocal
        lattice units) from the old reciprocal lattice to the new
        reciprocal lattice as follows:
    ```
    Qrlu_new = T * Qrlu_old
    ```
    where the $Q$ vectors are row vectors with 3 elements.
  
  ### See Also
  
  [spinw.genlattice] \| [spinw.gencoupling] \| [spinw.nosym]
 
  *[rlu]: reciprocal lattice unit


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('newcell')), 1)
        return m.newcell(self.handle, *args, nargout=nout)

    def nmagext(self, obj=None, **kwargs):
        """
  number of magnetic sites
 
  ### Syntax
 
  `nMagExt = nmagext(obj)`
 
  ### Description
 
  `nMagExt = nmagext(obj)` returns the number of magnetic sites
  in the magnetic supercell. If the magnetic supercell (stored
  in `spinw.mag_str.nExt` is identical to the crystal lattice)
  the number of magnetic sites is equal to the number of
  magnetic atoms in the unit cell. Where the number of magnetic
  atoms in the unit cell can be calculated using [spinw.matom].
 
  ### See Also
 
  [spinw.matom] \| [spinw.natom]


        """
        args = tuple(v for v in [obj] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('nmagext')), 1)
        return m.nmagext(self.handle, *args, nargout=nout)

    def nosym(self, *args, **kwargs):
        """
  reduces symmetry to P0
  
  ### Syntax
  
  `nosym(obj)`
  
  ### Description
  
  `nosym(obj)` reduces the crystal symmetry to $P0$ but keeps all symmetry
  generated atoms, that become all symmetry inequivalent. The function can
  be used to test different types of symmetry breaking terms in the spin
  Hamiltonian.
  
  ### Examples
  
  The example generates an FCC cell using explicit translations. After
  applying the `<strong>spinw/nosym</strong>` function, the `cryst.unit_cell.r` contains the
  four generated atomic positions, that are not symmetry equivalent any
  more.
 
  ```
  >>symOp = 'x+1/2,y+1/2,z;x+1/2,y,z+1/2;x,y+1/2,z+1/2'
  >>cryst = spinw
  >>cryst.genlattice('lat_const',[8 8 8],'sym',symOp,'label','FCC')
  >>cryst.addatom('r',[0 0 0],'label','Atom1')
  >>cryst.unit_cell.r>>
  >>cryst.nosym
  >>cryst.unit_cell.r>>
  ```
  
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  ### Output Arguments
  
  The `obj` input will have `obj.lattice.sym` field equal to zero and the
  [obj.unit_cell] field will contain all the generated atomic positions.
  
  ### See Also
  
  [spinw] \| [spinw.newcell]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('nosym')), 1)
        return m.nosym(self.handle, *args, nargout=nout)

    def notwin(self, *args, **kwargs):
        """
  removes all twins
  
  ### Syntax
  
  `notwin(obj)`
  
  ### Description
  
  `notwin(obj)` removes any crystallographic twin added using the
  [spinw.addtwin] function.
   
  ### See Also
 
  [spinw.addtwin]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('notwin')), 1)
        return m.notwin(self.handle, *args, nargout=nout)

    def optmagk(self, *args, **kwargs):
        """
  determines the magnetic propagation vector
  
  ### Syntax
  
  `res = optmagk(obj,Name,Value)`
  
  ### Description
  
  `res = optmagk(obj,Name,Value)` determines the optimal propagation vector
  using the Luttinger-Tisza method. It calculates the Fourier transform of
  the Hamiltonian as a function of wave vector and finds the wave vector
  that corresponds to the smalles global eigenvalue of the Hamiltonian.
  The global optimization is achieved using Particle-Swarm optimizer. This
  function sets k and F in spinw.mag_str, and also returns them.
  
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  ### Name-Value Pair Arguments
 
  `kbase`
  : Provides a set of vectors that span the space for possible propagation
    vectors:
 
    $ \mathbf{k} = \sum_i C(i)\cdot \mathbf{k}_{base}(i);$
 
    where the optimiser determines the $C(i)$ values that correspond
       to the lowest ground state energy. $\mathbf{k}_{base}$ is a
       matrix with dimensions $[3\times n_{base}]$, where $n_{base}\leq 3$. The basis
       vectors have to be linearly independent.
  
  The function also accepts all options of [ndbase.pso].
  
  ### Output Arguments
  
  `res`
  : Structure with the following fields:
    * `k`       Value of the optimal k-vector, with values between 0
                        and 1/2.
    * `F`       Fourier components for every spin in the magnetic
                        cell.
    * `E`       The most negative eigenvalue at the given propagation
                        vector.
    * `stat`    Full output of the [ndbase.pso] optimizer.
  
  ### See Also
  
  [ndbase.pso]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('optmagk')), 1)
        return m.optmagk(self.handle, *args, nargout=nout)

    def optmagsteep(self, *args, **kwargs):
        """
  quench optimization of magnetic structure
  
  ### Syntax
  
  `optm = optmagsteep(obj,Name,Value)`
  
  ### Description
  
  `optm = optmagsteep(obj,Name,Value)` determines the lowest energy
  magnetic configuration within a given magnetic supercell and previously
  fixed propagation (and normal) vector (see [spinw.optmagk]). It
  iteratively rotates each spin towards the local magnetic field thus
  achieving local energy minimum. Albeit not guaranteed this method often
  finds the global energy minimum. The methods works best for small
  magnetic cells and non-frustrated structures. Its execution is roughly
  equivalent to a thermal quenching from the paramagnetic state.
  
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  ### Name-Value Pair Arguments
  
  `'nRun'`
  : Number of iterations, default value is 100 (it is usually enough). Each
    spin will be quenched `nRun` times or until convergence is reached.
  
  `'boundary'`
  : Boundary conditions of the magnetic cell, string with allowed values:
    * `'free'`  Free, interactions between extedned unit cells are
                omitted.
    * `'per'`   Periodic, interactions between extended unit cells
                are retained.
 
    Default value is `{'per' 'per' 'per'}`.
  
  `'nExt'`
  : The size of the magnetic cell in number of crystal unit cells.
    Default value is taken from `obj.mag_str.nExt`.
  
  `'fSub'`
  : Function that defines non-interacting sublattices for parallelization.
    It has the following header:
        `cGraph = fSub(conn,nExt)`, where `cGraph` is a row vector with
        $n_{magExt}$ number of elements,
    `conn` is a matrix with dimensions of $[2\times n_{conn}]$ size matrix and $n_{ext}$ is equal to
    the `nExt` parameter. Default value is `@sw_fsub`.
  
  `'subLat'`
  : Vector that assigns all magnetic moments into non-interacting
    sublattices, contains a single index $(1,2,3...)$ for every magnetic
    moment in a row vector with $n_{magExt}$ number of elements. If
    undefined, the function defined in `fSub` will be used to partition the
    lattice.
  
  `'random'`
  : If `true` random initial spin orientations will be used (paramagnet),
    if initial spin configuration is undefined (`obj.mag_str.F` is empty)
    the initial configuration will be always random. Default value is
    `false`.
  
  `'TolX'`
  : Minimum change of the magnetic moment necessary to reach convergence.
  
  `'saveAll'`
  : Save moment directions for every loop, default value is `false`.
  
  `'Hmin'`
  : Minimum field value on the spin that moves the spin. If the
    molecular field absolute value is below this, the spin won't be
    turned. Default is 0.
  
  `'plot'`
  : If true, the magnetic structure in plotted in real time. Default value
    is `false`.
  
  `'pause'`
  : Time in second to pause after every optimization loop to slow down plot
    movie. Default value is 0.
 
  `'fid'`
  : Defines whether to provide text output. The default value is determined
    by the `fid` preference stored in [swpref]. The possible values are:
    * `0`   No text output is generated.
    * `1`   Text output in the MATLAB Command Window.
    * `fid` File ID provided by the `fopen` command, the output is written
            into the opened file stream.
  
  ### Output Arguments
  
  `optm`
  : Struct type variable with the following fields:
    * `obj`         spinw object that contains the optimised magnetic structure.
    * `M`           Magnetic moment directions with dimensions $[3\times n_{magExt}]$, if
                    `saveAll` parameter is `true`, it contains the magnetic structure
                    after every loop in a matrix with dimensions $[3\times n{magExt}\times n_{loop}]$.
    * `dM`          The change of magnetic moment vector averaged over all moments
                    in the last loop.
    * `e`           Energy per spin in the optimised structure.
    * `param`       Input parameters, stored in a struct.
    * `nRun`        Number of loops executed.
    * `datestart`   Starting time of the function.
    * `dateend`     End time of the function.
    * `title`       Title of the simulation, given in the input.
  
  ### See Also
  
  [spinw] \| [spinw.anneal] \| [sw_fsub] \| [sw_fstat]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('optmagsteep')), 1)
        return m.optmagsteep(self.handle, *args, nargout=nout)

    def optmagstr(self, *args, **kwargs):
        """
  general magnetic structure optimizer
  
  ### Syntax
  
  `optm = optmagstr(obj,Name,Value)`
  
  ### Description
  
  `optm = optmagstr(obj,Name,Value)` is a general magnetic structure
  optimizer that as the name suggests is general however usually less
  efficient than [spinw.optmagk] or [spinw.optmagsteep]. However this
  function enables the usage of constraint functions to improve the
  optimization. This function is most useful if there are 1-2 parameters
  that have to be optimized, such as a canting angle of the spins in
  a magnetic field. To optimize large numbers of spin angles
  [spinw.optmagsteep] might be faster. Only obj.mag_str.nExt is used from
  an already initialised magnetic structure, initial k and S are determined
  from the optimisation function parameters. If a magnetic structure has
  not been initialised in obj, nExt = [1 1 1] is used.
  
  ### Examples
  
  The example determines the propagation vector of the ground state of the
  triangular lattice antiferromagnet. The magnetic structure is constrained
  to be planar in the $xy$-plane. The [gm_planard] constraint function is
  used where the first 3 parameter determined the propagation vector,
  followed by the polar angles of the magnetic moments (here there is only
  1 magnetic moment in the unit cell) which is fixed to 0. Finally the last
  2 parameters corresponds to the polar angles of the normal to the
  spin-plane which is the $z$-axis ($\theta=0$, $\varphi=0$). The optimized
  magnetic structure is plotted.
 
  ```
  >>tri = sw_model('triAF',1)
  >>X1 = [0 0 0 0 0 0]
  >>X2 = [0 1/2 1/2 0 0 0]
  >>optRes = tri.optmagstr('func',@gm_planard,'xmin',X1,'xmax',X2)
  >>km = optRes.x(1:3)>>
  >>plot(tri)
  >>>swplot.zoom(1.5)
  >>snapnow
  ```
  
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  ### Name-Value Pair Arguments
  
  `'func'`
  : Function that produces the spin orientations, propagation vector and
    normal vector from the optimization parameters and has the following
    argument list:
    ```
    [M, k, n] = @(x)func(M0, x)
    ```
   here `M` is matrix with dimensions of $[3\times n_{magExt}]$, `k` is the
   propagation vector (row vector with 3 elements), `n` is the normal vector
   of the spin rotation plane (row vector with 3 elements). The
   default value is `@gm_spherical3d`. For planar magnetic structures
   use `@gm_planar`.
  
  `'xmin'`
  : Lower limit of the optimisation parameters.
  
  `'xmax'`
  : Upper limit of the optimisation parameters.
  
  `'x0'`
  : Starting value of the optimisation parameters. If empty
    or undefined, then random values are used within the given limits.
  
  `'boundary'`
  : Boundary conditions of the magnetic cell:
    * `'free'`  Free, interactions between extedned unit cells are
              omitted.
    * `'per'`   Periodic, interactions between extended unit cells
              are retained.
 
    Default value is `{'per' 'per' 'per'}`.
  
  `'epsilon'`
  : The smallest value of incommensurability that is tolerated
    without warning. Default value is $10^{-5}$.
  
  `'nRun'`
  : Number of runs. If random starting parameters are given, the
    optimisation process will be rerun `nRun` times and the best
    result (lowest ground state energy per spin) will be kept.
  
  `'title'`
  : Gives a title string to the simulation that is saved in the
    output.
  
  `'tid'`
  : Determines if the elapsed and required time for the calculation is
    displayed. The default value is determined by the `tid` preference
    stored in [swpref]. The following values are allowed (for more details
    see [sw_timeit]):
    * `0` No timing is executed.
    * `1` Display the timing in the Command Window.
    * `2` Show the timing in a separat pup-up window.
 
  #### Limits on selected prameters
 
  Limits can be given on any input parameter of the constraint function by
  giving the name of the parameter. For parameter names see the help of the
  used constraint function. Limits per optimization parameter can be given
  in the following format: `optmagstr('ParName',[min max],...)`. For example
  to fix the `nTheta` value of [gm_planar] during the optimisation to zero
  use: `optmagstr(obj,'func',@gm_planar,'nTheta',[0 0])`.
 
  
  #### Optimisation parameters
  
  The optimization parameters are identical to the input options of the
  Matlab built-in optimizer [matlab.fminsearch].
 
  `'tolx'`
  : Minimum change of `x` when convergence reached, default
      value is $10^{-4}$.
  
  `'tolfun'`
  : Minimum change of the $R$ value when convergence reached,
      default value is $10^{-5}$.
  
  `'maxfunevals'`
  : Maximum number of function evaluations, default value
      is $10^7$.
  
  `'maxiter'`
  : Maximum number of iterations, default value is $10^4$.
  
  ### Output Arguments
  
  `optm`
  : Struct type variable with the following fields:
    * `obj`       spinw object that contains the optimised magnetic structure.
    * `x`         Optimised paramters in a row vector with $n_{par}$ number
                  of elements.
    * `fname`     Name of the contraint function.
    * `xname`     Cell containing the name of the $x$ parameters with
                    $n_{par}$ elements.
    * `e`         Energy per spin in the optimised structure.
    * `exitflag`  Exit flag of the optimisation code, see [matlab.fminsearch].
    * `output`    Detailed output of the optimisation code, see [matlab.fminsearch].
    * `param`     Input parameters, stored in a struct.
  
  ### See Also
  
  [spinw] \| [spinw.anneal] \| [gm_spherical3d] \| [gm_planar] \| [fminsearch]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('optmagstr')), 1)
        return m.optmagstr(self.handle, *args, nargout=nout)

    def plot(self, *args, **kwargs):
        """
  plots 3D model
  
  ### Syntax
  
  `plot(obj,Name,Value)`
  `hFigure = plot(obj,Name,Value)`
  
  ### Description
  
  `plot(obj,Name,Value)` plots the atoms and couplings stored in `obj` onto
  an [swplot] figure (see [swplot.figure]). The generated 3D plot can be
  rotated using the mouse and panning works by keeping the Ctrl/Control
  button pressed. There is information about every object on the figure
  (here called tooltips) that is shown when clicked on the object. The 3D
  view direction can be changed programatically using [swplot.view] while
  translations are controlled using the [swplot.translate]. Arbitrary
  transformation (combination of rotation and translation) can be
  introduced using the [swplot.transform]. All these transformation act as
  a global transformation, relative transformation of the 3D objects is
  only possible at creation by defining the transformed coordinates.
   
  The `<strong>spinw/plot</strong>` function calls several high level plot routines to draw
  the different types of objects: [swplot.plotatom] (atoms),
  [swplot.plotmag] (magnetic moments), [swplot.plotion] (single ion
  properties), [swplot.plotbond] (bonds), [swplot.plotbase] (basis vectors)
  and [swplot.plotcell] (unit cells).
   
  The high level `<strong>spinw/plot</strong>` function can send send parameters to any of
  the above plot group functions. The paramer name has to be of the format:
  `['plot group name' 'group option']`. For example to set the `color` option
  of the cell (change the color of the unit cell) use the option
  'cellColor'. In this case `<strong>spinw/plot</strong>` will call the [swplot.plotcell]
  function with the `color` parameter set to the given value. For all the
  possible group plot function options see the corresponding help.
   
  It is possible to switch off calling any of the subfunctions by using the
  option `['plot group name' 'mode']` set to `'none'`. For example to skip
  plotting of the atoms set the `'atomMode'` parameter to `'none'`:
  `<strong>spinw/plot</strong>('atomMode','none')`.
   
  ### Name-Value Pair Arguments
   
  These are global options, that each plot group function recognizes, these global
  options can be added without the group name.
  
  `'range'`
  : Plotting range of the lattice parameters in lattice units,
    in a matrix with dimensions of $[3\times 2]$. For example to plot the
    first unit cell, use: `[0 1;0 1;0 1]`. Also the number unit cells can
    be given along the $a$, $b$ and $c$ directions, e.g. `[2 1 2]`, this is
    equivalent to `[0 2;0 1;0 2]`. Default value is the single unit cell.
  
  `'unit'`
  : Unit in which the range is defined. It can be the following
    string:
    * `'lu'`        Lattice units (default).
    * `'xyz'`       Cartesian coordinate system in \\ang units.
  
  `'figure'`
  : Handle of the [swplot] figure. Default is the active figure.
  
  `'legend'`
  : Whether to add legend to the plot, default value is `true`, for details
    see [swplot.legend].
  
  `'fontSize'`
  : Font size of the atom labels in pt units, default value is stored in
    `swpref.getpref('fontsize')`.
  
  `'nMesh'`
  : Resolution of the ellipse surface mesh. Integer number that is
    used to generate an icosahedron mesh with $n_{mesh}$ number of
    additional triangulation, default value is stored in
    `swpref.getpref('nmesh')`.
  
  `'nPatch'`
  : Number of points on the curve for the arrows and cylinders,
    default value is stored in `swpref.getpref('npatch')`.
  
  `'tooltip'`
  : If `true`, the tooltips will be shown when clicking on the plot.
    Default value is `true`.
  
  `'shift'`
  : Column vector with 3 elements, all objects will be shifted by
    the given value. Default value is `[0;0;0]`.
  
  `'replace'`
  : Replace previous plot if `true`. Default value is `true`.
  
  `'translate'`
  : If `true`, all plot objects will be translated to the figure
    center. Default is `true`.
  
  `'zoom'`
  : If `true`, figure will be automatically zoomed to the ideal scale.
    Default value is `true`.
 
  ### See Also
   
  [swplot.plotatom] \| [swplot.plotmag] \| [swplot.plotion] \| 
  [swplot.plotbond] \| [swplot.plotbase] \| [swplot.plotcell]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('plot')), 1)
        return m.plot(self.handle, *args, nargout=nout)

    def powspec(self, *args, **kwargs):
        """
  calculates powder averaged spin wave spectra
 
  ### Syntax
 
  `spectra = powspec(obj,QA)`
 
  `spectra = powspec(___,Name,Value)`
 
  ### Description
 
  `spectra = powspec(obj,QA)` calculates powder averaged spin wave spectrum
  by averaging over spheres with different radius around origin in
  reciprocal space. This way the spin wave spectrum of polycrystalline
  samples can be calculated. This method is not efficient for low
  dimensional (2D, 1D) magnetic lattices. To speed up the calculation with
  mex files use the `swpref.setpref('usemex',true)` option. 
 
  `spectra = powspec(___,Value,Name)` specifies additional parameters for
  the calculation. For example the function can calculate powder average of
  arbitrary spectral function, if it is specified using the `specfun`
  option. 
 
  ### Example
 
  Using only a few lines of code one can calculate the powder spectrum of
  the triangular lattice antiferromagnet ($S=1$, $J=1$) between $Q=0$ and 3
  \\ang$^{-1}$ (the lattice parameter is 3 \\ang).
 
  ```
  >>tri = sw_model('triAF',1);
  >>E = linspace(0,4,100);
  >>Q = linspace(0,4,300);
  >>triSpec = tri.powspec(Q,'Evect',E,'nRand',1e3);
  >>sw_plotspec(triSpec);
  >>snapnow
  ```
 
  ### Input arguments
 
  `obj`
  : [spinw] object.
 
  `QA`
  : Vector containing the $Q$ values in units of the inverse of the length
  unit (see [spinw.unit]) with default unit being \\ang$^{-1}$. The
  value are stored in a row vector with $n_Q$ elements.
 
  ### Name-Value Pair Arguments
 
  `specfun`
  : Function handle of a solver. Default value is `@spinwave`. It is
    currently tested with two functions:
 
    * `spinw.spinwave` 	Powder average spin wave spectrum.
    * `spinw.scga`      Powder averaged diffuse scattering spectrum.
 
  `nRand`
  : Number of random orientations per `QA` value, default value is 100.
 
  `Evect`
  : Row vector, defines the center/edge of the energy bins of the
    calculated output, number of elements is $n_E$. The energy units are
    defined by the `spinw.unit.kB` property. Default value is an edge bin
    `linspace(0,1.1,101)`.
 
  `binType`
  : String, determines the type of bin, possible options:
    * `'cbin'`    Center bin, the center of each energy bin is given.
    * `'ebin'`    Edge bin, the edges of each bin is given.
 
    Default value is `'ebin'`.
 
  `'T'`
  : Temperature to calculate the Bose factor in units
    depending on the Boltzmann constant. Default value taken from
    `obj.single_ion.T` value.
 
  `'title'`
  : Gives a title to the output of the simulation.
 
  `'extrap'`
  : If true, arbitrary additional parameters are passed over to
    the spectrum calculation function.
 
  `'fibo'`
  : If true, instead of random sampling of the unit sphere the Fibonacci
    numerical integration is implemented as described in
    [J. Phys. A: Math. Gen. 37 (2004)
    11591](<a href="matlab:web http://iopscience.iop.org/article/10.1088/0305-4470/37/48/005/meta">http://iopscience.iop.org/article/10.1088/0305-4470/37/48/005/meta</a>).
    The number of points on the sphere is given by the largest
    Fibonacci number below `nRand`. Default value is false.
 
  `'imagChk'`
  : Checks that the imaginary part of the spin wave dispersion is
    smaller than the energy bin size. Default value is true.
 
  `'component'`
  : See [sw_egrid] for the description of this parameter.
 
  The function also accepts all parameters of [spinw.spinwave] with the
  most important parameters are:
 
  `'formfact'`
  : If true, the magnetic form factor is included in the spin-spin
    correlation function calculation. The form factor coefficients are
    stored in `obj.unit_cell.ff(1,:,atomIndex)`. Default value is `false`.
 
  `'formfactfun'`
  : Function that calculates the magnetic form factor for given $Q$ value.
    value. Default value is `@sw_mff`, that uses a tabulated coefficients
    for the form factor calculation. For anisotropic form factors a user
    defined function can be written that has the following header:
    ```
    F = formfactfun(atomLabel,Q)
    ```
    where the parameters are:
    * `F`           row vector containing the form factor for every input 
                    $Q$ value
    * `atomLabel`   string, label of the selected magnetic atom
    * `Q`           matrix with dimensions of $[3\times n_Q]$, where each
                    column contains a $Q$ vector in $\\ang^{-1}$ units.
 
  `'gtensor'`
  : If true, the g-tensor will be included in the spin-spin correlation
    function. Including anisotropic g-tensor or different
    g-tensor for different ions is only possible here. Including a simple
    isotropic g-tensor is possible afterwards using the [sw_instrument]
    function.
 
  `'hermit'`
  : Method for matrix diagonalization with the following logical values:
  
    * `true`    using Colpa's method (for details see [J.H.P. Colpa, Physica 93A (1978) 327](<a href="matlab:web http://www.sciencedirect.com/science/article/pii/0378437178901607">http://www.sciencedirect.com/science/article/pii/0378437178901607</a>)),
                the dynamical matrix is converted into another Hermitian
                matrix, that will give the real eigenvalues.
    * `false`   using the standard method (for details see [R.M. White, PR 139 (1965) A450](<a href="matlab:web https://journals.aps.org/pr/abstract/10.1103/PhysRev.139.A450">https://journals.aps.org/pr/abstract/10.1103/PhysRev.139.A450</a>))
                the non-Hermitian $\mathcal{g}\times \mathcal{H}$ matrix
                will be diagonalised, which is computationally less
                efficient. Default value is `true`.
 
  {{note Always use Colpa's method, except when imaginary eigenvalues are
    expected. In this case only White's method work. The solution in this
    case is wrong, however by examining the eigenvalues it can give a hint
    where the problem is.}}
 
  `'fid'`
  : Defines whether to provide text output. The default value is determined
    by the `fid` preference stored in [swpref]. The possible values are:
    * `0`   No text output is generated.
    * `1`   Text output in the MATLAB Command Window.
    * `fid` File ID provided by the `fopen` command, the output is written
            into the opened file stream.
 
  `'tid'`
  : Determines if the elapsed and required time for the calculation is
    displayed. The default value is determined by the `tid` preference
    stored in [swpref]. The following values are allowed (for more details
    see [sw_timeit]):
    * `0` No timing is executed.
    * `1` Display the timing in the Command Window.
    * `2` Show the timing in a separat pup-up window.
 
  `dE`
  : Energy resolution (FWHM) can be function, or a numeric matrix that
    has length 1 or the number of energy bin centers.
 
  `'neutron_output'`
  : If `true`, the spinwave will output only `Sperp`, the S(q,w) component
    perpendicular to Q that is measured by neutron scattering, and will
    *not* output the  full Sab tensor. (Usually sw_neutron is used to 
    calculate `Sperp`.) Default value is `false`.
 
  `'fastmode'`
  : If `true`, will set `'neutron_output', true`, `'fitmode', true`,
    `'sortMode', false`, and will only output intensity for positive energy
    (neutron energy loss) modes. Default value is `false`.
 
  The function accepts some parameters of [spinw.scga] with the most important
  parameters are:
 
  `'nInt'`
  : Number of $Q$ points where the Brillouin zone is sampled for the
    integration.
 
  ### Output Arguments
 
  `spectra`
  : structure with the following fields:
 
    * `swConv` The spectra convoluted with the dispersion. The center
      of the energy bins are stored in `spectra.Evect`. Dimensions are
      $[n_E\times n_Q]$.
    * `hklA` Same $Q$ values as the input `hklA`.
    * `Evect` Contains the bins (edge values of the bins) of the energy transfer
      values, dimensions are $[1\times n_E+1]$.
    * `param` Contains all the input parameters.
    * `obj` The clone of the input `obj` object, see [spinw.copy].
 
  ### See also
 
  [spinw] \| [spinw.spinwave] \| [spinw.optmagstr] \| [sw_egrid]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('powspec')), 1)
        return m.powspec(self.handle, *args, nargout=nout)

    def quickham(self, *args, **kwargs):
        """
  quickly generate magnetic Hamiltonian
  
  ### Syntax
  
  `quickham(obj,J)`
  
  ### Description
  
  `quickham(obj,J)` generates the bonds from the predefined crystal
  structure and assigns exchange values to bonds such as `J(1)` to first
  neighbor, `J(2)` for second neighbor etc. The command will erase all
  previous bonds, anisotropy, g-tensor and matrix definitions. Even if
  `J(idx) == 0`, the corresponding bond and matrix will be created.
   
  
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  `J`
  : Vector that contains the Heisenberg exchange values. `J(1)` for
       first neighbor bonds, etc.
 
  ### See Also
 
  [spinw.gencoupling] \| [spinw.addcoupling] \| [spinw.matrix] \|
  [spinw.addmatrix]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('quickham')), 1)
        return m.quickham(self.handle, *args, nargout=nout)

    def rl(self, *args, **kwargs):
        """
  generates reciprocal lattice vectors
  
  ### Syntax
  
  `rlVec = rl(obj, {norm})`
  
  ### Description
  
  `rlVec = rl(obj, {norm})` returns the lattice vectors of the reciprocal
  lattice in a $[3\times 3]$ matrix, with the $a^*$, $b^*$ and $c^*$ vectors
  stored in **rows**. 
 
  
  ### Examples
  
  To convert from reciprocal lattice unit to \\ang$^{-1}$ ($xyz$
  Cartesian coordinate system) use: (`Q_rlu` is a row vector with 3
  elements):
 
  ```
  Q_xyz =  Q_rlu * rlVect
  ```
  
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  `norm`
  : If `true`, the basis vectors are normalized to 1. Default values is
  `false`, optional.
  
  ### Output Arguments
  
  `rlVec`
  : Stores the three basis vectors in the rows of matrix with dimensions of
    $[3\times 3]$.
  
  ### See Also
  
  [spinw] \| [spinw.abc] \| [spinw.basisvector]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('rl')), 1)
        return m.rl(self.handle, *args, nargout=nout)

    def saveobj(self, obj=None, **kwargs):
        """
  remove property change listeners


        """
        args = tuple(v for v in [obj] if v is not None)
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('saveobj')), 1)
        return m.saveobj(self.handle, *args, nargout=nout)

    def set(self, *args, **kwargs):
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
 
    See also <a href="matlab:help set -displayBanner">set</a>, <a href="matlab:help spinw -displayBanner">spinw</a>, <a href="matlab:help spinw/setdisp -displayBanner">spinw/setdisp</a>, <a href="matlab:help handle -displayBanner">handle</a>

Help for <strong>spinw/set</strong> is inherited from superclass <a href="matlab:help matlab.mixin.SetGet -displayBanner">matlab.mixin.SetGet</a>


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('set')), 1)
        return m.set(self.handle, *args, nargout=nout)

    def setdisp(self, *args, **kwargs):
        """
 <strong>setdisp</strong>    Specialized MATLAB object property display.
    <strong>setdisp</strong> is called by SET when SET is called with no output argument 
    and a single input parameter H an array of handles to MATLAB objects.  
    This method is designed to be overridden in situations where a
    special display format is desired to display the results returned by
    SET(H).  If not overridden, the default display format for the class
    is used.
 
    See also <a href="matlab:help matlab.mixin.SetGet.setdisp -displayBanner">setdisp</a>, <a href="matlab:help spinw -displayBanner">spinw</a>, <a href="matlab:help spinw/set -displayBanner">spinw/set</a>, <a href="matlab:help handle -displayBanner">handle</a>

Help for <strong>spinw/setdisp</strong> is inherited from superclass <a href="matlab:help matlab.mixin.SetGet -displayBanner">matlab.mixin.SetGet</a>


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('setdisp')), 1)
        return m.setdisp(self.handle, *args, nargout=nout)

    def setmatrix(self, *args, **kwargs):
        """
  sets exchange tensor values
  
  ### Syntax
  
  `setmatrix(obj,Name,Value)`
  
  ### Description
  
  `setmatrix(obj,Name,Value)` sets the value of a selected matrix based on
  symmetry analysis.
  
  ### Examples
  
  This example will set 'J1' coupling to the 6th symmetry allowed matrix,
  with prefactor 0.235.
  ```
  setmatrix(crystal,'label','J1','pref',{[6 0.235]})
  ```
  This will set 'J2' to antiferromagnetic Heisenberg exchange, with value
  of 1.25 meV.
  ```
  setmatrix(crystal,'label','J2','pref',{1.25})
  ```
 
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  ### Name-Value Pair Arguments
  
  One of the below options has to be given:
  
  `'mat'`
  : Label or index of the matrix that is already assigned to
    a bond, anisotropy or g-tensor.
  
  `'bond'`
  : Index of the bond in `spinw.coupling.idx`, e.g. 1 for first neighbor.
  
  `'subIdx'`
  : Selects a certain bond within the symmetry equivalent bonds, within
    default value is 1.
  
  `'aniso'`
  : Label or index of the magnetic atom that has a single ion
    anisotropy matrix is assigned, e.g. `'Cr3'` to select anisotropy on
    atoms with this label.
  
  `'gtensor'`
  : Label or index of the magnetic atom that has a g-tensor is 
    assigned.
  
  Optional inputs:
  
  `'pref'`
  : Defines prefactors as a vector for the symmetry allowed
            components in a row vector with $n_{symMat}$ number of elements. Alternatively, if only
            a few of the symmetry allowed matrices have non-zero
            prefactors, use:
    ```
    {[6 0.1 5 0.25]}
    ```
    This means, the 6th symmetry allowed matrix have prefactor 0.1,
            the 5th symmetry allowed matrix have prefactor 0.25. Since
            Heisenberg isotropic couplings are always allowed, a cell with
            a single element will create a Heisenberg coupling, example:
    ```
    {0.1}
    ```
    This is identical to `obj.matrix.mat = eye(3)*0.1`.
            For DM interactions (antisymmetric coupling matrices), use
            three element vector in the cell:
    ```
    {[D1 D2 D3]}
    ```
    In this case, these will be the prefactors of the 3
            antisymmetric symmetry allowed matrices. In case no crystal
            symmetry is defined, these will define directly the components
            of the  DM interaction in the $xyz$ coordinate system. Be
            carefull with the sign of the DM interaction, it depends on the
            order of the two interacting atoms! Default value is `{1}`.
            For anisotropy matrices antisymmetric matrices are not allowed.
  
  ### Output Arguments
  
  The selected `obj.matrix.mat` will contain the new value.
  
  ### See Also
  
  [spinw] \| [spinw.gencoupling] \| [spinw.getmatrix]
  
  *[DM]: Dzyaloshinskii-Moriya


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('setmatrix')), 1)
        return m.setmatrix(self.handle, *args, nargout=nout)

    def setunit(self, *args, **kwargs):
        """
  sets the physical units
  
  ### Syntax
  
  `setunit(obj,Name,Value)`
  
  ### Description
  
  `setunit(obj,Name,Value)` sets the physical units of the Hamiltonian.
  This includes the magnetic field, exchange interaction, length and
  temperature.
  
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  ### Name-Value Pair Arguments
  
  `'mode'`
  : Type of unit system, defined by one of the following strings:
    * `'AmeVTK'`    Typical units used in neutron/x-ray scattering:
                        [\\ang, meV, Tesla and Kelvin]
    * `'1'`         No units, all conversion factors are set to 1.
 
  ### See Also
 
  [spinw.unit]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('setunit')), 1)
        return m.setunit(self.handle, *args, nargout=nout)

    def softparamcheck(self, *args, **kwargs):
        """
SPINW/<strong>softparamcheck</strong> is an undocumented builtin function.


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('softparamcheck')), 1)
        return m.softparamcheck(self.handle, *args, nargout=nout)

    def spinwave(self, *args, **kwargs):
        """
  calculates spin correlation function using linear spin wave theory
 
  ### Syntax
 
  `spectra = spinwave(obj,Q)`
 
  `spectra = spinwave(___,Name,Value)`
 
  ### Description
 
  `spinwave(obj,Q,Name,Value)` calculates spin wave dispersion and
  spin-spin correlation function at the reciprocal space points $Q$. The
  function can solve any single-k magnetic structure exactly and any
  multi-k magnetic structure appoximately and quadratic spinw-spin
  interactions as well as single ion anisotropy and magnetic field.
  Biquadratic exchange interactions are also implemented, however only for
  $k_m=0$ magnetic structures.
 
  If the magnetic ordering wavevector is non-integer, the dispersion is
  calculated using a coordinate system rotating from unit cell to unit
  cell. In this case the spin Hamiltonian has to fulfill this extra
  rotational symmetry which is not checked programatically.
 
  Some of the code of the function can run faster if mex files are used. To
  switch on mex files, use the `swpref.setpref('usemex',true)` command. For
  details see the [sw_mex] and [swpref.setpref] functions.
 
  ### Examples
 
  To calculate and plot the spin wave dispersion of the
  triangular lattice antiferromagnet ($S=1$, $J=1$) along the $(h,h,0)$
  direction in reciprocal space we create the built in triangular lattice
  model using `sw_model`.
 
  ```
  >>tri = sw_model('triAF',1)
  >>spec = tri.spinwave({[0 0 0] [1 1 0]})
  >>sw_plotspec(spec)
  >>snapnow
  ```
 
  ### Input Arguments
 
  `obj`
  : [spinw] object.
 
  `Q`
  : Defines the $Q$ points where the spectra is calculated, in reciprocal
    lattice units, size is $[3\times n_{Q}]$. $Q$ can be also defined by
    several linear scan in reciprocal space. In this case `Q` is cell type,
    where each element of the cell defines a point in $Q$ space. Linear scans
    are assumed between consecutive points. Also the number of $Q$ points can
    be specified as a last element, it is 100 by defaults.
 
    For example to define a scan along $(h,0,0)$ from $h=0$ to $h=1$ using
    200 $Q$ points the following input should be used:
    ```
    Q = {[0 0 0] [1 0 0]  200}
    ```
 
    For symbolic calculation at a general reciprocal space point use `sym`
    type input.
 
    For example to calculate the spectrum along $(h,0,0)$ use:
    ```
    Q = [sym('h') 0 0]
    ```
    To calculate spectrum at a specific $Q$ point symbolically, e.g. at
    $(0,1,0)$ use:
    ```
    Q = sym([0 1 0])
    ```
 
  ### Name-Value Pair Arguments
 
  `'formfact'`
  : If true, the magnetic form factor is included in the spin-spin
    correlation function calculation. The form factor coefficients are
    stored in `obj.unit_cell.ff(1,:,atomIndex)`. Default value is `false`.
 
  `'formfactfun'`
  : Function that calculates the magnetic form factor for given $Q$ value.
    value. Default value is `@sw_mff`, that uses a tabulated coefficients
    for the form factor calculation. For anisotropic form factors a user
    defined function can be written that has the following header:
    ```
    F = formfactfun(atomLabel,Q)
    ```
    where the parameters are:
    * `F`           row vector containing the form factor for every input
                    $Q$ value
    * `atomLabel`   string, label of the selected magnetic atom
    * `Q`           matrix with dimensions of $[3\times n_Q]$, where each
                    column contains a $Q$ vector in $\\ang^{-1}$ units.
 
  `'cmplxBase'`
  : If `true`, we use a local coordinate system fixed by the
    complex magnetisation vectors:
    $\begin{align}  e_1 &= \Im(\hat{M})\\
                    e_3 &= Re(\hat{M})\\
                    e_2 &= e_3\times e_1
     \end{align}$
    If `false`, we use a coordinate system fixed to the moments:
    $\begin{align}  e_3 \parallel S_i\\
                    e_2 &= \S_i \times [1, 0, 0]\\
                    e_1 &= e_2 \times e_3
    \end{align}$
    Except if $S_i \parallel [1, 0, 0], e_2 = [0, 0, 1]$. The default is
   `false`.
 
  `'gtensor'`
  : If true, the g-tensor will be included in the spin-spin correlation
    function. Including anisotropic g-tensor or different
    g-tensor for different ions is only possible here. Including a simple
    isotropic g-tensor is possible afterwards using the [sw_instrument]
    function.
 
  `'neutron_output'`
  : If `true`, will output only `Sperp`, the S(q,w) component perpendicular
    to Q that is measured by neutron scattering, and will *not* output the
    full Sab tensor. (Usually sw_neutron is used to calculate `Sperp`.)
    Default value is `false`.
 
  `'fitmode'`
  : If `true`, function is optimized for multiple consecutive calls (e.g.
    the output spectrum won't contain the copy of `obj`), default is
    `false`.
 
  `'fastmode'`
  : If `true`, will set `'neutron_output', true`, `'fitmode', true`,
    `'sortMode', false`, and will only output intensity for positive energy
    (neutron energy loss) modes. Default value is `false`.
 
  `'notwin'`
  : If `true`, the spectra of the twins won't be calculated. Default is
    `false`.
 
  `'sortMode'`
  : If `true`, the spin wave modes will be sorted by continuity. Default is
    `true`.
 
  `'optmem'`
  : Parameter to optimise memory usage. The list of Q values will be cut
    into `optmem` number of pieces and will be calculated piece by piece to
    decrease peak memory usage. Default value is 0, when the number
    of slices are determined automatically from the available free memory.
 
  `'tol'`
  : Tolerance of the incommensurability of the magnetic ordering wavevector.
    Deviations from integer values of the ordering wavevector smaller than
    the tolerance are considered to be commensurate. Default value is
    $10^{-4}$.
 
  `'omega_tol'`
  : Tolerance on the energy difference of degenerate modes when
    diagonalising the quadratic form, default value is $10^{-5}$.
 
  `'hermit'`
  : Method for matrix diagonalization with the following logical values:
 
    * `true`    using Colpa's method (for details see [J.H.P. Colpa, Physica 93A (1978) 327](<a href="matlab:web http://www.sciencedirect.com/science/article/pii/0378437178901607">http://www.sciencedirect.com/science/article/pii/0378437178901607</a>)),
                the dynamical matrix is converted into another Hermitian
                matrix, that will give the real eigenvalues.
    * `false`   using the standard method (for details see [R.M. White, PR 139 (1965) A450](<a href="matlab:web https://journals.aps.org/pr/abstract/10.1103/PhysRev.139.A450">https://journals.aps.org/pr/abstract/10.1103/PhysRev.139.A450</a>))
                the non-Hermitian $\mathcal{g}\times \mathcal{H}$ matrix
                will be diagonalised, which is computationally less
                efficient. Default value is `true`.
 
  {{note Always use Colpa's method, except when imaginary eigenvalues are
    expected. In this case only White's method work. The solution in this
    case is wrong, however by examining the eigenvalues it can give a hint
    where the problem is.}}
 
  `'saveH'`
  : If true, the quadratic form of the Hamiltonian is also saved in the
    output. Be carefull, it can take up lots of memory. Default value is
    `false`.
 
  `'saveV'`
  : If true, the matrices that transform the normal magnon modes into the
    magnon modes localized on the spins are also saved into the output. Be
    carefull, it can take up lots of memory. Default value is `false`.
 
  `'saveSabp'`
  : If true, the dynamical structure factor in the rotating frame
    $S'(k,\omega)$ is saved. For incommensurate structures only. Default
    value is `false`.
 
  `'title'`
  : Gives a title string to the simulation that is saved in the output.
 
  `'fid'`
  : Defines whether to provide text output. The default value is determined
    by the `fid` preference stored in [swpref]. The possible values are:
    * `0`   No text output is generated.
    * `1`   Text output in the MATLAB Command Window.
    * `fid` File ID provided by the `fopen` command, the output is written
            into the opened file stream.
 
  `'tid'`
  : Determines if the elapsed and required time for the calculation is
    displayed. The default value is determined by the `tid` preference
    stored in [swpref]. The following values are allowed (for more details
    see [sw_timeit]):
    * `0` No timing is executed.
    * `1` Display the timing in the Command Window.
    * `2` Show the timing in a separat pup-up window.
 
  ### Output Arguments
 
  `spectra`
  : structure, with the following fields:
    * `omega`   Calculated spin wave dispersion with dimensions of
                $[n_{mode}\times n_{Q}]$.
    * `Sab`     Dynamical structure factor with dimensins of
                $[3\times 3\times n_{mode}\times n_{Q}]$. Each
                `(:,:,i,j)` submatrix contains the 9 correlation functions
                $S^{xx}$, $S^{xy}$, $S^{xz}$, etc. If given, magnetic form
                factor is included. Intensity is in \\hbar units, normalized
                to the crystallographic unit cell.
    * `Sperp`   The component of `Sab` perpendicular to $Q$, which neutron
                scattering measures. This is outputed *instead* of `Sab`
                if the `'neutron_output', true` is specified.
    * `H`       Quadratic form of the Hamiltonian. Only saved if `saveH` is
                true.
    * `V`       Transformation matrix from the normal magnon modes to the
                magnons localized on spins using the following:
                $x_i = \sum_j V_{ij} \times x_j'$
                Only saved if `saveV` is true.
    * `Sabp`    Dynamical structure factor in the rotating frame,
                dimensions are $[3\times 3\times n_{mode}\times n_{Q}]$,
                but the number of modes are equal to twice the number of
                magnetic atoms.
    * `hkl`     Contains the input $Q$ values, dimensions are $[3\times n_{Q}]$.
    * `hklA`    Same $Q$ values, but in $\\ang^{-1}$ unit, in the
                lab coordinate system, dimensins are $[3\times n_{Q}]$.
    * `formfact`Logical value, whether the form factor has been included in
                the spin-spin correlation function.
    * `incomm`  Logical value, tells whether the calculated spectra is
                incommensurate or not.
    * `helical` Logical value, whether the magnetic structure is a helix
                i.e. whether 2*k is non-integer.
    * `norm`    Logical value, is always false.
    * `nformula`Number of formula units in the unit cell that have been
                used to scale Sab, as given in spinw.unit.nformula.
    * `param`   Struct containing input parameters, each corresponds to the
                input parameter of the same name:
                * `notwin`
                * `sortMode`
                * `tol`
                * `omega_tol`
                * `hermit`
    * `title`   Character array, the title for the output spinwave, default
                is 'Numerical LSWT spectrum'
    * `gtensor` Logical value, whether a g-tensor has been included in the
                calculation.
    * `obj`     The copy (clone) of the input `obj`, see [spinw.copy].
    * `datestart`Character array, start date and time of the calculation
    * `dateend` Character array, end date and time of the calculation
 
  The number of magnetic modes (labeled by `nMode`) for commensurate
  structures is double the number of magnetic atoms in the magnetic cell.
  For incommensurate structures this number is tripled due to the
  appearance of the $(Q\pm k_m)$ Fourier components in the correlation
  functions. For every $Q$ points in the following order:
  $(Q-k_m,Q,Q+k_m)$.
 
  If several twins exist in the sample, `omega` and `Sab` are packaged into
  a cell, that contains $n_{twin}$ number of matrices.
 
  ### See Also
 
  [spinw] \| [spinw.spinwavesym] \| [sw_mex] \| [spinw.powspec] \| [sortmode]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('spinwave')), 1)
        return m.spinwave(self.handle, *args, nargout=nout)

    def spinwavesym(self, *args, **kwargs):
        """
  calculates symbolic spin wave dispersion
  
  ### Syntax
  
  `spectra = spinwavesym(obj,Name,Value)`
  
  ### Description
  
  `spectra = spinwavesym(obj,Name,Value)` calculates symbolic spin wave
  dispersion as a function of $Q$. The function can deal with arbitrary
  magnetic structure and magnetic interactions as well as single ion
  anisotropy and magnetic field. Biquadratic exchange interactions are also
  implemented, however only for $k=0$ magnetic structures.
  
  If the magnetic propagation vector is non-integer, the dispersion is
  calculated using a coordinate system rotating from cell to cell. In this
  case the Hamiltonian has to fulfill this extra rotational symmetry.
   
  The method works for incommensurate structures, however the calculated
  omega dispersion does not contain the $\omega(\mathbf{k}\pm \mathbf{k}_m)$ terms that has to be
  added manually.
   
  The method for matrix diagonalization is according to R.M. White, PR 139
  (1965) A450. The non-Hermitian g*H matrix will be diagonalised.
   
  ### Examples
 
  The first section of the example calculates the symbolic spin wave
  spectrum. Unfortunatelly the symbolic expression needs manipulations to
  bring it to readable form. To check the solution, the second section
  converts the symbolic expression into a numerical vector and the third
  section plots the real and imaginary part of the solution.
 
  ```
  >>tri = sw_model('triAF',1)
  >>tri.symbolic(true)
  >>tri.genmagstr('mode','direct','k',[1/3 1/3 0],'S',[1 0 0])
  >>symSpec = tri.spinwave
  >>pretty(symSpec.omega)>>
  >>J_1 = 1
  >>h = linspace(0,1,500)
  >>k = h
  >>omega = eval(symSpec.omega)
  >>p1 = plot(h,real(omega(1,:)),'k-')
  >>hold on
  >>plot(h,real(omega(2,:)),'k-')
  >>p2 = plot(h,imag(omega(1,:)),'r-')
  >>plot(h,imag(omega(2,:)),'r-')
  >>xlabel('Momentum (h,h,0) (r.l.u.)')
  >>ylabel('Energy (meV)')
  >>legend([p1 p2],'Real(\omega(Q))','Imag(\omega(Q))')
  >>title('Spin wave dispersion of the TLHAF')
  >>snapnow
  ```
 
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  ### Name-Value Pair Arguments
  
  `'hkl'`
  : Symbolic definition of $Q$ vector. Default is the general $Q$
    point:
    ```
    hkl = [sym('h') sym('k') sym('l')]
    ```
  
  `'eig'`
  : If true the symbolic Hamiltonian is diagonalised symbolically. For
    large matrices (many magnetic atom per unit cell) this might be
    impossible. Set `eig` to `false` to output only the quadratic
    Hamiltonian. Default is `true`.
  
  `'vect'`
  : If `true` the eigenvectors are also calculated. Default is `false`.
  
  `'tol'`
  : Tolerance of the incommensurability of the magnetic
    ordering wavevector. Deviations from integer values of the
    ordering wavevector smaller than the tolerance are
    considered to be commensurate. Default value is $10^{-4}$.
  
  `'norm'`
  : Whether to produce the normalized symbolic eigenvectors. It can be
    impossible for large matrices, in that case set it to
    `false`. Default is `true`.
  
  `'fid'`
  : Defines whether to provide text output. The default value is determined
    by the `fid` preference stored in [swpref]. The possible values are:
    * `0`   No text output is generated.
    * `1`   Text output in the MATLAB Command Window.
    * `fid` File ID provided by the `fopen` command, the output is written
            into the opened file stream.
 
  `'title'`
  : Gives a title string to the simulation that is saved in the
    output.
 
  ### Output Arguments
 
  `spectra`
  : Structure, with the following fields:
    * `omega`   Calculated spin wave dispersion, dimensins are
                $[2*n_{magExt}\times n_{hkl}]$, where $n_{magExt}$ is the number of magnetic
                atoms in the extended unit cell.
    * `V0`      Eigenvectors of the quadratic Hamiltonian.
    * `V`       Normalized eigenvectors of the quadratic Hamiltonian.
    * `ham`     Symbolic matrix of the Hamiltonian.
    * `incomm`  Whether the spectra calculated is incommensurate or not.
    * `obj`     The clone of the input `obj`.
 
  ### See Also
 
  [spinw] \| [spinw.spinwave]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('spinwavesym')), 1)
        return m.spinwavesym(self.handle, *args, nargout=nout)

    def struct(self, *args, **kwargs):
        """
  converts properties into struct
  
  ### Syntax
  
  `objS = struct(obj)`
  
  ### Description
  
  `objS = struct(obj)` converts all public properties of `obj` and saves
  them into `objS` struct.
  
  ### See Also
  
  [spinw] \| [spinw.copy]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('struct')), 1)
        return m.struct(self.handle, *args, nargout=nout)

    def structfact(self, *args, **kwargs):
        """
  calculates magnetic and nuclear structure factor
  
  ### Syntax
  
  `sFact   = structfact(obj, kGrid,Name,Value)`
 
  `sfTable = structfact(obj, kGrid,Name,Value)`
 
  ### Description
  
  `sFact   = structfact(obj, kGrid,Name,Value)` returns the calculated
  structure factors in units of barn. Magnetic structures (FM, AFM and
  helical) are checked against
  [FullProf](<a href="matlab:web https://www.ill.eu/sites/fullprof/">https://www.ill.eu/sites/fullprof/</a>). The structure factor
  includes the site occupancy and Debye-Waller factors calculated from
  `obj.unit_cell.biso`, using the same definition as in FullProf.
  
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  `kGrid`
  : Defines the reciprocal lattice vectors where the structure
       factor is to be calculated. For commensurate structures these
       are the possible positions of the magnetic Bragg peaks. For
       incommensurate helical/conical structures 3 Bragg peaks
       positions are possible: $(\mathbf{k}-\mathbf{k}_m,\mathbf{k},\mathbf{k}+\mathbf{k}_m) around every reciprocal
       lattice vector. In this case still the integer positions have
       to be given and the code calculates the intensities at all
       three points.
  
  ### Name-Value Pair Arguments
  
  `'mode'`
  : String, defines the type of calculation:
    * `mag`     Magnetic structure factor and intensities for
                unpolarised neutron scattering.
    * `nucn`    Nuclear structure factor and neutron scattering
                intensities.
    * `nucx`    X-ray scattering structure factor and
                intensities.
  
  `'sortq'`
  : Sorting the reflections according to increasing momentum
    value if `true`. Default is `false`.
  
  `'formfact'`
  : If true, the magnetic form factor is included in the structure factor
    calculation. The form factor coefficients are stored in
    `obj.unit_cell.ff(1,:,atomIndex)`. Default value is `false`.
 
  `'formfactfun'`
  : Function that calculates the magnetic form factor for given $Q$ value.
    value. Default value is `@sw_mff`, that uses a tabulated coefficients
    for the form factor calculation. For anisotropic form factors a user
    defined function can be written that has the following header:
    ```
    F = formfactfun(atomLabel,Q)
    ```
    where the parameters are:
    * `F`           row vector containing the form factor for every input 
                    $Q$ value
    * `atomLabel`   string, label of the selected magnetic atom
    * `Q`           matrix with dimensions of $[3\times n_Q]$, where each
                    column contains a $Q$ vector in $\\ang^{-1}$ units.
 
  `'gtensor'`
  : If true, the g-tensor will be included in the structure factor
    calculation. Including anisotropic g-tensor or different
    g-tensor for different ions is only possible here.
 
  `'lambda'`
  : Wavelength. If given, the $2\theta$ value for each reflection
    is calculated.
  
  `'dmin'`
  : Minimum $d$-value of a reflection, all higher order
    reflections will be removed from the results.
  
  `'output'`
  : String, defines the type of the output:
    * `struct`  Results are returned in a struct type variable,
                default.
    * `table`   Results are returned in a table type output for
                easy viewing and exporting.
  
  `'tol'`
  : Tolerance of the incommensurability of the magnetic
    ordering wavevector. Deviations from integer values of the
    ordering wavevector smaller than the tolerance are considered
    to be commensurate. Default value is $10^{-4}$.
  
  `'fitmode'`
  : Speed up the calculation for fitting mode (omitting
    cloning the [spinw] object into the output). Default is `false`.
  
  `'fid'`
  : Defines whether to provide text output. The default value is determined
    by the `fid` preference stored in [swpref]. The possible values are:
    * `0`   No text output is generated.
    * `1`   Text output in the MATLAB Command Window.
    * `fid` File ID provided by the `fopen` command, the output is written
            into the opened file stream.
 
  ### Output Arguments
  
  `sFact`
  : Structure with the following fields:
     * `F2`     Magnetic structure factor in a matrix with dimensions
                $[3\times n_{hkl}]$.
     * `Mk`     Square of the 3 dimensional magnetic structure factor,
                dimensions are:
                $[n_{ext}(1)\cdot f_{ext}(1)\times n_{ext}(2)\cdot f_{ext}(2)\times n_{ext}(3)\cdot f_{ext}(3)]$,
                where $n_{ext}$ is the size of the extended unit cell.
     * `hkl`    Contains the input $Q$ values in a matrix with dimensins of $[3\times n_{hkl}]$.
     * `hklA`   Same as `hkl`, but in \\ang$^{-1}$ units in the
                $xyz$ Cartesian coordinate system.
     * `incomm` Whether the spectra calculated is incommensurate or not.
     * `formfact` Cell containing the labels of the magnetic ions if form
                factor in included in the spin-spin correlation function.
     * `{tth}`  $2\theta$ value of the reflection for the given wavelength,
                only given if a wavelength is provided.
     * `obj`    Clone of the input `obj` object.
 
  `sfTable`
  : Table, optional output for quick viewing and saving the output into a
    text file.
  
  ### See Also
  
  [sw_qgrid] \| [sw_plotsf] \| [sw_intsf] \| [spinw.anneal] \| [spinw.genmagstr]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('structfact')), 1)
        return m.structfact(self.handle, *args, nargout=nout)

    def symbolic(self, *args, **kwargs):
        """
  switches between symbolic/numeric mode
  
  ### Syntax
  
  `symb = symbolic(obj)`
 
  `symbolic(obj, symb)`
  
  ### Description
  
  `symb = symbolic(obj)` returns `true` if symbolic calculation mode is on,
  `false` for numeric mode.
   
  `symbolic(obj, symb)` sets whether the calculations are in
  symbolic/numeric (`true`/`false`) mode. Switching to symbolic mode, the
  spin values, matrix elements, magnetic field, magnetic structure and
  physical units are converted into symbolic variables. If this is not
  desired, start with a symbolic mode from the beggining and have full
  control over the values of the above mentioned variables.
  
  ### See Also
  
  [spinw] \| [spinw.spinwavesym]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('symbolic')), 1)
        return m.symbolic(self.handle, *args, nargout=nout)

    def symmetry(self, *args, **kwargs):
        """
  returns whether symmetry is defined
  
  ### Syntax
  
  `sym = symmetry(obj)`
  
  ### Description
  
  `sym = symmetry(obj)` returns `true` if equivalent couplings are
  generated based on the crystal space group and all matrices (interaction,
  anisotropy and g-tensor) are transformed according to the symmetry
  operators. If `false`, equivalent couplings are generated based on bond
  length, equivalent matrices won't be transformed (all identical).
   
  To switch between the two behaviour use [spinw.gencoupling] with the
  `forceNoSym` parameter set to `true`. To remove all symmetry operators
  use [spinw.nosym].
  
  ### See Also
  
  [spinw] \| [spinw.nosym] \| [spinw.gencoupling]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('symmetry')), 1)
        return m.symmetry(self.handle, *args, nargout=nout)

    def symop(self, *args, **kwargs):
        """
  generates the bond symmetry operators
  
  ### Syntax
  
  `op = symop(obj)`
  
  ### Description
  
  `op = symop(obj)` generates the rotation matrices that transform single
  ion anisotropy, g-tensor and exchange interaction matrices between
  symmetry equivalent positions (on atoms or bond centers). The results are
  cached.
  
  ### See Also
  
  [spinw.intmatrix]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('symop')), 1)
        return m.symop(self.handle, *args, nargout=nout)

    def table(self, *args, **kwargs):
        """
  outputs easy to read tables of internal data
  
  ### Syntax
  
  `T = table(obj,type,{index},{showval})`
  
  ### Description
  
  `T = table(obj,type,{index},{showval})` returns a table that shows in an
  easy to read/export format different internal data, such as magnetic atom
  list, bond list, magnetic structure, etc.
   
  For the matrix labels in the list of bonds, the '>>' sign means that the
  matrix value is determined using the bond symmetry operators.
   
  {{note The `table` data type is only supported in Matlab R2013b or newer.
  When running older versions of Matlab, `<strong>spinw/table</strong>` returns a struct.}}
  
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  `type`
  : String, determines the type of data to show, possible values are:
    * `'matom'`     properties of magnetic atoms in the unit cell,
    * `'matrix'`    list of matrices,
    * `'ion'`       single ion term in the Hamiltonian,
    * `'bond'`      properties of selected bonds,
    * `'mag'`       magnetic structure.
  
  `index`
  : Indexing into the type of data to show, its meaning depends on the
    `type` parameter. For `'bond'` indexes the bonds (1 for first
    neighbors, etc.), if empty all bonds will be shown. For `'mag'` it
    indexes the propagation vectors, the magnetization of the selected
    propagation vector will be shown. Default value is 1, if empty vector `[]` is given, all
    bonds/propagation vector will be shown.
  
  `showVal`
  : If `true`, also the values of the single ion and exchange matrices
    will be shown. The values shown  are the symmetry transformed exchange
    values after the symmetry operations (if there is any). Default value
    is `false`.
  
  ### Output Arguments
  
  `T`
  : Matlab `table` type object.


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('table')), 1)
        return m.table(self.handle, *args, nargout=nout)

    def temperature(self, *args, **kwargs):
        """
  get/set temperature
  
  ### Syntax
  
  `temperature(obj, T)`
 
  `T = temperature(obj)`
  
  ### Description
  
  `temperature(obj, T)` sets the temperature stored in `obj` to `T`, where
  `T` is scalar. The units of temerature is determined by the
  `spinw.unit.kB` value, default unit is Kelvin.
   
  `T = temperature(obj)` returns the current temperature value stored in
  `obj`.


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('temperature')), 1)
        return m.temperature(self.handle, *args, nargout=nout)

    def twinq(self, *args, **kwargs):
        """
  calculates equivalent Q point in twins
  
  ### Syntax
  
  `[qTwin, rotQ] = twinq(obj, {Q0})`
  
  ### Description
  
  `[qTwin, rotQ] = twinq(obj, {q0})` calculates the $Q$ values in the twin
  coordinate systems, in rlu. It also returns the rotation matrices, that
  transforms the $Q$ point from the original lattice to the selected twin
  rlu coordinate system.
  
  ### Examples
  
  This example Calculates the $[1,0,0]$ and $[1,1,0]$ Bragg reflections
  equivalent positions in the twins.
 
  ```
  Q1 = [1 0 0; 1 1 0];
  Q2 = cryst.twinq(Q1');
  ```
  
  ### Input Arguments
  
  `Q0`
  : $Q$ values in the original crystal in rlu sotred in a matrix with
  dimensions of $[3\times n_Q]$, optional.
  
  ### Output Arguments
  
  `Qtwin`
  : $Q$ values in the twin oordinate system in a cell element for
            each twin.
 
  `rotQ`
  : Rotation matrices with dimensions of $[3\times 3\times n_{twin}]$.
  
  ### See Also
  
  [spinw] \| [spinw.addtwin]
 
  *[rlu]: Reciprocal Lattice Unit


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('twinq')), 1)
        return m.twinq(self.handle, *args, nargout=nout)

    def unitcell(self, *args, **kwargs):
        """
  returns unit cell data
  
  ### Syntax
  
  `cellInfo = unitcell(obj, idx)`
  
  ### Description
  
  `cellInfo = unitcell(obj, idx)` returns information on symmetry
  inequivalent atoms and allowing to subselect certain atoms using the
  `idx` index vector.
  
  ### Examples
  
  The example keeps only the first and third symmetry inequivalent atoms in
  `cryst` object.
  ```
  cryst.unit_cell = unitcell(cryst,[1 3]);
  ```
  The example keeps only the atoms with labels `'O'` (Oxygen) atoms in
  `cryst` object.
  ```
  cryst.unit_cell = unitcell(cryst,'O');
  ```
  
  ### Input Arguments
  
  `obj`
  : [spinw] object.
  
  `idx`
  : Selects certain atoms. If undefined `unit_cell(obj)` or
       `obj.unit_cell` returns information on all atoms. The selection
       can be also done according to the atom labels, in this case
       either a string of the label or cell of strings for several
       labels can be given.
  
  ### Output Arguments
  
  `cellInfo`
  : Structure that contains all the fields of [spinw.unit_cell].
  
  ### See Also
  
  [spinw.addtwin] \| [spinw.twinq] \| [spinw.unit_cell]


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('unitcell')), 1)
        return m.unitcell(self.handle, *args, nargout=nout)

    def validate(self, *args, **kwargs):
        """
  validates spinw object properties
 
  <strong>validate</strong>(obj, {fieldToValidate})


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(0, get_nlhs('validate')), 1)
        return m.validate(self.handle, *args, nargout=nout)

    def vararginnames(self, *args, **kwargs):
        """
SPINW/<strong>vararginnames</strong> is an undocumented builtin function.


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('vararginnames')), 1)
        return m.vararginnames(self.handle, *args, nargout=nout)

    def version(self, *args, **kwargs):
        """
  returns the version of SpinW
 
  ### Syntax
 
  `verInfo = version(obj)`


        """
        
        args += sum(kwargs.items(), ())
        nout = max(min(1, get_nlhs('version')), 1)
        return m.version(self.handle, *args, nargout=nout)

