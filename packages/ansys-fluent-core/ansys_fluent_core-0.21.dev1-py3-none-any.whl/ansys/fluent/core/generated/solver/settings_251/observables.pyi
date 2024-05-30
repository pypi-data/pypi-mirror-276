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

from .named_expressions import named_expressions as named_expressions_cls
from .definition_1 import definition as definition_cls
from .selection import selection as selection_cls

class observables(Group):
    fluent_name = ...
    child_names = ...
    named_expressions: named_expressions_cls = ...
    definition: definition_cls = ...
    selection: selection_cls = ...
