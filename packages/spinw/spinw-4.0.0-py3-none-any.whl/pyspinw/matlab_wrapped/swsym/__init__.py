import pyspinw
m = pyspinw.Matlab()


def point(symOp=None, r=None, **kwargs):
    """
% determines local point group symmetry in a space group
%
% ### Syntax
%
% `pOp = swsym.point(symOp, r)`
%
% ### Description
%
% `pOp = swsym.point(symOp, r)` determines the point group symmetry at a
% given position in the unit cell in a given space group. It returns all the
% rotation matrices of the point group.
%
% ### Input Arguments
%
% `symOp`
% : Symmetry operators of the space group stored in a matrix
%   with dimensions of $[3\times 4\times n_{op}]$.
%
% `r`
% : Column vector with 3 elements, position in the unit cell.
%
% ### Output Arguments
%
% `pOp`
% : Point group operators in a matrix with dimensions of $[3\times 3\times
%   n_{op}]$, the operators act on the relative atomic positions. To
%   convert these rotation operators to Cartesian coordinate system, use:
%
%   ```
%   R = BV*pOp(:,:,i)*inv(BV)
%   ```
%   where `BV` is the matrix of lattice basis vectors, see
%   [spinw.basisvector].
%
% ### See Also
%
% [swsym.generator] \| [swsym.operator] \| [swsym.position]
%
    """
    args = tuple(v for v in [symOp, r] if v is not None)
    return m.swsym.point(*args, **kwargs)


def isop(symOp=None, **kwargs):
    """
% determines if a matrix is symmetry operator
%
% ### Syntax
%
% `result = swsym.isop(op)`
%
% ### Description
%
% `result = swsym.isop(op)` determines whether the given matrix has
% dimensions that is compatible with the size requirements of space group
% operators. The given `op` matrix has to have dimensions of $[3\times
% 4\times n_{op}]$. The function returns `true` only if the input has these
% dimensions.
%
% ### See Also
%
% [swsym.generator] \| [swsym.operator]
%
    """
    args = tuple(v for v in [symOp] if v is not None)
    return m.swsym.isop(*args, **kwargs)


def genreduce(symOp=None, **kwargs):
    """
% reduces symmetry operators to the generators
%
% ### Syntax
%
% `[symOpG, isGen] = swsym.genreduce(symOp)`
%
% ### Description
%
% `[symOpG, isGen] = swsym.genreduce(symOp)` takes the list of symmetry
% operators in `symOp` and determines a minimum subset of operators that
% can generate the given list.
%
% ### Input Arguments
%
% `symOp`
% : Matrix that contains both the rotation and translation matrices
%   having dimensions of $[3\times 4\times n_{sym}]$, where the
%   `symMat(:,4,:)` stores the translation vectors, while the
%   `symMat(:,1:3,:)` stores the $3\times 3$ rotation matrices.
%
% ### Output Arguments
%
% `symOpG`
% : A set of operators, that can generate all the operators of the input.
%
% `isGen`
% : Vector, that gives whether a given input operator is part of
%   the generators, dimensions are $[1\times n_{sym}]$.
%
% ### See Also
%
% [swsym.add] \| [swsym.generator] \| [swsym.operator]
%
    """
    args = tuple(v for v in [symOp] if v is not None)
    return m.swsym.genreduce(*args, **kwargs)


def generator(sym=None, fid0=None, **kwargs):
    """
% returns symmetry operators of a given space group
%
% ### Syntax
%
% `[symOp, symInfo] = swsym.generator(sym)`
%
% `[symOp, symInfo] = swsym.generator(sym,fid)`
%
% ### Description
%
% `[symOp, symInfo] = swsym.generator(sym)` gives the symmetry operators
% based on a given space group number or a string of symmetry operators.
% Without arguments, the function returns the name of all space groups
% stored in [symmetry.dat] file.
%
% `[symOp, symInfo] = swsym.generator(sym,fid)` also prints the symmetry
% operators to the file identified by `fid`.
%
% ### Input Arguments
%
% `sym`
% : Either the label of the space group or the index from
%   the [International Tables of Crystallography](http://it.iucr.org/A/) or
%   string containing the space group operators in the same format as used
%   in the [symmetry.dat] file (for details see [swsym.str]).
%
% `fid`
% : If non-zero, the symmetry operators will be printed to the file
%   identified by `fid`, the following values are valid:
%   * `0`   no printed output (default),
%   * `1`   standard output (Command Line),
%   * `fid` text file opened before using `fid = fopen(path)`.
%
% ### Output Arguments
%
% `symOp`
% : Symmetry operators in a matrix with dimensions of $[3\times 4\times
%   n_{op}]$.
%
% `symInfo`
% : Structure that contains additional information about the space
%   group with the following fields:
%   * `name`    Name of the space group, if the `swsym.generator`
%               function is called with no input, name stores the name of
%               all space groups from [symmetry.dat] file in a cell.
%   * `str`     The string of the symmetry operations.
%   * `num`     The line index in the [symmetry.dat] file.
%
% ### See Also
%
% [swsym.add] \| [spinw] \| [spinw.gencoupling] \| [swsym.position]
%
    """
    args = tuple(v for v in [sym, fid0] if v is not None)
    return m.swsym.generator(*args, **kwargs)


