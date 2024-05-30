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

from .zone_name_8 import zone_name as zone_name_cls
from .abbreviate_types import abbreviate_types as abbreviate_types_cls
from .exclude import exclude as exclude_cls

class rename_by_adjacency(Command):
    fluent_name = ...
    argument_names = ...
    zone_name: zone_name_cls = ...
    abbreviate_types: abbreviate_types_cls = ...
    exclude: exclude_cls = ...
