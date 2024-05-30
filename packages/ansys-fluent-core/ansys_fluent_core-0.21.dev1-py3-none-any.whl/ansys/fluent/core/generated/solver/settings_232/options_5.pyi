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

from .relaxation_factor import relaxation_factor as relaxation_factor_cls
from .select_variables import select_variables as select_variables_cls
from .type_6 import type as type_cls

class options(Group):
    fluent_name = ...
    child_names = ...
    relaxation_factor: relaxation_factor_cls = ...
    select_variables: select_variables_cls = ...
    type: type_cls = ...
