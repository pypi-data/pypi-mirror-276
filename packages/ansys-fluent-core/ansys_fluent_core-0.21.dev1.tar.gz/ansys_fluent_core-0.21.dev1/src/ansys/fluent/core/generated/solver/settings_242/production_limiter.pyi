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

from .enabled_1 import enabled as enabled_cls
from .clip_factor import clip_factor as clip_factor_cls

class production_limiter(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    clip_factor: clip_factor_cls = ...
