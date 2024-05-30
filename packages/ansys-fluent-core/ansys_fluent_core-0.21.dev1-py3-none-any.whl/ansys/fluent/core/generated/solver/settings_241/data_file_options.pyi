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

from .reset_defined_derived_quantities import reset_defined_derived_quantities as reset_defined_derived_quantities_cls
from .derived_quantities import derived_quantities as derived_quantities_cls

class data_file_options(Command):
    fluent_name = ...
    argument_names = ...
    reset_defined_derived_quantities: reset_defined_derived_quantities_cls = ...
    derived_quantities: derived_quantities_cls = ...
