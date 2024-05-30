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

from .domain_2 import domain as domain_cls
from .zones_7 import zones as zones_cls
from .physics_1 import physics as physics_cls
from .write_to_file_2 import write_to_file as write_to_file_cls
from .file_name_14 import file_name as file_name_cls
from .append_data import append_data as append_data_cls

class film_heat_transfer(Command):
    fluent_name = ...
    argument_names = ...
    domain: domain_cls = ...
    zones: zones_cls = ...
    physics: physics_cls = ...
    write_to_file: write_to_file_cls = ...
    file_name: file_name_cls = ...
    append_data: append_data_cls = ...
