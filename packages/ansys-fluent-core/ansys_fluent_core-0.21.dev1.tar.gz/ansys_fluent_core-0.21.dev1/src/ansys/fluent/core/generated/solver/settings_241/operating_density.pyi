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

from .enable_3 import enable as enable_cls
from .method import method as method_cls
from .value import value as value_cls
from .print_1 import print as print_cls

class operating_density(Group):
    fluent_name = ...
    child_names = ...
    enable: enable_cls = ...
    method: method_cls = ...
    value: value_cls = ...
    command_names = ...

    def print(self, ):
        """
        Print operating density value.
        """

