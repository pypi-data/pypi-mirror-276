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
from .single_rate import single_rate as single_rate_cls
from .secondary_rate import secondary_rate as secondary_rate_cls
from .value_1 import value as value_cls

class thermolysis_model(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    single_rate: single_rate_cls = ...
    secondary_rate: secondary_rate_cls = ...
    value: value_cls = ...
