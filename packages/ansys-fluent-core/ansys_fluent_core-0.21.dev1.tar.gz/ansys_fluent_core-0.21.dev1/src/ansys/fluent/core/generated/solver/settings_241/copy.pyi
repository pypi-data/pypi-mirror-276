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

from .orig_beam_name import orig_beam_name as orig_beam_name_cls
from .beam_name import beam_name as beam_name_cls
from .ap_face_zone import ap_face_zone as ap_face_zone_cls
from .beam_length import beam_length as beam_length_cls
from .ray_npoints import ray_npoints as ray_npoints_cls
from .x_beam_vector import x_beam_vector as x_beam_vector_cls
from .y_beam_vector import y_beam_vector as y_beam_vector_cls
from .z_beam_vector import z_beam_vector as z_beam_vector_cls

class copy(Command):
    fluent_name = ...
    argument_names = ...
    orig_beam_name: orig_beam_name_cls = ...
    beam_name: beam_name_cls = ...
    ap_face_zone: ap_face_zone_cls = ...
    beam_length: beam_length_cls = ...
    ray_npoints: ray_npoints_cls = ...
    x_beam_vector: x_beam_vector_cls = ...
    y_beam_vector: y_beam_vector_cls = ...
    z_beam_vector: z_beam_vector_cls = ...
