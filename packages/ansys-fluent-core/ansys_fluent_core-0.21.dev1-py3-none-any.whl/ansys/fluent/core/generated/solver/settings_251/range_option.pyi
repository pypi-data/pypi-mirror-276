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

from .option_26 import option as option_cls
from .auto_range_on import auto_range_on as auto_range_on_cls
from .auto_range_off import auto_range_off as auto_range_off_cls

class range_option(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    auto_range_on: auto_range_on_cls = ...
    auto_range_off: auto_range_off_cls = ...
