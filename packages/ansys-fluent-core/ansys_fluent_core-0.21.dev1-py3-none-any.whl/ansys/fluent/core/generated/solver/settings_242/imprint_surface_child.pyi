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
from .surface_3 import surface as surface_cls
from .zones_5 import zones as zones_cls
from .display_4 import display as display_cls

class imprint_surface_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    surface: surface_cls = ...
    zones: zones_cls = ...
    command_names = ...

    def display(self, ):
        """
        Display a surface.
        """

