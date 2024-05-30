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

from .dbns_cases import dbns_cases as dbns_cases_cls
from .pbns_cases import pbns_cases as pbns_cases_cls

class flux_type(Group):
    fluent_name = ...
    child_names = ...
    dbns_cases: dbns_cases_cls = ...
    pbns_cases: pbns_cases_cls = ...
