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
from .output_dir import output_dir as output_dir_cls

class export_simulation_report_as_html(Command):
    fluent_name = ...
    argument_names = ...
    report_name: report_name_cls = ...
    output_dir: output_dir_cls = ...
