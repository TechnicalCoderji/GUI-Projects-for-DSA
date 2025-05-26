# This File to Save Algorithms Function For Creating and Solving Algorithms.
import time
import random
from typing import List, Iterator

# Global Variable
eliminate_dict = {}

# Functions That Used By Algorithm
def is_valid(grid, row, col, num):
    """Check if placing 'num' is valid according to Sudoku rules."""
    for i in range(9):
        if grid[(row, i)].text == num or grid[(i, col)].text == num:  # Row & Column check
            return False
        
    box_row, box_col = row - row % 3, col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[(box_row + i, box_col + j)].text == num:
                return False
    
    return True

def find_empty_cell(grid):
    """Find the next empty cell in the grid."""
    for row in range(9):
        for col in range(9):
            if grid[(row, col)].text == None:
                return row, col
    return None

def get_possibilities(grid):
    global eliminate_dict
    """Return a dict of possible values for each empty cell."""
    possibilities = {}
    for pos in grid:
        row,col = pos
        if grid[pos].text is None:
            options = set()
            for num in range(1, 10):
                if is_valid(grid, row, col, str(num)):
                    options.add(str(num))
            possibilities[pos] = options
        else:
            possibilities[pos] = set()

    # For Eliminate Naked And Hidden Pairs
    for pos in eliminate_dict:
        possibilities[pos] -= eliminate_dict[pos]

    return possibilities

def find_least_possibilities_cell(grid):
    """Find the cell with the fewest possibilities"""
    min_options = float('inf')
    selected_cell = None
    possibilities = {}

    for pos in grid:
        if grid[pos].text == None:
            options = {num for num in range(1, 10) if is_valid(grid, pos[0], pos[1], str(num))}
            if len(options) < min_options:
                min_options = len(options)
                selected_cell = pos
                possibilities[selected_cell] = options

    return selected_cell, possibilities.get(selected_cell, set())

# SUDOKU Solver Algorithms
# (1) Backtracking Algorithm
start = time.time()
def backtracking_solver(grid):
    
    empty_cell = find_empty_cell(grid)
    
    if not empty_cell:
        end = time.time()
        print(f"Execution time: {end - start} seconds")
        while True:
            yield  # Final solved grid
    
    row, col = empty_cell
    
    for num in range(1 ,10):  # Try numbers 1 to 9
        if is_valid(grid, row, col, str(num)):
            grid[(row, col)].text = str(num)  # Place number
            yield # Yield current state before recursion
            
            # Continue solving recursively
            yield from backtracking_solver(grid)
            
            grid[(row, col)].text = None  # Backtrack (undo placement)
            yield # Yield backtracked state
        
