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

from .max_num_steps import max_num_steps as max_num_steps_cls
from .step_size_controls import step_size_controls as step_size_controls_cls
from .expert_1 import expert as expert_cls

class tracking(Group):
    fluent_name = ...
    child_names = ...
    max_num_steps: max_num_steps_cls = ...
    step_size_controls: step_size_controls_cls = ...
    expert: expert_cls = ...
