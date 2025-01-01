# import modules
import pygame
from random import choice

# define resoluation of screen and grid sizes of maze
RES = WIDTH, HEIGHT = 900, 600
TILE = 50
cols, rows = WIDTH // TILE, HEIGHT // TILE
FPS = 30

# basic pygame for GUI
pygame.init()
sc = pygame.display.set_mode(RES)
pygame.display.set_caption("Depth First Search(DFS) Maze Maker Algorithm")
clock = pygame.time.Clock()

# class cell for cell drawing and doing things
class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color('#f70067'),
                         (x + 2, y + 2, TILE - 2, TILE - 2),border_radius=20)

    def draw(self):
        x, y = self.x * TILE, self.y * TILE

        if self.visited:
            pygame.draw.rect(sc, pygame.Color('#1e1e1e'),
                             (x, y, TILE, TILE))

        if self.walls['top']:
            pygame.draw.line(sc, (0,255,0), 
                             (x, y), (x + TILE, y), 3)
        if self.walls['right']:
            pygame.draw.line(sc, (0,255,0), 
                             (x + TILE, y), 
                             (x + TILE, y + TILE), 3)
        if self.walls['bottom']:
            pygame.draw.line(sc, (0,255,0), 
                             (x + TILE, y + TILE),
                             (x , y + TILE), 3)
        if self.walls['left']:
            pygame.draw.line(sc, (0,255,0), 
                             (x, y + TILE), (x, y), 3)

    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]
    
    def check_neighbors(self):
        neighbors = []

        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)

        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)

        return choice(neighbors) if neighbors else False

# remove walls betweem two cells
def remove_walls(current,next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False

    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False

# for creating 1D list of grid of cells
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
stack = []

while True:
    # background filling
    sc.fill(pygame.Color('#a6d5e2'))
    
    # close or exit event handling 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    #for draw cells
    [cell.draw() for cell in grid_cells]
    current_cell.visited = True
    current_cell.draw_current_cell()

    # actual Depth First Search(DFS) Maze Maker Algorithm
    next_cell = current_cell.check_neighbors()
    if next_cell:
        next_cell.visited = True
        remove_walls(current_cell,next_cell)
        stack.append(current_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()
        
    # basic pygame GUI to update screen and set FPS
    pygame.display.flip()
    clock.tick(FPS)