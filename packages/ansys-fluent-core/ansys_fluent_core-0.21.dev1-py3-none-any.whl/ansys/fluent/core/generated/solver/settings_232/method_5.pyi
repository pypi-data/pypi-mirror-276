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

from .partition_method import partition_method as partition_method_cls
from .count import count as count_cls

class method(Command):
    fluent_name = ...
    argument_names = ...
    partition_method: partition_method_cls = ...
    count: count_cls = ...
