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

from .velocity_inlet_child import velocity_inlet_child


class velocity_inlet(NamedObject[velocity_inlet_child], _NonCreatableNamedObjectMixin[velocity_inlet_child]):
    fluent_name = ...
    child_object_type = ...
