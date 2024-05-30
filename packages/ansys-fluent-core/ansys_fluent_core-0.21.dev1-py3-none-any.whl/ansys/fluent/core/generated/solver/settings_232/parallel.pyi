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

from .option_5 import option as option_cls
from .expert_options import expert_options as expert_options_cls
from .hybrid_options import hybrid_options as hybrid_options_cls

class parallel(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    expert_options: expert_options_cls = ...
    hybrid_options: hybrid_options_cls = ...
