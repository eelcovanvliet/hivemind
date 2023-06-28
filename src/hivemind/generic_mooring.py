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




class MooringSystem(Base):
    
    def __init__(self, parameters:ParameterSet):
        self._parameters = parameters
        self._possible_states = {
            "LayDown" : LayDown(self),
            "InSitu" : InSitu(self),
            "Weathered" : Weathered(self),
        }
        self._state = self._possible_states["InSitu"]
        self._previous_state = None

    @property   
    def state(self) -> MooringSystemState:
        return self._state
    
    @property
    def parameters(self) -> ParameterSet:
        return self._parameters

    @property
    def possible_states(self) -> Dict[str, MooringSystemState]:
        return self._possible_states
    
    def change_state(self, state:str) -> bool:
        self._previous_state = self._state
        self._state = self.possible_states[state]
        return True

    @property
    def state(self) -> MooringSystemState:
        return self._state

    @property
    def previous_state(self) -> MooringSystemState|None:
        raise NotImplementedError()

    def create_in_ofx(self, model):
        self.state.create_in_ofx(model)




class MooringSystemState(State):

    @abstractmethod
    def create_in_ofx(self, model):
        ...

class LayDown(MooringSystemState):

    def create_in_ofx(self):
        raise NotImplementedError()

class InSitu(MooringSystemState):

    def create_in_ofx(self):
        raise NotImplementedError()

class Weathered(MooringSystemState):

    def create_in_ofx(self):
        raise NotImplementedError()


class MooringSystemParameters(ParameterSet):
    AnchorRadius:Parameter = 200 * units.m
    NumberOfLinesPerBundle:Parameter = 4
    NumberOfBundles:Parameter = 3
    

if __name__ == "__main__":
    
    
    mp = MooringSystemParameters()
    

    
    ms = MooringSystem(mp)

    from abstracts import test_subclass
    test_subclass(ms)
    
    ms.create_in_ofx()

    
