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





class MooringSystem(Base):
    
    def __init__(self, parameters):
        self.parameters = parameters
        self._state = InSitu(self)
        self._states = {
            MooringSystemState.Enum.LayDown : LayDown,
            MooringSystemState.Enum.HookUp : HookUp,
            MooringSystemState.Enum.InSitu : InSitu,
            MooringSystemState.Enum.Weathered : Weathered,

        }

    @property   
    def state(self) -> MooringSystemState:
        return self._state
    
    @property
    def states(self) -> Dict[MooringSystemState.Enum, MooringSystemState]:
        return self._states



class MooringSystemState(State):

    class Enum:
        LayDown = 1
        HookUp = 2
        InSitu = 3
        Weathered = 4

    @abstractmethod
    def create_in_ofx(self, model):
        ...


class LayDown(MooringSystemState):
    pass

class HookUp(MooringSystemState):
    pass

class InSitu(MooringSystemState):
    pass

class Weathered(MooringSystemState):
    pass






