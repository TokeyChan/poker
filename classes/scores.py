from card import Card

ACE_VALUE = 12

class CardWrapper:
    def __init__(self, card):
        self.card = card
        self.is_used = False

    def __repr__(self):
        return str(self.card)

    @property
    def value(self):
        return self.card.value

    @property
    def suit(self):
        return self.card.suit

def pre(cards):
    wrapped_cards = [CardWrapper(card) for card in cards]
    sorted_cards = sorted(wrapped_cards, key=lambda x: x.card.value, reverse=True)
    return sorted_cards

def execute(cards):
    cards = pre(cards)
    results = []
    for scoring in SCORINGS:
        for card in cards:
            card.is_used = False
        result = scoring[1](cards)
        if result is not None:
            results.append([scoring[0], result])

    #print(results)


def has_pair(cards): # Card[]
    for card in cards:
        sames = [c for c in cards if c.value == card.value]

        if len(sames) >= 2:
            return sames[:2]

def has_two_pair(cards):
    pair_1 = has_pair(cards)

    for card in pair_1:
        card.is_used = True

    pair_2 = has_pair([c for c in cards if not c.is_used])

    return [pair_1, pair_2]

def has_triple(cards):
    for card in cards:
        sames = [c for c in cards if c.value == card.value]

        if len(sames) == 3:
            return sames

def has_poker(cards):
    for card in cards:
        sames = [c for c in cards if c.value == card.value]

        if len(sames) == 4:
            return sames

def has_straight(cards):
    values = sorted(list(set([c.value + 1 for c in cards])), reverse=True)

    if ACE_VALUE + 1 in values:
        values.append(0)

    streak = 1
    last_val = -100

    for val in values:
        if last_val - 1 == val:
            streak += 1
            if streak == 5:
                print(streak)
        else:
            streak = 1
        last_val = val

SCORINGS = [
    ("PAIR", has_pair),
    ("TWO_PAIR", has_two_pair),
    ("TRIPLE", has_triple),
    ("STRAIGHT", has_straight),
    #("FLUSH", has_flush),
    #("FULL_HOUSE", has_full_house),
    ("POKER", has_poker),
    #("STRAIGHT_FLUSH", has_straight_flush)
]


execute([
    Card(0, 10),
    Card(1, 8),
    Card(1, 11),
    Card(2, 9),
    Card(0, 10),
    Card(3, 12),
    Card(2, 8)
])
