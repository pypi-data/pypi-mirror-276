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
from .new_report_name import new_report_name as new_report_name_cls

class rename_simulation_report(Command):
    fluent_name = ...
    argument_names = ...
    report_name: report_name_cls = ...
    new_report_name: new_report_name_cls = ...
