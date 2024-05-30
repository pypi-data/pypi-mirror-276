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

from .flow_rate import flow_rate as flow_rate_cls
from .flow_rate_2 import flow_rate_2 as flow_rate_2_cls
from .total_flow_rate import total_flow_rate as total_flow_rate_cls
from .scale_by_area import scale_by_area as scale_by_area_cls

class flow_rate(Group):
    fluent_name = ...
    child_names = ...
    flow_rate: flow_rate_cls = ...
    flow_rate_2: flow_rate_2_cls = ...
    total_flow_rate: total_flow_rate_cls = ...
    scale_by_area: scale_by_area_cls = ...
