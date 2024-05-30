# Copyright 2024 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool.grpc.petrelinterface_pb2 import *
from .base_hub import BaseHub
import typing

class FaultInterpretationHub(BaseHub):
    def GetFaultInterpretation(self, msg) -> PetrelObjectRef: # type: ignore
        return self._wrapper("cegal.pythontool.GetFaultInterpretation", PetrelObjectRef, msg)

    def FaultInterpretation_GetFaultSticksDataframe(self, msg) -> typing.Iterable[FaultInterpretation_GetAllFaultSticks_Response]: # type: ignore
        return self._server_streaming_wrapper("cegal.pythontool.FaultInterpretation_GetAllFaultSticks", FaultInterpretation_GetAllFaultSticks_Response, msg)
    
    def FaultInterpretation_ClearAllPolylines(self, msg) -> ProtoBool: # type: ignore
        return self._wrapper("cegal.pythontool.FaultInterpretation_ClearAllPolylines", ProtoBool, msg)