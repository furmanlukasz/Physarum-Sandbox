# Physarum-Sandbox

Welcome to Physarum-Sandbox, an interactive simulation sandbox that implements granular behavior of physarum-polycephalum organisms using Object-Oriented Programming (OOP) in Python, with inspiration from [Jeff Jones'](https://uwe-repository.worktribe.com/output/980579) paper and [Sage Jensen's](https://sagejenson.com/physarum) blog. This application utilizes PyQt6 for GUI interactions and Pygame for rendering simulation elements, providing a user-friendly platform to experiment with various simulation configurations.

![Env](movie.gif)

## Features
- Interactive sliders for real-time adjustment of simulation parameters such as decay and diffusion rates.
- A rich simulation environment where agents representing physarum organisms seek food and navigate the grid.
- Real-time visualization of agent behavior and trail formation, with the ability to add or remove agents and food sources dynamically.
- Implementation of observer patterns for agent state management and efficient state updates.

## Requirements
- Python 3.6 or higher
- PyQt6
- Pygame
- Numba
- NumPy

## Installation
Clone the repository to your local machine using:
`git clone https://github.com/furmanlukasz/Physarum-Sandbox.git`

Install the required packages:
`pip install PyQt6 pygame numba numpy`


## Usage
Run `main.py` to start the simulation. Use the sliders to adjust decay and diffusion rates, and interact with the simulation grid to add or remove food sources or agents. Use `A` key to add agent at mouse position, `D` key to delete agent on mouse position, `LMB` to add food to the enviroment grid & `RMB` to decrese food produced by agent chemotrails. 

## Configuration
Edit `config.py` to tweak the simulation parameters like grid size, agent count, food count, and more to customize the simulation to your liking.

## Visualization
The `renderer.py` module uses Pygame to render the simulation, showcasing the movement and behavior of agents as well as the evolution of the environment over time. 

## Simulation Logic
`simulation.py` contains the main logic for the simulation, including agent behavior, grid updates, and interaction handling.

## Agents and States
`agents.py` and `state.py` define the agent behaviors and their states using a state pattern for modularity and ease of expansion.

## Contributions
Contributions are welcome! Please fork the repository, create your feature branch, and submit a pull request for review.

## License
This project is licensed under the MIT License.

