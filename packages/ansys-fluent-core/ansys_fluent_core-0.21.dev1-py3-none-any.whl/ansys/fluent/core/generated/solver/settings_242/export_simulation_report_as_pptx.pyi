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

from .report_name import report_name as report_name_cls
from .file_name_2 import file_name as file_name_cls

class export_simulation_report_as_pptx(Command):
    fluent_name = ...
    argument_names = ...
    report_name: report_name_cls = ...
    file_name: file_name_cls = ...
