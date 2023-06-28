from __future__ import annotations
from abstracts import Base, State, ParameterSet
from abc import ABC, abstractmethod, abstractproperty
from enum import Enum
from typing import Dict


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





class Mooring(Base):
    
    def __init__(self, parameters):
        self.parameters = parameters
        self._state = InSitu(self)
        self._states = {
            MooringState.Enum.LayDown : LayDown,
            MooringState.Enum.HookUp : HookUp,
            MooringState.Enum.InSitu : InSitu,
            MooringState.Enum.Weathered : Weathered,

        }

    @property   
    def state(self) -> MooringState:
        return self._state
    
    @property
    def states(self) -> Dict[MooringState.Enum, MooringState]:
        return self._states



class MooringState(State):

    class Enum:
        LayDown = 1
        HookUp = 2
        InSitu = 3
        Weathered = 4

    @abstractmethod
    def create_in_ofx(self, model):
        ...


class LayDown(MooringState):
    pass

class HookUp(MooringState):
    pass

class InSitu(MooringState):
    pass

class Weathered(MooringState):
    pass






