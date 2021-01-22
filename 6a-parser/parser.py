import nltk
import sys
import re

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

NONTERMINALS = """
S -> NP VP
NP -> N | Det N | Det AdjP N | NP PP | NP Conj NP | AdjP NP | N AdvP | Det N AdvP
VP -> V | V NP | V PP | AdvP VP | V AdvP | VP Conj VP | V S
AdjP -> Adj | Adj AdjP
AdvP -> Adv | Adv AdvP
PP -> P NP | P S
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

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    sentence = sentence.lower()
    tokens = nltk.word_tokenize(sentence)
    words = list()
    for token in tokens:
        if re.search('[a-z]', token):
            words.append(token)
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunks = list()
    for subtree in tree.subtrees():
        if is_np_chunk(subtree):
            np_chunks.append(subtree)
    return np_chunks


def is_np_chunk(tree):
    # helper function that checks if a particular subtree is a noun phrase chunk

    # return false if the subtree is not a noun phrase
    if tree.label() != 'NP':
        return False

    for subtree in tree.subtrees():
        # subtrees() function returns the original tree itself as well, so filter that out
        if subtree == tree:
            continue
        elif subtree.label() == 'NP':
            return False
    return True


if __name__ == "__main__":
    main()
