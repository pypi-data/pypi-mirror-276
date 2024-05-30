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

from .zone_name_4 import zone_name as zone_name_cls
from .shadow_zone_name import shadow_zone_name as shadow_zone_name_cls
from .rotate_periodic import rotate_periodic as rotate_periodic_cls
from .create import create as create_cls
from .auto_translation import auto_translation as auto_translation_cls
from .direction import direction as direction_cls

class make_periodic(Command):
    fluent_name = ...
    argument_names = ...
    zone_name: zone_name_cls = ...
    shadow_zone_name: shadow_zone_name_cls = ...
    rotate_periodic: rotate_periodic_cls = ...
    create: create_cls = ...
    auto_translation: auto_translation_cls = ...
    direction: direction_cls = ...
