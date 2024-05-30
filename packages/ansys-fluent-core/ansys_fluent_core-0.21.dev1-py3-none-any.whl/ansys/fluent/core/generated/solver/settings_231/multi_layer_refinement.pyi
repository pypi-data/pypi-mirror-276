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

from .refine_mesh import refine_mesh as refine_mesh_cls
from .boundary_zones import boundary_zones as boundary_zones_cls
from .layer_count import layer_count as layer_count_cls
from .parameters import parameters as parameters_cls

class multi_layer_refinement(Group):
    fluent_name = ...
    command_names = ...

    def refine_mesh(self, ):
        """
        Refine the mesh for multiple boundary layers.
        """

    def boundary_zones(self, ):
        """
        Specify boundary zones for refinement.
        """

    def layer_count(self, ):
        """
        Specify the layer count for refinement.
        """

    def parameters(self, ):
        """
        Specify parameters for multiple boundary layer refinement.
        """

