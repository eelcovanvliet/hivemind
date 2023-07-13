from __future__ import annotations
from .abstracts import Base, State
from .abstracts import Mesh, Inertia
from abc import ABC, abstractmethod, abstractproperty
from enum import Enum
from typing import Dict
from carg_io.abstracts import ParameterSet, Parameter, units



class Structure(Base):

    """Describe a structural object, i.e. anything that has mass and some spatial properties."""

    @abstractmethod
    def get_mesh(self) -> Mesh:
        ...
    
    @abstractmethod
    def get_inertia(self) -> Inertia:
        ...

    
