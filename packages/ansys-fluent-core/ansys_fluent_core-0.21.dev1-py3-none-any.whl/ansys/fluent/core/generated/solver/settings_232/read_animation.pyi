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

from .read_from_file import read_from_file as read_from_file_cls
from .animation_file_name import animation_file_name as animation_file_name_cls
from .select_from_available import select_from_available as select_from_available_cls
from .animation_name import animation_name as animation_name_cls

class read_animation(Command):
    fluent_name = ...
    argument_names = ...
    read_from_file: read_from_file_cls = ...
    animation_file_name: animation_file_name_cls = ...
    select_from_available: select_from_available_cls = ...
    animation_name: animation_name_cls = ...
