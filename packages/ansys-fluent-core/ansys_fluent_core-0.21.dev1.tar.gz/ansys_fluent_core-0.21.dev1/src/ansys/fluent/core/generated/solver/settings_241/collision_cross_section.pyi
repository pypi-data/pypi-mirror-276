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

from .option_7 import option as option_cls
from .cross_section_multicomponent import cross_section_multicomponent as cross_section_multicomponent_cls

class collision_cross_section(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    cross_section_multicomponent: cross_section_multicomponent_cls = ...
