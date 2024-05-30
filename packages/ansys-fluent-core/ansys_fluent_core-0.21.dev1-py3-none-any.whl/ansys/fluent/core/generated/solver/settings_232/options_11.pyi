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

from .option import option as option_cls
from .inside_1 import inside as inside_cls
from .outside import outside as outside_cls

class options(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    inside: inside_cls = ...
    outside: outside_cls = ...
