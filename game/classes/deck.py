from .card import CARD_VALUES, SUIT_NAMES, Card

import random

class Deck:
    cards = []
    def __init__(self):
        pass

    def _create_deck(self):
        for suit_index in range(len(SUIT_NAMES)):
            for value_index in range(len(CARD_VALUES)):
                self.cards.append(Card(suit_index, value_index))

    def shuffle(self):
        random.shuffle(self.cards)

    def restart(self):
        self.cards = []
        self._create_deck()
        self.shuffle()

    def pick_card(self):
        card = self.cards.pop(0)
        return card
