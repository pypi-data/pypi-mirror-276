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

from .same_for_active_enabled import same_for_active_enabled as same_for_active_enabled_cls
from .energy_source_same_active import energy_source_same_active as energy_source_same_active_cls
from .energy_source_active import energy_source_active as energy_source_active_cls
from .tab_elec_current import tab_elec_current as tab_elec_current_cls

class cht_model_settings(Group):
    fluent_name = ...
    child_names = ...
    same_for_active_enabled: same_for_active_enabled_cls = ...
    energy_source_same_active: energy_source_same_active_cls = ...
    energy_source_active: energy_source_active_cls = ...
    tab_elec_current: tab_elec_current_cls = ...
