# Physics Simulator

A Python-based physics simulator designed to simulate movement, collisions, and friction within a dynamic environment filled with customizable entities like polygons and balls. The project focuses on efficiency and precision through collision optimization techniques, making it suitable for educational purposes.

## Features
- **Collision optimization:**
    - Utilizes bounding boxes for efficient collision detection.
    - Implements spatial grids to further optimize performance in complex simulations.

- **Entity Support:**
    - Simulate the behavior of both rigid bodies like polygons and dynamic objects like balls.
- **Real-Time Simulation:**
    - Watch entities interact in real-time with adjustable parameters.
## Installation
To get started, follow these steps:
1. Clone the repository:
```bash
git clone https://github.com/leomanga/Armando
```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To launch the simulator, simply run the following command:
```bash
python main.py
```

To add new entities to the simulation, use the ```Spawner``` class located in ```./Models/```. The ```Spawner``` class allows you to define and customize the properties of new entities (e.g., shape, size, initial velocity).

# Future Enhancements
Here's a list of planned features and improvements:
   - [ ] Add acceleration to the field
   - [ ] Friction management
       - [ ] With air
       - [ ] With solids
       - [ ] Rolling friction
   - [ ] Handle window size based on screen resolution
   - [ ] Display velocity and acceleration vectors

## Authors
This project is developed by:
- **leomanga** - [Github Profile](https://github.com/leomanga)
- **Woodman04** - [Github Profile](https://github.com/Woodman04)
