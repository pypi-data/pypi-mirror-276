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

from .smooth_partitioning import smooth_partitioning as smooth_partitioning_cls
from .max_smoothing_iterations import max_smoothing_iterations as max_smoothing_iterations_cls

class smooth(Group):
    fluent_name = ...
    child_names = ...
    smooth_partitioning: smooth_partitioning_cls = ...
    max_smoothing_iterations: max_smoothing_iterations_cls = ...
