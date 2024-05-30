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

from .report_type import report_type as report_type_cls
from .old_props import old_props as old_props_cls

class icing_child(Group):
    fluent_name = ...
    child_names = ...
    report_type: report_type_cls = ...
    old_props: old_props_cls = ...
