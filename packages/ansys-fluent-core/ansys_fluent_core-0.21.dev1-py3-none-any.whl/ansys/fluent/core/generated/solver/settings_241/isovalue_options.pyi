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

from .hide_volume import hide_volume as hide_volume_cls
from .settings_3 import settings as settings_cls
from .reset_1 import reset as reset_cls

class isovalue_options(Group):
    fluent_name = ...
    child_names = ...
    hide_volume: hide_volume_cls = ...
    settings: settings_cls = ...
    command_names = ...

    def reset(self, ):
        """
        'reset' command.
        """

