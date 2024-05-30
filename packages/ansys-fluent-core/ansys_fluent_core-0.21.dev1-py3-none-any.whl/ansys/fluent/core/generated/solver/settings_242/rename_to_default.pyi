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
from .abbrev import abbrev as abbrev_cls
from .exclude import exclude as exclude_cls

class rename_to_default(Command):
    fluent_name = ...
    argument_names = ...
    zone_name: zone_name_cls = ...
    abbrev: abbrev_cls = ...
    exclude: exclude_cls = ...
