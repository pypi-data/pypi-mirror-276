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

from .riemann_invariants_tangency_correction import riemann_invariants_tangency_correction as riemann_invariants_tangency_correction_cls
from .type_3 import type as type_cls

class pressure_far_field(Group):
    fluent_name = ...
    child_names = ...
    riemann_invariants_tangency_correction: riemann_invariants_tangency_correction_cls = ...
    type: type_cls = ...
