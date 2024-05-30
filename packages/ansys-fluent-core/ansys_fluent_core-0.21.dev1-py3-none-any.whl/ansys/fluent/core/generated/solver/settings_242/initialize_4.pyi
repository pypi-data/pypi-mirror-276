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

from .turbulence_design_variables import turbulence_design_variables as turbulence_design_variables_cls

class initialize(Command):
    fluent_name = ...
    argument_names = ...
    turbulence_design_variables: turbulence_design_variables_cls = ...
