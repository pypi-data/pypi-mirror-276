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

from .blending_factor_1 import blending_factor as blending_factor_cls
from .bin_count import bin_count as bin_count_cls

class pressure_outlet(Group):
    fluent_name = ...
    child_names = ...
    blending_factor: blending_factor_cls = ...
    bin_count: bin_count_cls = ...
