# Copyright 2024 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from .petrelobject_grpc import PetrelObjectGrpc
from cegalprizm.pythontool.ooponly.ptutils import Utils
from cegalprizm.pythontool.grpc import petrelinterface_pb2

import pandas as pd
import typing
if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.petrelconnection import PetrelConnection
    from cegalprizm.pythontool.oophub.faultinterpretation_hub import FaultInterpretationHub

class FaultInterpretationGrpc(PetrelObjectGrpc):
    def __init__(self, guid: str, petrel_connection: "PetrelConnection"):
        super(FaultInterpretationGrpc, self).__init__("fault interpretation", guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._invariant_content = {}
        self._channel = typing.cast("FaultInterpretationHub", petrel_connection._service_faultinterpretation)

    def GetFaultSticksDataframe(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        responses = self._channel.FaultInterpretation_GetFaultSticksDataframe(request)
        ids = []
        xs, ys, zs = [], [], []
        for response in responses:
            for x in response.PointX:
                ids.append(response.FaultStickId)
                xs.append(x)
            for y in response.PointY:
                ys.append(y)
            for z in response.PointZ:
                zs.append(z)
        data = {}
        data["Fault Stick ID"] = pd.Series(ids, dtype = pd.Int64Dtype())
        data["X"] = pd.Series(xs, dtype = float)
        data["Y"] = pd.Series(ys, dtype = float)
        data["Z"] = pd.Series(zs, dtype = float)
        return pd.DataFrame(data)
    
    def ClearAllPolylines(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        self._channel.FaultInterpretation_ClearAllPolylines(request)

    def GetDomain(self) -> str:
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        response = self._plink._service_petrel_object.PetrelObject_GetDomain(request)
        if response.Domain == petrelinterface_pb2.DomainType.TIME:
            return "Elevation time"
        elif response.Domain == petrelinterface_pb2.DomainType.DEPTH:
            return "Elevation depth"
        else:
            return ""