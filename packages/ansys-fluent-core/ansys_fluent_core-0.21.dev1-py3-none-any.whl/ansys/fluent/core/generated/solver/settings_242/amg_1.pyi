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

from .tolerance_3 import tolerance as tolerance_cls
from .max_iterations import max_iterations as max_iterations_cls
from .show_iterations import show_iterations as show_iterations_cls

class amg(Group):
    fluent_name = ...
    child_names = ...
    tolerance: tolerance_cls = ...
    max_iterations: max_iterations_cls = ...
    show_iterations: show_iterations_cls = ...
