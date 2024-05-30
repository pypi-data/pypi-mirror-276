# Copyright 2024 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.




import typing
from cegalprizm.pythontool.exceptions import PythonToolException
import math
from cegalprizm.pythontool import chunk
from cegalprizm.pythontool.petrelobject import PetrelObject
from cegalprizm.pythontool.template import Template, DiscreteTemplate
from cegalprizm.pythontool.primitives import Extent
from cegalprizm.pythontool import primitives
from cegalprizm.pythontool.chunktype import ChunkType
from cegalprizm.pythontool import _utils
import cegalprizm.pythontool

if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.grpc.horizoninterpretation_grpc import HorizonInterpretationGrpc, HorizonProperty3dGrpc, HorizonInterpretation3dGrpc


class HorizonInterpretation(PetrelObject):
    """A class holding information about a Horizon Interpretation"""
    def __init__(self, python_petrel_property: "HorizonInterpretationGrpc"):
        super(HorizonInterpretation, self).__init__(python_petrel_property)
        self._extent = None
        self._horizoninterpretation_object_link = typing.cast("HorizonInterpretationGrpc", python_petrel_property)

    @property
    def horizon_interpretation_3ds(self) -> typing.List["HorizonInterpretation3d"]:
        return [HorizonInterpretation3d(po) for po in self._horizoninterpretation_object_link.GetHorizonInterpretation3dObjects()]

    @property
    def crs_wkt(self):
        """ The PROJCS well known text representation of the object CRS.

        returns:
            string: PROJCS well known text representation of the CRS.
        """
        return "Well-known text representation of coordinate reference systems not available for HorizonInterpretation objects."

    def __str__(self) -> str:
        """A readable representation of the HorizonInterpretation3D"""
        return 'HorizonInterpretation(petrel_name="{0}")'.format(self.petrel_name)

    def clone(self, name_of_clone: str, copy_values: bool = False) -> "HorizonInterpretation":
        """ Creates a clone of the Petrel object.

        The clone is placed in the same collection as the source object.
        A clone cannot be created with the same name as an existing Petrel object in the same collection.
        
        Parameters:
            name_of_clone: Petrel name of the clone

        Returns:
            HorizonInterpretation: The clone
            
        Raises:
            Exception: If there already exists a Petrel object with the same name
            ValueError: If name_of_clone is empty or contains slashes
        """
        return typing.cast("HorizonInterpretation", self._clone(name_of_clone, copy_values = copy_values))

