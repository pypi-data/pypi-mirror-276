# Copyright 2024 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import numpy as np
import datetime
import typing
import re
from cegalprizm.pythontool.exceptions import PythonToolException, UserErrorException
from cegalprizm.pythontool.template import Template, DiscreteTemplate

CPY3 = 'cpy3'


def python_env():
    return CPY3


def iterable_values(arr):
    return arr.flat


def clone_array(arr: np.ndarray) -> np.ndarray:
    return arr.copy()


def to_backing_arraytype(nparray):
    ''' Creates and returns a .NET Array that mirrors the provided numpy array

    @nparray: numpy array

    @Returns: .NET Array with element type matching nparray.dtype and identical dimensions with content that matches the provided numpy array
    '''
    return nparray

######################## Conversions from .NET ###########################

def from_backing_arraytype(src):
    ''' Creates and returns a numpy Array that mirrors the provided .NET array

    @src: .NET Array in in-process mode and a protobuf type in out-of-process mode

    @Returns: numpy Array with dtype matching src's element type, and identical dimensions with content that matches the provided .NET Array
    '''
    return src

def _to_shaped_ndarray(val, size_i, size_j, size_k, np_type, spanning_dims = 'ijk'):
    if isinstance(size_i, int):
        size_i = (size_i, size_i+1)
    if isinstance(size_j, int):
        size_j = (size_j, size_j+1)
    if isinstance(size_k, int):
        size_k = (size_k, size_k+1)
    if isinstance(val, list):
        val = np.array(val, dtype=np_type)

    if not hasattr(val, "__len__"):
        val_ndarray = np.empty(size_k, dtype = np_type)
        val_ndarray.fill(val)        
    else:
        val_ndarray = val
    
    if spanning_dims == 'ij':
        di, dj = size_i[1]-size_i[0], size_j[1] - size_j[0]
        val_ndarray.shape = (di, dj)
    elif spanning_dims == 'k':
        dk = size_k[1]-size_k[0]
        val_ndarray.shape = (dk)
    else:
        di, dj, dk = size_i[1]-size_i[0], size_j[1] - size_j[0], size_k[1]-size_k[0]
        val_ndarray.shape = (di, dj, dk)
            
    return val_ndarray.astype(np_type, copy = False, subok = True)

###################

def _ensure_1d_array(val, i, np_typ, net_typ, convert):
    if isinstance(val, np.ndarray):
        return val.astype(dtype=np_typ, copy=False)
    elif isinstance(val, list):
        if len(val) > i:
            raise ValueError("too many values")
        array = np.empty((i), np_typ)
        for index in range(0, i):
            array[index] = convert(val[index])
        return array

    raise ValueError("Cannot convert %s into 1d array" % val)

def ensure_1d_float_array(val, i):
    """Converts a flat list into a Array[float] if necessary"""
    return _to_shaped_ndarray(val, 1, 1, (0, i), np.float32, spanning_dims = 'k')

def ensure_1d_int_array(val, i):
    """Converts a flat list into a Array[int] if necessary"""
    return _to_shaped_ndarray(val, 1, 1, (0, i), np.int32, spanning_dims = 'k')

def ensure_2d_float_array(val, i, j):
    """Converts a flat or nested list into a Array[float]
    if necessary"""
    return _to_shaped_ndarray(val, (0, i), (0, j), 1, np.float32, spanning_dims = 'ij')

def ensure_2d_int_array(val, i, j):
    """Converts a flat or nested list into a Array[float]
    if necessary"""
    return _to_shaped_ndarray(val, (0, i), (0, j), 1, np.int32, spanning_dims = 'ij')

def ensure_3d_float_array(val, i, j, k):
    return _to_shaped_ndarray(val, (0, i), (0, j), (0, k), np.float32)

def ensure_3d_int_array(val, i, j, k):
    return _to_shaped_ndarray(val, (0, i), (0, j), (0, k), np.int32)

def str_has_content(s: typing.Optional[str]) -> bool:
    """Returns False if the string is None, empty, or just whitespace"""
    if s is None:
        return False
    return bool(s.strip())

def str_or_none(s: typing.Optional[str]) -> typing.Optional[str]:
    if not str_has_content(s):
        return None
    return s

def about_equal(a, b):
    return abs(a-b) < 0.0000001

def floatarray(lst):
    return ensure_1d_float_array(lst, len(lst))

def intarray(lst):
    return ensure_1d_int_array(lst, len(lst))

