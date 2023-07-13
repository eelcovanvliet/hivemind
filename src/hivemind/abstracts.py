
from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty
from carg_io.abstracts import ParameterSet, Parameter, units
from typing import List, Dict, Tuple

class Base(ABC):
    """Base offers a template for create parameteric object supporting finite states.
    
    E.g. A class BallastTank(Base) will accept a ParameterSet outlining the static properties
    of the tank (such as width, height, length) and may have a finite number of different
    states, such as Empty, InterMediate, Full.

    see https://refactoring.guru/design-patterns/template-method
    
    -------------------------------------------------------------------------------

    JUSTIFICATION of states:

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
    @abstractproperty
    def parameters(self) -> ParameterSet:
        ...
    
    @abstractproperty
    def state(self) -> State:
        """Should return the currently active state instance"""
        ...

    @abstractproperty
    def possible_states(self) -> Dict[str, State]:
        """Should return the possible finite states this object can take on."""
        ...

    @abstractproperty
    def previous_state(self) -> State|None:
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



class Inertia(ABC):
    """Describes the inertial properties of a point mass"""

    @abstractproperty
    def translation(self):
        """Should return the translational inertia (mass). In general
        this may be in different in three directions, but typically it's one
        values for all
        """
        ...

    @abstractproperty
    def rotation(self):
        """Should return the rotation inertia with respect to self.location"""
        ...

    @abstractproperty
    def location(self):
        """Should return the location of the point mass"""
        ...


class Mesh(ABC):
    """Describes a mesh conisting of nodes and connectivity (edges) between them"""

    @abstractproperty
    def nodes(self):
        ...
    
    @abstractproperty
    def connectivity(self):
        ...



def test_subclass(instance:Base):

    assert isinstance(instance, Base)
    assert isinstance(instance.parameters, ParameterSet)
    assert isinstance(instance.state, State)
    assert isinstance(instance.possible_states, dict)

    for string, state in instance.possible_states.items():
        assert isinstance(string, str)
        assert isinstance(state, State)

    try:
        out = instance.change_state(string)
        assert isinstance(out, bool)
    except NotImplementedError:
        pass

    try:
        out = instance.previous_state
        assert isinstance(out, None|State)
    except NotImplementedError:
        pass



