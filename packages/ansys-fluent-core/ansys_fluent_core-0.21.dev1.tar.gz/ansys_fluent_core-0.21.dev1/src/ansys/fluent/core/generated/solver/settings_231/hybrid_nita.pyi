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

from .outer_iterations import outer_iterations as outer_iterations_cls
from .initial_outer_iterations import initial_outer_iterations as initial_outer_iterations_cls
from .instability_detector import instability_detector as instability_detector_cls

class hybrid_nita(Group):
    fluent_name = ...
    child_names = ...
    outer_iterations: outer_iterations_cls = ...
    initial_outer_iterations: initial_outer_iterations_cls = ...
    instability_detector: instability_detector_cls = ...
