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

from .type import type as type_cls
from .layer_count import layer_count as layer_count_cls
from .boundary_list import boundary_list as boundary_list_cls
from .refine_mesh import refine_mesh as refine_mesh_cls

class multi_layer_refinement(Group):
    fluent_name = ...
    child_names = ...
    type: type_cls = ...
    layer_count: layer_count_cls = ...
    boundary_list: boundary_list_cls = ...
    command_names = ...

    def refine_mesh(self, ):
        """
        Refine the mesh for multiple boundary layers.
        """

