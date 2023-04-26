import nltk
from nltk.tokenize import word_tokenize
import sys

# DO NOT MODIFY
TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

# Modify these for solution
NONTERMINALS = """
S -> NP VP
S -> S Conj S
S -> S Conj VP
S -> S Adv | Adv S

NP -> N | Det NP
NP -> Adj NP

VP -> V | V NP
VP -> Adv VP | VP Adv
VP -> VP PP

PP -> P | NP PP | PP NP

"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

    #     print("Noun Phrase Chunks")
    #     for np in np_chunk(tree):
    #         print(" ".join(np.flatten()))


def preprocess(sentence):

    sentence = sentence.lower()
    parsed_sentence = word_tokenize(sentence)

    # Return only words that contain at least one alphabetic character
    parsed_sentence = [word for word in parsed_sentence if any(
        c.isalpha() for c in word)]

    return parsed_sentence


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
