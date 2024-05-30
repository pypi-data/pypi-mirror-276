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

from .keep_linearized_source_terms_constant import keep_linearized_source_terms_constant as keep_linearized_source_terms_constant_cls
from .linearize_source_terms import linearize_source_terms as linearize_source_terms_cls
from .linearized_source_terms_limiter import linearized_source_terms_limiter as linearized_source_terms_limiter_cls

class linearization(Group):
    fluent_name = ...
    child_names = ...
    keep_linearized_source_terms_constant: keep_linearized_source_terms_constant_cls = ...
    linearize_source_terms: linearize_source_terms_cls = ...
    linearized_source_terms_limiter: linearized_source_terms_limiter_cls = ...
