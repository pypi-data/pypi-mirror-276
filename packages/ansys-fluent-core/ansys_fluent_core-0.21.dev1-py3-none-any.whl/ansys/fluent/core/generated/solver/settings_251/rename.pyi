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

from .new_1 import new as new_cls
from .old import old as old_cls

class rename(CommandWithPositionalArgs):
    fluent_name = ...
    argument_names = ...
    new: new_cls = ...
    old: old_cls = ...
