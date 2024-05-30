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

from .include_pop_in_fsi_force import include_pop_in_fsi_force as include_pop_in_fsi_force_cls
from .steady_2way_fsi import steady_2way_fsi as steady_2way_fsi_cls
from .include_viscous_fsi_force import include_viscous_fsi_force as include_viscous_fsi_force_cls
from .explicit_fsi_force import explicit_fsi_force as explicit_fsi_force_cls
from .starting_t_re_initialization import starting_t_re_initialization as starting_t_re_initialization_cls

class expert(Group):
    fluent_name = ...
    child_names = ...
    include_pop_in_fsi_force: include_pop_in_fsi_force_cls = ...
    steady_2way_fsi: steady_2way_fsi_cls = ...
    include_viscous_fsi_force: include_viscous_fsi_force_cls = ...
    explicit_fsi_force: explicit_fsi_force_cls = ...
    starting_t_re_initialization: starting_t_re_initialization_cls = ...
