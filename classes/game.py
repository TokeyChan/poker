from .deck import Deck
from .player import Player

from .scores import execute as execute_score

class Game:
    # statics
    PLAYER_COUNT = 6
    BIG_BLIND = 1
    SMALL_BLIND = 0.5
    INITIAL_CHIPS = 100

    players = []
    active_players = []
    deck = None
    dealer_index = 0
    pot = 0
    betting_index = 0
    highest_bet = 0


    current_round = 0
    board = [] # Card[]

    def __init__(self):
        for p in range(self.PLAYER_COUNT):
            self.players.append(Player(self.INITIAL_CHIPS))
        
        self.deck = Deck()

        self.debugList = [''] * self.PLAYER_COUNT

    def start_round(self):
        self._setup()
        self.current_round = GameRounds.PREFLOP
        self._betting()
        self._flop()
        self._betting()
        self._turn()
        self._betting()
        self._river()
        self._betting()
        self._ending()


    def _setup(self):
        self.reset_players(True)
        self.current_round = GameRounds.SETUP
        self.deck.restart()
        self.board = []
        self.active_players = self.players
        self.deal()

    def _betting(self):
        self.reset_players()
        if self.current_round == GameRounds.PREFLOP:
            small_blind_player = self.get_small_blind()
            small_blind_player.set_bet(self.SMALL_BLIND)

            big_blind_player = self.get_big_blind()
            big_blind_player.set_bet(self.BIG_BLIND)

            self.betting_index = self.dealer_index + 3

        while not (self.all_players_finished() and self.all_bets_equal()):
            player = self.get_player(self.betting_index)
            self.betting_index += 1

            if player.is_folded or player.is_all_in:
                continue

            i = self.betting_index % 6
            self.debugList[i] = 'x'
            print(self.debugList) 
            self.debugList[i] = ''

            action = player.ask_for_action(self.entire_pot, self.highest_bet)

            match action:
                case 'FOLD':
                    player.is_folded = True
                    self.debugList[i] = 'f'
                case 'CHECK':
                    pass
                case 'CALL':
                    player.set_bet(self.highest_bet)
                case 'RAISE_50':
                    player.raise_bet(self.entire_pot, self.highest_bet, 1.5)
                case 'RAISE_75':
                    player.raise_bet(self.entire_pot, self.highest_bet, 1.75)
                case 'RAISE_100':
                    player.raise_bet(self.entire_pot, self.highest_bet, 2)
                case 'ALL_IN':
                    player.is_all_in = True
                    player.set_bet(player.bet + player.chips)
                    self.debugList[i] = 'a'

        self.pot = self.active_pot

    def _flop(self):
        self.current_round = GameRounds.FLOP
        self.board = [self.deck.pick_card(), self.deck.pick_card(), self.deck.pick_card()]
        print("FLOP")
        print([str(card) for card in self.board])

    def _turn(self):
        self.current_round = GameRounds.TURN
        self.board.append(self.deck.pick_card())
        print("TURN")
        print([str(card) for card in self.board])

    def _river(self):
        self.current_round = GameRounds.RIVER
        self.board.append(self.deck.pick_card())
        print("RIVER")
        print([str(card) for card in self.board])

    def _ending(self):
        for player in [p for p in self.active_players if not p.is_folded]:
            results = execute_score([player.hand[0], player.hand[1]] + self.board)

            if len(results) == 0:
                print(player.name)
                print("opfa")
                continue

            max_ = max(results, key=lambda x: x[1])

            print(player.name)
            print(max_)

    def all_players_finished(self):
        return all([p.action_completed or p.is_folded or p.is_all_in for p in self.active_players])

    def all_bets_equal(self):
        return all_equal([p.bet for p in self.active_players if not p.is_folded or p.is_all_in])

    def get_player(self, index):
        while index > (len(self.active_players) - 1):
            index -= len(self.active_players)
        
        return self.active_players[index]

    def get_small_blind(self):
        return self.get_player(self.dealer_index + 1)

    def get_big_blind(self):
        return self.get_player(self.dealer_index + 2)

    @property
    def dealer(self):
        return self.players[self.dealer_index]

    @property
    def active_pot(self):
        return sum([p.bet for p in self.players])

    @property
    def highest_bet(self):
        return max([p.bet for p in self.players])

    @property
    def entire_pot(self):
        return self.pot + self.active_pot

    def reset_players(self, hard_reset=False):
        for player in self.players:
            if hard_reset:
                player.hard_reset()
            else:
                player.soft_reset()

    def deal(self):
        for player in self.players:
            player.give_hand(
                self.deck.pick_card(),
                self.deck.pick_card()
            )

# dealer index geht am ende weiter

class GameRounds:
    SETUP = 0
    PREFLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4

def all_equal(iterator):
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == x for x in iterator)