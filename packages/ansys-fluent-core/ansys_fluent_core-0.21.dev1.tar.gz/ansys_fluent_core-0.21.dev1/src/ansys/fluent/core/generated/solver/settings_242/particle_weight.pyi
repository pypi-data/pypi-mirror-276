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

from .use import use as use_cls
from .user_defined_7 import user_defined as user_defined_cls
from .value_2 import value as value_cls
from .hybrid_optimization import hybrid_optimization as hybrid_optimization_cls

class particle_weight(Group):
    fluent_name = ...
    child_names = ...
    use: use_cls = ...
    user_defined: user_defined_cls = ...
    value: value_cls = ...
    hybrid_optimization: hybrid_optimization_cls = ...
