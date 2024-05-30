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
from .source_term_linearization_enabled import source_term_linearization_enabled as source_term_linearization_enabled_cls
from .enhanced_linearization_enabled import enhanced_linearization_enabled as enhanced_linearization_enabled_cls
from .linearized_source_terms_limiter import linearized_source_terms_limiter as linearized_source_terms_limiter_cls

class linearization(Group):
    fluent_name = ...
    child_names = ...
    keep_linearized_source_terms_constant: keep_linearized_source_terms_constant_cls = ...
    source_term_linearization_enabled: source_term_linearization_enabled_cls = ...
    enhanced_linearization_enabled: enhanced_linearization_enabled_cls = ...
    linearized_source_terms_limiter: linearized_source_terms_limiter_cls = ...
