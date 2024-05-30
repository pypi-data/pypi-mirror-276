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

from .project_filename import project_filename as project_filename_cls
from .convert_to_managed import convert_to_managed as convert_to_managed_cls

class save_as_copy(Command):
    fluent_name = ...
    argument_names = ...
    project_filename: project_filename_cls = ...
    convert_to_managed: convert_to_managed_cls = ...
