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

from .length import length as length_cls
from .boundary import boundary as boundary_cls

class knudsen_number_calculator(Command):
    fluent_name = ...
    argument_names = ...
    length: length_cls = ...
    boundary: boundary_cls = ...
