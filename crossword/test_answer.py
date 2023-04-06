import sys
import os
import itertools
from PIL import Image
from generate import main as generate_crossword

def generate_input_permutations():
    structure_files = [f"data/structure{i}.txt" for i in range(3)]
    words_files = [f"data/words{i}.txt" for i in range(3)]

    return list(itertools.product(structure_files, words_files))

def run_tests(inputs):
    test_results = []
    for index, (structure, words) in enumerate(inputs):
        output = f"results/result_{index}.png"
        sys.argv = ["generate.py", structure, words, output]
        try:
            generate_crossword()
            test_results.append((structure, words, output, True))
        except Exception as e:
            print(f"Error while processing {structure}, {words}: {e}")
            test_results.append((structure, words, output, False))

    return test_results


if __name__ == "__main__":
    inputs = generate_input_permutations()
    test_results = run_tests(inputs)
