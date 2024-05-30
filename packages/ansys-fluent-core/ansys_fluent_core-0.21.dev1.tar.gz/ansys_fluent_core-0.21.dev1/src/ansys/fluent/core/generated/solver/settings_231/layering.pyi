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

from .use_layering import use_layering as use_layering_cls
from .base_face_zone_for_partitioning import base_face_zone_for_partitioning as base_face_zone_for_partitioning_cls

class layering(Group):
    fluent_name = ...
    child_names = ...
    use_layering: use_layering_cls = ...
    base_face_zone_for_partitioning: base_face_zone_for_partitioning_cls = ...
