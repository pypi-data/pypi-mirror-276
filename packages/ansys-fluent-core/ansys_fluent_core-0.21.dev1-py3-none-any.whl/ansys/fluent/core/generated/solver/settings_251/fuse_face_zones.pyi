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

from .zone_names import zone_names as zone_names_cls
from .zone_name import zone_name as zone_name_cls

class fuse_face_zones(Command):
    fluent_name = ...
    argument_names = ...
    zone_names: zone_names_cls = ...
    zone_name: zone_name_cls = ...
