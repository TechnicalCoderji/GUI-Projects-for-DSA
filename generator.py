# Algorithms To Generate Sudoku
import pygame
import saver_loader as SL
# Import Classes from Tools
from tools import ToolButton, InputBox, GameBoard
# Import Functions from Tools
from tools import blit_text
from algorithm import sudoku_generator

pygame.init()

# For Screen/Window Basic
WIDTH = 700
HEIGHT = 600
RES = WIDTH,HEIGHT
win = pygame.display.set_mode(RES)
pygame.display.set_caption("SUDOKU - Dip Parmar - Generator")
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

# For Converting Sudoku back to object state
def togrid(list_grid):
    for i in range(9):
        for j in range(9):
            cell = list_grid[i][j]
            if cell:
                GameBoard.board[(i, j)].text = str(cell)
            else:    
                GameBoard.board[(i, j)].text = None

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
    blit_text(win,"  Sudoku\nGenerator\nAlgorithm",(15,500),font_small_33,(255,255,255))

    # For Tools Button
    for button in tool_buttons:
        button.draw(win)

    # For Game Board Drawing
    GameBoard.draw(win)

    if save_load_screen == "save":
        # For Transparent Background
        win.blit(transparent_surface,(0,0))

        # For Background Box
        pygame.draw.rect(win,(50,50,50),(250,200,300,200),0,20)
        pygame.draw.rect(win,(200,200,200),(250,200,300,200),5,20)
        pygame.draw.rect(win,(100,100,100),(250,200,300,50),0,border_top_left_radius=20,border_top_right_radius=20)

        blit_text(win,"Save Menu",(265,215),font_small,(255,255,255))
        blit_text(win,"Enter File Name:",(275,260),font_small_mini,(220,220,220))
        # For Input Box Draw
        input_box.draw(win)
        close_button.draw(win) # For Close Button Draw on Screen
        save_button.draw(win) # For Save Button Draw

# For Handling Game events
def handle_event(event):
    if save_load_screen == "save":
        close_button.handle_event(event)
        save_button.handle_event(event)
        input_box.handle_event(event)

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
# For Save File
def save_menu_fun():
    global save_load_screen
    save_load_screen = "save"

# For Delete Entire Board
def delete_fun():
    global gen
    for pos in GameBoard.board:
        GameBoard.board[pos].text = None
        GameBoard.board[pos].permanent = False

    gen = None

# For Close Mini-Window of Save-Load Screen
def close_fun():
    global save_load_screen
    save_load_screen = None

# For Finally Save The File
def save_fun():
    global save_load_screen
    SL.save_sudoku(input_box.text,GameBoard.board)
    save_load_screen = None

# For Choose Algorithm to Generate Sudoku
def algo_menu_fun(algo_name):
    global gen
    gen = sudoku_generator(algo_name)

# Objects
GameBoard.set_board(130,30,540)

# For Save
close_button = ToolButton(500,205,40,40,"img\close.png","Close",close_fun)
input_box = InputBox(270,280,260,40,"mygame")
save_button = ToolButton(370,330,60,60,"img\diskette.png","Save",save_fun)

tool_buttons = [] # For Tool Button List
# Save Tool Button
tool_buttons.append(ToolButton(40,40,50,50,"img\diskette.png","Save",save_menu_fun))
# Delete Tool Buttom
tool_buttons.append(ToolButton(40,95,50,50,"img\delete.png","Delete",delete_fun))

# For SUDOKU Generator Algorithm
tool_buttons.append(ToolButton(40,210,50,50,"img\\1.png","Easy",algo_menu_fun,("easy",)))
tool_buttons.append(ToolButton(40,265,50,50,"img\\2.png","Medium",algo_menu_fun,("medium",)))
tool_buttons.append(ToolButton(40,320,50,50,"img\\3.png","Hard",algo_menu_fun,("hard",)))
tool_buttons.append(ToolButton(40,375,50,50,"img\\4.png","Expert",algo_menu_fun,("expert",)))
tool_buttons.append(ToolButton(40,430,50,50,"img\\5.png"," Legendary ",algo_menu_fun,("legendary",)))

# Main Function That Start Execution Of Program
def main():
    global save_load_screen, gen

    gen = None
    save_load_screen = None

    # For Gameloop
    while True:

        # For Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            # For handle Sudoku Events
            handle_event(event)

        # For Sudoku Generation Steps
        if gen:
            n = next(gen)
            if n:
                togrid(n)
            else:
                gen = None
            
        # For Drawing Sudoku On Screen
        draw_win(win)

        pygame.display.flip()
        clock.tick(FPS)

if __name__=="__main__":
    main()
    pygame.quit()
    exit()