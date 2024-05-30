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

from .auto_scale import auto_scale as auto_scale_cls
from .scale_f import scale_f as scale_f_cls

class scale(Group):
    fluent_name = ...
    child_names = ...
    auto_scale: auto_scale_cls = ...
    scale_f: scale_f_cls = ...
