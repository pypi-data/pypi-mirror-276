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

from .general_nrbc import general_nrbc as general_nrbc_cls
from .turbo_sepcific_nrbc import turbo_sepcific_nrbc as turbo_sepcific_nrbc_cls

class non_reflecting_bc(Group):
    fluent_name = ...
    child_names = ...
    general_nrbc: general_nrbc_cls = ...
    turbo_sepcific_nrbc: turbo_sepcific_nrbc_cls = ...
