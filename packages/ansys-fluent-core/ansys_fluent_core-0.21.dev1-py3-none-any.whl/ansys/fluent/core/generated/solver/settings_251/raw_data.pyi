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

from .import_files_enabled import import_files_enabled as import_files_enabled_cls
from .number_of_files import number_of_files as number_of_files_cls
from .files import files as files_cls
from .capacify_fade_enabled import capacify_fade_enabled as capacify_fade_enabled_cls

class raw_data(Command):
    fluent_name = ...
    argument_names = ...
    import_files_enabled: import_files_enabled_cls = ...
    number_of_files: number_of_files_cls = ...
    files: files_cls = ...
    capacify_fade_enabled: capacify_fade_enabled_cls = ...
