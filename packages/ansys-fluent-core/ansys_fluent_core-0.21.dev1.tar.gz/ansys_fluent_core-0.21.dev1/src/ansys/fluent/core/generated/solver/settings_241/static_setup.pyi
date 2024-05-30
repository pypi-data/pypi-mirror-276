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

from .method_7 import method as method_cls
from .static_injection import static_injection as static_injection_cls

class static_setup(Group):
    fluent_name = ...
    child_names = ...
    method: method_cls = ...
    static_injection: static_injection_cls = ...
