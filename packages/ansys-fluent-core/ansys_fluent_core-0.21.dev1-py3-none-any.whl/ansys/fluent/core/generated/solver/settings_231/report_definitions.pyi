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

from .mesh_1 import mesh as mesh_cls
from .surface_1 import surface as surface_cls
from .volume import volume as volume_cls
from .force import force as force_cls
from .lift import lift as lift_cls
from .drag import drag as drag_cls
from .moment import moment as moment_cls
from .flux_1 import flux as flux_cls
from .injection import injection as injection_cls
from .user_defined_1 import user_defined as user_defined_cls
from .aeromechanics import aeromechanics as aeromechanics_cls
from .icing import icing as icing_cls
from .expression_1 import expression as expression_cls
from .single_val_expression import single_val_expression as single_val_expression_cls
from .custom import custom as custom_cls
from .compute_1 import compute as compute_cls
from .copy_1 import copy as copy_cls
from .list import list as list_cls

class report_definitions(Group, _ChildNamedObjectAccessorMixin):
    fluent_name = ...
    child_names = ...
    mesh: mesh_cls = ...
    surface: surface_cls = ...
    volume: volume_cls = ...
    force: force_cls = ...
    lift: lift_cls = ...
    drag: drag_cls = ...
    moment: moment_cls = ...
    flux: flux_cls = ...
    injection: injection_cls = ...
    user_defined: user_defined_cls = ...
    aeromechanics: aeromechanics_cls = ...
    icing: icing_cls = ...
    expression: expression_cls = ...
    single_val_expression: single_val_expression_cls = ...
    custom: custom_cls = ...
    command_names = ...

    def compute(self, report_defs: List[str]):
        """
        'compute' command.
        
        Parameters
        ----------
            report_defs : typing.List[str]
                'report_defs' child.
        
        """

    def copy(self, copy_from: str, copy_to: str):
        """
        'copy' command.
        
        Parameters
        ----------
            copy_from : str
                'copy_from' child.
            copy_to : str
                'copy_to' child.
        
        """

    def list(self, ):
        """
        'list' command.
        """

