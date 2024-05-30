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

from .coefficients_3 import coefficients as coefficients_cls
from .distance import distance as distance_cls

class create(Command):
    fluent_name = ...
    argument_names = ...
    coefficients: coefficients_cls = ...
    distance: distance_cls = ...
