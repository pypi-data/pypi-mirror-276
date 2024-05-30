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

from .enabled_8 import enabled as enabled_cls
from .blocking_max_vol_frac import blocking_max_vol_frac as blocking_max_vol_frac_cls
from .drag_scaling_enabled import drag_scaling_enabled as drag_scaling_enabled_cls
from .mom_source_scaling_enabled import mom_source_scaling_enabled as mom_source_scaling_enabled_cls
from .other_source_scaling_enabled import other_source_scaling_enabled as other_source_scaling_enabled_cls

class volume_displacement(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    blocking_max_vol_frac: blocking_max_vol_frac_cls = ...
    drag_scaling_enabled: drag_scaling_enabled_cls = ...
    mom_source_scaling_enabled: mom_source_scaling_enabled_cls = ...
    other_source_scaling_enabled: other_source_scaling_enabled_cls = ...
