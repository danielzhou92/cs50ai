import sys
import copy

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
        # if the word is not the required length of the variable, then delete the word from the set of words
        for var, words in self.domains.items():
            words_copy = copy.deepcopy(words)
            for word in words_copy:
                if len(word) != var.length:
                    words.remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # check to see if the 2 variables actially overlap, return false immedieatly if not
        overlap = self.crossword.overlaps[x, y]

        if overlap == None:
            return False

        word_1_index = overlap[0]
        word_2_index = overlap[1]
        revision_made = False

        # if a word in domain[x] has a possible corresponding word that can fit with it in domain 2 (based on overlaping characters), then leave it be
        # and if no possible corresponding word is found, then delete the word from x
        var_domain_copy = copy.deepcopy(self.domains[x])
        for word1 in var_domain_copy:
            char1 = word1[word_1_index]
            have_corresponding_word = False

            for word2 in self.domains[y]:
                char2 = word2[word_2_index]
                if char2 == char1:
                    have_corresponding_word = True
                    break

            if not have_corresponding_word:
                self.domains[x].discard(word1)
                revision_made = True

        return revision_made

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # if no arcs is passed in, loop thorugh the whole puzzle to get all the arcs first.
        if arcs == None:
            arcs = list()
            for var1 in self.domains:
                neighbor_vars = self.crossword.neighbors(var1)
                for var2 in neighbor_vars:
                    if (var1, var2) not in arcs:
                        arcs.append(tuple((var1, var2)))

        # go through all arcs to apply arc consistency
        while arcs:
            arc = arcs.pop(0)
            var1 = arc[0]
            var2 = arc[1]
            # if revision was made, que up additional que
            if self.revise(var1, var2):
                # if the variable domain is empty, then there is no solution, return false
                if len(self.domains[var1]) == 0:
                    return False
                # if change was made, que up all other neightbors to verify arc consistency
                else:
                    neighbor_vars = self.crossword.neighbors(var1)
                    neighbor_vars = neighbor_vars - {var2}
                    for neighbor_var in neighbor_vars:
                        arcs.append(tuple((neighbor_var, var1)))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if self.return_all_unassigned_variables(assignment) == None:
            # no unassigned variables left
            return True
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        assigned_values = set()

        for var, value in assignment.items():
            # return false if the value is a repeat of other variables
            if value in assigned_values:
                return False
            if value != None:
                # check and make sure value is correct length, return false if not
                if len(value) != var.length:
                    return False
                # check to make sure there is no conflict with neightboring values
                # aka shared character is the same
                neighbor_vars = self.crossword.neighbors(var)
                for neighbor_var in neighbor_vars:
                    # dont check if the neightbor variable has yet to be filled
                    if neighbor_var not in assignment.keys():
                        continue
                    else:
                        overlap = self.crossword.overlaps[var, neighbor_var]
                        if value[overlap[0]] != assignment[neighbor_var][overlap[1]]:
                            return False
            # add value as an value assigned already
            assigned_values.add(value)

        # if everything checks out, return true
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        all_neighbor_vars = self.crossword.neighbors(var)
        unassigned_neighbor_vars = set()
        # create a set that contains unassigned neighbors for the given variable
        for var2 in all_neighbor_vars:
            if var2 not in assignment.keys():
                unassigned_neighbor_vars.add(var2)

        word_dict = dict()
        # function is to loop through each possible values of the variable
        # to see how many words from neightboring unassigned variables that particular ward rules out
        for word in self.domains[var]:
            values_ruled_out = 0
            # loop through neighboring unassigned variable's words
            for var2 in unassigned_neighbor_vars:
                overlap = self.crossword.overlaps[var, var2]
                char1 = word[overlap[0]]
                for word2 in self.domains[var2]:
                    char2 = word2[overlap[1]]
                    # see if the overlaping character is not matching
                    # if not matching, the word is ruled out
                    if char1 != char2:
                        values_ruled_out += 1
            word_dict[word] = values_ruled_out

        return sorted(word_dict, key=word_dict.get)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # get a set of all unassigned variables
        all_unassigned_vars = self.return_all_unassigned_variables(assignment)
        if all_unassigned_vars == None:
            return None

        best_var = None
        for var in all_unassigned_vars:
            # find the variable's number of remaining words left in it's domain
            var_words_count = len(self.domains[var])
            # find the variables degree to other variables (aka. most neighbors, including known ones)
            var_degree = len(self.crossword.neighbors(var))
            # choose the variable with the lest remainign word in domain, if tied, choose variable with larger degree
            if not best_var:
                best_var = var
                lowest_word_count = var_words_count
                largest_degree = var_degree
            elif var_words_count < lowest_word_count or (var_words_count == lowest_word_count and var_degree > largest_degree):
                best_var = var
                lowest_word_count = var_words_count
                largest_degree = var_degree

        return best_var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        else:
            var = self.select_unassigned_variable(assignment)
            values = self.order_domain_values(var, assignment)
            for value in values:
                assignment[var] = value
                if self.consistent(assignment):
                    result = self.backtrack(assignment)
                    if result != None:
                        return result
                else:
                    assignment.pop(var)
            return None

    def return_all_unassigned_variables(self, assignment):
        # function returns all unassigned variables as a set
        all_variables = set(self.domains.keys())
        if not assignment:
            # empty dictionary
            return all_variables
        assigned_variables = set(assignment.keys())
        if len(all_variables) == len(assigned_variables):
            # all variables have been assigned
            return None
        # return the difference between the two sets as unassigned variable
        return all_variables - assigned_variables


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
