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

from .named_expressions_child import named_expressions_child


class named_expressions(NamedObject[named_expressions_child], _CreatableNamedObjectMixin[named_expressions_child]):
    """
    'named_expressions' child.
    """

    fluent_name = "named-expressions"

    child_object_type: named_expressions_child = named_expressions_child
    """
    child_object_type of named_expressions.
    """
