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

from .refinement_criteria import refinement_criteria as refinement_criteria_cls
from .coarsening_criteria import coarsening_criteria as coarsening_criteria_cls
from .manual_refinement_criteria import manual_refinement_criteria as manual_refinement_criteria_cls
from .manual_coarsening_criteria import manual_coarsening_criteria as manual_coarsening_criteria_cls
from .set import set as set_cls
from .profile import profile as profile_cls
from .free_hierarchy import free_hierarchy as free_hierarchy_cls
from .multi_layer_refinement import multi_layer_refinement as multi_layer_refinement_cls
from .geometry import geometry as geometry_cls
from .adapt_mesh import adapt_mesh as adapt_mesh_cls
from .display_adaption_cells import display_adaption_cells as display_adaption_cells_cls
from .list_adaption_cells import list_adaption_cells as list_adaption_cells_cls

class adapt(Group):
    fluent_name = ...
    child_names = ...
    refinement_criteria: refinement_criteria_cls = ...
    coarsening_criteria: coarsening_criteria_cls = ...
    manual_refinement_criteria: manual_refinement_criteria_cls = ...
    manual_coarsening_criteria: manual_coarsening_criteria_cls = ...
    set: set_cls = ...
    profile: profile_cls = ...
    free_hierarchy: free_hierarchy_cls = ...
    multi_layer_refinement: multi_layer_refinement_cls = ...
    geometry: geometry_cls = ...
    command_names = ...

    def adapt_mesh(self, ):
        """
        Adapt the mesh based on set refinement/coarsening criterion.
        """

    def display_adaption_cells(self, ):
        """
        Display cells marked for refinement/coarsening.
        """

    def list_adaption_cells(self, ):
        """
        List the number of cells marked for refinement/coarsening.
        """

