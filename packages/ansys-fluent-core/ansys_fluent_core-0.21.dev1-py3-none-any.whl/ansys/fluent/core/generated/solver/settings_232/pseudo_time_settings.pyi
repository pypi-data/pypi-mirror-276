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

from .verbosity_10 import verbosity as verbosity_cls
from .time_step_method_1 import time_step_method as time_step_method_cls

class pseudo_time_settings(Group):
    fluent_name = ...
    child_names = ...
    verbosity: verbosity_cls = ...
    time_step_method: time_step_method_cls = ...
