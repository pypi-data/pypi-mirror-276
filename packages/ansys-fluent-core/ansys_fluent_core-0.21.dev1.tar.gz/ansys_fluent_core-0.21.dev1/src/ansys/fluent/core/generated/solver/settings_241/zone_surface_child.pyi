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

from .name import name as name_cls
from .zone_name_1 import zone_name as zone_name_cls
from .display_3 import display as display_cls

class zone_surface_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    zone_name: zone_name_cls = ...
    command_names = ...

    def display(self, ):
        """
        'display' command.
        """

