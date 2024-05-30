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

from .option_23 import option as option_cls
from .iterations_1 import iterations as iterations_cls
from .time_steps import time_steps as time_steps_cls

class frequency(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    iterations: iterations_cls = ...
    time_steps: time_steps_cls = ...
