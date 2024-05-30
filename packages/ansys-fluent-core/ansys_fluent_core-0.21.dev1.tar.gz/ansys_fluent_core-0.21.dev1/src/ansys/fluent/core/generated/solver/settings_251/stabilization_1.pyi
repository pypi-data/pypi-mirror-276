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

from .strategy import strategy as strategy_cls
from .current_scheme import current_scheme as current_scheme_cls
from .first_scheme import first_scheme as first_scheme_cls
from .second_scheme import second_scheme as second_scheme_cls
from .default_3 import default as default_cls
from .complex_case import complex_case as complex_case_cls

class stabilization(Group):
    fluent_name = ...
    child_names = ...
    strategy: strategy_cls = ...
    current_scheme: current_scheme_cls = ...
    first_scheme: first_scheme_cls = ...
    second_scheme: second_scheme_cls = ...
    command_names = ...

    def default(self, ):
        """
        Set stabilization strategy controls to default for most cases.
        """

    def complex_case(self, ):
        """
        Set stabilization strategy controls to default values for complex case.
        """

