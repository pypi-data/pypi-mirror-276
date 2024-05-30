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

from .enabled_11 import enabled as enabled_cls
from .always_use_face_centroid_with_periodics import always_use_face_centroid_with_periodics as always_use_face_centroid_with_periodics_cls
from .flow_interpolation import flow_interpolation as flow_interpolation_cls
from .boundary_layer_tracking_enabled import boundary_layer_tracking_enabled as boundary_layer_tracking_enabled_cls
from .subtet_validity_checking_enabled import subtet_validity_checking_enabled as subtet_validity_checking_enabled_cls
from .auto_intersect_tol_enabled import auto_intersect_tol_enabled as auto_intersect_tol_enabled_cls
from .barycentric_intersection_enabled import barycentric_intersection_enabled as barycentric_intersection_enabled_cls
from .particle_relocation import particle_relocation as particle_relocation_cls
from .stuck_particle_removal_enabled import stuck_particle_removal_enabled as stuck_particle_removal_enabled_cls
from .barycentric_sampling_enabled import barycentric_sampling_enabled as barycentric_sampling_enabled_cls
from .quad_face_centroid_enabled import quad_face_centroid_enabled as quad_face_centroid_enabled_cls

class high_res_tracking(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    always_use_face_centroid_with_periodics: always_use_face_centroid_with_periodics_cls = ...
    flow_interpolation: flow_interpolation_cls = ...
    boundary_layer_tracking_enabled: boundary_layer_tracking_enabled_cls = ...
    subtet_validity_checking_enabled: subtet_validity_checking_enabled_cls = ...
    auto_intersect_tol_enabled: auto_intersect_tol_enabled_cls = ...
    barycentric_intersection_enabled: barycentric_intersection_enabled_cls = ...
    particle_relocation: particle_relocation_cls = ...
    stuck_particle_removal_enabled: stuck_particle_removal_enabled_cls = ...
    barycentric_sampling_enabled: barycentric_sampling_enabled_cls = ...
    quad_face_centroid_enabled: quad_face_centroid_enabled_cls = ...
