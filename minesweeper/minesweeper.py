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
        # If the number of cells in the sentence is equal to count which is higher than 0,
        # these cells must be mines. Then return those cells. Otherwise return an empty set.

        if len(self.cells) == self.count and self.count != 0:
            return self.cells

        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        # If the number of cells in the sentence is equal to count 0
        # these cells must be safe. Then return those cells. Otherwise return an empty set.
        if len(self.cells) == self.count and self.count == 0:
            return self.cells

        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        # If cell is included in the sentence, remove it and decrease count by 1.
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

        return

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        # If cell is included in the sentence, remove it. Count remains the same.
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

        # List of sentences arrived to as inference
        self.inferences = []

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
        """

        # Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # Mark the cell as safe
        self.safes.add(cell)

        for mine in self.mines:
            print(f"{mine} is a mine")
        if len(self.mines) == 0:
            print("No known mines")

        # Count neighbours
        neighbours = 0
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Check if cell in bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbours += 1

        # If count is 0, mark all neighbouring cells as safe
        if count == 0:
            # Loop over neighbouring cells and mark them as safe if not already marked as safe.
            for i in range(cell[0] - 1, cell[0] + 2):
                for j in range(cell[1] - 1, cell[1] + 2):

                    # Ignore the cell itself.
                    if (i, j) == cell:
                        continue

                    # Check if cell in bounds.
                    if 0 <= i < self.height and 0 <= j < self.width:
                        
                        # Add as a safe if not already in self.safes.
                        if (i, j) not in self.safes:
                            self.safes.add((i, j))

                            # Also update the knowledge base and mark the cell as safe in each sentence.
                            if len(self.knowledge) != 0:
                                for sentence in self.knowledge:
                                    sentence.mark_safe((i, j))


        # If count is equal to the number of neighbouring cells, mark all as mines.
        elif count == neighbours:
            for i in range(cell[0] - 1, cell[0] + 2):
                for j in range(cell[1] - 1, cell[1] + 2):

                    # Ignore the cell itself
                    if (i, j) == cell:
                        continue

                    # Check if cell in bounds and not already in self-mines.
                    if 0 <= i < self.height and 0 <= j < self.width and (i, j) not in self.mines:
                            self.mines.add((i, j))

                            # Also update the knowledge base and mark the cell as a mine
                            # in each sentence.
                            if len(self.knowledge) != 0:
                                for sentence in self.knowledge:
                                    sentence.mark_mine((i, j))


        # Otherwise, add a new sentence to the AI's knowledge base
        # based on the value of `cell` and `count`.
        else:
            cells = set()
            # Loop over all cells within one row and column
            for i in range(cell[0] - 1, cell[0] + 2):
                for j in range(cell[1] - 1, cell[1] + 2):

                    # Ignore the cell itself
                    if (i, j) == cell:
                        continue

                    # Check if cell in bounds
                    if 0 <= i < self.height and 0 <= j < self.width:
                        # Cell is only added to the sentence if it is not already marked
                        # as safe or a mine. If the cell is already marked as a mine,
                        # the count variable is decreased by 1.
                        if (i, j) not in self.moves_made and (i, j) not in self.safes:
                            if (i, j) in self.mines:
                                count -= 1
                            else:
                                cells.add((i, j))
                        
            # Add the new sentence to knowledge base
            new_sentence = Sentence(cells, count)

            # Sentence is only added to the knowledge base if it is not already in the knowledge
            # base and has not been in the knowledge base (sentences deleted from knowledge base
            # remain in self.inferences), otherwise an endless loop can occur.
            if new_sentence not in self.knowledge and new_sentence not in self.inferences:

                # It is also checked that the cells are not all mines or safes.
                if new_sentence.cells not in self.mines or new_sentence.cells not in self.safes:
                    self.knowledge.append(new_sentence)

        # A loop that updates knowledge base as long as there is new information added to the
        # knowledge base.
        new_knowledge = True
        while new_knowledge == True and len(self.knowledge) != 0:
            
            new_knowledge = False

            # Mark any additional cells as safe or as mines
            # if it can be concluded based on the AI's knowledge base
            if len(self.knowledge) != 0:
                for sentence in self.knowledge:

                    # If sentence is an empty set, remove it.
                    if len(sentence.cells) == 0:
                        self.knowledge.remove(sentence)
                        continue

                    # See if any mines can be found based on the sentence's information.
                    mines = sentence.known_mines()

                    if len(mines) != 0:
                        new_knowledge = True

                        # If the whole sentence will be deleted by mark_mine,
                        # save it in self.inferences.
                        if len(sentence.cells) == len(mines):
                            self.inferences.append(copy.deepcopy(sentence))
                        
                        for cell in mines.copy():
                            self.mines.add(cell)
                            sentence.mark_mine(cell)

                    # See if any safes can be found based on the sentence's information.
                    safes = sentence.known_safes()

                    if len(safes) != 0:

                        new_knowledge = True

                        # If the whole sentence will be deleted by mark_safe,
                        # save it in self inferences.
                        if len(sentence.cells) == len(safes):
                            self.inferences.append(copy.deepcopy(sentence))

                        for cell in safes.copy():
                            self.safes.add(cell)
                            print(f"New safe is {cell}")
                            sentence.mark_safe(cell)

            # Add any new sentences to the AI's knowledge base
            # if they can be inferred from existing knowledge
            if len(self.knowledge) > 1:
                for sentence in self.knowledge:
                    for sentence_two in self.knowledge:

                        # Skip comparing the sentence to itself.
                        if sentence is sentence_two:
                            continue

                        # Check if the values of the sentences are are different, the cells sets are
                        # not empty.
                        if sentence != sentence_two and len(sentence.cells) > 0 and len(sentence_two.cells) > 0:
                            # Check if one sentence is the subset of another.
                            if sentence.cells.issubset(sentence_two.cells):

                                # Form a new sentence based on the inference.
                                new_cells = (sentence_two.cells).difference(sentence.cells)
                                new_sentence = Sentence(new_cells, sentence_two.count - sentence.count)
                                
                                # Check that the sentence is not and has not been in knowledge base.
                                if new_sentence not in self.knowledge and new_sentence not in self.inferences:

                                    # Check if new cells are not already markes as mines or safes.
                                    if new_cells not in self.mines or new_cells not in self.safes:

                                        self.knowledge.append(new_sentence)

                                        # The inferences list is needed so that an inference
                                        # is not added multiple times in case
                                        # the inference/sentence is deleted from self.knowledge
                                        # by mark_safe or mark_mine.
                                        self.inferences.append(copy.deepcopy(new_sentence))
                                        new_knowledge = True

                        # If the values of the sentences are the same (duplicates), remove one
                        elif sentence == sentence_two:
                            self.knowledge.remove(sentence_two)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        # If there are no known safes, return None.
        if len(self.safes) == 0:
            return None
        else:
            # If there are cells known to be safe, draw a random cell from cells from these.
                for cell in self.safes:
                    if cell not in self.moves_made:
                        return cell

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        possible_moves = []

        # Go through all the cells and mark cell as a possible move if it is not already
        # in moves made and not in self mines.
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    possible_moves.append((i, j))

        # If there are no possible moves, return None.
        if len(possible_moves) == 0:
            return None

        # If there are possible moves, return a random possible move.
        else:
            i = random.randrange(len(possible_moves))
            random_move = possible_moves[i]
            return random_move
            


        
