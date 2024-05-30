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

from .damping_factor_1 import damping_factor as damping_factor_cls
from .damping_relaxation import damping_relaxation as damping_relaxation_cls
from .damping_order import damping_order as damping_order_cls
from .suppression import suppression as suppression_cls
from .default_2 import default as default_cls

class dissipation(Group):
    fluent_name = ...
    child_names = ...
    damping_factor: damping_factor_cls = ...
    damping_relaxation: damping_relaxation_cls = ...
    damping_order: damping_order_cls = ...
    suppression: suppression_cls = ...
    command_names = ...

    def default(self, ):
        """
        Set residual minimization scheme controls to default.
        """

