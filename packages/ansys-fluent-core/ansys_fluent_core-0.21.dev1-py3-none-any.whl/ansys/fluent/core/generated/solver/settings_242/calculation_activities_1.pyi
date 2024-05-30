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

from .monitor_3 import monitor as monitor_cls
from .autosave_1 import autosave as autosave_cls

class calculation_activities(Group):
    fluent_name = ...
    child_names = ...
    monitor: monitor_cls = ...
    autosave: autosave_cls = ...
