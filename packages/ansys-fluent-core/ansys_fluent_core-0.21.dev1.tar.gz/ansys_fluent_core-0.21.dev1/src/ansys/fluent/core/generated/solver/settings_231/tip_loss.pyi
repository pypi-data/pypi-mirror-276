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

from .model_tip_loss import model_tip_loss as model_tip_loss_cls
from .tip_loss_limit import tip_loss_limit as tip_loss_limit_cls
from .prandtl_tuning_coefficient import prandtl_tuning_coefficient as prandtl_tuning_coefficient_cls

class tip_loss(Group):
    fluent_name = ...
    child_names = ...
    model_tip_loss: model_tip_loss_cls = ...
    tip_loss_limit: tip_loss_limit_cls = ...
    prandtl_tuning_coefficient: prandtl_tuning_coefficient_cls = ...
