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

from .enabled_2 import enabled as enabled_cls
from .option_name import option_name as option_name_cls

class enable_motion_transfer_across_interfaces(Command):
    fluent_name = ...
    argument_names = ...
    enabled: enabled_cls = ...
    option_name: option_name_cls = ...
