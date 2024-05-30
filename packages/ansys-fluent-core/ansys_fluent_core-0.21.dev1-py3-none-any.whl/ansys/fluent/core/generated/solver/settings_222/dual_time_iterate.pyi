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

from .number_of_total_periods import number_of_total_periods as number_of_total_periods_cls
from .number_of_time_steps import number_of_time_steps as number_of_time_steps_cls
from .total_number_of_time_steps import total_number_of_time_steps as total_number_of_time_steps_cls
from .total_time import total_time as total_time_cls
from .incremental_time import incremental_time as incremental_time_cls
from .max_iteration_per_step import max_iteration_per_step as max_iteration_per_step_cls
from .postprocess import postprocess as postprocess_cls
from .num_of_post_iter_per_timestep import num_of_post_iter_per_timestep as num_of_post_iter_per_timestep_cls

class dual_time_iterate(Command):
    fluent_name = ...
    argument_names = ...
    number_of_total_periods: number_of_total_periods_cls = ...
    number_of_time_steps: number_of_time_steps_cls = ...
    total_number_of_time_steps: total_number_of_time_steps_cls = ...
    total_time: total_time_cls = ...
    incremental_time: incremental_time_cls = ...
    max_iteration_per_step: max_iteration_per_step_cls = ...
    postprocess: postprocess_cls = ...
    num_of_post_iter_per_timestep: num_of_post_iter_per_timestep_cls = ...
