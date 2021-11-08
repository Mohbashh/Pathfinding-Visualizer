# Pathfinding-Visualizer

This is a pathfinding algorithm visualizer that can demonstrate how Depth-First Search, Breadth-First Search, A* Search, and Greedy-Best-First Search. You select a start and end location by clicking a position on the grid, then you can place walls in any location you wish. After doing that, you can use any of the following commands:

Q - Creates random walls iteratively from the top, bottom, and left <br />
R - Creates random walls probabilistically throughout the grid <br />
X - Creates an X pattern on the grid <br />
<br />
D - Depth First Search <br />
B - Breadth First Search <br />
G - Greedy Best First Search <br />
[SPACE] - A* search <br />

M - menu with all the instructions from above
C - Clears the board

# Requirements
import pygame <br />
import pygame_menu <br />
import random <br />
from queue import PriorityQueue
