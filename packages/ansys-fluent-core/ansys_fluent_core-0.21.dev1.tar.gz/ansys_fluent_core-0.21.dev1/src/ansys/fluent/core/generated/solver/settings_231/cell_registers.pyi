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

from .cell_registers_child import cell_registers_child


class cell_registers(NamedObject[cell_registers_child], _CreatableNamedObjectMixin[cell_registers_child]):
    fluent_name = ...
    child_object_type = ...