def position(symOp=None, r0=None, fid=None, tol=None, **kwargs):
    """
% generates symmetry equivalent positions
%
% ### Syntax
%
% `[r, aIdx, opInfo] = swsym.position(sym,r0)`
%
% `[r, aIdx, opInfo] = swsym.position(sym,r0,fid)`
%
% `[r, aIdx, opInfo] = swsym.position(sym,r0,fid,tol)`
%
% ### Description
%
% `[r, aIdx, opInfo] = swsym.position(sym, r0, fid, tol)` generates all
% symmetry equivalent atomic positions from a given space group and
% coordinates of the symmetry inequivalent atoms. If `fid` is defined, the
% result are printed onto the corresponding file.
%
% ### Input Arguments
%
% `sym`
% : Either the label of the space group or the index from
%   the [International Tables of Crystallography](http://it.iucr.org/A/) or
%   string containing the space group operators in the same format as used
%   in the [symmetry.dat] file (for details see [swsym.str]).
%
% `r0`
% : Atomic position in lattice units in a matrix with dimensions of
%   $[3\times n_{atom}]$.
%
% `fid`
% : If non-zero, the symmetry operators will be printed to the file
%   identified by `fid`, the following values are valid:
%   * `0`   no printed output (default),
%   * `1`   standard output (Command Line),
%   * `fid` text file opened before using `fid = fopen(path)`.
%
% `tol`
% : Tolerance, distance within two atoms are considered
%   identical, default value is $10^{-5}$ lattice unit. Necessary to check
%   for badly defined atomic positions (when atoms are not exactly on the
%   symmetry element) and to avoid numerical errors.
%
% ### Output Arguments
%
% `r`
% : All generated atomic positions stored in a matrix with dimensions of
%   $[3\times n_{genAtom}]$.
%
% `aIdx`
% : The index of the symmetry inequivalent position for every
%   generated position, stored in a row vector with $n_{genAtom}$ number of
%   elements.
%
% `opInfo`
% : Structure with the following fields:
%   * `ismoved`     Cell, where each element contains a vector with logical
%                   values, whether the given operator moved the atom or
%                   not. Each vector has a dimensions of $[1\times n_{sym}]$, where
%                   the $n_{sym}$ is multiplicity of the general position.
%   * `opmove`      The rotation operator that moved the original atom the
%                   equivalent position stored in a matrix with dimensions
%                   of $[3\times 3\times n_{genAtom}]$.
%
% ### See Also
%
% [swsym.operator]
%
    """
    args = tuple(v for v in [symOp, r0, fid, tol] if v is not None)
    return m.swsym.position(*args, **kwargs)


def add(symStr=None, symName=None, **kwargs):
    """
% saves user defined symmetry operators
%
% ### Syntax
%
% `sym = swsym.add(symStr)`
%
% `sym = swsym.add(symStr,symName)`
%
% ### Description
%
% `sym = swsym.add(symStr)` saves the symmetry generators in `symStr` into
% the [symmetry.dat] file and returns the line number of the space group in
% the [symmetry.dat] file.
%
% `sym = swsym.add(symStr,symName)` also assigns a label `symName` to the
% new symmetry operators (space group).
%
% ### Input Arguments
%
% `symStr`
% : String, that contains the operators of the space group. If
%   not only the generators are given, a possible set of
%   generators will be determined and only those will be saved. The format
%   of the string is described in [swsym.str].
%
% `symName`
% : Label for the space group.
%
% ### See Also
%
% [swsym.generator] \| [swsym.genreduce]
%
    """
    args = tuple(v for v in [symStr, symName] if v is not None)
    return m.swsym.add(*args, **kwargs)


def str(symOp=None, **kwargs):
    """
% generates a string equivalent of symmetry operators
%
% ### Syntax
%
% `symstr = swsym.str(symop)`
%
% ### Description
%
% `symStr = swsym.str(symOp)` generates a string equivalent of the given
% symmetry operator matrix. The string contains the operators separated by
% `;` and the $xyz$ axis transformations are separated by `,`. For example
% a valid symmetry operator is `'x,y+1/2,z+1/2'`. Translations are given as
% fractions and the `'xyz'` letters correspond to the 3 crystal axes.
%
% ### Input Arguments
%
% `symOp`
% : Symmetry operators in a matrix with dimensions of $[3\times 4\times
%   n_{op}]$, where rotations matrices are stored in `symOp(:,1:3,:)` and
%   and translation vectors in `symOp(:,4,:)`.
%
% ### Output Arguments
%
% `strSym`
% : String that contains the symmetry operations.
%
% ### See Also
%
% [swsym.add] \| [swsym.generator]
%
    """
    args = tuple(v for v in [symOp] if v is not None)
    return m.swsym.str(*args, **kwargs)


