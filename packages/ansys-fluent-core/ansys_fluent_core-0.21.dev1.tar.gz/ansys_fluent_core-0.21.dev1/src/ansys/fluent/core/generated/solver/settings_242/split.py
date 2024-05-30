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

from .name_7 import name as name_cls
from .location_3 import location as location_cls

class split(Command):
    """
    Input volume name to split.
    
    Parameters
    ----------
        name : str
            Input new volume name.
        location : typing.List[str]
            Input location name which should be part of new volume.
    
    """

    fluent_name = "split"

    argument_names = \
        ['name', 'location']

    _child_classes = dict(
        name=name_cls,
        location=location_cls,
    )

