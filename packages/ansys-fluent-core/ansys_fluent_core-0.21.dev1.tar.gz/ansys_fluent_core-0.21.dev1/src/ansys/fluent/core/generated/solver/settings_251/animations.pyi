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

from .playback import playback as playback_cls
from .scene_animation import scene_animation as scene_animation_cls

class animations(Group):
    fluent_name = ...
    child_names = ...
    playback: playback_cls = ...
    scene_animation: scene_animation_cls = ...
