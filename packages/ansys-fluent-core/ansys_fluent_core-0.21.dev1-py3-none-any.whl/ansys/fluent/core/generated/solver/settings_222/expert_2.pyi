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

from .reactions_1 import reactions as reactions_cls
from .reaction_source_term_relaxation_factor import reaction_source_term_relaxation_factor as reaction_source_term_relaxation_factor_cls
from .numerics import numerics as numerics_cls
from .numerics_dbns import numerics_dbns as numerics_dbns_cls

class expert(Group):
    fluent_name = ...
    child_names = ...
    reactions: reactions_cls = ...
    reaction_source_term_relaxation_factor: reaction_source_term_relaxation_factor_cls = ...
    numerics: numerics_cls = ...
    numerics_dbns: numerics_dbns_cls = ...
