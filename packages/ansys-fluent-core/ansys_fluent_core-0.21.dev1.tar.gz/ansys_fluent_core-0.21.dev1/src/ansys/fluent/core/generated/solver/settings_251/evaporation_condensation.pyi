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

from .vof_from_min_limit import vof_from_min_limit as vof_from_min_limit_cls
from .vof_from_max_limit import vof_from_max_limit as vof_from_max_limit_cls
from .vof_to_min_limit import vof_to_min_limit as vof_to_min_limit_cls
from .vof_to_max_limit import vof_to_max_limit as vof_to_max_limit_cls
from .ia_norm_min_limit import ia_norm_min_limit as ia_norm_min_limit_cls
from .max_rel_humidity import max_rel_humidity as max_rel_humidity_cls

class evaporation_condensation(Group):
    fluent_name = ...
    child_names = ...
    vof_from_min_limit: vof_from_min_limit_cls = ...
    vof_from_max_limit: vof_from_max_limit_cls = ...
    vof_to_min_limit: vof_to_min_limit_cls = ...
    vof_to_max_limit: vof_to_max_limit_cls = ...
    ia_norm_min_limit: ia_norm_min_limit_cls = ...
    max_rel_humidity: max_rel_humidity_cls = ...
