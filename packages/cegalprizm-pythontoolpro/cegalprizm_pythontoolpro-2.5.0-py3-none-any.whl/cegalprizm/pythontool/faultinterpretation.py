# Copyright 2024 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import typing
import pandas as pd
from pandas.api.types import is_bool_dtype
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_integer_dtype

from cegalprizm.pythontool import exceptions
from cegalprizm.pythontool import PetrelObject, SeismicLine, SeismicCube

if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.grpc.faultinterpretation_grpc import FaultInterpretationGrpc

class FaultInterpretation(PetrelObject):
    """A class holding information about a fault interpretation in Petrel.
    """  

    def __init__(self, interpretation_grpc: "FaultInterpretationGrpc"):
        super(FaultInterpretation, self).__init__(interpretation_grpc)
        self._fault_interpretation_object_link = interpretation_grpc

    def __str__(self) -> str:
        return "FaultInterpretation(petrel_name=\"{0}\")".format(self.petrel_name)
    
    @property
    def domain(self) -> str:
        """Returns the domain of the FaultInterpretation as a string.
        
        Possible values are "Elevation time" and "Elevation depth".
        """
        return self._fault_interpretation_object_link.GetDomain()
    
    def as_dataframe(self) -> pd.DataFrame:
        """ Get a dataframe with the interpreted fault polylines (fault sticks) for the FaultInterpretation.

        The values in the Z column will be in either time or depth units, depending on the domain of the FaultInterpretation. Domain information can be retrieved through the domain property.

        Returns:
            pd.DataFrame: A dataframe with Fault Stick ID, X, Y and Z values for the polylines in the FaultInterpretation.
        """
        return self._fault_interpretation_object_link.GetFaultSticksDataframe()
    
    def clone(self, name_of_clone: str, copy_values: bool = False) -> "FaultInterpretation":
        """Creates a clone of the FaultInterpretation.
        
        The clone is placed in the same collection as the original FaultInterpretation.
        If copy_values is set to False, only the geometry (polylines) will be copied
        If copy_values is set to True, the polylines and any attributes with their values will be copied to the clone.
        
        Args:
            name_of_clone (str): The name of the clone.
            copy_values (bool): If True, the values of the original FaultInterpretation are copied to the clone. Defaults to False.

        Returns:
            FaultInterpretation: The clone of the FaultInterpretation.
        
        Raises:
            ValueError: If the name_of_clone is empty or contains slashes.
        """
        return typing.cast("FaultInterpretation", self._clone(name_of_clone, copy_values))
    
    def clear(self) -> None:
        """Clear all polylines from the FaultInterpretation.

        Raises:
            PythonToolException: If the FaultInterpretation is readonly
        """
        if(self.readonly):
            raise exceptions.PythonToolException("The FaultInterpretation is readonly")
        self._fault_interpretation_object_link.ClearAllPolylines()