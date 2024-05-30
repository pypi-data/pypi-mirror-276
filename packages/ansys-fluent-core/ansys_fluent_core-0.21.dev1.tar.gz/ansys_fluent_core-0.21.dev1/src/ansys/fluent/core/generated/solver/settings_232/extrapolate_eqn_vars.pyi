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

from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .multi_component_diffusion_mf_child import multi_component_diffusion_mf_child


class extrapolate_eqn_vars(NamedObject[multi_component_diffusion_mf_child], _NonCreatableNamedObjectMixin[multi_component_diffusion_mf_child]):
    fluent_name = ...
    command_names = ...

    def list(self, ):
        """
        'list' command.
        """

    def list_properties(self, object_name: str):
        """
        'list_properties' command.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        
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

    child_object_type = ...
