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

from .phase_11 import phase as phase_cls
from .thermal_bc import thermal_bc as thermal_bc_cls
from .temperature import temperature as temperature_cls
from .q import q as q_cls

class network_end_child(Group):
    fluent_name = ...
    child_names = ...
    phase: phase_cls = ...
    thermal_bc: thermal_bc_cls = ...
    temperature: temperature_cls = ...
    q: q_cls = ...
