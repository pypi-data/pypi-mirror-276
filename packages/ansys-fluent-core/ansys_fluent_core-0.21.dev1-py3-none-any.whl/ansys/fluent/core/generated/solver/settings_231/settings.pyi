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

from .set_cgns_export_filetype import set_cgns_export_filetype as set_cgns_export_filetype_cls

class settings(Group):
    fluent_name = ...
    command_names = ...

    def set_cgns_export_filetype(self, set_filetype: bool):
        """
        Select HDF5 or ADF as file format for CGNS.
        
        Parameters
        ----------
            set_filetype : bool
                'set_filetype' child.
        
        """

