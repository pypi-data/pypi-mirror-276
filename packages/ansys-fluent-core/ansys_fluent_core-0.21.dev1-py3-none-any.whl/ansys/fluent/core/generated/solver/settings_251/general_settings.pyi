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

from .interaction import interaction as interaction_cls
from .unsteady_tracking import unsteady_tracking as unsteady_tracking_cls
from .contour_plotting import contour_plotting as contour_plotting_cls

class general_settings(Group):
    fluent_name = ...
    child_names = ...
    interaction: interaction_cls = ...
    unsteady_tracking: unsteady_tracking_cls = ...
    contour_plotting: contour_plotting_cls = ...
