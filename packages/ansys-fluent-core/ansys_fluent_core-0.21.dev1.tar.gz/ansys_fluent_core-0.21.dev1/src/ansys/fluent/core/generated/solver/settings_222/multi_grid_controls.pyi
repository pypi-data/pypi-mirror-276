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

from .multi_grid_controls_child import multi_grid_controls_child


class multi_grid_controls(NamedObject[multi_grid_controls_child], _CreatableNamedObjectMixin[multi_grid_controls_child]):
    fluent_name = ...
    child_object_type = ...
