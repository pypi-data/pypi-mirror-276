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

from .enable_prod_limiter import enable_prod_limiter as enable_prod_limiter_cls
from .clip_factor import clip_factor as clip_factor_cls

class production_limiter(Group):
    fluent_name = ...
    child_names = ...
    enable_prod_limiter: enable_prod_limiter_cls = ...
    clip_factor: clip_factor_cls = ...
