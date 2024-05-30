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

from .components_2 import components as components_cls
from .list_properties_4 import list_properties as list_properties_cls

class groups_child(Group):
    fluent_name = ...
    child_names = ...
    components: components_cls = ...
    command_names = ...

    def list_properties(self, ):
        """
        'list_properties' command.
        """

