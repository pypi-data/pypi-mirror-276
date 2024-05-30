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

from .band_width import band_width as band_width_cls
from .reorder_domain import reorder_domain as reorder_domain_cls
from .reorder_zones import reorder_zones as reorder_zones_cls

class reorder(Group):
    fluent_name = ...
    command_names = ...

    def band_width(self, ):
        """
        Print cell bandwidth.
        """

    def reorder_domain(self, ):
        """
        Reorder cells and faces by reverse Cuthill-McKee.
        """

    def reorder_zones(self, ):
        """
        Reorder zones by partition, type, and id.
        """

