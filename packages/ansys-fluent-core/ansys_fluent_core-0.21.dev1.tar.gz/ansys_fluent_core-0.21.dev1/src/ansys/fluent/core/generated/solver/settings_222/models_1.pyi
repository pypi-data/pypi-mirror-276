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

from .energy import energy as energy_cls
from .multiphase import multiphase as multiphase_cls
from .viscous import viscous as viscous_cls

class models(Group):
    fluent_name = ...
    child_names = ...
    energy: energy_cls = ...
    multiphase: multiphase_cls = ...
    viscous: viscous_cls = ...
