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

from .file_name_19 import file_name as file_name_cls
from .unit import unit as unit_cls

class import_surfaces(Command):
    fluent_name = ...
    argument_names = ...
    file_name: file_name_cls = ...
    unit: unit_cls = ...
