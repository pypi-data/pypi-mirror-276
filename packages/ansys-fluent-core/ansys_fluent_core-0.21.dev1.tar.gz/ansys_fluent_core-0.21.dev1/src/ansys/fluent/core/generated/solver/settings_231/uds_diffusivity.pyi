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

from .option_10 import option as option_cls
from .uds_diffusivities import uds_diffusivities as uds_diffusivities_cls
from .user_defined_function import user_defined_function as user_defined_function_cls

class uds_diffusivity(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    uds_diffusivities: uds_diffusivities_cls = ...
    user_defined_function: user_defined_function_cls = ...
