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

from .backflow_total_temperature import backflow_total_temperature as backflow_total_temperature_cls

class thermal(Group):
    fluent_name = ...
    child_names = ...
    backflow_total_temperature: backflow_total_temperature_cls = ...
