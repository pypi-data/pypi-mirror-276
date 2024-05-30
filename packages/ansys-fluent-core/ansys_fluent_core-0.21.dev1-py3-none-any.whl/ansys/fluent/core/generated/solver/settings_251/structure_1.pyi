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

from .x_disp_boundary_condition import x_disp_boundary_condition as x_disp_boundary_condition_cls
from .x_disp_boundary_value import x_disp_boundary_value as x_disp_boundary_value_cls
from .y_disp_boundary_condition import y_disp_boundary_condition as y_disp_boundary_condition_cls
from .y_disp_boundary_value import y_disp_boundary_value as y_disp_boundary_value_cls
from .z_disp_boundary_condition import z_disp_boundary_condition as z_disp_boundary_condition_cls
from .z_disp_boundary_value import z_disp_boundary_value as z_disp_boundary_value_cls

class structure(Group):
    fluent_name = ...
    child_names = ...
    x_disp_boundary_condition: x_disp_boundary_condition_cls = ...
    x_disp_boundary_value: x_disp_boundary_value_cls = ...
    y_disp_boundary_condition: y_disp_boundary_condition_cls = ...
    y_disp_boundary_value: y_disp_boundary_value_cls = ...
    z_disp_boundary_condition: z_disp_boundary_condition_cls = ...
    z_disp_boundary_value: z_disp_boundary_value_cls = ...
