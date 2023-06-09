import sys
from collections import deque
from crossword import *
import copy


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
        for var in self.domains:
            word_length = var.length
            self.domains[var] = {word for word in self.crossword.words
                                 if len(word) == word_length}

    def revise(self, x, y):
        revised = False
        x_domain = copy.deepcopy(self.domains[x])

        overlap = self.crossword.overlaps[x, y]
        if not overlap:
            return revised

        for word1 in x_domain:
            satisfactoryDomain = [
                word2 for word2 in self.domains[y] if word1[overlap[0]] == word2[overlap[1]]]

            if not satisfactoryDomain:
                self.domains[x].remove(word1)
                revised = True

        return revised

    def ac3(self, arcs=None):
        if not arcs:
            arcs = set()
            vars = [var for var in self.domains]

            for var in vars:
                neighbors = self.crossword.neighbors(var)
                for neighbor in neighbors:
                    arcs.add((var, neighbor))

        queue = deque(arcs)
        while len(queue) > 0:
            current_arc = queue.popleft()
            x, y = current_arc[0], current_arc[1]
            if self.revise(x, y):
                if not self.domains[x]:
                    return False
                for z in (self.crossword.neighbors(x) - {y}):
                    queue.append((z, x))

        return True

    def assignment_complete(self, assignment):

        if len(assignment.keys()) != len(self.crossword.variables):
            return False

        if any(assignment[key] is None for key in assignment):
            return False

        return True

    def consistent(self, assignment):
        word_set = set(assignment.values())
        if len(word_set) != len(assignment):
            return False

        for var in assignment:
            if assignment[var]:
                if len(assignment[var]) != var.length:
                    return False

        for var in assignment:
            if assignment[var] is None:
                continue
            neighbors = self.crossword.neighbors(var)
            for neighbor in neighbors:
                overlap = self.crossword.overlaps[var, neighbor]
                if neighbor in assignment and assignment[var] and assignment[neighbor]:  # Check if the neighbor has an assignment
                    if not (assignment[var][overlap[0]] == assignment[neighbor][overlap[1]]):
                        return False

        return True

    def order_domain_values(self, var, assignment):

        neighbors = self.crossword.neighbors(var)
        cost_dict = {word: 0 for word in self.domains[var]}

        for word in cost_dict:
            cost = 0
            for neighbor in neighbors:
                if word in self.domains[neighbor]:
                    cost += 1
            cost_dict[word] += 1

        return sorted(cost_dict, key=cost_dict.get)

    def select_unassigned_variable(self, assignment):

        all_vars = set(self.domains.keys())
        assigned_vars = set(assignment.keys())
        remaining_vars = all_vars - assigned_vars

        domain_lengths = {var: len(self.domains[var]) for var in remaining_vars}
        min_length_domain = min(domain_lengths.values())
        min_keys = [var for var, value in domain_lengths.items() if value == min_length_domain]

        if len(min_keys) == 1:
            return min_keys[0]

        neighbor_count = {var: len(self.crossword.neighbors(var)) for var in min_keys}
        return max(neighbor_count, key=neighbor_count.get)


    def backtrack(self, assignment):
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value

            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)

                if result:
                    return result

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
