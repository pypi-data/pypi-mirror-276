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

from .adjoint_equations_1 import adjoint_equations as adjoint_equations_cls
from .options_18 import options as options_cls
from .plot_1 import plot as plot_cls

class monitors(Group):
    fluent_name = ...
    child_names = ...
    adjoint_equations: adjoint_equations_cls = ...
    options: options_cls = ...
    command_names = ...

    def plot(self, ):
        """
        Plot residuals.
        """

