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

from .always_use_face_centroid_with_periodics import always_use_face_centroid_with_periodics as always_use_face_centroid_with_periodics_cls
from .interpolation import interpolation as interpolation_cls
from .boundary_layer_tracking import boundary_layer_tracking as boundary_layer_tracking_cls
from .check_subtet_validity import check_subtet_validity as check_subtet_validity_cls
from .use_automatic_intersection_tolerance import use_automatic_intersection_tolerance as use_automatic_intersection_tolerance_cls
from .use_barycentric_intersection import use_barycentric_intersection as use_barycentric_intersection_cls
from .particle_relocation import particle_relocation as particle_relocation_cls
from .remove_stuck_particles import remove_stuck_particles as remove_stuck_particles_cls
from .use_barycentric_sampling import use_barycentric_sampling as use_barycentric_sampling_cls
from .use_quad_face_centroid import use_quad_face_centroid as use_quad_face_centroid_cls

class high_res_tracking_options(Group):
    fluent_name = ...
    child_names = ...
    always_use_face_centroid_with_periodics: always_use_face_centroid_with_periodics_cls = ...
    interpolation: interpolation_cls = ...
    boundary_layer_tracking: boundary_layer_tracking_cls = ...
    check_subtet_validity: check_subtet_validity_cls = ...
    use_automatic_intersection_tolerance: use_automatic_intersection_tolerance_cls = ...
    use_barycentric_intersection: use_barycentric_intersection_cls = ...
    particle_relocation: particle_relocation_cls = ...
    remove_stuck_particles: remove_stuck_particles_cls = ...
    use_barycentric_sampling: use_barycentric_sampling_cls = ...
    use_quad_face_centroid: use_quad_face_centroid_cls = ...
