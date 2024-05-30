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

from .solve_tke import solve_tke as solve_tke_cls
from .wall_echo import wall_echo as wall_echo_cls

class reynolds_stress_options(Group):
    fluent_name = ...
    child_names = ...
    solve_tke: solve_tke_cls = ...
    wall_echo: wall_echo_cls = ...
