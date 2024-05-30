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

from .delete_all_1 import delete_all as delete_all_cls
from .name_5 import name as name_cls

class delete(CommandWithPositionalArgs):
    fluent_name = ...
    argument_names = ...
    delete_all: delete_all_cls = ...
    name: name_cls = ...
