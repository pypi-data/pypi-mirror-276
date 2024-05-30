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

from .option_6 import option as option_cls
from .length_scale import length_scale as length_scale_cls
from .step_length_factor import step_length_factor as step_length_factor_cls

class step_size_controls(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    length_scale: length_scale_cls = ...
    step_length_factor: step_length_factor_cls = ...
