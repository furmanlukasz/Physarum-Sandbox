from patterns import GridBuilder
import numpy as np

class PhysarumGridBuilder(GridBuilder):
    """ Grid builder class for the Physarum simulation."""
    def __init__(self):
        self.grid = None

    def set_dimensions(self, width, height):
        self.grid = np.zeros((width, height))
        return self

    def build(self):
        return self.grid