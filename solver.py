# For Main Sudoku Logic and Game
import pygame
import saver_loader as SL
# Import Classes from Tools
from tools import ToolButton, FileBrowserBox, GameBoard
# Import Functions from Tools
from tools import blit_text
from algorithm import backtracking_solver, brute_force_solver, constraint_propagation_solver, advanced_backtracking_solver, DLX

pygame.init()

# For Screen/Window Basic
WIDTH = 700
HEIGHT = 600
RES = WIDTH,HEIGHT
win = pygame.display.set_mode(RES)
pygame.display.set_caption("SUDOKU - Dip Parmar")
clock = pygame.Clock()
FPS = 30

# Global Variables
font_small = pygame.font.Font(None, 45)
font_small_33 = pygame.font.Font(None, 33)
font_small_mini = pygame.font.Font(None, 25)

# Define a color with an alpha value (RGBA)
transparent_color = (0, 0, 0, 150)  # RGB Color with 50% transparency

# Create a surface with transparency
transparent_surface = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
transparent_surface.fill(transparent_color)

# Funtions and Classes
# class for Sudoku Solver
class Algorithm:
    algo_dict = {"brute force":brute_force_solver,
                 "backtracking":backtracking_solver,
                 "advanced backtracking":advanced_backtracking_solver,
                 "constraint propagation":constraint_propagation_solver,
                 "dlx":DLX}
    
    def __init__(self,algorithm):
        self.name = algorithm
        self.current_gen = Algorithm.algo_dict[algorithm]
        if algorithm == "dlx":
            self.current_gen(GameBoard.board)
        else:
            self.gen = self.current_gen(GameBoard.board)

    def update(self):
        if self.name != "dlx":
            next(self.gen)

# For Drawing Screen
def draw_win(win:pygame.surface.Surface):

    win.fill((97, 136, 199))

    # For Side-1 Box
    pygame.draw.rect(win, (0,0,0), (30,30,70,125))
    pygame.draw.rect(win, (200,200,200), (30,30,70,125), 5)
    blit_text(win,"Tools",(25,160),font_small,(255,255,255))

    # For Side-2 Box
    pygame.draw.rect(win, (0,0,0), (30,200,70,290))
    pygame.draw.rect(win, (200,200,200), (30,200,70,290), 5)
    blit_text(win,"  Sudoku\n   Solver\nAlgorithm",(15,500),font_small_33,(255,255,255))

    # For Game Board Drawing
    GameBoard.draw(win)

    # For Tools Button
    for button in tool_buttons:
        button.draw(win)

    if save_load_screen == "open":
        # For Transparent Background
        win.blit(transparent_surface,(0,0))

        # For Background Box
        pygame.draw.rect(win,(50,50,50),(250,100,300,400),0,20)
        pygame.draw.rect(win,(200,200,200),(250,100,300,400),5,20)
        pygame.draw.rect(win,(100,100,100),(250,100,300,50),0,border_top_left_radius=20,border_top_right_radius=20)
        
        blit_text(win,"Open Menu",(265,115),font_small,(255,255,255))
        blit_text(win,"Select File To Open:",(275,160),font_small_mini,(220,220,220))

        close_button_1.draw(win) # For Close Button Draw on Screen
        filelist_box.draw(win)
        open_button.draw(win)

# For Handling Game events
def handle_event(event):
    if save_load_screen == "open":
        close_button_1.handle_event(event)
        open_button.handle_event(event)
        filelist_box.handle_event(event)

    else:

        if event.type == pygame.MOUSEBUTTONDOWN:
            GameBoard.handle_event(event)

        for button in tool_buttons:
            button.handle_event(event)

        if event.type == pygame.KEYDOWN:
            # For Print Something -- Only for Test
            if event.key == pygame.K_p:
                print(len(GameBoard.undo_stack))

# Functions For Tools

# For Open File
def open_menu_fun():
    global save_load_screen
    save_load_screen = "open"

# For Delete Entire Board
def delete_fun():
    global algo_obj
    for pos in GameBoard.board:
        GameBoard.board[pos].text = None
        GameBoard.board[pos].permanent = False

    # Add logic to stop Algorithm
    algo_obj = None

# For Close Mini-Window of Save-Load Screen
def close_fun():
    global save_load_screen
    save_load_screen = None

# For Finally Open The File
def open_fun():
    global save_load_screen
    SL.load_sudoku(filelist_box.selected_file,GameBoard.board)
    save_load_screen = None

# For Solving Algorithm
def algo_menu_fun(algo_name):
    global algo_obj
    algo_obj = Algorithm(algo_name)

# Objects
GameBoard.set_board(130,30,540)

# Close Load
close_button_1 = ToolButton(500,105,40,40,"img\close.png","Close",close_fun)
open_button = ToolButton(370,430,60,60,"img\\folder.png","Open",open_fun)
filelist_box = FileBrowserBox(270,180,260,240,"game boards")

tool_buttons = [] # For Tool Button List
# Open Tool Button
tool_buttons.append(ToolButton(40,40,50,50,"img\\folder.png","Open",open_menu_fun))
# Delete Tool Buttom
tool_buttons.append(ToolButton(40,95,50,50,"img\delete.png","Delete",delete_fun))

# For SUDOKU Solving Algorithm
tool_buttons.append(ToolButton(40,210,50,50,"img\\1.png","Brute Force",algo_menu_fun,("brute force",)))
tool_buttons.append(ToolButton(40,265,50,50,"img\\2.png","Backtracking",algo_menu_fun,("backtracking",)))
tool_buttons.append(ToolButton(40,320,50,50,"img\\3.png","Advanced Backtracking",algo_menu_fun,("advanced backtracking",)))
tool_buttons.append(ToolButton(40,375,50,50,"img\\4.png","Constraint Propagation",algo_menu_fun,("constraint propagation",)))
tool_buttons.append(ToolButton(40,430,50,50,"img\\5.png","Dancing Links (DLX)",algo_menu_fun,("dlx",)))

# Main Function That Start Execution Of Program
def main():
    global save_load_screen, algo_obj
    
    algo_obj = None
    save_load_screen = None

    # For Gameloop
    while True:

        # For Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            # For handle Sudoku Events
            handle_event(event)

        # For Algorithm Update
        if algo_obj:
            algo_obj.update()

        # For Drawing Sudoku On Screen
        draw_win(win)

        pygame.display.flip()
        clock.tick(FPS)

if __name__=="__main__":
    main()
    pygame.quit()
    exit()