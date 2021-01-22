from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# lay the fundational game rule: each character is either a knight or a knave.
game_rule = And(Or(AKnight, AKnave), Or(Not(AKnight), Not(AKnave)),
                Or(BKnight, BKnave), Or(Not(BKnight), Not(BKnave)),
                Or(CKnight, CKnave), Or(Not(CKnight), Not(CKnave)))

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    game_rule,

    # if character is telling the truth then they are a knight, represented using bi-conditional
    Biconditional(And(AKnight, AKnave), AKnight)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    game_rule,

    # if character is telling the truth then they are a knight, represented using bi-conditional
    Biconditional(And(AKnave, BKnave), AKnight)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    game_rule,

    # if character is telling the truth then they are a knight, represented using bi-conditional
    Biconditional(Or(And(AKnight, BKnight), And(AKnave, BKnave)), AKnight),
    Biconditional(Or(And(AKnight, BKnave), And(AKnave, BKnight)), BKnight)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    game_rule,

    # if character is telling the truth then they are a knight, represented using bi-conditional
    Biconditional(Or(AKnight, AKnave), AKnight),
    Biconditional(Biconditional(AKnave, AKnight), BKnight),
    Biconditional(CKnave, BKnight),
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
