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

from .option_3 import option as option_cls
from .default import default as default_cls
from .reverse import reverse as reverse_cls

class curve_length(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    default: default_cls = ...
    reverse: reverse_cls = ...
