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

from .zone_1 import zone as zone_cls
from .y_axis_function_1 import y_axis_function as y_axis_function_cls
from .x_axis_function_2 import x_axis_function as x_axis_function_cls
from .axes import axes as axes_cls
from .curves import curves as curves_cls
from .plot_10 import plot as plot_cls

class interpolated_data(Group):
    fluent_name = ...
    child_names = ...
    zone: zone_cls = ...
    y_axis_function: y_axis_function_cls = ...
    x_axis_function: x_axis_function_cls = ...
    axes: axes_cls = ...
    curves: curves_cls = ...
    command_names = ...

    def plot(self, ):
        """
        Plot interpolated data.
        """

