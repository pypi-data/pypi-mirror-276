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

from .field import field as field_cls
from .scalefactor import scalefactor as scalefactor_cls

class ribbon(Group):
    fluent_name = ...
    child_names = ...
    field: field_cls = ...
    scalefactor: scalefactor_cls = ...
