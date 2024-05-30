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

from .vof_min_seeding import vof_min_seeding as vof_min_seeding_cls
from .ia_grad_sym import ia_grad_sym as ia_grad_sym_cls

class area_density(Group):
    fluent_name = ...
    child_names = ...
    vof_min_seeding: vof_min_seeding_cls = ...
    ia_grad_sym: ia_grad_sym_cls = ...
