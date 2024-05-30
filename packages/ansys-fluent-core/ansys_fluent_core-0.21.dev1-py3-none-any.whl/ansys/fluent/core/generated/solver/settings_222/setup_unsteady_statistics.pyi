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

from .udf_cf_names import udf_cf_names as udf_cf_names_cls

class setup_unsteady_statistics(Command):
    fluent_name = ...
    argument_names = ...
    udf_cf_names: udf_cf_names_cls = ...
