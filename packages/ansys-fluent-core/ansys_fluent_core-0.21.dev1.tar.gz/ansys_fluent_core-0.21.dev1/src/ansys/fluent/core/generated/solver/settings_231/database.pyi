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

from .database_type import database_type as database_type_cls
from .copy_by_formula import copy_by_formula as copy_by_formula_cls
from .copy_by_name import copy_by_name as copy_by_name_cls
from .list_materials import list_materials as list_materials_cls
from .list_properties import list_properties as list_properties_cls

class database(Group):
    fluent_name = ...
    child_names = ...
    database_type: database_type_cls = ...
    command_names = ...

    def copy_by_formula(self, type: str, formula: str):
        """
        Copy a material from the database (pick by formula).
        
        Parameters
        ----------
            type : str
                'type' child.
            formula : str
                'formula' child.
        
        """

    def copy_by_name(self, type: str, name: str):
        """
        Copy a material from the database (pick by name).
        
        Parameters
        ----------
            type : str
                'type' child.
            name : str
                'name' child.
        
        """

    def list_materials(self, ):
        """
        List all materials in the database.
        """

    def list_properties(self, name: str):
        """
        List the properties of a material in the database.
        
        Parameters
        ----------
            name : str
                'name' child.
        
        """

