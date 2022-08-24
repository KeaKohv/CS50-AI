        print("Adding knowledge")
        # Mark the cell as a move that has been made
        print("Mark the cell as a move that has been made")
        self.moves_made.add(cell)

        # Mark the cell as safe
        print("Mark the cell as safe")
        self.safes.add(cell)

        # Count neighbours
        print("Count neighbours")
        neighbours = 0
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Check if cell in bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbours += 1

        # If count is 0, mark all neighboring cells as safe
        if count == 0:
            print("Count 0, all safe")
            # For that, loop over neighboring cells and mark them as safe if not already markes as safe.
            for i in range(cell[0] - 1, cell[0] + 2):
                for j in range(cell[1] - 1, cell[1] + 2):

                    # Ignore the cell itself
                    if (i, j) == cell:
                        continue

                    # Check if cell in bounds
                    if 0 <= i < self.height and 0 <= j < self.width:
                        
                        # Add as a safe if not already in self.safes
                        if (i, j) not in self.safes:
                            print(f"Marked {(i, j)} as safe")
                            self.safes.add((i, j))

                            # Also update the knowledge base and mark the cell as safe in each sentence
                            for sentence in self.knowledge:
                                sentence.mark_safe((i, j))


        # If count is equal to the number of neighboring cells, mark all as mines.
        elif count == neighbours:
            print("Count equal to neighbours")
            for i in range(cell[0] - 1, cell[0] + 2):
                for j in range(cell[1] - 1, cell[1] + 2):

                    # Ignore the cell itself
                    if (i, j) == cell:
                        continue

                    # Check if cell in bounds
                    if 0 <= i < self.height and 0 <= j < self.width:
                        if (i, j) not in self.mines:
                            print(f"Flagged {(i, j)} as mines")
                            self.mines.add((i, j))

                             # Also update the knowledge base and mark the cell as a mine
                             # in each sentence
                            for sentence in self.knowledge:
                                sentence.mark_mine((i, j))


        # Otherwise, add a new sentence to the AI's knowledge base
        # based on the value of `cell` and `count`
        else:
            print("adding new sentence")
            cells = set()
            # Loop over all cells within one row and column
            for i in range(cell[0] - 1, cell[0] + 2):
                for j in range(cell[1] - 1, cell[1] + 2):

                    # Ignore the cell itself
                    if (i, j) == cell:
                        continue

                    # Check if cell in bounds
                    if 0 <= i < self.height and 0 <= j < self.width:
                        # Cell is only added to the sentence if it is not already marked as safe or a mine.
                        # If the cell is already marked as a mine, the count variable is decreased by 1.
                        if (i, j) not in self.moves_made and (i, j) not in self.safes:
                            if (i, j) in self.mines:
                                count -= 1
                            else:
                                cells.add((i, j))
                        

            # Add the new sentence to knowledge base
            new_sentence = Sentence(cells, count)
            if new_sentence not in self.knowledge:
                self.knowledge.append(Sentence(cells, count))

        print("Knowledge loop")
        # Mark any additional cells as safe or as mines
        # if it can be concluded based on the AI's knowledge base
        for sentence in self.knowledge:
            print(f"Check for mines in {sentence}")
            mines = sentence.known_mines()
            if mines != None:
                print("mine founf")
                for cell in mines.copy():
                    sentence.mark_mine(cell)

            print(f"Check for safes in {sentence}")
            safes = sentence.known_safes()
            if safes != None:
                print("safe found")
                for cell in safes.copy():
                    sentence.mark_safe(cell)

        # Add any new sentences to the AI's knowledge base
        # if they can be inferred from existing knowledge
        print("Check for new sentences as subsets")
        for sentence in self.knowledge:
            for sentence_two in self.knowledge:
                if sentence is sentence_two:
                    continue
                if sentence != sentence_two:
                    if sentence.cells.issubset(sentence_two.cells):
                        new_cells = (sentence_two.cells).difference(sentence.cells)
                        new_sentence = Sentence(new_cells, sentence_two.count - sentence.count)
                        self.knowledge.append(new_sentence)
                elif sentence == sentence_two:
                    # If sentence and sentence_two are the same (duplicates), remove one
                    self.knowledge.remove(sentence_two)
        print("Done")