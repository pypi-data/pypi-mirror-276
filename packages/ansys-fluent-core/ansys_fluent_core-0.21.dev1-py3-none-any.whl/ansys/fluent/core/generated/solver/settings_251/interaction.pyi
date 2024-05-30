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

from .enabled_2 import enabled as enabled_cls
from .iteration_interval_1 import iteration_interval as iteration_interval_cls
from .update_sources_every_iteration import update_sources_every_iteration as update_sources_every_iteration_cls

class interaction(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    iteration_interval: iteration_interval_cls = ...
    update_sources_every_iteration: update_sources_every_iteration_cls = ...
