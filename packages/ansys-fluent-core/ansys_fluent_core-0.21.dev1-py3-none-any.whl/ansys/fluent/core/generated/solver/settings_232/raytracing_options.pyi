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

from .background_2 import background as background_cls
from .rendering import rendering as rendering_cls
from .display_live_preview import display_live_preview as display_live_preview_cls

class raytracing_options(Group):
    fluent_name = ...
    child_names = ...
    background: background_cls = ...
    rendering: rendering_cls = ...
    command_names = ...

    def display_live_preview(self, ):
        """
        Display the raytracing rendering for the active window.
        """

