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

from .high_order_pressure import high_order_pressure as high_order_pressure_cls
from .interpolation_method import interpolation_method as interpolation_method_cls
from .orphan_cell_treatment import orphan_cell_treatment as orphan_cell_treatment_cls
from .expert_6 import expert as expert_cls

class overset(Group):
    fluent_name = ...
    child_names = ...
    high_order_pressure: high_order_pressure_cls = ...
    interpolation_method: interpolation_method_cls = ...
    orphan_cell_treatment: orphan_cell_treatment_cls = ...
    expert: expert_cls = ...
