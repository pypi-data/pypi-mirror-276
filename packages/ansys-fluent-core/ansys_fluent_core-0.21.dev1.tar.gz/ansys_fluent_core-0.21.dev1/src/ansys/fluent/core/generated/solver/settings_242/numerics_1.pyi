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

from .polynomials import polynomials as polynomials_cls
from .rbf import rbf as rbf_cls
from .direct_interpolation import direct_interpolation as direct_interpolation_cls
from .default_5 import default as default_cls

class numerics(Group):
    fluent_name = ...
    child_names = ...
    polynomials: polynomials_cls = ...
    rbf: rbf_cls = ...
    direct_interpolation: direct_interpolation_cls = ...
    command_names = ...

    def default(self, ):
        """
        Reset morphing numerics to default.
        """

