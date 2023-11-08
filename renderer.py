# renderer.py :

from patterns import Renderer
from states import SearchState, FeedState
from config import Config
from utils import color_from_value
import pygame
import numpy as np
import numba

class PygameRenderer(Renderer):
    """ Renderer class for the Pygame visualization."""
    def __init__(self, window, cell_size, grid_size):
        self.window = window
        self.cell_size = cell_size
        self.grid_size = grid_size

    def render(self, grid):
        self.window.fill(Config.BACKGROUND_COLOR)  # Fill the background

        # Draw the grid
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                   self.cell_size, self.cell_size)
                color = self._get_color_from_value(grid[x, y], Config.MAX_TRAIL_VALUE)
                pygame.draw.rect(self.window, color, rect)

        pygame.display.update()  # Update the display

    @staticmethod
    def _get_color_from_value(value, max_trail_value):
        """
        Determine the color of a cell based on its value using the 'viridis' colormap.
        """
        return color_from_value(value, max_trail_value)


    def update_agent_position(self, x, y, agent_state):
        """
        Update the agent's position on the screen. This could involve drawing a
        special icon or using a different color to denote the agent's position.
        """
        pixel_x = x * self.cell_size
        pixel_y = y * self.cell_size
        if isinstance(agent_state, SearchState):
            agent_color = Config.AGENT_SEARCH_COLOR
        elif isinstance(agent_state, FeedState):
            agent_color = Config.AGENT_FEED_COLOR
        else:
            agent_color = Config.AGENT_DEFAULT_COLOR
        pygame.draw.circle(self.window, agent_color, (pixel_x, pixel_y), self.cell_size // 2)

    def draw_agent(self, agent):
        # Assuming agent color is defined in the agent class or through its state
        agent_color = self._get_agent_color(agent)
        pixel_x = int(agent.x * self.cell_size)
        pixel_y = int(agent.y * self.cell_size)
        pygame.draw.circle(self.window, agent_color, (pixel_x, pixel_y), self.cell_size // 2)

    def _get_agent_color(self, agent):
        # Return color based on agent's state
        if isinstance(agent.state, SearchState):
            return Config.AGENT_SEARCH_COLOR
        elif isinstance(agent.state, FeedState):
            return Config.AGENT_FEED_COLOR
        return Config.AGENT_DEFAULT_COLOR