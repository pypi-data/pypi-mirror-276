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

from .open_channel_flow import open_channel_flow as open_channel_flow_cls
from .open_channel_flow_wave_bc import open_channel_flow_wave_bc as open_channel_flow_wave_bc_cls

class vof_sub_models(Group):
    """
    Set vof sub model.
    """

    fluent_name = "vof-sub-models"

    child_names = \
        ['open_channel_flow', 'open_channel_flow_wave_bc']

    _child_classes = dict(
        open_channel_flow=open_channel_flow_cls,
        open_channel_flow_wave_bc=open_channel_flow_wave_bc_cls,
    )

