import itertools
import random
import copy


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
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        return

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        return


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

        # Initialize list of all coordinates on the board
        self.board = set()
        for i in range(self.height):
            for j in range(self.width):
                coord = (i, j)
                self.board.add(coord)

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        num_sentences = len(self.knowledge)
        for i in range(num_sentences):
            self.knowledge[i].mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        num_sentences = len(self.knowledge)
        for i in range(num_sentences):
            self.knowledge[i].mark_safe(cell)

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
        # mark the cell as move made
        self.moves_made.add(cell)

        # mark the cell as safe
        self.mark_safe(cell)

        # get neighbors and filter out know cells by checking to see if any neighbors are already determined safe, or mine
        all_neighbor_cells = self.find_neighbors(cell)
        filtered_neighbor_cells = all_neighbor_cells.copy()
        for cell in all_neighbor_cells:
            if cell in self.safes:
                filtered_neighbor_cells.remove(cell)
            elif cell in self.mines:
                filtered_neighbor_cells.remove(cell)
                count -= 1

        # if it's not an empty sentence (aka. not all neighboring cells are already know to be either safe or mine),
        # insert new sentence to the begining of the list, mark new mines/safes in the entire knowledge base, based on this new derived sentence, may produce duplicates
        if filtered_neighbor_cells:
            new_sentence = Sentence(filtered_neighbor_cells, count)
            self.knowledge.insert(0, new_sentence)
            knowledge_len = len(self.knowledge)
            for i in range(knowledge_len):
                self.mark_mines_and_safes(self.knowledge[i])

            # derive new sentenses by see if any sentence is a subset of any other sentence
            # (aka. looking at common cells between 2 sentences and deducing posibilities)
            i = 0
            while i < knowledge_len - 1:
                # keep track of current derived sentences (cells) so that we don't derive duplicate sentences (common if a lot of cells are known around eachother)
                curr_derived_cells = []
                set1 = self.knowledge[i].cells
                count1 = self.knowledge[i].count
                if set1:
                    j = i + 1
                    while j < knowledge_len:
                        set2 = self.knowledge[j].cells
                        count2 = self.knowledge[j].count
                        if set2:
                            if set1 == set2:
                                # if the sets are the exact same Skip it, so that we dont produce new empty sentences
                                j += 1
                                continue
                            elif set1.issubset(set2):
                                cells = set2 - set1
                                # if not in current derived sentences list, we add it to knowledge base, this is to minimize duplicates
                                if cells not in curr_derived_cells:
                                    curr_derived_cells.append(cells)
                                    new_sentence = Sentence(
                                        cells, count2 - count1)
                                    self.knowledge.append(new_sentence)
                                    self.mark_mines_and_safes(new_sentence)
                            elif set2.issubset(set1):
                                cells = set1 - set2
                                # if not in current derived sentences list, we add it to knowledge base, this is to minimize duplicates
                                if cells not in curr_derived_cells:
                                    curr_derived_cells.append(cells)
                                    new_sentence = Sentence(
                                        cells, count1 - count2)
                                    self.knowledge.append(new_sentence)
                                    self.mark_mines_and_safes(new_sentence)
                        j += 1
                i += 1

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        try:
            # pop a ramdom valid move
            move = (self.safes - self.moves_made).pop()
        except KeyError:
            # no available moves
            move = None
        return move

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        try:
            # pop a ramdom valid move
            move = (self.board - self.moves_made - self.mines).pop()
        except KeyError:
            # no available moves
            move = None
        return move

    def find_neighbors(self, cell):
        # Loop over all cells within one row and column to find neightbors,
        # not counting the cell itself or anything out side of the board
        neighbor_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if 0 <= i < self.height and 0 <= j < self.width and (i, j) != cell:
                    neighbor_cell = (i, j)
                    neighbor_cells.add(neighbor_cell)
        return neighbor_cells

    def mark_mines_and_safes(self, sentence):
        # function used to mark mines and safes together
        # calls the mark_mine and mark_safe functions
        # utilizes deepcopy so that we don't get error while iterating since we will be ultering the set while looping thorugh them
        known_mines = copy.deepcopy(sentence.known_mines())
        known_safes = copy.deepcopy(sentence.known_safes())
        for mine in known_mines:
            self.mark_mine(mine)
        for safe in known_safes:
            self.mark_safe(safe)
