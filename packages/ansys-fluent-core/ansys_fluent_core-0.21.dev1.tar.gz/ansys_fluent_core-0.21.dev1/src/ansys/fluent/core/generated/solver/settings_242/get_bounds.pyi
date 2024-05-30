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

from .bounded_zones import bounded_zones as bounded_zones_cls
from .comfortable_region import comfortable_region as comfortable_region_cls
from .automatic_coordinate import automatic_coordinate as automatic_coordinate_cls

class get_bounds(Command):
    fluent_name = ...
    argument_names = ...
    bounded_zones: bounded_zones_cls = ...
    comfortable_region: comfortable_region_cls = ...
    automatic_coordinate: automatic_coordinate_cls = ...
