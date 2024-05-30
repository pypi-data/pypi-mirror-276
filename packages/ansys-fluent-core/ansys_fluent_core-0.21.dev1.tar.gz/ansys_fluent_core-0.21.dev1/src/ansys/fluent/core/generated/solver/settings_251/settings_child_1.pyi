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

from .active import active as active_cls
from .value_2 import value as value_cls
from .transparency import transparency as transparency_cls
from .color_6 import color as color_cls

class settings_child(Group):
    fluent_name = ...
    child_names = ...
    active: active_cls = ...
    value: value_cls = ...
    transparency: transparency_cls = ...
    color: color_cls = ...
