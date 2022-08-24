import nltk
import sys

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
S -> NP VP  | NP VP NP NP | NP VP PP Conj NP VP | NP Adv VP Conj NP VP PP Adv
S -> NP VP Conj VP NP | NP VP NP NP Conj VP PP | NP VP PP
NP -> N | Det N  | P N  | Det Adj N | Det Adj Adj Adj N |  Det N P Det N
VP -> V | V NP  | V Adv
PP -> P NP
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

    # Convert all uppercase letters to lowercase
    sentence = sentence.lower() 

    # Convert the sentence into a list of substrings
    words = nltk.word_tokenize(sentence)

    # Go through the list and remove words that do not contain at least one alphabetic
    # character
    for word in words:
        if any(letter.isalpha() for letter in word) is False:
            words.remove(word)
    
    return words


def check_for_NP(subtree):
    """
    Check if the subtree has any subtrees itself that have the NP label
    """

    # Go through the subtrees
    for sub in subtree:

        # If the label of the subtree is NP, return True
        if sub.label() == "NP":
            return True

        # If the subtree itself has more subtrees, also check that their subtrees do not contain NP chuncks
        elif len(sub) != 1:
            if check_for_NP(sub) is True:
                return True
    
    # If NP chucks in subtrees were not found, return False
    return False


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    # Create a list for the NP chuncks
    chunks = []

    # Go through all the subtrees in the tree
    for subtree in tree.subtrees():

        # Check if the label of the tree is NP
        if subtree.label() == "NP":

            # Check if the subtree has any subtrees itself that have the NP label, if not, add to list
            if check_for_NP(subtree) is False:
                chunks.append(subtree)

    return chunks


if __name__ == "__main__":
    main()