class HorizonProperty3d(PetrelObject):
    def __init__(self, python_petrel_property: "HorizonProperty3dGrpc"):
        super(HorizonProperty3d, self).__init__(python_petrel_property)
        self._extent: typing.Optional[Extent] = None
        self._horizonproperty3d_object_link = python_petrel_property
        
    @property
    def affine_transform(self):
        """ The affine transform of the object.

        returns:
            1d array: An array with 6 coefficients of the affine transformation matrix. If array is
            represented as [a, b, c, d, e, f] then this corresponds to a affine transformation matrix of
            form:
            | a b e |
            | c d f |
            | 0 0 1 |
        """
        return _utils.from_backing_arraytype(
            self._horizonproperty3d_object_link.GetAffineTransform()
        )

    @property
    def crs_wkt(self):
        """ The PROJCS well known text representation of the object CRS.

        returns:
            string: PROJCS well known text representation of the CRS.
        """
        return self._horizonproperty3d_object_link.GetCrs()

    @property
    def extent(self) -> Extent:
        """The number of nodes in the i and j directions

        Returns:
            A :class:`cegalprizm.pythontool.Extent` object
        """
        if self._extent is None:
            i = self._horizonproperty3d_object_link.NumI()
            j = self._horizonproperty3d_object_link.NumJ()
            self._extent = Extent(i=i, j=j, k=1)

        return self._extent

    def indices(self, x: float, y: float) -> primitives.Indices:
        """The indices of the node nearest the specified point

        Please note: the node indices are 0-based, but in the Petrel
        UI they are 1-based.

        Args:
            x: the x-coordinate
            y: the y-coordinate

        Returns: A :class:`cegalprizm.pythontool.primitives.Indices` object
            representing the indices of the node nearest the point.
            `K` will always be `None`.

        Raises:

            ValueError: if the point is outside the beyond the extent
                        of the horizon property

        """
        index2 = self._horizonproperty3d_object_link.IndexAtPosition(x, y)
        if index2 is None:
            raise ValueError("Position not in horizon property")
        if (
            index2 is None
            or index2.GetValue().I < 0
            or index2.GetValue().J < 0
            or index2.GetValue().I >= self.extent.i
            or index2.GetValue().J >= self.extent.j
        ):
            raise ValueError("Position not in horizon property")
        return primitives.Indices(index2.GetValue().I, index2.GetValue().J, None)

    def position(self, i: int, j: int) -> primitives.Point:
        """The position of the node

        Args:
            i: the i-index of the node
            j: the j -index of the node

        Returns: A :class:`cegalprizm.pythontool.Point` object
            representing the position of the node.

        Raises:
            ValueError: if the indices are outside the horizon property
        """
        point3 = self._horizonproperty3d_object_link.PositionAtIndex(i, j)
        if point3 is None:
            raise ValueError("Index not valid for interpretation")
        return primitives.Point(
            point3.GetValue().X, point3.GetValue().Y, point3.GetValue().Z
        )

    def is_undef_value(self, value: typing.Union[float, int]) -> bool:
        """Whether the value is the 'undefined value' for the attribute

        Petrel represents some undefined values by ``MAX_INT``, others
        by ``NaN``.  A comparison with ``NaN`` will always return
        ``False`` (e.g. ``float.nan != float.nan``) so it is
        preferable to always use this method to test for undefined
        values.

        Args:
            value: the value to test

        Returns:
            bool: True if value is 'undefined' for this horizon property
            attribute

        """
        return self._is_undef_value(value)

    def clone(self, name_of_clone: str, copy_values: bool = False, template: "Template" = None) -> "HorizonProperty3d":
        """Creates a clone of the horizon property 3d.

        The clone is placed in the same collection as the source horizon property 3d.
        A clone cannot be created with the same name as an existing Petrel object in the same collection.
        
        A clone can be created with a continuous Template. Cloning with template is only possible if copy_values=False.
        When cloning with template, the clone will get the default color table of the given template.
        If a template argument is not provided, the clone will have the same template and color table as the source object.

        Args:
            name_of_clone: Petrel name of the clone
            copy_values: Set to True if values shall be copied into the clone. Defaults to False.
            template: Template to use for the clone. Defaults to None.

        Returns:
            cegalprizm.pythontool.HorizonProperty3d: the cloned HorizonProperty3d object
               
        Raises:
            Exception: If there already exists a Petrel object with the same name
            ValueError: If name_of_clone is empty or contains slashes
            UserErrorException: If template is used as argument when copy_values=True. Can only clone with template if copy_values=False
            UserErrorException: If template is not a Template object
        """
        _utils.verify_continuous_clone(copy_values, template)
        return typing.cast("HorizonProperty3d",self._clone(name_of_clone, copy_values = copy_values, template = template))

    def _is_undef_value(self, value: typing.Union[float, int]) -> bool:
        return math.isnan(value)

    @property
    def undef_value(self) -> float:
        """The 'undefined value' for this attribute

        Use this value when setting a slice's value to 'undefined'.
        Do not attempt to test for undefinedness by comparing with
        this value, use :meth:`is_undef_value` instead.

        Returns:
           The 'undefined value' for this attribute
        """
        return self._undef_value()

    def _undef_value(self) -> float:
        return float("nan")

    @property
    def unit_symbol(self) -> typing.Optional[str]:
        """The symbol for the unit which the values are measured in

        Returns:

            string: The symbol for the unit, or None if no unit is used
        """
        return self._unit_symbol()

    def _unit_symbol(self) -> typing.Optional[str]:
        return _utils.str_or_none(self._horizonproperty3d_object_link.GetDisplayUnitSymbol())

    def all(self) -> chunk.Chunk:
        """Creates a :class:`cegalprizm.pythontool.Chunk` with the values for the attribute

        Returns:
            cegalprizm.pythontool.Chunk:  A `Slice` containing the values for the attribute
        """
        return self._make_chunk(i=None, j=None)

    def chunk(self, i: typing.Optional[typing.Tuple[int, int]] = None, j: typing.Optional[typing.Tuple[int, int]] = None) -> chunk.Chunk:
        """Creates a :class:`cegalprizm.pythontool.Chunk` with the values for the attribute

        Args:
            i: A tuple(i1,i2) where i1 is the start index and i2 is the end index. 
                The start and end value in this range is inclusive. If None include all i values.
            j: A tuple(j1,j2) where j1 is the start index and j2 is the end index. 
                The start and end value in this range is inclusive. If None include all j values.

        Returns:
            cegalprizm.pythontool.Chunk:  A `Slice` containing the values for the attribute
        """
        return self._make_chunk(i=i, j=j)

    def _make_chunk(self, i=None, j=None) -> "cegalprizm.pythontool.Chunk":
        value_getters = {
            ChunkType.k: lambda i, j, k: _utils.from_backing_arraytype(
                self._horizonproperty3d_object_link.GetChunk(i, j)
            )
        }
        value_setters = {
            ChunkType.k: lambda i, j, k, values: self._horizonproperty3d_object_link.SetChunk(
                i, j, _utils.to_backing_arraytype(values)
            )
        }
        value_shapers = {
            ChunkType.k: lambda i, j, k, values: _utils.ensure_2d_float_array(
                values, i, j
            )
        }
        value_accessors = {ChunkType.k: lambda i, j, k: _utils.native_accessor((i, j))}

        return cegalprizm.pythontool.Chunk(
            i,
            j,
            None,
            self,
            self.extent,
            value_getters,
            value_setters,
            value_shapers,
            value_accessors,
            (True, True, False),
            ChunkType.k,
            readonly=self.readonly,
        )

    def __str__(self) -> str:
        """A readable representation of the HorizonInterpretation3D"""
        return 'HorizonProperty3D(petrel_name="{0}")'.format(self.petrel_name)

    @_utils.positions_doc_decorator_2d
    def positions_to_ijks(self, positions: typing.Union[typing.Tuple[typing.List[float], typing.List[float]], typing.Tuple[typing.List[float], typing.List[float], typing.List[float]]])\
            -> typing.Tuple[typing.List[float], typing.List[float]]:
        return _utils.positions_to_ijks_2d(self._horizonproperty3d_object_link, positions)
    
    @_utils.ijks_doc_decorator_2d
    def ijks_to_positions(self, indices: typing.Tuple[typing.List[float], typing.List[float]]) -> typing.Tuple[typing.List[float], typing.List[float], typing.List[float]]:
        return _utils.ijks_to_positions(extent = self.extent, 
                                        object_link = self._horizonproperty3d_object_link, 
                                        indices = indices, 
                                        dimensions = 2)

    @property
    def horizon_interpretation_3d(self) -> "HorizonInterpretation3d":
        """The parent 3d horizon interpretation of the horizon property.

        Returns:
            cegalprizm.pythontool.HorizonInterpretation3d: The parent grid of the property
        """   
        return HorizonInterpretation3d(self._horizonproperty3d_object_link.GetParentHorizonInterpretation3d())

    @_utils.get_template_decorator
    def get_template(self) -> typing.Union["Template", "DiscreteTemplate", None]:
        return self._get_template()

