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

from .model_ramping import model_ramping as model_ramping_cls
from .ramp_flow import ramp_flow as ramp_flow_cls
from .ramp_turbulence import ramp_turbulence as ramp_turbulence_cls
from .ramp_scalars import ramp_scalars as ramp_scalars_cls

class models(Group):
    fluent_name = ...
    child_names = ...
    model_ramping: model_ramping_cls = ...
    ramp_flow: ramp_flow_cls = ...
    ramp_turbulence: ramp_turbulence_cls = ...
    ramp_scalars: ramp_scalars_cls = ...
