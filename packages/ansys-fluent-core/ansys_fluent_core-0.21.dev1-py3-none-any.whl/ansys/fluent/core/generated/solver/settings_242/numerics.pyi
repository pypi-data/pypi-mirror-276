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

from .tracking_1 import tracking as tracking_cls
from .source_term_settings import source_term_settings as source_term_settings_cls
from .node_based_averaging import node_based_averaging as node_based_averaging_cls
from .dynamic_interaction_range_enabled import dynamic_interaction_range_enabled as dynamic_interaction_range_enabled_cls
from .parcel_count_control import parcel_count_control as parcel_count_control_cls
from .high_res_tracking import high_res_tracking as high_res_tracking_cls

class numerics(Group):
    fluent_name = ...
    child_names = ...
    tracking: tracking_cls = ...
    source_term_settings: source_term_settings_cls = ...
    node_based_averaging: node_based_averaging_cls = ...
    dynamic_interaction_range_enabled: dynamic_interaction_range_enabled_cls = ...
    parcel_count_control: parcel_count_control_cls = ...
    high_res_tracking: high_res_tracking_cls = ...