class HorizonInterpretation3d(HorizonProperty3d):
    def __init__(self, python_petrel_property: "HorizonInterpretation3dGrpc"):
        super(HorizonInterpretation3d, self).__init__(python_petrel_property)
        self._extent = None
        self._horizoninterpretation3d_object_link = python_petrel_property
        
    def __str__(self) -> str:
        """A readable representation of the HorizonInterpretation3d"""
        return 'HorizonInterpretation3D(petrel_name="{0}")'.format(self.petrel_name)

    @property
    def sample_count(self) -> int:
        """The number of samples contained in the Horizon Interpretation 3d object.

        Returns:
            int: The number of points in the interpretation.
        """        
        return self._horizoninterpretation3d_object_link.SampleCount()

    @property
    def horizon_interpretation(self) -> HorizonInterpretation:
        """Returns the parent Horizon interpretation of the 3d horizon interpretation grid."""            
        return HorizonInterpretation(self._horizoninterpretation3d_object_link.GetParent())

    @property
    def horizon_property_3ds(self) -> typing.List[HorizonProperty3d]:
        """A readonly iterable collection of the 3d horizon interpretation properties for the 3d horizon interpretation grid 
        
        Returns:
            cegalprizm.pythontool.HorizonProperties:the 3d horizon interpretation properties
              for the 3d horizon interpretation grid"""
        return [
            HorizonProperty3d(po)
            for po in self._horizoninterpretation3d_object_link.GetAllHorizonPropertyValues()
        ]

    def clone(self, name_of_clone: str, copy_values: bool = False) -> "HorizonInterpretation3d":
        """ Creates a clone of the horizon interprepretation 3d.

        The clone is placed in the same collection as the source horizon interpretation 3d.
        A clone cannot be created with the same name as an existing Petrel object in the same collection.
        
        Args:
            name_of_clone: Petrel name of the clone
            copy_values: Set to True if values shall be copied into the clone. Defaults to False.

        Returns:
            cegalprizm.pythontool.HorizonInterpretation3d: the cloned HorizonInterpretation3d object
            
        Raises:
            Exception: If there already exists a Petrel object with the same name
            ValueError: If name_of_clone is empty or contains slashes
        """
        return typing.cast("HorizonInterpretation3d", self._clone(name_of_clone, copy_values = copy_values))