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

from .banded_coloring import banded_coloring as banded_coloring_cls
from .number_of_bands import number_of_bands as number_of_bands_cls

class coloring(Group):
    fluent_name = ...
    child_names = ...
    banded_coloring: banded_coloring_cls = ...
    number_of_bands: number_of_bands_cls = ...
