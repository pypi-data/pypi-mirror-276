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

from .sb0 import sb0 as sb0_cls
from .sb1 import sb1 as sb1_cls
from .angle import angle as angle_cls
from .pl_name import pl_name as pl_name_cls

class make_phaselag_from_boundaries(Command):
    fluent_name = ...
    argument_names = ...
    sb0: sb0_cls = ...
    sb1: sb1_cls = ...
    angle: angle_cls = ...
    pl_name: pl_name_cls = ...
