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

from .porous_jump_child import porous_jump_child


class porous_jump(NamedObject[porous_jump_child], _NonCreatableNamedObjectMixin[porous_jump_child]):
    fluent_name = ...
    child_object_type = ...
