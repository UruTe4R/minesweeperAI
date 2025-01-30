import itertools
import random
import math


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If mine_count is equal to the number of cells, all cells are mines
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()
        



    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If mine count is 0, all cells are safe
        if self.count == 0 and len(self.cells) != 0:
            return self.cells
        else:
            return set()

        

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Is cell in self.cells?
        if cell in self.cells:
            # Remove cell from self.cells
            self.cells.remove(cell)
            # -1 mine from self.count
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Is cell in self.cells?
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1)
        
        self.moves_made.add(cell)
        # 2)
        self.mark_safe(cell)
        # 3)
        # What are surrounding cells around the cell?
        row = cell[0]
        col = cell[1]
        sur_cells = []
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):

                if i >= 0 and j >= 0 and i < self.height and j < self.width: # within boudary?
                    # if it's not the cell itself and not already in moves_made, add it to sur_cells
                    if (i, j) not in self.moves_made and (i, j) != cell and (i, j) not in self.safes:
                        
                        # if cell is included in marked_mine, remove the cell and reduce count by 1
                        if (i, j) in self.mines:
                            count -= 1    
                        else:
                            sur_cells.append((i, j))
        '''
        今現在いる地点のセルの周囲のセルがmoves_madeと真ん中のセル(現在地)を除いて
        sur_cellsのリストに保存されている。
        '''      
        new_sentence = Sentence(sur_cells, count)
        if new_sentence.known_safes():
            for cell in new_sentence.known_safes():
                if cell not in self.safes and cell not in self.moves_made:
                    self.mark_safe(cell)
        if new_sentence.known_mines():
            for cell in new_sentence.known_mines():
                if cell not in self.mines and cell not in self.moves_made:
                    self.mark_mine(cell)
        self.knowledge.append(new_sentence)

        additional_knowledges = []
        # 4) Update sentence in knowledge based on new sentence
        for sentence in self.knowledge[:-1]:
            # Create new knowledge based on knowledge in self.knowledge and new_sentence created by action
            # if len(sentence.cells) < len(new_sentence.cells):
            #     small_sentence = sentence

             # is surrounding cells are overlapping with cells in sentence?
            cells = sentence.cells - new_sentence.cells
            mine_count = sentence.count - new_sentence.count
            # If there is no mines in cells, mark all cells as safe
            new_knowledge = Sentence(cells, mine_count)
            if new_knowledge.known_safes():
                for cell in new_knowledge.known_safes():
                    if cell not in self.safes and cell not in self.moves_made:
                        self.mark_safe(cell)
            if new_knowledge.known_mines():
                for cell in new_knowledge.known_mines():
                    if cell not in self.mines and cell not in self.moves_made:
                        self.mark_mine(cell)
            additional_knowledges.append(new_knowledge)
        
        self.knowledge.extend(additional_knowledges)





    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for sentence in self.knowledge:
            if sentence.known_safes():
                return sentence.known_safes().pop()
        # If there is no safe moves left that hasn't been made
        if len(self.safes - self.moves_made) == 0:
            return None
        # There should be a safe move that hasn't been made
        else:
            return random.choice(list(self.safes - self.moves_made))



    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = []
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    possible_moves.append((i, j))

        if len(possible_moves) == 0:
            return None
        return random.choice(possible_moves)