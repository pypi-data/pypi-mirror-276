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

from .option_3 import option as option_cls
from .auto_range import auto_range as auto_range_cls
from .clip_to_range_1 import clip_to_range as clip_to_range_cls

class range(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    auto_range: auto_range_cls = ...
    clip_to_range: clip_to_range_cls = ...
