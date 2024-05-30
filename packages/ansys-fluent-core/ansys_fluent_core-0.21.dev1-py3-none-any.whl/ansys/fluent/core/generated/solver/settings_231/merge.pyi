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

from .merge_small_regions import merge_small_regions as merge_small_regions_cls
from .max_merge_iterations import max_merge_iterations as max_merge_iterations_cls

class merge(Group):
    fluent_name = ...
    child_names = ...
    merge_small_regions: merge_small_regions_cls = ...
    max_merge_iterations: max_merge_iterations_cls = ...
