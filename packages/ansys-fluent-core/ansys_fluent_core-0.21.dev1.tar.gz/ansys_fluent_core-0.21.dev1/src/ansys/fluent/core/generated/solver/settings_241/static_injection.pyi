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
from .static_injection_child import static_injection_child


class static_injection(ListObject[static_injection_child]):
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

    child_object_type = ...
