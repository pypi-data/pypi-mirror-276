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

from .blade_flapping_cone import blade_flapping_cone as blade_flapping_cone_cls
from .blade_flapping_cyclic_sin import blade_flapping_cyclic_sin as blade_flapping_cyclic_sin_cls
from .blade_flapping_cyclic_cos import blade_flapping_cyclic_cos as blade_flapping_cyclic_cos_cls

class blade_flap_angles(Group):
    fluent_name = ...
    child_names = ...
    blade_flapping_cone: blade_flapping_cone_cls = ...
    blade_flapping_cyclic_sin: blade_flapping_cyclic_sin_cls = ...
    blade_flapping_cyclic_cos: blade_flapping_cyclic_cos_cls = ...
