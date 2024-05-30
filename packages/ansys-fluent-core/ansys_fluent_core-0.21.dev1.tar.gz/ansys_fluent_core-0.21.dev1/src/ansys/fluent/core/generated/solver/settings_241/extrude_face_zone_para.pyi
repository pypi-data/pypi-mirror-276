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

from .face_zone import face_zone as face_zone_cls
from .normal_distance import normal_distance as normal_distance_cls
from .parametric_coordinates import parametric_coordinates as parametric_coordinates_cls

class extrude_face_zone_para(Command):
    fluent_name = ...
    argument_names = ...
    face_zone: face_zone_cls = ...
    normal_distance: normal_distance_cls = ...
    parametric_coordinates: parametric_coordinates_cls = ...
