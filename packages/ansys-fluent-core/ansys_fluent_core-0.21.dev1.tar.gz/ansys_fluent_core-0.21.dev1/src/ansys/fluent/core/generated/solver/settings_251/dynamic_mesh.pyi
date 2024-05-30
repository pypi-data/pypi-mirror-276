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

from .use import use as use_cls
from .auto_1 import auto as auto_cls
from .threshold import threshold as threshold_cls
from .interval import interval as interval_cls

class dynamic_mesh(Group):
    fluent_name = ...
    child_names = ...
    use: use_cls = ...
    auto: auto_cls = ...
    threshold: threshold_cls = ...
    interval: interval_cls = ...
