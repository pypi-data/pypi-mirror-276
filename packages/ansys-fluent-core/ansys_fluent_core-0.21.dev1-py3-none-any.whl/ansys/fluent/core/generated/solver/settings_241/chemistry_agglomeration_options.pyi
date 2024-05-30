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

from .chemistry_agglomeration_error_tolerance import chemistry_agglomeration_error_tolerance as chemistry_agglomeration_error_tolerance_cls
from .chemistry_agglomeration_temperature_bin import chemistry_agglomeration_temperature_bin as chemistry_agglomeration_temperature_bin_cls

class chemistry_agglomeration_options(Group):
    fluent_name = ...
    child_names = ...
    chemistry_agglomeration_error_tolerance: chemistry_agglomeration_error_tolerance_cls = ...
    chemistry_agglomeration_temperature_bin: chemistry_agglomeration_temperature_bin_cls = ...
