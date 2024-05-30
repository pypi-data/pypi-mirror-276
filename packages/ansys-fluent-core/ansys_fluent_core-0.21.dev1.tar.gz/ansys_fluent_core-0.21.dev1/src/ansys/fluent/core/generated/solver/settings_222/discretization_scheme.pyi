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

from .uds_bc_child import uds_bc_child


class discretization_scheme(NamedObject[uds_bc_child], _CreatableNamedObjectMixin[uds_bc_child]):
    fluent_name = ...
    child_object_type = ...
