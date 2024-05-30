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

from .active_zone import active_zone as active_zone_cls
from .passive_zone import passive_zone as passive_zone_cls
from .positive_tab import positive_tab as positive_tab_cls
from .negative_tab import negative_tab as negative_tab_cls
from .virtual_connection import virtual_connection as virtual_connection_cls
from .print_battery_connection import print_battery_connection as print_battery_connection_cls

class zone_assignment(Group):
    fluent_name = ...
    child_names = ...
    active_zone: active_zone_cls = ...
    passive_zone: passive_zone_cls = ...
    positive_tab: positive_tab_cls = ...
    negative_tab: negative_tab_cls = ...
    command_names = ...

    def virtual_connection(self, enabled: bool, file_name: str):
        """
        'virtual_connection' command.
        
        Parameters
        ----------
            enabled : bool
                'enabled' child.
            file_name : str
                'file_name' child.
        
        """

    def print_battery_connection(self, ):
        """
        Print battery connection information.
        """

