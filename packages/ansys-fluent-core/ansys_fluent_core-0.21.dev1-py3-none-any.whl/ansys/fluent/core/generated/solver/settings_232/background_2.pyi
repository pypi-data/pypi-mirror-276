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

from .hide_environment_keep_effects import hide_environment_keep_effects as hide_environment_keep_effects_cls
from .environment_image import environment_image as environment_image_cls
from .latitude_1 import latitude as latitude_cls
from .longitude_1 import longitude as longitude_cls
from .view_zoom import view_zoom as view_zoom_cls
from .show_backplate import show_backplate as show_backplate_cls
from .backplate_color import backplate_color as backplate_color_cls
from .backplate_image import backplate_image as backplate_image_cls

class background(Group):
    fluent_name = ...
    child_names = ...
    hide_environment_keep_effects: hide_environment_keep_effects_cls = ...
    environment_image: environment_image_cls = ...
    latitude: latitude_cls = ...
    longitude: longitude_cls = ...
    view_zoom: view_zoom_cls = ...
    show_backplate: show_backplate_cls = ...
    backplate_color: backplate_color_cls = ...
    backplate_image: backplate_image_cls = ...
