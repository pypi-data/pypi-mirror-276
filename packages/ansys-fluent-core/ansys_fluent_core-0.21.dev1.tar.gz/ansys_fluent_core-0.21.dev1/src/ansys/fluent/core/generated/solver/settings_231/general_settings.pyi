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

from .contour_plotting_option import contour_plotting_option as contour_plotting_option_cls
from .interaction import interaction as interaction_cls
from .unsteady_tracking import unsteady_tracking as unsteady_tracking_cls

class general_settings(Group):
    fluent_name = ...
    child_names = ...
    contour_plotting_option: contour_plotting_option_cls = ...
    interaction: interaction_cls = ...
    unsteady_tracking: unsteady_tracking_cls = ...
