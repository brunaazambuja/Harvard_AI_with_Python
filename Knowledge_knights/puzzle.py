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
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))), # Each character is either a knight or a knave, but not both

    Implication(AKnight, And(AKnight, AKnave)), # If A is a knight, he will tell the truth
    Implication(AKnave, Not(And(AKnight, AKnave))), # If A is a knave, he will lie
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))), # Each character is either a knight or a knave, but not both
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))), # Each character is either a knight or a knave, but not both

    Implication(AKnight, And(AKnave, BKnave)), # If A is a knight, he will tell the truth
    Implication(AKnave, Not(And(AKnave, BKnave))), # If A is a knave, he will lie
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))), # Each character is either a knight or a knave, but not both
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))), # Each character is either a knight or a knave, but not both

    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))), # If A is a knight, he will tell the truth
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))), # If A is a knave, he will lie

    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))), # If B is a knight, he will tell the truth
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight)))), # If B is a knave, he will lie
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And( 
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))), # Each character is either a knight or a knave, but not both
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))), # Each character is either a knight or a knave, but not both
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))), # Each character is either a knight or a knave, but not both

    Implication(AKnight, Or(AKnight, AKnave)), # If A is a knight, he will tell the truth
    Implication(AKnave, Not(Or(AKnight, AKnave))), # If A is a knave, he will lie


    Implication(BKnight, And(CKnave, Implication(AKnight, BKnave))), # If B is a knight, and A is also a knight, they will both tell the truth
    Implication(BKnave, Not(And(CKnave, Implication(AKnight, BKnave)))), # If B is a knave, he will lie, but A is a knight, so he will tell the truth
    
    Implication(BKnight, And(CKnave, Implication(AKnave, Not(BKnave)))), # If B is a knight, he will tell the truth, but A is a knave, so he will lie
    Implication(BKnave, Not(And(CKnave, Implication(AKnave, Not(BKnave))))), # If B is a knave, and A is also a knave, they will both lie
    

    Implication(CKnight, AKnight), # If C is a knight, he will tell the truth
    Implication(CKnave, Not(AKnight)), # If C is a knave, he will lie
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
