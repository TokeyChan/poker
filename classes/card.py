
CARD_VALUES = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]
SUIT_NAMES = ["Spades", "Heart", "Diamonds", "Clubs"]

class Card:
    def __init__(self, suit, value):
        self.value = value
        self.suit = suit

    @property
    def name(self):
        return f"{CARD_VALUES[self.value]} of {SUIT_NAMES[self.suit]}"

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name