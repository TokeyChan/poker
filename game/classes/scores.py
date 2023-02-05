from .card import Card

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
            results.append([scoring[0], scoring[2], result])

    return max(results, key=lambda x: x[1]) if len(results) > 0 else ["HIGH_CARD", 0, sorted(cards, key=lambda x: x.value, reverse=True)[0]]


def has_pair(cards): # Card[]
    for card in cards:
        sames = [c for c in cards if c.value == card.value and not c.is_used]

        if len(sames) >= 2:
            return sames[:2]

def has_two_pair(cards):
    pair_1 = has_pair(cards)

    if pair_1 is None:
        return

    for card in pair_1:
        card.is_used = True

    pair_2 = has_pair([c for c in cards if not c.is_used])

    if pair_1 and pair_2:
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
    values = [(c.value + 1, c) for c in cards]
    result = []

    if ACE_VALUE + 1 in values:
        values.append(0)

    streak = []
    last_val = -100
    last_card = None

    for val, card in values:
        if last_val - 1 == val:
            if len(streak) == 0:
                streak.append(last_card)
            streak.append(card)

            if len(streak) == 5:
                result.append(list(reversed(streak)))
                streak.pop(0)
        elif last_val != val:
            streak = []
        last_val = val
        last_card = card

    return result if len(result) > 0 else None

def has_flush(cards):
    five_same = [suit for suit in range(4) if len([c for c in cards if c.suit == suit]) >= 5]

    if len(five_same) == 0:
        return

    suit = five_same[0]
    return [c for c in cards if c.suit == suit][:5]

def has_full_house(cards):
    triple = has_triple(cards)

    if triple is None:
        return
    
    for card in triple:
        card.is_used = True
    
    pair = has_pair(cards)

    if pair is None:
        return

    

def has_straight_flush(cards):
    straights = has_straight(cards)

    if straights is None:
        return

    for straight in straights:
        if len(set([card.suit for card in straight])) == 1:
            return straight

SCORINGS = [
    ("PAIR", has_pair, 1),
    ("TWO_PAIR", has_two_pair, 2),
    ("TRIPLE", has_triple, 3),
    ("STRAIGHT", has_straight, 4),
    ("FLUSH", has_flush, 5),
    ("FULL_HOUSE", has_full_house, 6),
    ("POKER", has_poker, 7),
    ("STRAIGHT_FLUSH", has_straight_flush, 8)
]

def handle_draw(max_, winners):
    print(f"DRAW WITH A {max_[0]}")
    match max_[0]:
        case 'PAIR':
            highest_pair_value = max(winners, key=lambda x: x[1][2][0].value)

            if len([p for p in winners if p[1][2][0].value == highest_pair_value[1][2][0].value]) == 1:
                return [highest_pair_value]

            hands = [sorted(p[0].hand, key=lambda x: x.value) for p in winners]

    return []