from __future__ import annotations
from .abstracts import Base, State
from .abstracts import Mesh, Inertia
from .structural import Structure
from abc import ABC, abstractmethod, abstractproperty
from enum import Enum
from typing import Dict
from carg_io.abstracts import ParameterSet, Parameter, units



class Naval(Base):

    """Describe a structural object, i.e. anything that has mass and some spatial properties."""

    @abstractproperty
    def structure(self) -> Structure:
        ...

    @abstractmethod
    def get_stability(self):
        ...
    
    def get_hydrostatic_stiffness(self):
        ...

    @abstractmethod
    def get_natural_periods(self):
        ...

    
