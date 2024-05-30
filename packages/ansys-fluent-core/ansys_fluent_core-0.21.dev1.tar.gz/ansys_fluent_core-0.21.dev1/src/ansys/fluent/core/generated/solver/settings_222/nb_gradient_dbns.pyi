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

from .boundary_treatment import boundary_treatment as boundary_treatment_cls
from .extended_boundary_treatment import extended_boundary_treatment as extended_boundary_treatment_cls

class nb_gradient_dbns(Group):
    fluent_name = ...
    child_names = ...
    boundary_treatment: boundary_treatment_cls = ...
    extended_boundary_treatment: extended_boundary_treatment_cls = ...
