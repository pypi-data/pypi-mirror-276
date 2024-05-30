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

from .compute_statistics import compute_statistics as compute_statistics_cls
from .statistics_level import statistics_level as statistics_level_cls

class miscellaneous(Group):
    fluent_name = ...
    child_names = ...
    compute_statistics: compute_statistics_cls = ...
    statistics_level: statistics_level_cls = ...
