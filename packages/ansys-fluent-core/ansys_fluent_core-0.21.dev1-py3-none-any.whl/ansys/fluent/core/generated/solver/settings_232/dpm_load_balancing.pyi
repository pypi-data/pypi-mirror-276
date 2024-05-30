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

from .load_balancing import load_balancing as load_balancing_cls
from .threshold import threshold as threshold_cls
from .interval import interval as interval_cls

class dpm_load_balancing(Group):
    fluent_name = ...
    child_names = ...
    load_balancing: load_balancing_cls = ...
    threshold: threshold_cls = ...
    interval: interval_cls = ...
