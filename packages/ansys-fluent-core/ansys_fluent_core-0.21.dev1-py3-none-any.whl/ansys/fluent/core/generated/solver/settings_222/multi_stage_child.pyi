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

from .coefficient import coefficient as coefficient_cls
from .dissipation import dissipation as dissipation_cls
from .viscous_1 import viscous as viscous_cls

class multi_stage_child(Group):
    fluent_name = ...
    child_names = ...
    coefficient: coefficient_cls = ...
    dissipation: dissipation_cls = ...
    viscous: viscous_cls = ...
