#
# This is an auto-generated file.  DO NOT EDIT!
#


from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    _CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    _HasAllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from typing import Union, List, Tuple

from .list_properties import list_properties as list_properties_cls
from .add_zone import add_zone as add_zone_cls
from .list_zone import list_zone as list_zone_cls
from .delete_zone import delete_zone as delete_zone_cls
from .contact_resis_child import contact_resis_child


class tortuosity_interface(ListObject[contact_resis_child]):
    fluent_name = ...
    command_names = ...

    def list_properties(self, object_at: int):
        """
        List properties of selected object.
        
        Parameters
        ----------
            object_at : int
                Select object index to delete.
        
        """

    def add_zone(self, zone_name: str, value: Union[float, str]):
        """
        'add_zone' command.
        
        Parameters
        ----------
            zone_name : str
                'zone_name' child.
            value : real
                'value' child.
        
        """

    def list_zone(self, ):
        """
        'list_zone' command.
        """

    def delete_zone(self, face_name: str):
        """
        'delete_zone' command.
        
        Parameters
        ----------
            face_name : str
                Pick ~a zone you want to delete.
        
        """

    child_object_type = ...
