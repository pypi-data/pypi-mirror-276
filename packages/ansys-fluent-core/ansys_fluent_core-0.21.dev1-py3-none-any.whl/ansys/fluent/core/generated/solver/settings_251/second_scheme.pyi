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

from .method_14 import method as method_cls
from .iterations_2 import iterations as iterations_cls
from .residual_minimization import residual_minimization as residual_minimization_cls

class second_scheme(Group):
    fluent_name = ...
    child_names = ...
    method: method_cls = ...
    iterations: iterations_cls = ...
    residual_minimization: residual_minimization_cls = ...
