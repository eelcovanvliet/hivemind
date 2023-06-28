from __future__ import annotations
from abstracts import Base, State
from abc import ABC, abstractmethod, abstractproperty
from enum import Enum
from typing import Dict
from carg_io.abstracts import ParameterSet, Parameter, units



class SiteParameters(ParameterSet):
    MeanSeaLevel = 100
    WaterDensity = 1.025
    WaterTemperature = 10
    MarineGrowthFactor = 100
    SoilStiffness = 50

class Site(Base):

    def __init__(self, parameters:SiteParameters) -> None:
        super().__init__()
        self._parameters = parameters
        self._state = MSL(self)

class SiteState(State):
    pass

class MSL(SiteState):
    pass

class HAT(SiteState):
    pass

class LAT(SiteState):
    pass