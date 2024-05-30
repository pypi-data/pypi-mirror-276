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

from .relaxation_factor_child import relaxation_factor_child


class global_dt_pseudo_relax(NamedObject[relaxation_factor_child], _CreatableNamedObjectMixin[relaxation_factor_child]):
    fluent_name = ...
    child_object_type = ...
