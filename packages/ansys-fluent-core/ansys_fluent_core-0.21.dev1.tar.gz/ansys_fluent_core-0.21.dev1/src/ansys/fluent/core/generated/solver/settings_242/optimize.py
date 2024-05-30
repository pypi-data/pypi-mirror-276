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

from .current_warnings import current_warnings as current_warnings_cls
from .disable_settings_validation import disable_settings_validation as disable_settings_validation_cls

class optimize(Command):
    """
    Disable warnings detecting possibly wrong settings before running the optimizer.
    
    Parameters
    ----------
        current_warnings : typing.List[str]
            Warnings based on current settings.
        disable_settings_validation : bool
            Ignore warnings and proceed with optimization.
    
    """

    fluent_name = "optimize"

    argument_names = \
        ['current_warnings', 'disable_settings_validation']

    _child_classes = dict(
        current_warnings=current_warnings_cls,
        disable_settings_validation=disable_settings_validation_cls,
    )

