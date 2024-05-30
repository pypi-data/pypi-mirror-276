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

from .light_number import light_number as light_number_cls
from .light_on import light_on as light_on_cls
from .rgb_vector import rgb_vector as rgb_vector_cls
from .use_view_factor import use_view_factor as use_view_factor_cls
from .change_light_direction import change_light_direction as change_light_direction_cls
from .direction_vector_1 import direction_vector as direction_vector_cls

class set_light(Command):
    fluent_name = ...
    argument_names = ...
    light_number: light_number_cls = ...
    light_on: light_on_cls = ...
    rgb_vector: rgb_vector_cls = ...
    use_view_factor: use_view_factor_cls = ...
    change_light_direction: change_light_direction_cls = ...
    direction_vector: direction_vector_cls = ...
