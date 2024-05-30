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

from .option import option as option_cls
from .growth_ratio_refinement import growth_ratio_refinement as growth_ratio_refinement_cls

class type(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    growth_ratio_refinement: growth_ratio_refinement_cls = ...
