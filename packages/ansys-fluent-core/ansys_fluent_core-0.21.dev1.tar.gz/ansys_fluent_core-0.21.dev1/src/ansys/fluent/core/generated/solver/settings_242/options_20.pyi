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

from .enable_turbulence_source_term import enable_turbulence_source_term as enable_turbulence_source_term_cls

class options(Group):
    fluent_name = ...
    child_names = ...
    enable_turbulence_source_term: enable_turbulence_source_term_cls = ...
