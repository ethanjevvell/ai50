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
S -> NP VP PP | PP NP VP
S -> S Conj S
S -> S Conj VP
S -> S Adv | Adv S

NP -> N | Det N | Det Adj N | Det Adj NP
NP -> Adj N | Adj NP

VP -> V | V NP
VP -> Adv VP | VP Adv
VP -> VP PP

PP -> P NP | P N
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
        print(f"Total NP chunks: {len(np_chunk(tree))}")
        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


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

    # Get all trees with NP root
    np_subtrees = list(tree.subtrees(lambda t: t.label() == "NP"))
    np_chunks = []

    # Iterate through NP subtrees
    for tree in np_subtrees:
        if len(list(tree.subtrees(lambda t: t.label() == "NP"))) == 1:
            np_chunks.append(tree)

    return np_chunks


if __name__ == "__main__":
    main()
