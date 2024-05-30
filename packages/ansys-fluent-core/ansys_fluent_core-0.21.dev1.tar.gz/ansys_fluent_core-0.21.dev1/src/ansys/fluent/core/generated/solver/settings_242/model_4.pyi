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

from .type_12 import type as type_cls
from .settings_6 import settings as settings_cls
from .offline_training import offline_training as offline_training_cls
from .management import management as management_cls
from .default_8 import default as default_cls
from .unhook import unhook as unhook_cls

class model(Group):
    fluent_name = ...
    child_names = ...
    type: type_cls = ...
    settings: settings_cls = ...
    offline_training: offline_training_cls = ...
    management: management_cls = ...
    command_names = ...

    def default(self, ):
        """
        Use the default model and training parameters settings.
        """

    def unhook(self, ):
        """
        Unhook the model related to turbulence model optimizer.
        """

