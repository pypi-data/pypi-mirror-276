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

from .enhanced_method_enabled import enhanced_method_enabled as enhanced_method_enabled_cls
from .support_for_std_track_data_read_enabled import support_for_std_track_data_read_enabled as support_for_std_track_data_read_enabled_cls
from .overset_robustness_level import overset_robustness_level as overset_robustness_level_cls
from .legacy_method_enabled import legacy_method_enabled as legacy_method_enabled_cls

class particle_relocation(Group):
    fluent_name = ...
    child_names = ...
    enhanced_method_enabled: enhanced_method_enabled_cls = ...
    support_for_std_track_data_read_enabled: support_for_std_track_data_read_enabled_cls = ...
    overset_robustness_level: overset_robustness_level_cls = ...
    legacy_method_enabled: legacy_method_enabled_cls = ...
