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

from .method_3 import method as method_cls
from .injection_hole import injection_hole as injection_hole_cls

class holes_setup(Group):
    fluent_name = ...
    child_names = ...
    method: method_cls = ...
    injection_hole: injection_hole_cls = ...
