# simulation.py :
from patterns import Observer
from grid import PhysarumGridBuilder
from renderer import PygameRenderer
from agents import PhysarumAgentFactory
from states import SearchState, FeedState
from config import Config
import numba
import pygame
import numpy as np


class PhysarumSimulation(Observer):
    """ Simulation class for the Physarum simulation."""
    def __init__(self, grid_size, agent_count, food_count):
        self.grid_size = grid_size
        self.agent_count = agent_count
        self.food_count = food_count
        self.grid_builder = PhysarumGridBuilder()

        self.grid = self._initialize_grid()
        self._place_initial_food()
        self.agents = self._initialize_agents()
        self._attach_agents()

        # Initialize the Pygame window and renderer
        pygame.init()
        window_size = (self.grid_size[0] * Config.CELL_SIZE, self.grid_size[1] * Config.CELL_SIZE)
        self.window = pygame.display.set_mode(window_size)
        self.renderer = PygameRenderer(self.window, Config.CELL_SIZE, self.grid_size)


    def _initialize_grid(self):
        # Use unpacking to pass the width and height separately
        self.grid_builder.set_dimensions(*self.grid_size)
        return self.grid_builder.build()

    def _initialize_agents(self):
        """ Initialize agents with random positions and directions. """
        agents = []
        for _ in range(self.agent_count):
            x = np.random.randint(self.grid_size[0])
            y = np.random.randint(self.grid_size[1])
            angle = np.random.rand() * 2 * np.pi
            # Create a new agent using the factory and pass in the initial parameters
            agent = PhysarumAgentFactory().create_agent(x, y, angle)
            agents.append(agent)
            # Register the simulation as an observer to the agent's state changes
            agent.register_observer(self)
        return agents

    @staticmethod
    @numba.jit(nopython=True)
    def _place_food(grid, x, y, radius, food_value):
        """ Place food on the grid at the specified location and radius. """
        min_x = max(0, x - radius)
        max_x = min(grid.shape[0], x + radius + 1)
        min_y = max(0, y - radius)
        max_y = min(grid.shape[1], y + radius + 1)

        for i in range(min_x, max_x):
            for j in range(min_y, max_y):
                if (i - x) ** 2 + (j - y) ** 2 <= radius ** 2:
                    grid[i, j] = food_value

    def _place_initial_food(self):
        """ Randomly place initial food particles on the grid. """
        for _ in range(self.food_count):
            x = np.random.randint(self.grid_size[0])
            y = np.random.randint(self.grid_size[1])
            self._place_food(self.grid, x, y, Config.INIT_FOOD_RADIUS, Config.INIT_FOOD_VALUE)

    def _attach_agents(self):
        for agent in self.agents:
            agent.register_observer(self)

    def update(self, data):
        """
        Update the simulation based on the agent's state.
        This method is called by the agents when they change their state.
        """
        # Check if 'agent' key is in the data, then use it
        agent = data.get('agent', None)
        if agent:
            # Pass the agent itself to the state's handle method
            agent.state.handle(agent)


            # Unpack the data received from the agent
            x, y, agent_state = data['x'], data['y'], data['state']

            # Update the grid based on the agent's actions
            if isinstance(agent_state, SearchState):
                self._handle_search_state(x, y)
            elif isinstance(agent_state, FeedState):
                self._handle_feed_state(x, y)

            # Update the visualization
            self._update_visualization(x, y, agent_state)

    def update_decay(self, value):
        Config.DECAY = value / 100.0
        print("Updated Decay: ", Config.DECAY)

    def update_diffusion(self, value):
        Config.DIFFUSION = value / 100.0
        print("Updated Diffusion: ", Config.DIFFUSION)

    def _handle_search_state(self, x, y):
        """
        Handle updates to the grid when the agent is in a search state.
        """
        # Increase the value at the current grid position to leave a trail
        self.grid[x, y] += Config.TRAIL_VALUE

    def _handle_feed_state(self, x, y):
        """
        Handle updates to the grid when the agent is in a feed state.
        """
        # Decrease the food amount at the agent's position
        self.grid[x, y] = max(0, self.grid[x, y] - Config.FOOD_CONSUMED)

    def _update_visualization(self, x, y, agent_state):
        """
        Update the visualization based on the agent's position and actions.
        """
        # Use the renderer to update the display
        if self.renderer:
            self.renderer.update_agent_position(x, y, agent_state)
            # If you're using Pygame, you might need to call `pygame.display.update()` or similar
    
    @staticmethod
    @numba.jit(nopython=True)
    def _apply_decay_and_diffusion(grid, decay, diffusion, cell_size):
        """ Apply decay and diffusion to the grid. """
        new_grid = np.empty_like(grid)
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                # Apply decay
                new_grid[i, j] = grid[i, j] * (1 - decay)

                # Apply diffusion
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        ii = (i + di) % grid.shape[0]
                        jj = (j + dj) % grid.shape[1]
                        new_grid[i, j] += grid[ii, jj] * diffusion / cell_size

        grid[:, :] = new_grid[:, :]

    @staticmethod
    @numba.jit(nopython=True)
    def _clear_chemotrails(grid, x, y, radius):
        """ Clear chemotrails on the grid at the specified location and radius. """
        min_x = max(0, x - radius)
        max_x = min(grid.shape[0], x + radius + 1)
        min_y = max(0, y - radius)
        max_y = min(grid.shape[1], y + radius + 1)

        for i in range(min_x, max_x):
            for j in range(min_y, max_y):
                if (i - x) ** 2 + (j - y) ** 2 <= radius ** 2:
                    grid[i, j] = 0

    def render(self, renderer):
        renderer.render(self.grid)

    def run_step(self):
        # Handle Pygame events
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x, grid_y = mouse_x // Config.CELL_SIZE, mouse_y // Config.CELL_SIZE
        # Process Pygame events to handle user input or window closure
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_a:  # 'A' key to add a new agent

                    # Create a new agent at the mouse position with a random angle
                    new_angle = np.random.rand() * 2 * np.pi
                    new_agent = PhysarumAgentFactory().create_agent(grid_x, grid_y, new_angle)
                    
                    # Add the new agent to the simulation
                    self.agents.append(new_agent)
                    new_agent.register_observer(self)

                if event.key == pygame.K_d:  # Delete agent with 'D' key

                    # Define the radius within which agents will be deleted
                    delete_radius = 5  # Adjust as necessary

                    # Create a list to hold agents that are not deleted
                    surviving_agents = []
                    for agent in self.agents:
                        agent_x = agent.x * Config.CELL_SIZE
                        agent_y = agent.y * Config.CELL_SIZE
                        distance = np.sqrt((agent_x - mouse_x)**2 + (agent_y - mouse_y)**2)

                        if distance > delete_radius * Config.CELL_SIZE:
                            surviving_agents.append(agent)

                    # Update the agents list to only include surviving agents
                    self.agents = surviving_agents

            # Implement food placement and chemotrail clearing
        if pygame.mouse.get_pressed()[0]:
            self._place_food(self.grid, grid_x, grid_y, Config.FOOD_RADIUS, Config.POSTFOOD_VALUE)
        elif pygame.mouse.get_pressed()[2]:
            # self.clear_chemotrails(grid_x, grid_y, Config.CLEAR_RADIUS)
            self._clear_chemotrails(self.grid, grid_x, grid_y, Config.CLEAR_RADIUS)

        # Update agents and grid for a single step
        for agent in self.agents:
            agent.sense_and_move(self.grid)

        # Apply decay and diffusion to the grid
        self._apply_decay_and_diffusion(self.grid, Config.DECAY, Config.DIFFUSION, Config.CELL_SIZE)

        # Render the grid and agents
        self.renderer.render(self.grid)
        for agent in self.agents:
            self.renderer.draw_agent(agent)

        # Update the Pygame display
        # pygame.display.flip()  # Or pygame.display.update(), depending on your version of Pygame
        pygame.display.update()
        # Control the simulation speed if needed, might be unnecessary if QTimer is used
        # If Config.SIMULATION_DELAY > 0:
        #     pygame.time.delay(Config.SIMULATION_DELAY)

    def run(self):
        self._place_initial_food()

        clock = pygame.time.Clock()

        running = True
        while running:
            # Handle Pygame events
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x, grid_y = mouse_x // Config.CELL_SIZE, mouse_y // Config.CELL_SIZE

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_a:  # 'A' key to add a new agent

                        # Create a new agent at the mouse position with a random angle
                        new_angle = np.random.rand() * 2 * np.pi
                        new_agent = PhysarumAgentFactory().create_agent(grid_x, grid_y, new_angle)
                        
                        # Add the new agent to the simulation
                        self.agents.append(new_agent)
                        new_agent.register_observer(self)

                    if event.key == pygame.K_d:  # Delete agent with 'D' key

                        # Define the radius within which agents will be deleted
                        delete_radius = 5  # Adjust as necessary

                        # Create a list to hold agents that are not deleted
                        surviving_agents = []
                        for agent in self.agents:
                            agent_x = agent.x * Config.CELL_SIZE
                            agent_y = agent.y * Config.CELL_SIZE
                            distance = np.sqrt((agent_x - mouse_x)**2 + (agent_y - mouse_y)**2)

                            if distance > delete_radius * Config.CELL_SIZE:
                                surviving_agents.append(agent)

                        # Update the agents list to only include surviving agents
                        self.agents = surviving_agents

             # Implement food placement and chemotrail clearing
            if pygame.mouse.get_pressed()[0]:
                self._place_food(self.grid, grid_x, grid_y, Config.FOOD_RADIUS, Config.POSTFOOD_VALUE)
            elif pygame.mouse.get_pressed()[2]:
                # self.clear_chemotrails(grid_x, grid_y, Config.CLEAR_RADIUS)
                self._clear_chemotrails(self.grid, grid_x, grid_y, Config.CLEAR_RADIUS)

            # Update agents and grid
            for agent in self.agents:
                agent.sense_and_move(self.grid)

            # Apply decay and diffusion
            self._apply_decay_and_diffusion(self.grid, Config.DECAY, Config.DIFFUSION, Config.CELL_SIZE)

            # Render the grid and agents
            self.renderer.render(self.grid)
            for agent in self.agents:
                self.renderer.draw_agent(agent)

            pygame.display.update()  # Update the display

            # Delay to control simulation speed
            if Config.SIMULATION_DELAY > 0:
                pygame.time.delay(Config.SIMULATION_DELAY)

            # Ensure constant framerate
            clock.tick(Config.FRAMERATE)

        pygame.quit()

