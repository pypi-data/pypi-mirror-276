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

from .discrete_phase_bc_type import discrete_phase_bc_type as discrete_phase_bc_type_cls
from .dem_collision_partner import dem_collision_partner as dem_collision_partner_cls
from .reinj_inj import reinj_inj as reinj_inj_cls
from .discrete_phase_bc_function import discrete_phase_bc_function as discrete_phase_bc_function_cls
from .mixing_plane_thread import mixing_plane_thread as mixing_plane_thread_cls

class dpm(Group):
    fluent_name = ...
    child_names = ...
    discrete_phase_bc_type: discrete_phase_bc_type_cls = ...
    dem_collision_partner: dem_collision_partner_cls = ...
    reinj_inj: reinj_inj_cls = ...
    discrete_phase_bc_function: discrete_phase_bc_function_cls = ...
    mixing_plane_thread: mixing_plane_thread_cls = ...
