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

from .adjustable_tolerance import adjustable_tolerance as adjustable_tolerance_cls
from .length_factor import length_factor as length_factor_cls

class set_one_to_one_pairing_tolerance(Command):
    fluent_name = ...
    argument_names = ...
    adjustable_tolerance: adjustable_tolerance_cls = ...
    length_factor: length_factor_cls = ...
