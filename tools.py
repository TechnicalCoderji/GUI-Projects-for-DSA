# Classes and Functions For Pygame GUI and Game Related Function For Common Use In All Files
import pygame
import os

pygame.init()

# Global Variables

# Font Variables
font_35 = pygame.font.Font(None,35)
font_24 = pygame.font.Font(None, 24)
font_small_mini = pygame.font.Font(None, 25)
font_small = pygame.font.Font(None, 45)

# Class For Text Blinking
def blit_text(screen, text, position, font, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

# Class For Tool Button
class ToolButton:

    def __init__(self, x, y, width, height, image_path, subtext, action_fun,args:tuple=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path) # Load an image
        self.image = pygame.transform.scale(self.image, (width-20, height-20))  # For Resize the image
        self.image_rect = self.image.get_rect() # Create a rectangle around the image
        self.image_rect.topleft = (x+10,y+10) # Set the position of the rectangle

        # Create an oval shape for subtext background
        self.font = font_small_mini
        self.subtext = subtext
        if len(subtext)<8:
            self.oval_rect = pygame.Rect(0, 0, 80, 30)  # Width and height of oval
            self.oval_rect.center = (self.rect.centerx, self.rect.top - 10)  # Position above button
        else:
            self.oval_rect = pygame.Rect(0, 0, len(subtext)*10, 30)  # Width and height of oval
            self.oval_rect.topleft = (self.rect.left - 30, self.rect.top - 10)  # Position above button

        self.button_color = (50,50,50)
        self.outline_color = (200,200,200)
        self.hover_color = (100,100,100)
        self.oval_color = (0,0,0)
        self.oval_border_color = (200,200,200)
        self.subtext_color = (255,255,255)

        self.action_fun = action_fun
        self.hovered = False
        self.args =args

    def draw(self, screen):

        # Change color if hovered
        if self.hovered:
            pygame.draw.rect(screen, self.outline_color, self.rect, 0, 10)
            pygame.draw.rect(screen, self.hover_color, self.rect, 3, 10)
            
        # For Normal Button
        else:
            pygame.draw.rect(screen, self.button_color, self.rect, 0, 10)
            pygame.draw.rect(screen, self.outline_color, self.rect, 3, 10)
        
        # For Drawing Image
        screen.blit(self.image, self.image_rect.topleft)

        # Change color if hovered
        if self.hovered:
            # For Sub-Text
            pygame.draw.rect(screen, self.oval_color, self.oval_rect, 0, 10) # Draw oval background
            pygame.draw.rect(screen, self.oval_border_color, self.oval_rect, 2, 10) # Draw oval border
            subtext_surface = self.font.render(self.subtext, True, self.subtext_color) # Add subtext
            screen.blit(subtext_surface, (self.oval_rect.centerx - subtext_surface.get_width() // 2, self.oval_rect.centery - subtext_surface.get_height() //2))

    def handle_event(self, event):
        # Check if the mouse is over the button
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

         # Check if the button is clicked
        if self.hovered and event.type == pygame.MOUSEBUTTONDOWN:
            if self.args:
                self.action_fun(*self.args)
            else:
                self.action_fun()

# For FileBrowserBox
class FileBrowserBox:
    def __init__(self, x, y, width, height, folder_path):
        self.rect = pygame.Rect(x+5, y+5, width-10, height-10)
        self.big_rect = pygame.Rect(x, y, width, height)
        self.folder_path = folder_path
        self.files = [file_name[:-7] for file_name in os.listdir(folder_path)]
        self.selected_file = None
        self.scroll_offset = 0
        self.font = font_24
        self.bg_color = (200,200,200)
        self.out_line_color = (100,100,100)
        self.hover_color = (150, 150, 250)
        self.click_color = (50, 200, 50)
        self.text_color = (0, 0, 0)
        self.file_height = 30
        self.scroll_bar_width = 10
        self.hovered_file = None

    def draw(self, screen):
        # Draw the box background
        pygame.draw.rect(screen, self.bg_color, self.big_rect,0,10)

        # Calculate visible files
        max_files = self.rect.height // self.file_height
        start_index = self.scroll_offset
        end_index = min(start_index + max_files, len(self.files))

        # Draw files in the box
        for index in range(start_index, end_index):
            file_name = self.files[index]
            file_rect = pygame.Rect(
                self.rect.x, self.rect.y + (index - start_index) * self.file_height,
                self.rect.width - self.scroll_bar_width, self.file_height
            )

            # Draw the file's background (hover and click visual effects handled in handle_event)
            if file_name == self.hovered_file:
                pygame.draw.rect(screen, self.hover_color, file_rect)
                
            if file_name == self.selected_file:
                pygame.draw.rect(screen, self.click_color, file_rect)

            # Draw the file name
            blit_text(screen,file_name,(file_rect.x + 5, file_rect.y + 5),self.font,self.text_color)

        # Draw the scroll bar
        total_files = len(self.files)
        if total_files > max_files:
            scroll_bar_rect = pygame.Rect(
                self.rect.x + self.rect.width - self.scroll_bar_width, self.rect.y,
                self.scroll_bar_width, self.rect.height
            )
            pygame.draw.rect(screen, (180, 180, 180), scroll_bar_rect)

            # Scroll bar handle
            scroll_ratio = self.scroll_offset / max(1, total_files - max_files)
            scroll_bar_height = max(20, self.rect.height * (max_files / total_files))
            scroll_bar_y = self.rect.y + scroll_ratio * (self.rect.height - scroll_bar_height)
            scroll_bar_handle_rect = pygame.Rect(
                self.rect.x + self.rect.width - self.scroll_bar_width, scroll_bar_y,
                self.scroll_bar_width, scroll_bar_height
            )
            pygame.draw.rect(screen, (100, 100, 100), scroll_bar_handle_rect)

        pygame.draw.rect(screen, self.out_line_color, self.big_rect,5,10)

    def scroll(self, direction):

        max_files = self.rect.height // self.file_height
        if direction == 'up' and self.scroll_offset > 0:
            self.scroll_offset -= 1
        elif direction == 'down' and self.scroll_offset < len(self.files) - max_files:
            self.scroll_offset += 1

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 4:  # Scroll up
                self.scroll('up')
            elif event.button == 5:  # Scroll down
                self.scroll('down')
            elif event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                max_files = self.rect.height // self.file_height
                start_index = self.scroll_offset
                end_index = min(start_index + max_files, len(self.files))

                for index in range(start_index, end_index):
                    file_rect = pygame.Rect(
                        self.rect.x, self.rect.y + (index - start_index) * self.file_height,
                        self.rect.width - self.scroll_bar_width, self.file_height
                    )
                    if file_rect.collidepoint(mouse_pos):
                        self.selected_file = self.files[index]

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            max_files = self.rect.height // self.file_height
            start_index = self.scroll_offset
            end_index = min(start_index + max_files, len(self.files))

            self.hovered_file = None
            for index in range(start_index, end_index):
                file_rect = pygame.Rect(
                    self.rect.x, self.rect.y + (index - start_index) * self.file_height,
                    self.rect.width - self.scroll_bar_width, self.file_height
                )
                if file_rect.collidepoint(mouse_pos):
                    self.hovered_file = self.files[index]
                
    def update(self):
        self.files = [file_name[:-7] for file_name in os.listdir(self.folder_path)]

# Class For Input-Text
class InputBox:

    def __init__(self,x,y,width,height,text=""):
        self.rect = pygame.Rect(x,y,width,height)
        self.text = text
        self.active = False
        self.font = font_35

        # Colors
        self.box_color = (25,25,25)
        self.font_color = (125,125,125)
        self.outline_color = (125,125,125)
        self.active_box_color = (100,100,100)
        self.active_font_color = (225,225,225)
        self.active_outline_color = (225,225,225)

    def draw(self,screen):
        if self.active:
            pygame.draw.rect(screen,self.active_box_color,self.rect,0,5)
            pygame.draw.rect(screen,self.active_outline_color,self.rect,3,5)
            pos = (self.rect.topleft[0]+10,self.rect.topleft[1]+7)
            blit_text(screen,self.text,pos,self.font,self.active_font_color)
        else:
            pygame.draw.rect(screen,self.box_color,self.rect,0,5)
            pygame.draw.rect(screen,self.outline_color,self.rect,3,5)
            pos = (self.rect.topleft[0]+10,self.rect.topleft[1]+7)
            blit_text(screen,self.text,pos,self.font,self.font_color)

    def handle_event(self,event):
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse is over the button
            mouse_pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(mouse_pos):
                self.active = True
            else:
                self.active = False

        if self.active and event.type == pygame.KEYDOWN:
        
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1] if self.text else ""
            elif event.unicode.isalnum():
                self.text += event.unicode

# Class for individual Block
class Block:
    main_pos = (0,0)
    pen_color = (255,255,255)

    def __init__(self, x, y ,text ,width):
        self.x = x # X(column) Position of Block in Board Dictonary
        self.y = y # Y(row) Position of Block in Board Dictonary
        self.text = text # Number Between 1-9, Value of Block
        self.width = width # Width of Block
        self.rect = pygame.Rect(Block.main_pos[0]+(x*self.width), Block.main_pos[1]+(y*self.width), self.width, self.width) # Block Rect
        self.pen_color = Block.pen_color
        self.text_color = self.pen_color
        self.outline_color = (200,200,200)
        self.highlight_color = (50,70,70)
        self.highlight1_color = (100,110,110)
        self.permanent = False
        self.error = False
        self.highlight = False
        self.highlight1 = False

    def draw(self, screen:pygame.surface.Surface):
        if self.highlight1:
            pygame.draw.rect(screen, self.highlight1_color, self.rect)
        elif self.highlight:
            pygame.draw.rect(screen, self.highlight_color, self.rect)

        # For Change Color Where Error
        if self.permanent:
            self.text_color = (0,200,0)
        # For Error block
        elif self.error:
            self.text_color = (200,0,0)
            self.outline_color = (255,0,0)
        # For Normal Block
        else:
            self.text_color = self.pen_color
            self.outline_color = (200,200,200)

        # For outline of all Small box
        pygame.draw.rect(screen, self.outline_color, self.rect, 1)

        # For Numbers blit on Screen
        if self.text:
            blit_text(screen, self.text, (self.rect.x+20, self.rect.y+20), font_small, self.text_color)

    def handle_event(self, event):
        # Check if the mouse is over the button
        mouse_pos = pygame.mouse.get_pos()
        
        # Check if the button is clicked
        if self.rect.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
            if RemainingButton.selected_text and not self.permanent:
                GameBoard.undo_stack.append([GameBoard.board[pos].text for pos in GameBoard.board])
                self.text = RemainingButton.selected_text
                self.pen_color = Block.pen_color
                GameBoard.check_error()
                GameBoard.current_selected_block = self
            else:
                GameBoard.current_selected_block = self

# Class For Game Board
class GameBoard:
    current_selected_block = None
    undo_stack = []

    @staticmethod
    def set_board(x,y,width):
        GameBoard.y = y # Y position of Game Board
        GameBoard.x = x # X position of Game Board
        GameBoard.width = width # Width of Game Board
        GameBoard.rect = (GameBoard.x, GameBoard.y, GameBoard.width, GameBoard.width) # Rect of Game Board
        GameBoard.big_box_width = width/3 # 3x3 Box Width
        GameBoard.remaining_numbers = {str(i):0 for i in range(1,10)} # Remaining number List of Sudoku

        Block.main_pos = (x,y) # Setting Block Start Cordinets
        GameBoard.board = {(a,b):Block(a,b,None,GameBoard.width/9) for a in range(9) for b in range(9)}
        GameBoard.blocks = GameBoard.__split_into_blocks() # For 3x3 Block Division
        GameBoard.selected_box_set = set()
        GameBoard.selected_box_set1 = set()

    @staticmethod
    def draw(screen:pygame.surface.Surface):
        # For Selecting Boxes
        GameBoard.selected_box_set.clear() # Clear Old Set
        GameBoard.selected_box_set1.clear() # Clear Old Set
        if GameBoard.current_selected_block:
            GameBoard.__select_box()

        for pos in GameBoard.board.keys():
            box = GameBoard.board[pos]

            # For Background Color
            if (pos[0]%3 == 0) and (pos[1]%3 == 0):

                # For Black and Light-Black
                color_bg = (50,50,50)
                if ((pos[0]*3)+pos[1])%2 == 0:
                    color_bg = (0,0,0)
                    
                # For Background Color
                pygame.draw.rect(screen, color_bg, (box.rect.x, box.rect.y , GameBoard.big_box_width, GameBoard.big_box_width))

            # For Highlight Logic
            if GameBoard.selected_box_set and (box in GameBoard.selected_box_set):
                box.highlight = True
            else:
                box.highlight = False

            # For Highlight - 1 Logic
            if GameBoard.selected_box_set1 and (box in GameBoard.selected_box_set1):
                box.highlight1 = True
            else:
                box.highlight1 = False

            # For Block Drawing
            box.draw(screen)

        for pos in GameBoard.board.keys():
            box = GameBoard.board[pos]

            if (pos[0]%3 == 0) and (pos[1]%3 == 0):
                # For outline of 3x3 box
                pygame.draw.rect(screen, (200,200,200),(box.rect.x, box.rect.y , GameBoard.big_box_width, GameBoard.big_box_width), 3)

        # For Outline of Big box - Game Board 
        pygame.draw.rect(screen,(200,200,200),GameBoard.rect,5)

        # Logic For Update Important things on every Frame
        # For Updating Remainig Number
        GameBoard.remaining_numbers = {str(i):0 for i in range(1,10)}
        for pos in GameBoard.board:
            value = GameBoard.board[pos].text
            if value:
                GameBoard.remaining_numbers[value] += 1

        if RemainingButton.selected_text and GameBoard.remaining_numbers[RemainingButton.selected_text]>8:
            RemainingButton.selected_text = None

        while len(GameBoard.undo_stack) > 50: # Limit Of Undo
            GameBoard.undo_stack.pop(0)

    @staticmethod
    def handle_event(event):
        # For checking Every Box event
        for pos in GameBoard.board.keys():
            box = GameBoard.board[pos]
            box.handle_event(event)

    # Method For Select Highlighted box
    @staticmethod
    def __select_box():
        selected_box = GameBoard.current_selected_block
        selected_pos = (selected_box.x , selected_box.y)
        GameBoard.selected_box_set1.add(selected_box) # Current Box
        selected_blocks = list(GameBoard.__identify_block(*selected_pos)) # 3x3 Block List

        for pos in GameBoard.board:
            my_block = GameBoard.board[pos]

            # For Selected Number
            if selected_box.text and my_block.text == selected_box.text:
                GameBoard.selected_box_set1.add(my_block)

            # For Row and Column
            if pos[0] == selected_pos[0] or pos[1] == selected_pos[1]:
                GameBoard.selected_box_set.add(my_block)

            # For 3x3 Box
            if pos in selected_blocks:
                GameBoard.selected_box_set.add(my_block)

    # Function to split dictionary into 3x3 blocks
    @staticmethod
    def __split_into_blocks():
        blocks = {}
        for i in range(3):  # 3 rows of blocks
            for j in range(3):  # 3 columns of blocks
                # Extract members belonging to the (i, j)-th block
                blocks[(i, j)] = [(x, y) for (x, y) in GameBoard.board.keys() 
                                if x // 3 == i and y // 3 == j]
        return blocks

    # Function to identify which block the given coordinate belongs to
    @staticmethod
    def __identify_block(x, y):
        for block_members in GameBoard.blocks.values():
            if (x ,y) in block_members:
                return block_members
        return None
    
    @staticmethod
    def check_error():
        # Checking Sudoku Rules
        for pos in GameBoard.board:
            my_block = GameBoard.board[pos]
            if my_block.text:

                # For Row
                row = [GameBoard.board[(i,j)] for i,j in GameBoard.board if i == pos[0]]
                row.remove(my_block)
                for block in row:
                    if block.text == my_block.text:
                        my_block.error = True
                        break
                else:

                    # For Column
                    col = [GameBoard.board[(i,j)] for i,j in GameBoard.board if j == pos[1]]
                    col.remove(my_block)
                    for block in col:
                        if block.text == my_block.text:
                            my_block.error = True
                            break
                    else:

                        # For Block
                        selected_blocks = list(GameBoard.__identify_block(pos[0],pos[1]))
                        selected_blocks.remove(pos)
                        for block_pos in selected_blocks:
                            if GameBoard.board[block_pos].text == my_block.text:
                                my_block.error = True
                                break
                        else:
                            my_block.error = False
            else:
                my_block.error = False # For No Error

# Class For Remaining Button
class RemainingButton:
    # Static Variable For Class
    selected_text = None

    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font_small
        self.font_min = font_small_mini
        self.font_color = (255,255,255)
        self.button_color = (50,50,50)
        self.outline_color = (200,200,200)
        self.hover_color = (100,100,100)
        self.selected_color = (0, 200, 0)
        # self.selected = False
        self.hovered = False

    def draw(self, screen):

        # Draw Remaining text
        remaining_text = str(9-GameBoard.remaining_numbers[self.text])
        r_text_surf = self.font_min.render(remaining_text, True, (0,0,0))
        cordinates = (self.rect.topright[0]-5,self.rect.topright[1]+5)
        r_text_rect = r_text_surf.get_rect(center=cordinates)

        # Change color if hovered or selected
        if self.text == RemainingButton.selected_text:
            pygame.draw.rect(screen, self.selected_color, self.rect, 0, 10)
            pygame.draw.rect(screen, self.outline_color, self.rect, 3, 10)

            # For Circle at Top-Right
            pygame.draw.circle(screen,(50,50,50),cordinates,12,2)
            pygame.draw.circle(screen,(200,200,200),cordinates,10)
            screen.blit(r_text_surf, r_text_rect)

        elif self.hovered:
            pygame.draw.rect(screen, self.outline_color, self.rect, 0, 10)
            pygame.draw.rect(screen, self.hover_color, self.rect, 3, 10)

            # For Circle at Top-Right
            pygame.draw.circle(screen,(50,50,50),cordinates,12,2)
            pygame.draw.circle(screen,(200,200,200),cordinates,10)
            screen.blit(r_text_surf, r_text_rect)

        else:
            pygame.draw.rect(screen, self.button_color, self.rect, 0, 10)
            pygame.draw.rect(screen, self.outline_color, self.rect, 3, 10)
        
        # Draw text
        text_surf = self.font.render(self.text, True, self.font_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        # Check if the mouse is over the button
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        # Check if the button is clicked
        if self.hovered and event.type == pygame.MOUSEBUTTONDOWN:
            GameBoard.current_selected_block = None
            if self.text == RemainingButton.selected_text:
                RemainingButton.selected_text = None
            else:
                RemainingButton.selected_text = self.text

if __name__ == "__main__":
    pass