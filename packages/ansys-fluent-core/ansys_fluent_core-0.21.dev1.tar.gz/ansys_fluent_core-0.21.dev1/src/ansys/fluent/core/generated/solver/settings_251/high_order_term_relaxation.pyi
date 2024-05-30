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

from .enable_16 import enable as enable_cls
from .options_7 import options as options_cls

class high_order_term_relaxation(Group):
    fluent_name = ...
    child_names = ...
    enable: enable_cls = ...
    options: options_cls = ...
