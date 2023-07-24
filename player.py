from card import Card


class Player:

    ACTION_FOLD_STR = "FOLD"
    ACTION_CALL_STR = "CALL"
    ACTION_RAISE_STR = "RAISE"
    ACTION_SMALL_BLIND = "SMALLBLIND"
    ACTION_BIG_BLIND = "BIGBLIND"
    ACTION_ANTE = "ANTE"
    
    def __init__(self, name="no name"):
        self.name = name
        self.hole_card = []
        
    def add_holecard(self, cards):
        if len(self.hole_card) != 0:
            raise ValueError(self.__dup_hole_msg)
        if len(cards) != 2:
            raise ValueError(self.__wrong_num_hole_msg % (len(cards)))
        if not all([isinstance(card, Card) for card in cards]):
            raise ValueError(self.__wrong_type_hole_msg)
        self.hole_card = cards
        

    __dup_hole_msg = "Hole card is already set"
    __wrong_num_hole_msg = "You passed  %d hole cards"
    __wrong_type_hole_msg = "You passed not Card object as hole card"
    

player1 = Player(name="mathieu")
player2 = Player(name="loic")
