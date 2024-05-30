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

from .add_contact_resistance import add_contact_resistance as add_contact_resistance_cls
from .list_contact_face import list_contact_face as list_contact_face_cls
from .delete_contact_face import delete_contact_face as delete_contact_face_cls

class contact_resistance(Group):
    fluent_name = ...
    command_names = ...

    def add_contact_resistance(self, contact_face: str, resistance_value: Union[float, str]):
        """
        'add_contact_resistance' command.
        
        Parameters
        ----------
            contact_face : str
                Set contact face.
            resistance_value : real
                Set resistance value.
        
        """

    def list_contact_face(self, ):
        """
        'list_contact_face' command.
        """

    def delete_contact_face(self, face_name: str):
        """
        'delete_contact_face' command.
        
        Parameters
        ----------
            face_name : str
                Pick contact face you want to delete.
        
        """

