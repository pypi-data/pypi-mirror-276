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

from .fluid_2 import fluid as fluid_cls
from .solid_3 import solid as solid_cls

class volumes(Group):
    fluent_name = ...
    child_names = ...
    fluid: fluid_cls = ...
    solid: solid_cls = ...
