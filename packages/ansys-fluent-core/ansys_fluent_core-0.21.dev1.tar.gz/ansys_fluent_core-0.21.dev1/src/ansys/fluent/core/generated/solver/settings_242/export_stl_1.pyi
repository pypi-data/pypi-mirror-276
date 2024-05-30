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

from .frequency_8 import frequency as frequency_cls
from .surfaces_18 import surfaces as surfaces_cls

class export_stl(Group):
    fluent_name = ...
    child_names = ...
    frequency: frequency_cls = ...
    surfaces: surfaces_cls = ...
