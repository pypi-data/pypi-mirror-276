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

from .enabled_10 import enabled as enabled_cls
from .source_avg_enabled import source_avg_enabled as source_avg_enabled_cls
from .average_every_step import average_every_step as average_every_step_cls
from .kernel import kernel as kernel_cls

class node_based_averaging(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    source_avg_enabled: source_avg_enabled_cls = ...
    average_every_step: average_every_step_cls = ...
    kernel: kernel_cls = ...