# (2) Constraint Propagation
def constraint_propagation_solver(grid):
    global eliminate_dict
    eliminate_dict = {(pos):set() for pos in grid}
    
    while True:
        print("okey")
        possibilities = get_possibilities(grid)
        changed = False

        # Naked Singles
        for pos in possibilities.copy():
            if len(possibilities[pos]) == 1:
                grid[pos].text = possibilities[pos].pop()
                changed = True
                yield

        # Hidden Singles
        for pos in grid:
            if grid[pos].text == None:

                # Check row for hidden single
                possibilities = get_possibilities(grid)
                possible_values = possibilities[pos]
                for value in possible_values:
                    is_hidden_single = True
                    for col in range(9):
                        if col != pos[1] and grid[(pos[0],col)].text == None:
                            other_values = possibilities[(pos[0],col)]
                            if value in other_values:
                                is_hidden_single = False
                                break

                    if is_hidden_single:
                        grid[pos].text = value
                        possibilities[pos] = set()
                        changed = True
                        yield
                        break

                # Check column for hidden single
                for value in possible_values:
                    is_hidden_single = True
                    for row in range(9):
                        if row != pos[0] and grid[(row,pos[1])].text == None:
                            other_values = possibilities[(row, pos[1])]
                            if value in other_values:
                                is_hidden_single = False
                                break

                    if is_hidden_single:
                        grid[pos].text = value
                        possibilities[pos] = set()
                        changed = True
                        yield
                        break

                # Check 3x3 box for hidden single
                box_row, box_col = 3 * (pos[0] // 3), 3 * (pos[1] // 3)
                for value in possible_values:
                    is_hidden_single = True
                    for r in range(box_row, box_row + 3):
                        for c in range(box_col, box_col + 3):
                            if (r != pos[0] or c != pos[1]) and grid[(r,c)].text == None:
                                other_values = possibilities[(r,c)]
                                if value in other_values:
                                    is_hidden_single = False
                                    break

                    if is_hidden_single:
                        grid[pos].text = value
                        possibilities[pos] = set()
                        changed = True
                        yield
                        break
        
        # Naked Pairs
        
        # Check each row
        possibilities = get_possibilities(grid)
        temp_posibilities = possibilities.copy()
        for row in range(9):
            # Find cells with exactly 2 possibilities
            pair_cells = [(col, possibilities[(row,col)]) for col in range(9) if len(possibilities[(row,col)]) == 2]
            
            # Look for matching pairs
            for i in range(len(pair_cells)):
                for j in range(i + 1, len(pair_cells)):
                    if pair_cells[i][1] == pair_cells[j][1]:  # Same two digits
                        # Found a naked pair
                        pair_values = pair_cells[i][1]
                        col1, col2 = pair_cells[i][0], pair_cells[j][0]
                        
                        # Remove these digits from other cells in same row
                        for col in range(9):
                            if col != col1 and col != col2:
                                eliminate_dict[(row,col)] |= pair_values
        
        # Check each column
        possibilities = get_possibilities(grid)
        for col in range(9):
            # Find cells with exactly 2 possibilities
            pair_cells = [(row, possibilities[(row,col)]) for row in range(9) if len(possibilities[(row,col)]) == 2]
            
            # Look for matching pairs
            for i in range(len(pair_cells)):
                for j in range(i + 1, len(pair_cells)):
                    if pair_cells[i][1] == pair_cells[j][1]:  # Same two digits
                        # Found a naked pair
                        pair_values = pair_cells[i][1]
                        row1, row2 = pair_cells[i][0], pair_cells[j][0]
                        
                        # Remove these digits from other cells in same column
                        for row in range(9):
                            if row != row1 and row != row2:
                                eliminate_dict[(row,col)] |= pair_values
        
        # Check each 3x3 box
        possibilities = get_possibilities(grid)
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                # Find cells with exactly 2 possibilities in this box
                pair_cells = []
                for row in range(box_row, box_row + 3):
                    for col in range(box_col, box_col + 3):
                        if len(possibilities[(row,col)]) == 2:
                            pair_cells.append(((row, col), possibilities[(row,col)]))
                
                # Look for matching pairs
                for i in range(len(pair_cells)):
                    for j in range(i + 1, len(pair_cells)):
                        if pair_cells[i][1] == pair_cells[j][1]:  # Same two digits
                            # Found a naked pair
                            pair_values = pair_cells[i][1]
                            pos1, pos2 = pair_cells[i][0], pair_cells[j][0]
                            
                            # Remove these digits from other cells in same box
                            for row in range(box_row, box_row + 3):
                                for col in range(box_col, box_col + 3):
                                    if (row, col) != pos1 and (row, col) != pos2:
                                        eliminate_dict[(row,col)] |= pair_values

        # Hidden Pairs

        # Check rows
        possibilities = get_possibilities(grid)
        for row in range(9):
            # Get empty cells in this row
            empty_cells = [(row, col) for col in range(9) if grid[(row,col)].text == None]
            
            # Get all possible numbers in this row
            all_numbers = set()
            for pos in empty_cells:
                all_numbers.update(possibilities[pos])
            
            # Check each pair of numbers
            for num1 in all_numbers:
                for num2 in all_numbers:
                    if num1 >= num2:
                        continue
                    
                    # Find cells containing both numbers
                    cells_with_pair = []
                    for pos in empty_cells:
                        if num1 in possibilities[pos] and num2 in possibilities[pos]:
                            cells_with_pair.append(pos)
                    
                    # Check if we have a hidden pair
                    if len(cells_with_pair) == 2:
                        # Verify no other cells in row contain these numbers
                        other_cells_numbers = set()
                        for pos in empty_cells:
                            if pos not in cells_with_pair:
                                other_cells_numbers.update(possibilities[pos])
                        
                        if num1 not in other_cells_numbers and num2 not in other_cells_numbers:
                            # Update candidates for the pair cells
                            eliminate_dict[cells_with_pair[0]] |= possibilities[cells_with_pair[0]] - {num1, num2}
                            eliminate_dict[cells_with_pair[1]] |= possibilities[cells_with_pair[1]] - {num1, num2}

        # Check columns
        possibilities = get_possibilities(grid)
        for col in range(9):
            empty_cells = [(row, col) for row in range(9) if grid[(row,col)].text == None]
            
            all_numbers = set()
            for pos in empty_cells:
                all_numbers.update(possibilities[pos])
            
            for num1 in all_numbers:
                for num2 in all_numbers:
                    if num1 >= num2:
                        continue
                    
                    cells_with_pair = []
                    for pos in empty_cells:
                        if num1 in possibilities[pos] and num2 in possibilities[pos]:
                            cells_with_pair.append(pos)
                    
                    if len(cells_with_pair) == 2:
                        other_cells_numbers = set()
                        for pos in empty_cells:
                            if pos not in cells_with_pair:
                                other_cells_numbers.update(possibilities[pos])
                        
                        if num1 not in other_cells_numbers and num2 not in other_cells_numbers:
                            eliminate_dict[cells_with_pair[0]] |= possibilities[cells_with_pair[0]] - {num1, num2}
                            eliminate_dict[cells_with_pair[1]] |= possibilities[cells_with_pair[1]] - {num1, num2}

        # Check 3x3 subgrids
        possibilities = get_possibilities(grid)
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                empty_cells = [
                    (row, col)
                    for row in range(box_row, box_row + 3)
                    for col in range(box_col, box_col + 3)
                    if grid[(row,col)].text == None
                ]
                
                all_numbers = set()
                for pos in empty_cells:
                    all_numbers.update(possibilities[pos])
                
                for num1 in all_numbers:
                    for num2 in all_numbers:
                        if num1 >= num2:
                            continue
                        
                        cells_with_pair = []
                        for pos in empty_cells:
                            if num1 in possibilities[pos] and num2 in possibilities[pos]:
                                cells_with_pair.append(pos)
                        
                        if len(cells_with_pair) == 2:
                            other_cells_numbers = set()
                            for pos in empty_cells:
                                if pos not in cells_with_pair:
                                    other_cells_numbers.update(possibilities[pos])
                            
                            if num1 not in other_cells_numbers and num2 not in other_cells_numbers:
                                eliminate_dict[cells_with_pair[0]] |= possibilities[cells_with_pair[0]] - {num1, num2}
                                eliminate_dict[cells_with_pair[1]] |= possibilities[cells_with_pair[1]] - {num1, num2}
        
        possibilities = get_possibilities(grid)
        if not changed and (temp_posibilities == possibilities):
            break
    
    empty_cell = find_empty_cell(grid)
    if not empty_cell:
        while True:
            yield # Final solved grid
    
    print("BackUP-Backtrack Algorithm")
    yield from backtracking_solver(grid)

# (3) Brute Force Algorithm
def brute_force_solver(grid):

    for pos in grid:
        if grid[pos].text == None:
            for num in range(1, 10):
                if is_valid(grid, pos[0], pos[1], str(num)):
                    grid[pos].text = str(num)
                    yield # Yield current grid state

                    yield from brute_force_solver(grid)

                    grid[pos].text = None  # Backtrack
                    yield # Yield backtracked state

            return # Important: stop trying after the first empty cell
    yield # Final solution

    # Final solution reached, start infinite yield loop
    while True:
        yield [r[:] for r in grid]

# (4) Advanced Backtracking Algorithm
def advanced_backtracking_solver(grid):
    cell, options = find_least_possibilities_cell(grid)
    
    if not cell:
        while True:
            yield  # Final solved grid
    
    row, col = cell
    sorted_options = sorted(options)  # Sorting possibilities
    
    for num in sorted_options:
        if is_valid(grid, row, col, str(num)):
            grid[(row, col)].text = str(num)  # Place number
            yield # Yield current state before recursion
            
            # Continue solving recursively
            yield from advanced_backtracking_solver(grid)
            
            grid[(row, col)].text = None  # Backtrack (undo placement)
            yield # Yield backtracked state

# (5) Dancing Links (DLX)
class Node:
    def __init__(self):
        self.left = self.right = self.up = self.down = self
        self.column = None

class ColumnNode(Node):
    def __init__(self, col_id):
        super().__init__()
        self.id = col_id
        self.size = 0

def create_matrix(grid):
    header = ColumnNode(-1)
    col_nodes = []
    prev = header
    for i in range(324):
        col = ColumnNode(i)
        col.left = prev
        prev.right = col
        col.right = header
        header.left = col
        prev = col
        col_nodes.append(col)
    
    for row in range(9):
        for col in range(9):
            num = grid[(row,col)].text
            nums = [int(num)] if num != None else range(1, 10)
            for n in nums:
                cell_idx = row * 9 + col
                row_idx = 81 + row * 9 + (n - 1)
                col_idx = 162 + col * 9 + (n - 1)
                box_idx = 243 + (3*(row//3) + (col//3)) * 9 + (n - 1)
                nodes = []
                for idx in [cell_idx, row_idx, col_idx, box_idx]:
                    node = Node()
                    node.column = col_nodes[idx]
                    node.up = node.column.up
                    node.down = node.column
                    node.column.up.down = node
                    node.column.up = node
                    node.column.size += 1
                    nodes.append(node)
                for i in range(4):
                    nodes[i].right = nodes[(i + 1) % 4]
                    nodes[i].left = nodes[(i - 1) % 4]
    return header

def cover(col):
    col.right.left = col.left
    col.left.right = col.right
    node = col.down
    while node != col:
        row_node = node.right
        while row_node != node:
            row_node.up.down = row_node.down
            row_node.down.up = row_node.up
            row_node.column.size -= 1
            row_node = row_node.right
        node = node.down

def uncover(col):
    node = col.up
    while node != col:
        row_node = node.left
        while row_node != node:
            row_node.up.down = row_node
            row_node.down.up = row_node
            row_node.column.size += 1
            row_node = row_node.left
        node = node.up
    col.right.left = col
    col.left.right = col

def search(header, solution):
    if header.right == header:
        return True
    col = header.right
    min_size = col.size
    current = col.right
    while current != header:
        if current.size < min_size:
            min_size = current.size
            col = current
        current = current.right
    cover(col)
    node = col.down
    while node != col:
        solution.append(node)
        row_node = node.right
        while row_node != node:
            cover(row_node.column)
            row_node = row_node.right
        if search(header, solution):
            return True
        solution.pop()
        row_node = node.left
        while row_node != node:
            uncover(row_node.column)
            row_node = row_node.left
        node = node.down
    uncover(col)
    return False

def DLX(grid):
    start = time.time()

    header = create_matrix(grid)
    solution = []
    if not search(header, solution):
        return False
    for node in solution:
        current = node
        while True:
            if current.column.id < 81:
                cell_id = current.column.id
                row = cell_id // 9
                col = cell_id % 9
                break
            current = current.right
        num_node = current.right
        num = (num_node.column.id - 81) % 9 + 1
        grid[(row,col)].text = str(num)
    # Your code here
    end = time.time()
    print(f"Execution time: {end - start} seconds")
    return True

# SUDOKU Generator Algorithms
# (1) Backtracking-Based Sudoku Generation - depth-first search approach
# (2) Randomized Fill & Pruning
# (3) Constraint Propagation
# (4) Hybrid Approach -- We use that so all are included.

# Algorithm: Hybrid Backtracking with Constraint Propagation & Controlled Pruning(HBCPCP)

N = 9
SQN = 3
ALL_DIGITS = set(range(1, N+1))

def shuffled_digits():
    nums = list(range(1, 10))
    random.shuffle(nums)
    return nums

def seed_3x3_box(grid):
    digits = shuffled_digits()
    for i in range(SQN):
        for j in range(SQN):
            grid[i][j] = digits[i*SQN + j]

def get_candidates(grid, row, col):
    taken = set()
    taken.update(grid[row])
    taken.update(grid[i][col] for i in range(N))
    br, bc = SQN*(row//SQN), SQN*(col//SQN)
    for r in range(br, br+SQN):
        for c in range(bc, bc+SQN):
            taken.add(grid[r][c])
    return list(ALL_DIGITS - taken)

def find_empty(grid):
    for r in range(N):
        for c in range(N):
            if grid[r][c] == 0:
                return r, c
    return None

def fill_grid(grid) -> bool:
    empty = find_empty(grid)
    if not empty:
        return True
    row, col = empty
    candidates = get_candidates(grid, row, col)
    random.shuffle(candidates)
    for num in candidates:
        grid[row][col] = num
        if fill_grid(grid):
            return True
        grid[row][col] = 0
    return False

def generate_full_grid() -> List[List[int]]:
    grid = [[0]*N for _ in range(N)]
    seed_3x3_box(grid)
    for band in range(3):
        rows = list(range(band*SQN, (band+1)*SQN))
        random.shuffle(rows)
        temp = [grid[row][:] for row in rows]
        for i, r in enumerate(rows):
            grid[r] = temp[i]
    for stack in range(3):
        cols = list(range(stack*SQN, (stack+1)*SQN))
        random.shuffle(cols)
        temp_cols = [ [grid[r][c] for c in cols] for r in range(N)]
        for i, c in enumerate(cols):
            for r in range(N):
                grid[r][c] = temp_cols[r][i]
    fill_grid(grid)
    return grid

def symmetric_pairs():
    pairs = []
    for r in range(N):
        for c in range(N):
            sym = (N-1-r, N-1-c)
            if (r, c) <= sym:
                pairs.append(((r,c), sym) if (r,c) != sym else ((r,c),))
    return pairs

def solve_and_count(grid: List[List[int]], limit: int=2) -> int:
    def solve_inner(g) -> int:
        blank = find_empty(g)
        if not blank:
            return 1
        row, col = blank
        count = 0
        for candidate in get_candidates(g, row, col):
            g[row][col] = candidate
            count += solve_inner(g)
            if count >= limit:
                g[row][col] = 0
                break
            g[row][col] = 0
        return count
    return solve_inner([r[:] for r in grid])

def remove_clues_stepwise(grid: List[List[int]], difficulty: str="medium") -> Iterator[List[List[int]]]:
    clue_target = {
        "easy": random.randint(36, 40),
        "medium": random.randint(30, 35),
        "hard": random.randint(25, 29),
        "expert": random.randint(19, 24),
        "legendary": random.randint(17, 18),
    }[difficulty]
    puzzle = [row[:] for row in grid]
    pairs = symmetric_pairs()
    random.shuffle(pairs)
    clues_remaining = N*N
    for pair in pairs:
        if clues_remaining <= clue_target:
            break
        idxs = [pair[0]] if len(pair) == 1 else [pair[0], pair[1]]
        for (r,c) in idxs:
            puzzle[r][c] = 0
        yield [row[:] for row in puzzle]
        if solve_and_count(puzzle, 2) != 1:
            for (r, c) in idxs:
                puzzle[r][c] = grid[r][c]
            yield [row[:] for row in puzzle]
        else:
            clues_remaining -= len(idxs)
            yield [row[:] for row in puzzle]
    yield [row[:] for row in puzzle]

def sudoku_generator(difficulty: str = "medium") -> Iterator[List[List[int]]]:
    grid = generate_full_grid()
    yield [row[:] for row in grid]
    for partial_grid in remove_clues_stepwise(grid, difficulty):
        yield [row[:] for row in partial_grid]

    print("Complated")
    yield