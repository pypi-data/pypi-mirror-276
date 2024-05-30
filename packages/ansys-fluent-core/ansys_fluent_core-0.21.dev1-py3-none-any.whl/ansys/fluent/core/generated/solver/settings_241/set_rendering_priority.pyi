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

from .surface_3 import surface as surface_cls
from .priority import priority as priority_cls

class set_rendering_priority(Command):
    fluent_name = ...
    argument_names = ...
    surface: surface_cls = ...
    priority: priority_cls = ...
