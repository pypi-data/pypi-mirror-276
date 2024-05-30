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

from .ambient_color import ambient_color as ambient_color_cls
from .headlight_setting import headlight_setting as headlight_setting_cls
from .lights_on import lights_on as lights_on_cls
from .lighting_interpolation import lighting_interpolation as lighting_interpolation_cls
from .set_light import set_light as set_light_cls

class lights(Group):
    fluent_name = ...
    child_names = ...
    ambient_color: ambient_color_cls = ...
    headlight_setting: headlight_setting_cls = ...
    lights_on: lights_on_cls = ...
    lighting_interpolation: lighting_interpolation_cls = ...
    command_names = ...

    def set_light(self, light_number: int, light_on: bool, rgb_vector: List[Union[float, str]], use_view_factor: bool, change_light_direction: bool, direction_vector: List[Union[float, str]]):
        """
        'set_light' command.
        
        Parameters
        ----------
            light_number : int
                'light_number' child.
            light_on : bool
                'light_on' child.
            rgb_vector : typing.List[real]
                'rgb_vector' child.
            use_view_factor : bool
                'use_view_factor' child.
            change_light_direction : bool
                'change_light_direction' child.
            direction_vector : typing.List[real]
                'direction_vector' child.
        
        """

