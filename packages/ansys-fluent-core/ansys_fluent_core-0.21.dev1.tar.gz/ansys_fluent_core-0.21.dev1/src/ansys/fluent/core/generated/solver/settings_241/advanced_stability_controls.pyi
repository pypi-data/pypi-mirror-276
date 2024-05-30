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

from .pseudo_transient import pseudo_transient as pseudo_transient_cls
from .p_v_coupling_1 import p_v_coupling as p_v_coupling_cls
from .hybrid_nita import hybrid_nita as hybrid_nita_cls
from .equation_order import equation_order as equation_order_cls
from .anti_diffusion import anti_diffusion as anti_diffusion_cls

class advanced_stability_controls(Group):
    fluent_name = ...
    child_names = ...
    pseudo_transient: pseudo_transient_cls = ...
    p_v_coupling: p_v_coupling_cls = ...
    hybrid_nita: hybrid_nita_cls = ...
    equation_order: equation_order_cls = ...
    anti_diffusion: anti_diffusion_cls = ...
