
from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty
from carg_io.abstracts import ParameterSet


class Base(ABC):

    @abstractproperty
    def parameters(self) -> ParameterSet:
        ...
    
    @abstractproperty
    def state(self) -> State:
        """Should return the currently active state.

        -------------------------------------------------------------------------------

        JUSTIFICATION:

        In favor of state:

        What is close to reality? What is the Structure?
        Does it include ballast?
        Does it include the assemmbly of new parts?

        If a structure has been laying in the same spot for 20 years,
        it is the same structure, but the properties changed.
        i.e. it now has marine growth, or it was partly corroded.
        Do we create a NEW instance for that? Does not seem not close to reality.
        
        However, say you have a floater, and you stick a turbine on top.
        Now it's a pretty different thing.

        The parameteric part will be handled by a builder pattern:    
        https://refactoring.guru/design-patterns/builder

        The potential for an object to switch states will be handled by a state-pattern:
        https://refactoring.guru/design-patterns/state

        So now, the structure will return different values for the same method,
        depending on what state is is.

        """
        ...

    @abstractproperty
    def previous_state(self) -> State:
        """Should return the state of the previous state, but not actually
        change to this state)"""
        ...

    @abstractmethod
    def change_state(self, state:State|str) -> bool:
        """Method that facilitates the change of one state to another.
        Should return a boolean to indicate succes or failure of change."""
        ...
    


    


class State(ABC):
    """
    Abstract base class that represents one of the finite states a Structure may take on.
    
    https://refactoring.guru/design-patterns/state
    """

    def __init__(self, base:Base):
        self.base = base
