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

from .update_stage_gradients import update_stage_gradients as update_stage_gradients_cls
from .runge_kutta import runge_kutta as runge_kutta_cls

class fast_transient_settings(Group):
    fluent_name = ...
    child_names = ...
    update_stage_gradients: update_stage_gradients_cls = ...
    runge_kutta: runge_kutta_cls = ...
