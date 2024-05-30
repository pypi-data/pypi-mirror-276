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

from .allow_repair_at_boundaries import allow_repair_at_boundaries as allow_repair_at_boundaries_cls
from .include_local_polyhedra_conversion_in_repair import include_local_polyhedra_conversion_in_repair as include_local_polyhedra_conversion_in_repair_cls
from .repair_poor_elements import repair_poor_elements as repair_poor_elements_cls
from .improve_quality import improve_quality as improve_quality_cls
from .repair import repair as repair_cls
from .repair_face_handedness import repair_face_handedness as repair_face_handedness_cls
from .repair_face_node_order import repair_face_node_order as repair_face_node_order_cls
from .repair_wall_distance import repair_wall_distance as repair_wall_distance_cls

class repair_improve(Group):
    fluent_name = ...
    child_names = ...
    allow_repair_at_boundaries: allow_repair_at_boundaries_cls = ...
    include_local_polyhedra_conversion_in_repair: include_local_polyhedra_conversion_in_repair_cls = ...
    command_names = ...

    def repair_poor_elements(self, ):
        """
        Report invalid and poor quality elements.
        """

    def improve_quality(self, ):
        """
        Tries to improve the mesh quality.
        """

    def repair(self, ):
        """
        Tries to repair mesh problems identified by mesh check.
        """

    def repair_face_handedness(self, repair: bool, disable_repair: bool):
        """
        Correct face handedness at left handed faces if possible.
        
        Parameters
        ----------
            repair : bool
                'repair' child.
            disable_repair : bool
                'disable_repair' child.
        
        """

    def repair_face_node_order(self, ):
        """
        Reverse order of face nodes if needed.
        """

    def repair_wall_distance(self, repair: bool):
        """
        Correct wall distance at very high aspect ratio hexahedral/polyhedral cells.
        
        Parameters
        ----------
            repair : bool
                'repair' child.
        
        """

