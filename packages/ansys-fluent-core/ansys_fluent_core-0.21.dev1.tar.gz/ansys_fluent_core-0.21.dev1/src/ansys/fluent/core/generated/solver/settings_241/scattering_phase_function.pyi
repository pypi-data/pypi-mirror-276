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

from .option_7 import option as option_cls
from .value_3 import value as value_cls
from .delta_eddington import delta_eddington as delta_eddington_cls
from .user_defined_function import user_defined_function as user_defined_function_cls

class scattering_phase_function(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    value: value_cls = ...
    delta_eddington: delta_eddington_cls = ...
    user_defined_function: user_defined_function_cls = ...
