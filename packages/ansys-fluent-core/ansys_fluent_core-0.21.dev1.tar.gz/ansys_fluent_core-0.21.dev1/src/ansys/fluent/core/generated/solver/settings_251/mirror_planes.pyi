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

from .delete_1 import delete as delete_cls
from .rename import rename as rename_cls
from .list import list as list_cls
from .list_properties_1 import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .create_3 import create as create_cls
from .mirror_planes_child import mirror_planes_child


class mirror_planes(NamedObject[mirror_planes_child], _NonCreatableNamedObjectMixin[mirror_planes_child]):
    fluent_name = ...
    command_names = ...

    def delete(self, name_list: List[str]):
        """
        Delete selected objects.
        
        Parameters
        ----------
            name_list : typing.List[str]
                Select objects to be deleted.
        
        """

    def rename(self, new: str, old: str):
        """
        Rename the object.
        
        Parameters
        ----------
            new : str
                New name for the object.
            old : str
                Select object to rename.
        
        """

    def list(self, ):
        """
        List the names of the objects.
        """

    def list_properties(self, object_name: str):
        """
        List active properties of the object.
        
        Parameters
        ----------
            object_name : str
                Select object for which properties are to be listed.
        
        """

    def make_a_copy(self, from_: str, to: str):
        """
        Create a copy of the object.
        
        Parameters
        ----------
            from_ : str
                Select the object to duplicate.
            to : str
                Specify the name of the new object.
        
        """

    def create(self, coefficients: List[Union[float, str]], distance: Union[float, str]):
        """
        To define a mirror plane for a non-symmetric domain.
        
        Parameters
        ----------
            coefficients : typing.List[real]
                Set the cofficients of X, Y and Z.
            distance : real
                Set the distance of the plane from the origin.
        
        """

    child_object_type = ...
