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

from .field import field as field_cls
from .options_7 import options as options_cls
from .enabled_2 import enabled as enabled_cls
from .filter_minimum import filter_minimum as filter_minimum_cls
from .filter_maximum import filter_maximum as filter_maximum_cls

class filter_settings(Group):
    fluent_name = ...
    child_names = ...
    field: field_cls = ...
    options: options_cls = ...
    enabled: enabled_cls = ...
    filter_minimum: filter_minimum_cls = ...
    filter_maximum: filter_maximum_cls = ...
