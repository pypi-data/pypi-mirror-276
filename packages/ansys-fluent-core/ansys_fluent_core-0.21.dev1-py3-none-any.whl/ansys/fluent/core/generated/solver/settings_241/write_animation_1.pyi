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

from .format_name import format_name as format_name_cls
from .file_name import file_name as file_name_cls

class write_animation(Command):
    fluent_name = ...
    argument_names = ...
    format_name: format_name_cls = ...
    file_name: file_name_cls = ...
