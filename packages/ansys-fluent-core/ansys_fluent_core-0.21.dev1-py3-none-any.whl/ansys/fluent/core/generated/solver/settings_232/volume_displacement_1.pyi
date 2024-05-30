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

from .option_9 import option as option_cls
from .max_vf_allowed_for_blocking import max_vf_allowed_for_blocking as max_vf_allowed_for_blocking_cls
from .drag_scaling_enabled import drag_scaling_enabled as drag_scaling_enabled_cls
from .source_term_scaling_enabled import source_term_scaling_enabled as source_term_scaling_enabled_cls

class volume_displacement(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    max_vf_allowed_for_blocking: max_vf_allowed_for_blocking_cls = ...
    drag_scaling_enabled: drag_scaling_enabled_cls = ...
    source_term_scaling_enabled: source_term_scaling_enabled_cls = ...
