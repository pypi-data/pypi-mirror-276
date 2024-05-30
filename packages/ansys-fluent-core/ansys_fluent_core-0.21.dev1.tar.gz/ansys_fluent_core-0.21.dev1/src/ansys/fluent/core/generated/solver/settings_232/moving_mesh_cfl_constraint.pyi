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

from .moving_mesh_constraint import moving_mesh_constraint as moving_mesh_constraint_cls
from .mesh_courant_number import mesh_courant_number as mesh_courant_number_cls

class moving_mesh_cfl_constraint(Group):
    fluent_name = ...
    child_names = ...
    moving_mesh_constraint: moving_mesh_constraint_cls = ...
    mesh_courant_number: mesh_courant_number_cls = ...
