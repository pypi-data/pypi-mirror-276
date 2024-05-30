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

from .fixed import fixed as fixed_cls
from .cylindrical_fixed_var import cylindrical_fixed_var as cylindrical_fixed_var_cls
from .fixes import fixes as fixes_cls

class fixed_values(Group):
    fluent_name = ...
    child_names = ...
    fixed: fixed_cls = ...
    cylindrical_fixed_var: cylindrical_fixed_var_cls = ...
    fixes: fixes_cls = ...
