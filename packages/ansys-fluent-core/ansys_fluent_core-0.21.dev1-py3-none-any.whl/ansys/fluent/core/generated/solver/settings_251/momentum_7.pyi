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

from .gauge_pressure import gauge_pressure as gauge_pressure_cls
from .mach_number import mach_number as mach_number_cls
from .non_equil_boundary import non_equil_boundary as non_equil_boundary_cls
from .coordinate_system_1 import coordinate_system as coordinate_system_cls
from .flow_direction import flow_direction as flow_direction_cls
from .axis_direction_2 import axis_direction as axis_direction_cls
from .axis_origin_2 import axis_origin as axis_origin_cls

class momentum(Group):
    fluent_name = ...
    child_names = ...
    gauge_pressure: gauge_pressure_cls = ...
    mach_number: mach_number_cls = ...
    non_equil_boundary: non_equil_boundary_cls = ...
    coordinate_system: coordinate_system_cls = ...
    flow_direction: flow_direction_cls = ...
    axis_direction: axis_direction_cls = ...
    axis_origin: axis_origin_cls = ...
