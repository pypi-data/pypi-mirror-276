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

from .type_of_smoothing import type_of_smoothing as type_of_smoothing_cls
from .number_of_iterations import number_of_iterations as number_of_iterations_cls
from .relaxtion_factor import relaxtion_factor as relaxtion_factor_cls
from .percentage_of_cells import percentage_of_cells as percentage_of_cells_cls
from .skewness_threshold import skewness_threshold as skewness_threshold_cls

class smooth_mesh(Command):
    fluent_name = ...
    argument_names = ...
    type_of_smoothing: type_of_smoothing_cls = ...
    number_of_iterations: number_of_iterations_cls = ...
    relaxtion_factor: relaxtion_factor_cls = ...
    percentage_of_cells: percentage_of_cells_cls = ...
    skewness_threshold: skewness_threshold_cls = ...
