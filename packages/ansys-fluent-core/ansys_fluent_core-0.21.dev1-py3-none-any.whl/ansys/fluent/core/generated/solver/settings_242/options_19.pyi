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

from .list_surfaces_inside_region_only import list_surfaces_inside_region_only as list_surfaces_inside_region_only_cls
from .display_settings import display_settings as display_settings_cls

class options(Group):
    fluent_name = ...
    child_names = ...
    list_surfaces_inside_region_only: list_surfaces_inside_region_only_cls = ...
    display_settings: display_settings_cls = ...