def to_python_datetime(dt: typing.Union[typing.Any, datetime.datetime]) -> datetime.datetime:
    if isinstance(dt, datetime.datetime):
        return dt
    else:
        raise ValueError("Argument was expected to be a datetime.datetime object, got {}".format(dt))

def from_python_datetime(dt):
    return dt

def native_accessor(accessor):
    if not isinstance(accessor, tuple):
        raise TypeError("accessor is not tuple")
    return accessor

## Get object from iterable collection
def get_item_from_collection_petrel_name(collection: typing.Iterable, key):
    if isinstance(key, int):
        return collection[key]
    elif isinstance(key, str):
        result = [x for x in collection if x.petrel_name == key]
        if(len(result) == 0):
            return None
        elif len(result) == 1:
            return result[0]
        else:
            return result
        
## Check and Get wells for wells_filter
def get_wells(well = None, wells_filter = None):
    check_wells(well, wells_filter)
    if well is None and wells_filter is None:
        return []
    if wells_filter is not None:
        return wells_filter
    if well is not None:
        return [well]

def check_well(well):
    from cegalprizm.pythontool.borehole import Well
    if well is not None:
        if not isinstance(well, Well):
            raise ValueError("Each well input must be a Well object as returned from petrelconnection.wells")
        
def check_wells(well = None, wells_filter = None):
    if well is None and wells_filter is None:
        return
    if wells_filter is not None:
        if not isinstance(wells_filter, list):
            raise TypeError("wells_filter must be a list of Well objects as returned from petrelconnection.wells")
        for well in wells_filter:
            check_well(well)
    if well is not None:
        check_well(well)

# Unit header is on the form "{name} [{unit}]"
unit_header_regex = r"(?P<objectname>.+)(?P<unit>\[.+\]|\[\])$"
def to_unit_header(name, unit):
    header = name + ' [' + unit + ']'
    if not is_valid_unit_header(header):
        raise ValueError("\"" + header + "\" is not a valid unit header")
    return header

def name_from_unit_header(header):
    if is_valid_unit_header(header):
        return re.search(unit_header_regex, header).group(1).rstrip()

def unit_from_unit_header(header):
    unit_with_brackets = re.search(unit_header_regex, header).group(2)
    return str(unit_with_brackets)[1:-1]

def is_valid_unit_header(header):
    return re.fullmatch(unit_header_regex, header) is not None

## IJK

def check_extent_2d(extent, indices):
        for i_, j_ in zip(*indices[:2]):
            if i_ < 0 or j_ < 0 :
                raise PythonToolException("Index cannot be less than zero")
            if i_ >= extent.i or j_ >= extent.j:
                raise PythonToolException("Index cannot be greater than object extent")

def check_extent_3d(extent, indices):
     for i_, j_, k_ in zip(*indices):
            if i_ < 0 or j_ < 0 or k_ < 0:
                raise PythonToolException("Index cannot be less than zero")
            if i_ >= extent.i or j_ >= extent.j or k_ >= extent.k:
                raise PythonToolException("Index cannot be greater than object extent")
            
def ijks_to_positions(
            extent,
            object_link, 
            indices: typing.Tuple[typing.List[float], typing.List[float], typing.List[float]],
            dimensions: int)\
            -> typing.Tuple[typing.List[float], typing.List[float], typing.List[float]]:
    if dimensions == 3:
        check_extent_3d(extent, indices)
        [i, j, k] = indices
    elif dimensions == 2:
        check_extent_2d(extent, indices)
        [i, j] = indices[:2]
    else: 
        raise PythonToolException("ijks_to_positions called with unsupported number of dimensions")
    
    lst_x = []
    lst_y = []
    lst_z = []
    n = 1000
    for i_ in range(0, len(i), n):
        if dimensions == 3:
            data = object_link.GetPositions(i[i_:i_+n], j[i_:i_+n], k[i_:i_+n])
        elif dimensions == 2:
            data = object_link.GetPositions(i[i_:i_+n], j[i_:i_+n])
        lst_x.append(data[0])
        lst_y.append(data[1])
        lst_z.append(data[2])

    d = ([i for i_s in lst_x for i in i_s ], 
        [j for j_s in lst_y for j in j_s ], 
        [k for k_s in lst_z for k in k_s ])
    return d

