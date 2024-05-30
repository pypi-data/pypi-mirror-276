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

from .command_list import command_list as command_list_cls
from .filename import filename as filename_cls

class export_modifications(Command):
    fluent_name = ...
    argument_names = ...
    command_list: command_list_cls = ...
    filename: filename_cls = ...
