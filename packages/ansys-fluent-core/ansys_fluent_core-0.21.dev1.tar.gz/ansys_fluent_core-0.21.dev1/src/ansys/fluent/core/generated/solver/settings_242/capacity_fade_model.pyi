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

from .enabled_25 import enabled as enabled_cls
from .capacity_fade_table import capacity_fade_table as capacity_fade_table_cls

class capacity_fade_model(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    capacity_fade_table: capacity_fade_table_cls = ...
