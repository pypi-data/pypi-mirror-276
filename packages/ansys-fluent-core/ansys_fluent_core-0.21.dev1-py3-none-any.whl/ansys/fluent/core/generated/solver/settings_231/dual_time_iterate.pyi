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

from .total_period_count import total_period_count as total_period_count_cls
from .time_step_count_1 import time_step_count as time_step_count_cls
from .total_time_step_count import total_time_step_count as total_time_step_count_cls
from .total_time import total_time as total_time_cls
from .incremental_time import incremental_time as incremental_time_cls
from .max_iter_per_step import max_iter_per_step as max_iter_per_step_cls
from .postprocess import postprocess as postprocess_cls
from .post_iter_per_time_step_count import post_iter_per_time_step_count as post_iter_per_time_step_count_cls

class dual_time_iterate(Command):
    fluent_name = ...
    argument_names = ...
    total_period_count: total_period_count_cls = ...
    time_step_count: time_step_count_cls = ...
    total_time_step_count: total_time_step_count_cls = ...
    total_time: total_time_cls = ...
    incremental_time: incremental_time_cls = ...
    max_iter_per_step: max_iter_per_step_cls = ...
    postprocess: postprocess_cls = ...
    post_iter_per_time_step_count: post_iter_per_time_step_count_cls = ...