def oporder(symOp=None, **kwargs):
    """
% determine the order of the symmetry operator
%
% ### Syntax
%
% `N = swsym.oporder(symOp)`
%
% ### Description
%
% `N = swsym.oporder(symOp)` determines the order of the `symOp` symmetry
% operator, where `symOp(:,1:3)` is a rotation matrix and `symOp(:,4)` is a
% translation. The value of 10 is returned if the matrix is not a valid
% crystallographic symmetry operator.
%
% ### Examples
%
% Raising any operator to the calculated order will alway return identity:
%
% ```
% >>O = swsym.generator('y,z,x')>>
% >>R = O(:,1:3)^swsym.oporder(O)>>
% ```
%
% ### Input Arguments
%
% `symOp`
% :	Symmetry operator in a matrix with dimensions of $[3\times 4]$.
%
% ### Output Arguments
%
% `N`
% : Integer, the order of the operator.
%
% ### See Also
%
% [swsym.generator] \| [sw_basismat]
%
    """
    args = tuple(v for v in [symOp] if v is not None)
    return m.swsym.oporder(*args, **kwargs)


def bond(r=None, bv=None, bond=None, symOp=None, tol=None, **kwargs):
    """
% generates all symmetry equivalent bonds
%
% ### Syntax
%
% `[genBond, uBond] = swsym.bond(r,bv,bond,symOp)`
%
% `[genBond, uBond] = swsym.bond(r,bv,bond,symOp,tol)`
%
% ### Description
%
% `[genBond, uBond] = swsym.bond(r,bv,bond,symOp)` generates all bonds that
% are symmetry equivalent to the given `bond`. The function uses the given
% space group operators and positions of magnetic atoms to return a list of
% equivalent bonds in a matrix. The function also checks the validity of
% the calculation by measuring the length of each equivalent bond using the
% given `bv` base and if the difference in length between equivalent bonds
% is larger than the tolerance throws a warning.
%
% `[genBond, uBond] = swsym.bond(r,bv,bond,symOp,tol)` also defines the
% tolerance using `tol`.
%
% ### Input Arguments
%
% `r`
% : Positions of the magnetic atoms in lattice units stored in a matrix
%   with dimensions of $[3\times n_{magAtom}]$.
%
% `bv`
% : Basis vectors that define the lattice, used for checking the bond
%   length of equivalent bonds, see [spinw.basisvector] for details.
%
% `bond`
% : Vector that contains the starting bond with elements of
%   `[dl_a dl_b dl_c atom_1 atom_2]`, where `dl` is vector of lattice
%   translation between the two atoms if they are not in the same unit cell
%   in lattice units, `atom_1` and `atom_2` are indices of atoms in the
%   list of positions stored in `r`.
%
% `symOp`
% : Matrix, that contains the rotation and translation operators of
%   the space group with dimensions of $[3\times 4\times n_{op}]$.
%
% `tol`
% : Tolerance, default value is $10^{-5}$.
%
% ### Output Arguments
%
% `genBond`
% : Matrix, whith each column defines a bond, the meaning of each
%           row is the same as the input `bond` variable.
%
% `uBond`
% : Logical variable, `true` if all the generated bonds are unique.
%
% ### See Also
%
% [spinw.gencoupling] \| [swsym.operator] \| [swsym.position]
%
    """
    args = tuple(v for v in [r, bv, bond, symOp, tol] if v is not None)
    return m.swsym.bond(*args, **kwargs)


def operator(sym=None, fid=None, **kwargs):
    """
% generates all symmetry elements from given space group
%
% ### Syntax
%
% `[symOp, symInfo] = swsym.operator(sym)`
%
% `[symOp, symInfo] = swsym.operator(sym,fid)`
%
% ### Description
%
% `[symOp, symInfo] = swsym.operator(sym)` generates *all* symmetry
% elements from a given set of generators. It also accepts space group
% labels or space group index or string of symmetry operators.
%
% ### Input Arguments
%
% `sym`
% : Line index in the [symmetry.dat] file or string of the
%   symmetry operators or matrix of symmetry generators with dimensions of
%   $[3\times 4\times n_{op}]$. For example: `sym = 'P n m a'`.
%
% `fid`
% : If non-zero, the symmetry operators will be printed to the file
%   identified by `fid`, the following values are valid:
%   * `0`   no printed output (default),
%   * `1`   standard output (Command Line),
%   * `fid` text file opened before using `fid = fopen(path)`.
%
% ### Output Arguments
%
% `symOp`
% : All the symmetry elements in a matrix with dimensions of $[3\times
%   4\times n_{op}]$.
%
% `symInfo`
% : Structure that contains additional information about the space
%   group with the following fields:
%   * `name`    Name of the space group, if the `swsym.generator`
%               function is called with no input, name stores the name of
%               all space groups from [symmetry.dat] file in a cell.
%   * `str`     The string of the symmetry operations.
%   * `num`     The line index in the [symmetry.dat] file.
%
% ### See Also
%
% [swsym.generator]
%
    """
    args = tuple(v for v in [sym, fid] if v is not None)
    return m.swsym.operator(*args, **kwargs)