def positions_to_ijks_2d(
        object_link,
        positions: typing.Union[typing.Tuple[typing.List[float], typing.List[float]], typing.Tuple[typing.List[float], typing.List[float], typing.List[float]]])\
        -> typing.Tuple[typing.List[int], typing.List[int]]:
    if len(positions) == 2:
        positions = typing.cast(typing.Tuple[typing.List[float], typing.List[float]], positions)
        [x, y] = positions
    elif len(positions) == 3:
        positions = typing.cast(typing.Tuple[typing.List[float], typing.List[float], typing.List[float]], positions)
        [x, y, _] = positions
    lst_is = []
    lst_js = []
    n = 1000
    for i in range(0, len(x), n):
        data = object_link.GetIjk(x[i:i+n], y[i:i+n])
        lst_is.append(data[0])
        lst_js.append(data[1])
    d = ([int(round(i)) for i_s in lst_is for i in i_s ], 
        [int(round(j)) for js in lst_js for j in js ])
    return d

def positions_to_ijks_3d(
            object_link, 
            positions: typing.Tuple[typing.List[float], typing.List[float], typing.List[float]])\
            -> typing.Tuple[typing.List[int], typing.List[int], typing.List[int]]:            
        [x, y, z] = positions
        lst_is = []
        lst_js = []
        lst_ks = []
        n = 1000
        for i in range(0, len(x), n):
            data = object_link.GetIjk(x[i:i+n], y[i:i+n], z[i:i+n])
            lst_is.append(data[0])
            lst_js.append(data[1])
            lst_ks.append(data[2])
        d = ([int(round(i)) for i_s in lst_is for i in i_s ], 
            [int(round(j)) for js in lst_js for j in js ], 
            [int(round(k)) for ks in lst_ks for k in ks ])
        return d

def ijks_doc_decorator_2d(func):
    func.__doc__ = ijks_docstring_2d()
    return func

def ijks_docstring_2d() ->  str:
    return """Converts a list with i and j indices to xyz.

        Args:
            indices: A tuple([i],[j]) where [i] is a list of i indices
              and [j] is a list of j indices.

        Returns:
            A tuple([x],[y],[z]) where [x] is a list of x coordinates, 
             [y] is a list of y coordinates and [z] is a list of z coordinates.
        """ 

def ijks_doc_decorator_3d(func):
    func.__doc__ = ijks_docstring_3d()
    return func

def ijks_docstring_3d() -> str:
    return """Converts a tuple with ijk indices to xyz.

        Args:
            indices: A tuple([i],[j],[k]) where [i] is a list of i indices, [j] is a list of j indices
                and [k] is a list of k indices.

        Returns:
            A tuple([x], [y], [z]), where [x] is a list of x coordinates, 
                [y] is a list of y positions and [z] is a list of z (time/depth) coordinates.
        """

def positions_doc_decorator_2d(func):
    func.__doc__ = positions_docstring_2d()
    return func

def positions_docstring_2d() -> str:
    return """Converts a list of xyzs to ijk

        Args:
            positions: A tuple([x],[y]) where [x] is a list of x coordinates 
              and [y] is a list of y coordinates.

        Returns:
            A tuple([i],[j]) where [i] is a list of i indices
              and [j] is a list of j indices.
        """ 

def positions_doc_decorator_3d(func):
    func.__doc__ = positions_docstring_3d()
    return func

def positions_docstring_3d() -> str:
    return """Converts a tuple with xyzs to ijk.

        Args:
            positions: A tuple([x], [y], [z]), where [x] is a list of x coordinates, 
                [y] is a list of y positions and [z] is a list of z (time/depth) coordinates.
            
        Returns:
            A tuple([i],[j],[k]) where [i] is a list of i indices, [j] is a list of j indices
                and [k] is a list of k indices.
        """

def verify_continuous_clone(copy_values, template):
    if (copy_values and not template == None):
        raise UserErrorException('Cannot clone with template if copy_values=True')
    if (not (template == None) and not isinstance(template, Template)):
        raise UserErrorException('The template argument must be a Template object')
        
def verify_discrete_clone(copy_values, discrete_template):
    if (copy_values and not discrete_template == None):
        raise UserErrorException('Cannot clone with discrete_template if copy_values=True')
    if (not (discrete_template == None) and not isinstance(discrete_template, DiscreteTemplate)):
        raise UserErrorException('The discrete_template argument must be a DiscreteTemplate object')

def verify_clone_name(name_of_clone):
    if not name_of_clone or '/' in name_of_clone:
        raise ValueError('Name of clone cannot be empty or None or contain slashes')

def get_template_docstring() -> str:
    return """Returns the Petrel template for the object as a Template or DiscreteTemplate object"""

def get_template_decorator(func):
    func.__doc__ = get_template_docstring()
    return func
