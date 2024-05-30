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

from .option_9 import option as option_cls
from .hybrid import hybrid as hybrid_cls
from .expert_2 import expert as expert_cls

class parallel(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    hybrid: hybrid_cls = ...
    expert: expert_cls = ...
