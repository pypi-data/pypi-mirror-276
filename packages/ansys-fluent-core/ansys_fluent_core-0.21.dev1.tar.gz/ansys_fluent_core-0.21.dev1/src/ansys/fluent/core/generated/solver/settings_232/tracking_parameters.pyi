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

from .control_by import control_by as control_by_cls
from .max_number_of_steps import max_number_of_steps as max_number_of_steps_cls
from .length_scale import length_scale as length_scale_cls
from .step_length_factor import step_length_factor as step_length_factor_cls

class tracking_parameters(Group):
    fluent_name = ...
    child_names = ...
    control_by: control_by_cls = ...
    max_number_of_steps: max_number_of_steps_cls = ...
    length_scale: length_scale_cls = ...
    step_length_factor: step_length_factor_cls = ...
