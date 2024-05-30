# Copyright 2024 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool.exceptions import PythonToolException, UserErrorException
from cegalprizm.pythontool.experimental import experimental_method
from cegalprizm.pythontool import exceptions
from cegalprizm.pythontool.grpc import utils as grpc_utils
from cegalprizm.pythontool.grpc.template_grpc import TemplateGrpc, DiscreteTemplateGrpc
from cegalprizm.pythontool.template import Template, DiscreteTemplate
from cegalprizm.pythontool import _utils
import re
import typing
import pandas as pd

if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.grpc.petrelobject_grpc import PetrelObjectGrpc

class PetrelObject(object):
    def __init__(self, petrel_object_link: "PetrelObjectGrpc") -> None:
        self._petrel_object_link = petrel_object_link
        self._readonly: bool = True
        petrel_object_link._domain_object = self

    @property
    def readonly(self) -> bool:
        """The read-only status of this object

        Returns:
            bool: True if the object is read-only"""        
        return self._readonly

    @readonly.setter
    def readonly(self, value: bool) -> None:
        """Setting the read-only status of this object

        This is a Python Tool Pro feature and is not available when running scripts in the editor integrated in Python Tool or in a workflow.
        
        Parameters:
            value (bool): True if the object is read-only

        :raises:
            NotImplementedError: If the property is set when not running as a Python Tool Pro script"""

        if value == False:
            readonly_error = self._petrel_object_link.IsAlwaysReadonly()
            if readonly_error:
                raise exceptions.PythonToolException(readonly_error + ' Cannot modify read-only for this object.' )

        self._readonly = value

    @property
    def petrel_name(self) -> str:
        """Returns the name of this object in Petrel"""
        return self._petrel_object_link.GetPetrelName()

    @property
    def path(self) -> str:
        """ The path of this object in Petrel. Neither the Petrel name nor the path is guaranteed to be unique.
        
        Returns:
            str: The path of the Petrel object"""
        return self._petrel_object_link.GetPath()

    def retrieve_stats(self) -> typing.Dict[str, str]:
        """Retrieves a dictionary summarizing the statistics for the object

        The statistics are a snapshot of the information in the
        Statistics page of the Settings panel of the object in the
        Petrel tree.  Both the dict key and value are strings, and may
        contain punctuation, English phrases or just filler
        information.  Any changes to the dict returned will not be
        saved or affect anything.

        Note: this operation may be slow, since the statistics are
        'live' - they represent the most up to date information.

        Returns:
            dict: The statistics of the object as reported by Petrel
        """
        s = self._petrel_object_link.RetrieveStats()
        return s


    def retrieve_history(self) -> pd.DataFrame:
        """The Petrel history for the object.

        Returns the Petrel history for the object as Pandas dataframe.

        Returns:
            DataFrame: The history of the object as reported by Petrel
        """
        import pandas as pd
        s = self._petrel_object_link.RetrieveHistory()
        return pd.DataFrame.from_dict({"Date": [el for el in s[0]],
                                        "User": [el for el in s[1]],
                                        "Action": [el for el in s[2]],
                                        "Description": [el for el in s[3]]})

    @property
    def droid(self) -> str:
        """The Petrel Droid (object id or guid) for the object

        Returns the Petrel Droid or object id or guid for the object.
        If not available, will throw a PythonToolException.

        This property is planned to be deprecated in favour of a similar
        but more general id schema in future releases.
        
        Returns:
            str: The Petrel Droid of the object
        """
        try:
            return self._petrel_object_link._guid
        except Exception:
            raise PythonToolException("Droid not available")
            
    def __repr__(self) -> str:
        return str(self)
            
    def _clone(self, name_of_clone, copy_values = False, template: typing.Union["Template", "DiscreteTemplate"] = None):
        _utils.verify_clone_name(name_of_clone)
        path_of_clone = re.sub('[^/]+$', '',  self.path) + name_of_clone
        return self._petrel_object_link.ClonePetrelObject(path_of_clone, copy_values, template)

    @property
    def template(self) -> str:
        """Returns the Petrel template for the object as a string. If no template available, will return an empty string."""
        return self._petrel_object_link.GetTemplateString()

    @property
    def comments(self):
        """The comments on the PetrelObject.
        
        Returns:
            string: The comments on the PetrelObject as a string.
        """
        return self._petrel_object_link.GetComments()

    def add_comment(self, new_comment: str, overwrite: bool = False) -> None:
        """Add a comment to the already existing comments on the PetrelObject, or overwrite the existing comments.
        
        Args:
            new_comment: The new comment to add to the PetrelObject.
            overwrite: Boolean flag to overwrite all existing comments with the new comment. Default is False.
        
        Raises:
            PythonToolException: if object is read-only
        """
        if self.readonly:
            raise exceptions.PythonToolException("Object is readonly")

        ok = self._petrel_object_link.AddComments(new_comment, overwrite)
        if not ok:
            raise UserErrorException("An error occured while adding the comment.")

    # Helper method
    def _get_template(self) -> typing.Union[Template, DiscreteTemplate, None]:
        template_ref = self._petrel_object_link.GetTemplate()
        template = grpc_utils.pb_PetrelObjectRef_to_grpcobj(template_ref, self._petrel_object_link._plink)
        if isinstance(template, TemplateGrpc):
            return Template(template)
        elif isinstance(template, DiscreteTemplateGrpc):
            return DiscreteTemplate(template)
        else:
            return None
        
    @experimental_method
    def _get_color_table_droid(self) -> str:
        """Helper method to get the droid of the color table of the object. Used for unit testing."""
        return self._petrel_object_link.GetColorTableDroid()