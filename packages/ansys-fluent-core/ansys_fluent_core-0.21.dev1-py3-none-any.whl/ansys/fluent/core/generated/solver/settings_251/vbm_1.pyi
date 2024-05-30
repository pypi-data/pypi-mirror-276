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

from .output_quantity import output_quantity as output_quantity_cls
from .rotor_name import rotor_name as rotor_name_cls
from .scale_output import scale_output as scale_output_cls
from .write_to_file_1 import write_to_file as write_to_file_cls
from .file_name_2 import file_name as file_name_cls
from .append_1 import append as append_cls

class vbm(Command):
    fluent_name = ...
    argument_names = ...
    output_quantity: output_quantity_cls = ...
    rotor_name: rotor_name_cls = ...
    scale_output: scale_output_cls = ...
    write_to_file: write_to_file_cls = ...
    file_name: file_name_cls = ...
    append: append_cls = ...
