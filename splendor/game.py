"""
game.py - TODO
"""

PLAYERS_COUNT_MIN = 2
PLAYERS_COUNT_MAX = 4

class GameState:
    """
    Record of a particular state of the game.
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

