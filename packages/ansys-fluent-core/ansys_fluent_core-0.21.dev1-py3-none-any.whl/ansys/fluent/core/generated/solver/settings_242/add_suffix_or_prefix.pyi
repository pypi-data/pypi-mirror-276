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
from .append import append as append_cls
from .text import text as text_cls

class add_suffix_or_prefix(Command):
    fluent_name = ...
    argument_names = ...
    zone_name: zone_name_cls = ...
    append: append_cls = ...
    text: text_cls = ...
