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

from .moving_mesh_cfl_constraint import moving_mesh_cfl_constraint as moving_mesh_cfl_constraint_cls
from .physics_based_constraint import physics_based_constraint as physics_based_constraint_cls
from .time_scale_options import time_scale_options as time_scale_options_cls
from .verbosity_7 import verbosity as verbosity_cls

class multiphase_specific_time_constraints(Group):
    fluent_name = ...
    child_names = ...
    moving_mesh_cfl_constraint: moving_mesh_cfl_constraint_cls = ...
    physics_based_constraint: physics_based_constraint_cls = ...
    time_scale_options: time_scale_options_cls = ...
    verbosity: verbosity_cls = ...
