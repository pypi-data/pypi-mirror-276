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

from .equations_1 import equations as equations_cls
from .options_11 import options as options_cls
from .axes import axes as axes_cls
from .curves import curves as curves_cls
from .reset_1 import reset as reset_cls
from .renormalize import renormalize as renormalize_cls
from .plot_1 import plot as plot_cls

class residual(Group):
    fluent_name = ...
    child_names = ...
    equations: equations_cls = ...
    options: options_cls = ...
    axes: axes_cls = ...
    curves: curves_cls = ...
    command_names = ...

    def reset(self, ):
        """
        Delete the residual history and reset iteration counter to unity.
        """

    def renormalize(self, ):
        """
        Renormalize residuals by maximum values.
        """

    def plot(self, ):
        """
        Plot residuals.
        """

