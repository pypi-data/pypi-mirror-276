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

from .relaxation_bounding_method import relaxation_bounding_method as relaxation_bounding_method_cls
from .default_min_max_relaxation_limits import default_min_max_relaxation_limits as default_min_max_relaxation_limits_cls
from .minimum_allowed_effctive_relaxation import minimum_allowed_effctive_relaxation as minimum_allowed_effctive_relaxation_cls
from .maximum_allowed_effctive_relaxation import maximum_allowed_effctive_relaxation as maximum_allowed_effctive_relaxation_cls

class relaxation_bounds(Command):
    fluent_name = ...
    argument_names = ...
    relaxation_bounding_method: relaxation_bounding_method_cls = ...
    default_min_max_relaxation_limits: default_min_max_relaxation_limits_cls = ...
    minimum_allowed_effctive_relaxation: minimum_allowed_effctive_relaxation_cls = ...
    maximum_allowed_effctive_relaxation: maximum_allowed_effctive_relaxation_cls = ...
