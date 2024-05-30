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

from .species_1 import species_1 as species_1_cls
from .species_2 import species_2 as species_2_cls
from .coefficient_1 import coefficient_1 as coefficient_1_cls
from .coefficient_2 import coefficient_2 as coefficient_2_cls

class expert_child(Group):
    fluent_name = ...
    child_names = ...
    species_1: species_1_cls = ...
    species_2: species_2_cls = ...
    coefficient_1: coefficient_1_cls = ...
    coefficient_2: coefficient_2_cls = ...
