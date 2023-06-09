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

    # def known_mines(self):
    #     """
    #     Returns the set of all cells in self.cells known to be mines.
    #     """

    #     raise NotImplementedError

    # def known_safes(self):
    #     """
    #     Returns the set of all cells in self.cells known to be safe.
    #     """
    #     raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
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
        self.board_cells = {(i, j) for i in range(height)
                            for j in range(width)}

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
        self.moves_made.add(cell)
        # mark_safe adds the cell to self.safes, so no need to do that here
        self.mark_safe(cell)
        sentence = Sentence(self.cell_and_surrounding(cell), count)
        self.knowledge.append(sentence)

        # Mark all cells have mines where len(cells) = count (i.e., {(1,2), (2,3)} = 2)
        knowledge_copy = [copy.deepcopy(sentence)
                          for sentence in self.knowledge]

        for sentence in knowledge_copy:
            if sentence.count == len(sentence.cells):
                for cell in sentence.cells:
                    self.mark_mine(cell)

        # Mark all cells safe where sentence.count = 0
        knowledge_copy = [copy.deepcopy(sentence)
                          for sentence in self.knowledge]

        for sentence in knowledge_copy:
            if sentence.count == 0:
                for cell in sentence.cells:
                    self.mark_safe(cell)

        # Create new sentences by combining sentences with overlapping cells
        newSentences = []
        for i, s1 in enumerate(self.knowledge):
            for j, s2 in enumerate(self.knowledge):
                if i != j and s1.cells & s2.cells:
                    if s1.cells.issubset(s2.cells):
                        new_cells = s2.cells - s1.cells
                        new_count = s2.count - s1.count
                        newSentence = Sentence(new_cells, new_count)
                        if newSentence not in self.knowledge and newSentence not in newSentences:
                            newSentences.append(newSentence)
                    elif s2.cells.issubset(s1.cells):
                        new_cells = s1.cells - s2.cells
                        new_count = s1.count - s2.count
                        newSentence = Sentence(new_cells, new_count)
                        if newSentence not in self.knowledge and newSentence not in newSentences:
                            newSentences.append(newSentence)

        for new_sentence in newSentences:
            self.knowledge.append(new_sentence)
        # To filter out any sentence.cells that = {}, if they somehow occur
        knowledge_copy = [copy.deepcopy(sentence)
                          for sentence in self.knowledge if sentence.cells]
        self.knowledge = knowledge_copy

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safeMoves = [
            cell for cell in self.board_cells if cell in self.safes and cell not in self.moves_made and cell not in self.mines]

        if safeMoves != []:
            r = random.randint(0, len(safeMoves) - 1)
            return safeMoves[r]

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possibleMoves = [
            cell for cell in self.board_cells if cell not in self.mines and cell not in self.moves_made]

        if possibleMoves != []:
            r = random.randint(0, len(possibleMoves) - 1)
            return possibleMoves[r]

        return None

    def cell_and_surrounding(self, cell):
        i, j = cell[0], cell[1]
        cells = set()

        for x, y in itertools.product(range(i - 1, i + 2), range(j - 1, j + 2)):
            if self.inBounds(x, y) and (x, y) != (i, j):
                cells.add((x, y))

        return cells

    def inBounds(self, i, j):
        if i >= 0 and i <= self.height - 1:
            if j >= 0 and j <= self.width - 1:
                return True

        return False
