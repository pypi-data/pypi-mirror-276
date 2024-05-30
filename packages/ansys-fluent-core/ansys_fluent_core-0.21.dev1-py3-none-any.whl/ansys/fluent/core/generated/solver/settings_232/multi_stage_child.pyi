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
from .update_dissipation import update_dissipation as update_dissipation_cls
from .update_viscous import update_viscous as update_viscous_cls

class multi_stage_child(Group):
    fluent_name = ...
    child_names = ...
    coefficient: coefficient_cls = ...
    update_dissipation: update_dissipation_cls = ...
    update_viscous: update_viscous_cls = ...
