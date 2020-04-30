"""
game.py - TODO
"""

PLAYERS_COUNT_MIN = 2
PLAYERS_COUNT_MAX = 4

class GameState:
    """
    Record of a particular state of the game.

    >>> dc0 = DevCard(level=1, t=DevCardType("black"), ppoints=2, cost={"blue": 2, "red": 1})
    >>> dc1 = DevCard(level=1, t=DevCardType("black"), ppoints=0, cost={"blue": 3})
    >>> dc2 = DevCard(level=1, t=DevCardType("blue"), ppoints=1, cost={"white": 1, "red": 1, "green": 3})
    >>> dc3 = DevCard(level=1, t=DevCardType("red"), ppoints=4, cost={"white": 1, "red": 1, "green": 3})
    >>> dc4 = DevCard(level=1, t=DevCardType("red"), ppoints=4, cost={"white": 1, "red": 1, "green": 3})
    >>> dc5 = DevCard(level=1, t=DevCardType("red"), ppoints=0, cost={"red": 1, "green": 3})
    >>> dc6 = DevCard(level=1, t=DevCardType("white"), ppoints=0, cost={"white": 1, "green": 3})
    >>> dev_card_deck_1 = DevCardDeck(1, [dc0, dc1, dc2, dc3, dc4, dc5, dc6])

    >>> dc0 = DevCard(level=2, t=DevCardType("black"), ppoints=2, cost={"blue": 2, "red": 1})
    >>> dc1 = DevCard(level=2, t=DevCardType("black"), ppoints=0, cost={"blue": 3})
    >>> dc2 = DevCard(level=2, t=DevCardType("blue"), ppoints=1, cost={"white": 1, "red": 1, "green": 3})
    >>> dc3 = DevCard(level=2, t=DevCardType("red"), ppoints=4, cost={"white": 1, "red": 1, "green": 3})
    >>> dc4 = DevCard(level=2, t=DevCardType("red"), ppoints=4, cost={"white": 1, "red": 1, "green": 3})
    >>> dev_card_deck_2 = DevCardDeck(2, [dc0, dc1, dc2, dc3, dc4])
    
    >>> dc0 = DevCard(level=3, t=DevCardType("black"), ppoints=4, cost={"blue": 2, "red": 5})
    >>> dc1 = DevCard(level=3, t=DevCardType("black"), ppoints=5, cost={"blue": 6})
    >>> dc2 = DevCard(level=3, t=DevCardType("blue"), ppoints=5, cost={"white": 3, "red": 5, "green": 3})
    >>> dc3 = DevCard(level=3, t=DevCardType("red"), ppoints=4, cost={"white": 3, "red": 3, "green": 3})
    >>> dc4 = DevCard(level=3, t=DevCardType("red"), ppoints=4, cost={"white": 3, "red": 3, "green": 3})
    >>> dc5 = DevCard(level=3, t=DevCardType("red"), ppoints=5, cost={"red": 4, "green": 3})
    >>> dc6 = DevCard(level=3, t=DevCardType("white"), ppoints=4, cost={"white": 5, "green": 3})
    >>> dev_card_deck_3 = DevCardDeck(3, [dc0, dc1, dc2, dc3, dc4, dc5, dc6])

    >>> n1 = Noble(3, {'black': 4, 'white': 4})
    >>> n2 = Noble(3, {'black': 3, 'white': 3, 'blue': 3})
    >>> n3 = Noble(3, {'black': 4, 'green': 4})
    >>> n4 = Noble(3, {'white': 4, 'red': 4})
    >>> nobles_in_play = NoblesInPlay(set((n1, n2, n3, n4)))

    >>> game_token_cache = GameTokenCache(players_count=2)
    
    >>> game_state = GameState(
            dev_card_deck_1,
            dev_card_deck_2,
            dev_card_deck_3,
            nobles_in_play,
            game_token_cache,
            )



    """
    dev_card_deck_1: DevCardDeck
    dev_card_deck_2: DevCardDeck
    dev_card_deck_3: DevCardDeck
    nobles_in_play: NoblesInPlay
    game_token_cache: GameTokenCache

    def __init__(self):
        pass

    def action_take_three_tokens(self, token_1: Token, token_2: Token, token_3: Token) -> None:
        pass
    
    def action_take_two_tokens(self, token_1: Token, token_2: Token) -> None:
        pass

    def action_reserve_dev_card(self, dev_card: DevCard, level: int) -> None:
        pass

    def action_purchase_dev_card(self, dev_card: DevCard, level: int) -> None
        pass

    def action_obtain_noble(self, noble: Noble) -> None:
        pass


class GameStateHistory:
    """
    Record of all of the historical states of the game.

    >>> game_state_history = GameStateHistory()
    >>> game_state_history.append(game_state)

    """
    l: List[GameState]
    
    def __init__(self) -> None:
        self.l = list()

    # __str__() # needed?
    
    def append(self, new_state) -> None:
        self.l.append(new_state)
        return

    def get_current_state(self) -> GameState:
        """ Retrieve the current state within this GameStateHistory. """
        if len(self.l) == 0:
            return None
        return self.l[len(self.l) - 1]

    def get_current_state_no(self) -> int:
        """ Return the one-based state number (or zero, if the list is empty)."""
        return len(self.l)

    def revert(self, state_no: int) -> None:
        """ Revert history to state at state_no, and remove newer states. """
        if state_no <= 0:
            raise Exception("state number cannot be negative")
        if state_no > len(self.l):
            raise Exception(
                "state number cannot be greater than the current state number"
            )
        self.l = self.l[0:state_no]
        return
  

class Game:
    players: List[Player] # list b/c order of play matters
    game_state_history: GameStateHistory
    round_number: int
    __init__(players_count: int) # set up new game
    add_player(player: Player)
    play()
    action_take_three_gems(player: Player, gem_types_set: Set(3)) -> None # analyze current state; if applicable, create new state
    action_take_two_gems(player: Player, gem_type: GemType) -> None
    action_reserve() -> None
    action_purchase() -> None

