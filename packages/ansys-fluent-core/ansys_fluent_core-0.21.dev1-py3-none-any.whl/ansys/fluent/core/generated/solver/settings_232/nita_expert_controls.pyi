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

from .verbosity_6 import verbosity as verbosity_cls
from .skewness_neighbor_coupling import skewness_neighbor_coupling as skewness_neighbor_coupling_cls
from .hybrid_nita_settings import hybrid_nita_settings as hybrid_nita_settings_cls

class nita_expert_controls(Group):
    fluent_name = ...
    child_names = ...
    verbosity: verbosity_cls = ...
    skewness_neighbor_coupling: skewness_neighbor_coupling_cls = ...
    hybrid_nita_settings: hybrid_nita_settings_cls = ...
