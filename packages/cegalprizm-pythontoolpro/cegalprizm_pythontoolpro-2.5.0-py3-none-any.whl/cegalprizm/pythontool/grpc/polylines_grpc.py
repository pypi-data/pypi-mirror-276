# Copyright 2024 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from .petrelobject_grpc import PetrelObjectGrpc

from cegalprizm.pythontool.grpc import petrelinterface_pb2, utils
from .petrelinterface_pb2 import Primitives
from .points_grpc import PropertyTableHandler


import pandas as pd
import typing
if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.petrelconnection import PetrelConnection
    from cegalprizm.pythontool.oophub.polylines_hub import PolylinesHub

class PolylineSetGrpc(PetrelObjectGrpc):

    def __init__(self, guid: str, petrel_connection: "PetrelConnection"):
        super(PolylineSetGrpc, self).__init__('polylineset', guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._channel = typing.cast("PolylinesHub", petrel_connection._service_polylines)
        self._table_handler = PropertyTableHandler(self._guid, self._plink, self._channel, 'polylineset')

    def GetCrs(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.PolylineSet_GetCrs_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._channel.PolylineSet_GetCrs(request)
             
        return response.GetCrs

    def GetNumPolylines(self) -> int:
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)        
        return self._channel.PolylineSet_GetNumPolylines(request).value 

    def GetDisplayUnitSymbol(self, idx):
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.PetrelObjectGuidAndIndex(
            guid = po_guid,
            index = idx
        )
        return self._channel.PolylineSet_DisplayUnitSymbol(request).value

    def IsClosed(self, idx) -> bool:
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.PetrelObjectGuidAndIndex(
            guid = po_guid,
            index = idx
        )
        return self._channel.PolylineSet_IsClosed(request).value 

    def GetPoints(self, idx):
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.PetrelObjectGuidAndIndex(guid = po_guid, index = idx)        
        responses = self._channel.PolylineSet_GetPoints(request)
        points = []
        for response in responses:
            point = Primitives.Double3(x = response.x, y = response.y, z = response.z)
            points.append(point)

        point_array = [None] * 3
        point_array[0] = []
        point_array[1] = []
        point_array[2] = []
        
        for p in points:
            point_array[0].append(p.x) 
            point_array[1].append(p.y) 
            point_array[2].append(p.z) 
        
        return point_array

    def SetPolylinePoints(self, idx, xs, ys, zs, closed = False):
        if not xs or len(xs) == 0:
            return

        self.write_test()
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        no_points_per_streamed_unit = self._table_handler.no_points_per_streamed_unit(len(xs), self._plink._preferred_streamed_unit_bytes)
        no_points = len(xs)
        start_inds = range(0, no_points, no_points_per_streamed_unit)
        
        iterable_requests = map(
            lambda start_ind : self._table_handler.setpoints_request(start_ind, po_guid, xs, ys, zs, no_points_per_streamed_unit, idx = idx, closed = closed),
            start_inds
        )

        ok = self._channel.PolylineSet_SetPolylinePoints(iterable_requests)
        return ok.value

    def AddPolyline(self, arrayx, arrayy, arrayz, closed):
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        point_inds = range(len(arrayx))
        iterable_requests = map(
            lambda point_ind : self._add_polyline_request(po_guid, arrayx[point_ind], arrayy[point_ind], arrayz[point_ind], closed),
            point_inds
        )

        return self._channel.PolylineSet_AddPolyline(iterable_requests).value

    def _add_polyline_request(self, po_guid, x, y, z, closed):
        point = petrelinterface_pb2.Primitives.Double3(x = x, y = y, z = z)
        return petrelinterface_pb2.AddPolyline_Request(
            guid = po_guid,
            point = point,
            closed = closed
        )
    
    def AddMultiplePolylines(self, polylines_dict: dict, contains_closed: bool = False):
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        iterable_requests = []
        for poly_index, values in polylines_dict.items():
            request = petrelinterface_pb2.AddMultiplePolylines_Request(
                Guid = po_guid,
                PolyIndex = poly_index,
                VertIndex = [vi for vi in values[0]],
                Xs = [x for x in values[1]],
                Ys = [y for y in values[2]],
                Zs = [z for z in values[3]],
                ## If no column provided, we assume all polylines are closed
                IsClosed = bool(values[4][0]) if contains_closed else True
            )
            iterable_requests.append(request)

        self._channel.PolylineSet_AddMultiplePolylines(r for r in iterable_requests)

    def DeletePolyline(self, polyline_index):
        self.write_test()
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.PetrelObjectGuidAndIndex(guid = po_guid, index = polyline_index)        
        return self._channel.PolylineSet_DeletePolyline(request).value

    def DeleteAll(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.PolylineSet_DeleteAll_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._channel.PolylineSet_DeleteAll(request)
             
        return response.DeleteAll
    
    def GetPointsDataFrame(self) -> pd.DataFrame:
        request = petrelinterface_pb2.PolylineSet_GetPointsDataframe_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        responses = self._channel.PolylineSet_GetPointsDataframe(request)

        poly_indices = []
        vertice_indices = []
        xs = []
        ys = []
        zs = []
        for response in responses:
            poly_indices.append(response.PolyIndex)
            vertice_indices.append(response.VerticeIndex)
            xs.append(round(response.X, 2))
            ys.append(round(response.Y, 2))
            zs.append(round(response.Z, 2))

        data = {}
        data["Poly"] = pd.Series(poly_indices, dtype = pd.Int64Dtype())
        data["Vert"] = pd.Series(vertice_indices, dtype = pd.Int64Dtype())
        data["X"] = pd.Series(xs, dtype = float)
        data["Y"] = pd.Series(ys, dtype = float)
        data["Z"] = pd.Series(zs, dtype = float)

        df = pd.DataFrame(data)
        return df
    
    def GetAttributesDataFrame(self) -> pd.DataFrame:
        request = petrelinterface_pb2.PolylineSet_GetAttributesDataframe_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        responses = self._channel.PolylineSet_GetAttributesDataframe(request)

        poly_indices, att_names, att_values, att_types = [], [], [], []

        for response in responses:
            poly_indices.append(response.PolyIndex)
            att_names.append(response.AttributeNames)
            att_values.append(response.AttributeValues)
            att_types.append(response.AttributeTypes)

        unordered_data = {}
        unordered_data["Poly"] = pd.Series(poly_indices, dtype = pd.Int64Dtype())

        if(len(att_names) > 0):
            unordered_data = utils.HandleUserDefinedProperties(unordered_data, att_names, att_values, att_types)

        ordered_data = self._get_ordered_dictionary(unordered_data)

        df = pd.DataFrame(ordered_data)
        ## Handle edge-case with no polylines, in this case polyindex is 0
        if len(df) == 1 and df['Poly'][0] == 0:
            df = df.drop(df.index[0])

        return df

    def _get_ordered_dictionary(self, unordered_data):
        ordered_data = {}
        if "Poly" in unordered_data:
            ordered_data["Poly"] = unordered_data.pop("Poly")
        if "Show polygon" in unordered_data:
            ordered_data["Show polygon"] = unordered_data.pop("Show polygon")
        if "Show polygon (1)" in unordered_data:
            ordered_data["Show polygon (1)"] = unordered_data.pop("Show polygon (1)")
        if "Label X" in unordered_data:
            ordered_data["Label X"] = unordered_data.pop("Label X").round(2)
        if "Label X (1)" in unordered_data:
            ordered_data["Label X (1)"] = unordered_data.pop("Label X (1)").round(2)
        if "Label Y" in unordered_data:
            ordered_data["Label Y"] = unordered_data.pop("Label Y").round(2)
        if "Label Y (1)" in unordered_data:
            ordered_data["Label Y (1)"] = unordered_data.pop("Label Y (1)").round(2)
        if "Label Z" in unordered_data:
            ordered_data["Label Z"] = unordered_data.pop("Label Z").round(2)
        if "Label Z (1)" in unordered_data:
            ordered_data["Label Z (1)"] = unordered_data.pop("Label Z (1)").round(2)
        if "Label angle" in unordered_data:
            ordered_data["Label angle"] = unordered_data.pop("Label angle").round(2)
        if "Label angle (1)" in unordered_data:
            ordered_data["Label angle (1)"] = unordered_data.pop("Label angle (1)").round(2)

        for key in unordered_data:
            ordered_data[key] = unordered_data[key]
        return ordered_data
    
    def AddAttribute(self, name: str, prop_type: petrelinterface_pb2.PointPropertyType, template_guid: str):
        self._plink._opened_test()
        request = petrelinterface_pb2.PolylineSet_AddAttribute_Request(
            Guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type),
            AttributeName = name,
            AttributeType = prop_type,
            TemplateGuid = petrelinterface_pb2.PetrelObjectGuid(guid = template_guid)
        )
        response = self._channel.PolylineSet_AddAttribute(request)
        return response
    
    def DeleteAttribute(self, polylineset_guid: str, attribute_guid: str) -> bool:
        self._plink._opened_test()
        request = petrelinterface_pb2.PolylineSet_DeleteAttribute_Request(
            PolylineSetGuid = petrelinterface_pb2.PetrelObjectGuid(guid = polylineset_guid),
            AttributeGuid = petrelinterface_pb2.PetrelObjectGuid(guid = attribute_guid)
        )
        response = self._channel.PolylineSet_DeleteAttribute(request)
        return response.value
    
    def GetAllAttributes(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        responses = self._channel.PolylineSet_GetAllAttributes(request)
        object_refs = []
        for response in responses:
            object_refs.append(response)
        return object_refs
    
    def GetPolylineType(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        response = self._channel.PolylineSet_GetPolylineType(request)
        return response.PolylineType
