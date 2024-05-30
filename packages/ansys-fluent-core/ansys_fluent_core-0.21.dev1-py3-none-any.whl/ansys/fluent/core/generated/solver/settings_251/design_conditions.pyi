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

from .definition_3 import definition as definition_cls
from .selection_1 import selection as selection_cls
from .options_19 import options as options_cls

class design_conditions(Group):
    fluent_name = ...
    child_names = ...
    definition: definition_cls = ...
    selection: selection_cls = ...
    options: options_cls = ...
