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

from .name import name as name_cls
from .field_1 import field as field_cls
from .surfaces_5 import surfaces as surfaces_cls
from .min_3 import min as min_cls
from .max_3 import max as max_cls
from .display_3 import display as display_cls

class iso_clip_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    field: field_cls = ...
    surfaces: surfaces_cls = ...
    min: min_cls = ...
    max: max_cls = ...
    command_names = ...

    def display(self, ):
        """
        'display' command.
        """

