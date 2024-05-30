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

from .set_1 import set as set_cls
from .list_properties_2 import list_properties as list_properties_cls

class poor_mesh_numerics(Group):
    fluent_name = ...
    child_names = ...
    set: set_cls = ...
    command_names = ...

    def list_properties(self, ):
        """
        List the properties of a definition for automatic poor mesh numerics.
        """

