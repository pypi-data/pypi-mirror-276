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

from .enable_10 import enable as enable_cls
from .discretization import discretization as discretization_cls
from .under_relaxation_1 import under_relaxation as under_relaxation_cls
from .verbosity_5 import verbosity as verbosity_cls
from .initialize import initialize as initialize_cls
from .show_status import show_status as show_status_cls

class turbo_sepcific_nrbc(Group):
    fluent_name = ...
    child_names = ...
    enable: enable_cls = ...
    discretization: discretization_cls = ...
    under_relaxation: under_relaxation_cls = ...
    verbosity: verbosity_cls = ...
    command_names = ...

    def initialize(self, ):
        """
        Initialize turbo-specific non-reflecting b.c.'s.
        """

    def show_status(self, ):
        """
        Show current status of turbo-specific non-reflecting b.c.'s.
        """

