# agents.py :
from patterns import AgentFactory, Agent, Subject
from states import SearchState
from config import Config
import numpy as np

class PhysarumAgent(Subject, Agent):
    """ Agent class for the Physarum simulation."""
    def __init__(self, x, y, angle):
        super().__init__()
        
        self.x = int(x)  # Make sure this is an integer
        self.y = int(y)  # Make sure this is an integer
        self.angle = float(angle)  # Make sure this is a float
        self.state = SearchState()
        self.grid_size = Config.GRID_SIZE

        # Assign random values for sensor and move distance for each agent
        self.sensor_distance = np.random.uniform(low=2.0, high=8.0)  # Adjust range as needed
        self.move_distance = np.random.uniform(low=2.0, high=4.0)  # Adjust range as needed

        print(f'Creating agent at ({x}, {y}) with angle {angle}')
        print(f'Agent {self} moving {self.move_distance} units with sensor distance {self.sensor_distance}')

    def sense_and_move(self, grid):
        x = float(self.x)
        y = float(self.y)
        angle = float(self.angle)

        # Use configuration values
        sensor_angle = Config.SENSOR_ANGLE
        # sensor_distance = Config.SENSOR_DISTANCE
        sensor_distance = self.sensor_distance
        # move_distance = Config.MOVE_DISTANCE
        move_distance = self.move_distance
        
        food_value = Config.FOOD_RADIUS
        grid_size = Config.GRID_SIZE

        # Sense for food at sensor points using configuration values
        left_sensor = ((int(x + np.cos(angle - sensor_angle) * sensor_distance) % grid_size[0]),
                       (int(y + np.sin(angle - sensor_angle) * sensor_distance) % grid_size[1]))
        front_sensor = ((int(x + np.cos(angle) * sensor_distance) % grid_size[0]),
                        (int(y + np.sin(angle) * sensor_distance) % grid_size[1]))
        right_sensor = ((int(x + np.cos(angle + sensor_angle) * sensor_distance) % grid_size[0]),
                        (int(y + np.sin(angle + sensor_angle) * sensor_distance) % grid_size[1]))

        # Get the food concentration at sensor points
        left_val = grid[left_sensor]
        front_val = grid[front_sensor]
        right_val = grid[right_sensor]

        # Determine the new angle based on sensor readings
        self._update_angle(left_val, front_val, right_val, sensor_angle)

        # Move agent forward
        self._move_forward(move_distance, grid_size)

        # Leave a trail
        self._leave_trail(grid, food_value)

        # Bounce on the wall
        self._bounce_on_wall(grid_size)

        # Notify observers about the move
        self.notify_observers({'agent': self, 'x': self.x, 'y': self.y, 'state': self.state})

    def _update_angle(self, left_val, front_val, right_val, sensor_angle):
        # Move towards the direction with highest food concentration
        if left_val > right_val and left_val > front_val:
            self.angle -= sensor_angle
        elif right_val > left_val and right_val > front_val:
            self.angle += sensor_angle

    def _move_forward(self, move_distance, grid_size):
        # Update position based on the angle and move distance
        self.x = (int(self.x + np.cos(self.angle) * move_distance) % grid_size[0])
        self.y = (int(self.y + np.sin(self.angle) * move_distance) % grid_size[1])

    def _leave_trail(self, grid, food_value):
        # Increase the value at the current grid position to leave a trail
        grid[self.x, self.y] += food_value
        self.notify_observers({'agent': self, 'x': self.x, 'y': self.y, 'state': self.state})

    def _bounce_on_wall(self, grid_size):
        # Bounce on the wall if the agent is outside the grid
        if self.x < 1:
            self.x = 3
            self.angle = np.pi - self.angle
        elif self.x >= grid_size[0]-1:
            self.x = grid_size[0] - 3
            self.angle = np.pi - self.angle
        if self.y < 1:
            self.y = 3
            self.angle = -self.angle
        elif self.y >= grid_size[1]-1:
            self.y = grid_size[1] - 3
            self.angle = -self.angle

    def change_state(self, new_state):
        self.state = new_state
        self.notify_observers({'agent': self})


class PhysarumAgentFactory(AgentFactory):
    """ Factory class for creating Physarum agents. """
    def create_agent(self, x, y, angle):
        return PhysarumAgent(x, y, angle)