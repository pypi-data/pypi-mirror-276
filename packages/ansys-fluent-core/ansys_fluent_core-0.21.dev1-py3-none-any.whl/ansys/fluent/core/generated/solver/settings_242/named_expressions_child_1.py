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

from .name import name as name_cls
from .named_expression import named_expression as named_expression_cls

class named_expressions_child(Group):
    """
    'child_object_type' of named_expressions.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'named_expression']

    _child_classes = dict(
        name=name_cls,
        named_expression=named_expression_cls,
    )

