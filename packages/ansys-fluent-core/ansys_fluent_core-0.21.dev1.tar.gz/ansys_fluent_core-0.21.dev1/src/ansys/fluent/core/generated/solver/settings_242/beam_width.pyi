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

from .theta import theta as theta_cls
from .coll_dphi import coll_dphi as coll_dphi_cls

class beam_width(Group):
    fluent_name = ...
    child_names = ...
    theta: theta_cls = ...
    coll_dphi: coll_dphi_cls = ...
