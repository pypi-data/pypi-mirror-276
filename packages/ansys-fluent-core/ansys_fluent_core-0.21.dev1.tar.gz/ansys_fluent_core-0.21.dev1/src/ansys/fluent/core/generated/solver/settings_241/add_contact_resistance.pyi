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

from .contact_face import contact_face as contact_face_cls
from .resistance_value import resistance_value as resistance_value_cls

class add_contact_resistance(Command):
    fluent_name = ...
    argument_names = ...
    contact_face: contact_face_cls = ...
    resistance_value: resistance_value_cls = ...
