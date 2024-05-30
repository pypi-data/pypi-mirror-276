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

from .delete_1 import delete as delete_cls
from .list import list as list_cls
from .list_properties_1 import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .copy import copy as copy_cls
from .beams_child import beams_child


class beams(NamedObject[beams_child], _CreatableNamedObjectMixin[beams_child]):
    fluent_name = ...
    command_names = ...

    def delete(self, name_list: List[str]):
        """
        Delete selected objects.
        
        Parameters
        ----------
            name_list : typing.List[str]
                Select objects to be deleted.
        
        """

    def list(self, ):
        """
        List the names of the objects.
        """

    def list_properties(self, object_name: str):
        """
        List active properties of the object.
        
        Parameters
        ----------
            object_name : str
                Select object for which properties are to be listed.
        
        """

    def make_a_copy(self, from_: str, to: str):
        """
        Create a copy of the object.
        
        Parameters
        ----------
            from_ : str
                Select the object to duplicate.
            to : str
                Specify the name of the new object.
        
        """

    def copy(self, orig_beam_name: str, beam_name: str, ap_face_zone: str, beam_length: Union[float, str], ray_npoints: int, x_beam_vector: Union[float, str], y_beam_vector: Union[float, str], z_beam_vector: Union[float, str]):
        """
        Copy optical beam grid.
        
        Parameters
        ----------
            orig_beam_name : str
                Choose the name for the optical beam to be copied.
            beam_name : str
                Set a unique name for each optical beam.
            ap_face_zone : str
                Set the wall face zones to specify the optical aperture surface.
            beam_length : real
                Set the length of optical beam propagation.
            ray_npoints : int
                Set the number of grid point in each ray of the optical beam.
            x_beam_vector : real
                Set the x-component of the beam propagation vector.
            y_beam_vector : real
                Set the y-component of the beam propagation vector.
            z_beam_vector : real
                Set the z-component of the beam propagation vector.
        
        """

    child_object_type = ...
