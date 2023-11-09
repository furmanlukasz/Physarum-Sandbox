# patterns.py : 
from abc import ABC, abstractmethod

class Subject:
    """ Subject class for the observer pattern. """
    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self, data):
        for observer in self._observers:
            observer.update(data)

class Observer(ABC):
    """ Observer class for the observer pattern. """
    @abstractmethod
    def update(self, data):
        pass

class AgentFactory(ABC):
    """ Abstract factory class for creating agents. """
    @abstractmethod
    def create_agent(self):
        pass

class Agent(ABC):
    """ Abstract class for agents."""
    @abstractmethod
    def sense_and_move(self, grid):
        pass

class Renderer(ABC):
    """ Abstract class for rendering the simulation. """
    @abstractmethod
    def render(self, grid):
        pass


class GridBuilder(ABC):
    """ Abstract class for building the grid. """
    @abstractmethod
    def set_dimensions(self, width, height):
        pass

class State(ABC):
    """ Abstract class for agent states. """
    @abstractmethod
    def handle(self, agent):
        pass