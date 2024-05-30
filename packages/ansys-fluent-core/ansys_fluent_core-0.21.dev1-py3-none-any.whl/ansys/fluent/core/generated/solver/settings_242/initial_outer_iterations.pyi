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

from .initial_time_steps import initial_time_steps as initial_time_steps_cls
from .initial_outer_iter import initial_outer_iter as initial_outer_iter_cls

class initial_outer_iterations(Group):
    fluent_name = ...
    child_names = ...
    initial_time_steps: initial_time_steps_cls = ...
    initial_outer_iter: initial_outer_iter_cls = ...
