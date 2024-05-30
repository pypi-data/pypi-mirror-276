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

from .settings_2 import settings as settings_cls
from .reset_1 import reset as reset_cls
from .invert import invert as invert_cls

class transparency_options(Group):
    fluent_name = ...
    child_names = ...
    settings: settings_cls = ...
    command_names = ...

    def reset(self, ):
        """
        'reset' command.
        """

    def invert(self, ):
        """
        'invert' command.
        """

