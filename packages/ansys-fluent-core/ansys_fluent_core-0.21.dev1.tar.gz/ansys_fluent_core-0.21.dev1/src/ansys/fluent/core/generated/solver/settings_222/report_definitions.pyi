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

from .mesh import mesh as mesh_cls
from .surface import surface as surface_cls
from .volume import volume as volume_cls
from .force import force as force_cls
from .lift import lift as lift_cls
from .drag import drag as drag_cls
from .moment import moment as moment_cls
from .flux import flux as flux_cls
from .injection import injection as injection_cls
from .user_defined import user_defined as user_defined_cls
from .aeromechanics import aeromechanics as aeromechanics_cls
from .expression import expression as expression_cls
from .custom import custom as custom_cls
from .compute_2 import compute as compute_cls

class report_definitions(Group):
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
    expression: expression_cls = ...
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

