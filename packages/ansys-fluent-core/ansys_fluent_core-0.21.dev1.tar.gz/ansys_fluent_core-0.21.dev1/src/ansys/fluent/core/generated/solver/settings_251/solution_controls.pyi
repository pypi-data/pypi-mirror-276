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

from .mapping_frequency import mapping_frequency as mapping_frequency_cls
from .under_relaxation_factor_1 import under_relaxation_factor as under_relaxation_factor_cls

class solution_controls(Command):
    fluent_name = ...
    argument_names = ...
    mapping_frequency: mapping_frequency_cls = ...
    under_relaxation_factor: under_relaxation_factor_cls = ...
