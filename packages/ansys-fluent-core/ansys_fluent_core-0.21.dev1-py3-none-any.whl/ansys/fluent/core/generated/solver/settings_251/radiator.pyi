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

from .porous_jump_turb_wall_treatment import porous_jump_turb_wall_treatment as porous_jump_turb_wall_treatment_cls
from .loss_coefficient import loss_coefficient as loss_coefficient_cls
from .hc import hc as hc_cls
from .t import t as t_cls
from .heat_flux import heat_flux as heat_flux_cls
from .discrete_phase_bc_type import discrete_phase_bc_type as discrete_phase_bc_type_cls
from .dem_collision_partner import dem_collision_partner as dem_collision_partner_cls
from .reinj_inj import reinj_inj as reinj_inj_cls
from .discrete_phase_bc_function import discrete_phase_bc_function as discrete_phase_bc_function_cls
from .strength import strength as strength_cls

class radiator(Group):
    fluent_name = ...
    child_names = ...
    porous_jump_turb_wall_treatment: porous_jump_turb_wall_treatment_cls = ...
    loss_coefficient: loss_coefficient_cls = ...
    hc: hc_cls = ...
    t: t_cls = ...
    heat_flux: heat_flux_cls = ...
    discrete_phase_bc_type: discrete_phase_bc_type_cls = ...
    dem_collision_partner: dem_collision_partner_cls = ...
    reinj_inj: reinj_inj_cls = ...
    discrete_phase_bc_function: discrete_phase_bc_function_cls = ...
    strength: strength_cls = ...
