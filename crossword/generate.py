from errno import EBUSY
import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Loop through all the variables
        for variable in self.domains:

            words_to_remove = []

            # Loop through each variable's domain (possible words)
            for word in self.domains[variable]:

                # Check the possible word's length to see if it is
                # the same as the variable's possible length.
                # If not, remove word from the variable's domain.
                if len(word) != variable.length:
                    words_to_remove.append(word)

            for word in words_to_remove:
                self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        revision = False

        # If x and y have no overlaps, return False
        if self.overlaps[x, y] == None:
            return revision

        # Otherwise, loop through the domain of x (possible words)
        for word in self.domains[x]:

            # Loop through the overlaps
            for i, j in self.overlaps[x, y]:

                option_exists = False

                # Check if there is a word in y's domain that satisfies the overlap
                for other_word in self.domains[y]:

                    # If there is a possible value in y's domain, break the loop
                    # and check the next overlap
                    if word[i] == other_word[j]:
                        option_exists == True
                        break

                # If no such word exists, remove the word possible word (item of x's domain)
                # from x's domain
                if option_exists == False:
                    self.domains[x].remove(word)

                    # Set revision to True
                    revision = True

        # return revision
        return revision

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # If arcs in None, add all arcs to the list of arcs
        if arcs == None:
            arcs = []
            # Loop through all the variable pairs
            for variable in self.crossword.variables:
                for variable_two in self.crossword.variables:
                    if variable != variable_two:
                        # If the variables have an overlap (i.e. they are neighbors, add them to arcs)
                        if self.crossword.overlaps[variable, variable_two] != None:
                            arcs.append((variable, variable_two))

        else:
            # If the list of arcs is non-empty, take an arc from the list and enforce arc-consistency
            while arcs != None:
                (x, y) = arcs.pop(0)
                if self.revise(self, x, y):

                    # If revisions were made, check if the domain of X is now empty
                    # If it is empty, return None as the problem cannot be solved
                    if self.domains[x] != None:
                        return False

                    # If revisions were made, add x's neighbors to the list of arcs
                    for variable in self.variables:
                        if x != variable and variable != y:
                            if self.overlaps[x, variable] != None and (x, variable) not in arcs:
                                arcs.append((x, variable))
            return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        # See if any of the values of the variables are None, if yes, return False
        for key, value in assignment.items():
            if value == None:
                return False

        # Check if all the variables exist in the assignment as keys
        for variable in self.crossword.variables:
            if variable not in assignment:
                return False

        # Otherwise, all the values are assigned, return True
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # Go through all the keys (variables) in the assignment and check if all values are distinct
        list_of_values = []
        for key in assignment:
            value = assignment[key]
            if value in list_of_values:
                return False
            list_of_values.append(value)

            # Also, check if the value is the correct length
            if len(value) != key.length:
                return False

            # Also, check that there are no conflicts between neighboring variables
            for key, value in assignment.items():

                # Loop over neighbors
                for neighbor in self.crossword.neighbors(key):
                    # If that neighbor is also in the assignment, check if the overlap is consistent
                    if neighbor in assignment.keys():
                        overlap = self.crossword.overlaps[key, neighbor]
                        if value[overlap[0]] != assignment[neighbor][overlap[1]]:
                            return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        # A function by which the domain will be sorted
        def sorting(value):

            # Counter n keeps track of how many words in the domains of the neighbors
            # would be eliminated of this value was chosen for var.
            n = 0

            for neighbor in self.crossword.neighbors(var):

                # If neighbor is already assigned, go to the next one
                if neighbor in assignment.keys():
                    break
                
                # Get the overlap
                overlap = self.crossword.overlaps[var, neighbor]
                
                # If the overlap does not match, increase n by 1
                for word in self.domains[neighbor]:
                    if value[overlap[0]] != word[overlap[1]]:
                        n += 1

            return n

        # Sort domain by ascending order of eliminated values
        ordered_values = sorted(self.domains[var], key=sorting)

        return ordered_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # A dict to keep track of domain sizes
        domain_sizes = dict()

        # Loop through variables and create a new dict with a variables as keys
        # and size of each variable's domain as value
        for variable in self.crossword.variables:

            # Only consider not assigned variables
            if variable not in assignment.keys():
                
                # Add the variable and its domain size as key/value pair to the dict
                domain_size = len(self.domains[variable])
                domain_sizes[variable] = domain_size

        sorted_dict = sorted(domain_sizes.items(), key=lambda x: x[1])

        # If the variable with the smallest domain is not in a tie with the next smallest, return it
        smallest = sorted_dict.pop(0)

        # If there is another item in the dict, check for a tie
        if len(sorted_dict) != 0:
            second_smallest = sorted_dict.pop(0)

            # If there is not a tie, return the variable with the smallest domain size
            if smallest[1] < second_smallest[1]:
                return smallest[0]

        # If there is only one possible available variable, return it
        else:
            return smallest[0]

        # Otherwise, choose the variable that has most neighbors
        nr_neighbors = dict()

        for variable in self.crossword.variables:

            # Only consider not assigned variables
            if variable not in assignment.keys():

                # Add each variable and its nr of neighbors to the dict
                nr = len(self.crossword.neighbors(variable))
                nr_neighbors[variable] = nr

        # Sort from highest to smallest
        sorted_dict_two = sorted(domain_sizes.items(), key=lambda x: x[1], reverse=True)
        highest_degree_variable = sorted_dict_two.pop()
        return highest_degree_variable[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # If assignment is completed, return assignment
        if self.assignment_complete(assignment):
            return assignment
        
        # Otherwise, choose an unassigned variable
        var = self.select_unassigned_variable(assignment)
        
        # Pick a value for that variable from its domain
        for value in self.order_domain_values(var, assignment):

            # Assign that value to the variable
            assignment.update({var: value})

            # Check if the value is consistent with the assignment
            if self.consistent(assignment):
                # If it is consistent, do the same for the next node                
                result = self.backtrack(assignment)
                if result != None:
                    return result
            # If the value is not consistent, remove it and try the next one
            else:
                assignment.pop(var)
        
        # If the assignment is not complete and no possible values were left that would be consistent,
        # then return None
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
