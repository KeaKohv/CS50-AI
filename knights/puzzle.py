from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A can be either a Knight or a Knave but cannot be both at the same time.
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # If it is true that you can be both a Knight and a Knave, then A is a Knight.
    Biconditional(And(AKnight, AKnave), AKnight),
    # If it is false, then A is a Knave.
    Biconditional(Not(And(AKnight, AKnave)), AKnave)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A can be either a Knight or a Knave but cannot be both at the same time.
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # B can be either a Knight or a Knave but cannot be both at the same time.
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # If it is true that A and B both Knaves, then A is a Knight.
    Biconditional(And(BKnave, AKnave), AKnight),
    # If it is false, then A is a Knave.
    Biconditional(Not(And(BKnave, AKnave)), AKnave),
    # If B is not a Knave, then he must be a Knight and vice versa
    Biconditional(Not(BKnave), BKnight),
    Biconditional(Not(BKnight), BKnave),
    # Same for A
    Biconditional(Not(AKnave), AKnight),
    Biconditional(Not(AKnight), AKnave)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A can be either a Knight or a Knave but cannot be both at the same time.
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # B can be either a Knight or a Knave but cannot be both at the same time.
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # If B is not a Knave, then he must be a Knight and vice versa
    Biconditional(Not(BKnave), BKnight),
    Biconditional(Not(BKnight), BKnave),
    # Same for A
    Biconditional(Not(AKnave), AKnight),
    Biconditional(Not(AKnight), AKnave),

    # If what A says is true, then A is a Knight. A says "We are the same kind."
    Biconditional(Or(And(AKnight, BKnight), And(AKnave, BKnave)), AKnight),

    # If what B says is true, then B is a Knight. B says 'We are of different kinds.'
    Biconditional(Or(And(AKnight, BKnave), And(BKnight, AKnave)), BKnight)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A can be either a Knight or a Knave but cannot be both at the same time.
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # B can be either a Knight or a Knave but cannot be both at the same time.
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # C can be either a Knight or a Knave but cannot be both at the same time.
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # If B is not a Knave, then he must be a Knight and vice versa
    Biconditional(Not(BKnave), BKnight),
    Biconditional(Not(BKnight), BKnave),
    # Same for A
    Biconditional(Not(AKnave), AKnight),
    Biconditional(Not(AKnight), AKnave),
    # Same for C
    Biconditional(Not(CKnave), CKnight),
    Biconditional(Not(CKnight), CKnave),

    # If what A says is true, he is a Knight.
    # A says either "I am a knight." or "I am a knave.", but you don't know which.
    Biconditional(Or(AKnight, AKnave), Or(AKnight, AKnave)),

    # If what B says is true, then he is a knight.
    # B says "A said 'I am a knave'."
    # B says "C is a knave."
    Biconditional(Biconditional(AKnave, AKnight), BKnight),
    Biconditional(CKnave, BKnight),

    # If what C says is true, then he is a knight. C says "A is a knight."
    Biconditional(AKnight, CKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
