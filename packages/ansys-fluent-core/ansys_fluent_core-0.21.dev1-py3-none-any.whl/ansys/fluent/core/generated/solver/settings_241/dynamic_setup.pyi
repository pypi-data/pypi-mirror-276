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

from .method_6 import method as method_cls
from .dynamic_injection import dynamic_injection as dynamic_injection_cls

class dynamic_setup(Group):
    fluent_name = ...
    child_names = ...
    method: method_cls = ...
    dynamic_injection: dynamic_injection_cls = ...
