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

from .volumes import volumes as volumes_cls
from .interfaces import interfaces as interfaces_cls
from .list_physics import list_physics as list_physics_cls

class physics(Group):
    fluent_name = ...
    child_names = ...
    volumes: volumes_cls = ...
    interfaces: interfaces_cls = ...
    command_names = ...

    def list_physics(self, ):
        """
        'list_physics' command.
        """

