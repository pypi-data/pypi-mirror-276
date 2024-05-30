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

from .list_2 import list as list_cls
from .list_properties_5 import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .set_1 import set as set_cls
from .register_based_child import register_based_child


class register_based(NamedObject[register_based_child], _CreatableNamedObjectMixin[register_based_child]):
    fluent_name = ...
    command_names = ...

    def list(self, ):
        """
        List the names of the definitions for poor mesh numerics.
        """

    def list_properties(self, register_name: str):
        """
        List the properties of a definition for poor mesh numerics.
        
        Parameters
        ----------
            register_name : str
                'register_name' child.
        
        """

    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        
        Parameters
        ----------
            from_ : str
                'from' child.
            to : str
                'to' child.
        
        """

    def set(self, ):
        """
        'set' command.
        """

    child_object_type = ...
