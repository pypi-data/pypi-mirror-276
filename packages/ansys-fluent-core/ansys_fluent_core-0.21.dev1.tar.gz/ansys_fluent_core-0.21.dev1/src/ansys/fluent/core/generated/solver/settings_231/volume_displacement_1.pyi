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
from .enable_drag_scaling import enable_drag_scaling as enable_drag_scaling_cls
from .enable_source_term_scaling import enable_source_term_scaling as enable_source_term_scaling_cls

class volume_displacement(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    max_vf_allowed_for_blocking: max_vf_allowed_for_blocking_cls = ...
    enable_drag_scaling: enable_drag_scaling_cls = ...
    enable_source_term_scaling: enable_source_term_scaling_cls = ...
