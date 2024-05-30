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

from .relaxation_factor_2 import relaxation_factor as relaxation_factor_cls
from .select_variables import select_variables as select_variables_cls
from .relaxation_options import relaxation_options as relaxation_options_cls

class options(Group):
    fluent_name = ...
    child_names = ...
    relaxation_factor: relaxation_factor_cls = ...
    select_variables: select_variables_cls = ...
    relaxation_options: relaxation_options_cls = ...
