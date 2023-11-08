# config.py :
PI = 3.14159

class Config:
    DECAY = 0.45 # Decay rate of the chemotrails
    DIFFUSION = 0.4 # Diffusion rate of the chemotrails
    SENSOR_ANGLE = PI / 8 # Angle between each sensor
    SENSOR_DISTANCE = 3 # Distance to sense for food sources
    MOVE_DISTANCE = 2 # Distance to move forward each step
    AGENT_COUNT = 2 # Number of agents to place on the grid at the start of the simulation 
    FOOD_COUNT = 100 # Number of food sources to place on the grid at the start of the simulation
    FOOD_VALUE = 1.0 # Amount of food to add when a food source is consumed by an agent
    INIT_FOOD_RADIUS = 1 # Radius of initial food sources
    INIT_FOOD_VALUE = 1.0 # Amount of food to add when a food source is placed on the grid
    FOOD_RADIUS = 7 # Radius of food sources
    POSTFOOD_VALUE = 1.0 # Amount of food to add when a food source is placed on the grid after simulation start - work with mouse click
    GRID_SIZE = (150, 150) # Size of the grid in cells
    CELL_SIZE = 10 # Size of each cell in pixels
    SIMULATION_DELAY = 0 # Delay between simulation steps in milliseconds
    BACKGROUND_COLOR = (0, 0, 0)
    AGENT_DEFAULT_COLOR = (255, 255, 255)
    AGENT_SEARCH_COLOR = (255, 0, 0)
    AGENT_FEED_COLOR = (0, 255, 0)
    MAX_TRAIL_VALUE = 1 # Maximum value of a cell in the grid
    TRAIL_VALUE = 1 # Amount of trail to add when an agent moves
    CLEAR_RADIUS = 5 # Radius within which chemotrails are cleared
    FRAMERATE = 60 # Framerate of the visualization



