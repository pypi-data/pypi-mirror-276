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

from .player import player as player_cls
from .start_frame_1 import start_frame as start_frame_cls
from .end_frame_1 import end_frame as end_frame_cls
from .increment_1 import increment as increment_cls
from .playback_mode import playback_mode as playback_mode_cls
from .speed_1 import speed as speed_cls

class play(Command):
    fluent_name = ...
    argument_names = ...
    player: player_cls = ...
    start_frame: start_frame_cls = ...
    end_frame: end_frame_cls = ...
    increment: increment_cls = ...
    playback_mode: playback_mode_cls = ...
    speed: speed_cls = ...
