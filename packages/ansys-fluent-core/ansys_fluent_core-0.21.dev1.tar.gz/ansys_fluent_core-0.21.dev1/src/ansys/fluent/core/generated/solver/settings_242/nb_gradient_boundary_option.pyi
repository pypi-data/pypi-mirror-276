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

from .nb_gradient import nb_gradient as nb_gradient_cls
from .nb_gradient_dbns import nb_gradient_dbns as nb_gradient_dbns_cls

class nb_gradient_boundary_option(Group):
    fluent_name = ...
    child_names = ...
    nb_gradient: nb_gradient_cls = ...
    nb_gradient_dbns: nb_gradient_dbns_cls = ...
