import names

PLAYER_ACTIONS = ["FOLD", "CHECK", "CALL", "ALL_IN", "RAISE_50", "RAISE_75", "RAISE_100"]

class Player:
    # general
    chips = 0
    name = ""
    
    # game
    hand = None # Card Tuple
    
    # round
    bet = 0
    action_completed = False
    is_all_in = False
    is_folded = False
    
    def __init__(self, chips):
        self.chips = chips
        self.name = names.get_first_name()

    def __str__(self):
        return self.name

    def buy_in(self, value):
        self.chips += value

    def give_hand(self, card1, card2): # hand = (Card, Card)
        self.hand = (card1, card2)

    def soft_reset(self):
        self.bet = 0
        self.action_completed = False

    def hard_reset(self):
        self.bet = 0
        self.action_completed = False
        self.is_all_in = False
        self.is_folded = False

    # cool methods:

    def ask_for_action(self, entire_pot, highest_bet):
        check_is_possible = highest_bet == self.bet
        call_is_possible = (highest_bet - self.bet) < self.chips and not check_is_possible
        raise_50_is_possible = (entire_pot + (highest_bet - self.bet)) * 1.5 < self.chips
        raise_75_is_possible = (entire_pot + (highest_bet - self.bet)) * 1.75 < self.chips
        raise_100_is_possible = (entire_pot + (highest_bet - self.bet)) * 2 < self.chips

        possible_actions = ['FOLD', 'ALL_IN']
        if check_is_possible:
            possible_actions.append('CHECK')
        if call_is_possible:
            possible_actions.append('CALL')
        if raise_50_is_possible:
            possible_actions.append('RAISE_50')
        if raise_75_is_possible:
            possible_actions.append('RAISE_75')
        if raise_100_is_possible:
            possible_actions.append('RAISE_100')

        self.action_completed = True
        if check_is_possible:
            return "CHECK"
        elif call_is_possible:
            return "CALL"
        else:
            return "FOLD"

        action = None
        if True:
            print(f"Hi {self.name}!")
            print(f"You have {str(self.hand[0])} and {str(self.hand[1])}")
            print(f"Your current bet is {self.bet}")
            print(f"You have {self.chips} chips")
            print(f"The current pot is {entire_pot}")
            print(f"The highest bet is {highest_bet}")
            if call_is_possible:
                print(f"You need {highest_bet - self.bet} to call")
        while not action in possible_actions:
            action = input(f"What do you want to do? ({', '.join(possible_actions)}) ").upper()
        
        self.action_completed = True
        return action

    def set_bet(self, value):
        chips_to_pay = value - self.bet
        self.chips -= chips_to_pay
        self.bet = value

    def raise_bet(self, entire_pot, highest_bet, percentage):
        goal = (entire_pot + (highest_bet - self.bet)) * percentage

        rounded_goal = round(goal * 2) / 2

        self.set_bet(rounded_goal)


