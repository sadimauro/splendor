"""
game.py - TODO
"""

from copy import deepcopy
from core import (
        DevCard,
        DevCardDeck,
        DevCardType,
        GameTokenCache,
        Noble,
        NoblesInPlay,
        Token,
        TokenType,
        )
from player import (
        Player,
        )
from typing import List, Dict, Set, Tuple

PLAYERS_COUNT_MIN = 2
PLAYERS_COUNT_MAX = 4

WINNING_SCORE = 15

TAKE_TWO_TOKENS_MINIMUM = 4

class GameState:
    """
    Record of a particular state of the game.  Does not include Players.

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
    
    >>> game_state = GameState(dev_card_deck_1, dev_card_deck_2, dev_card_deck_3, nobles_in_play, game_token_cache)

    """
    dev_card_decks: Tuple[List, List, List] # idx=i -> deck #i+1
    nobles_in_play: NoblesInPlay
    token_cache: GameTokenCache

    def __init__(
        self,
        dev_card_deck_1: DevCardDeck,
        dev_card_deck_2: DevCardDeck,
        dev_card_deck_3: DevCardDeck,
        nobles_in_play: NoblesInPlay,
        game_token_cache: GameTokenCache,
    ) -> None:
        self.dev_card_decks = ((dev_card_deck_1, dev_card_deck_2, dev_card_deck_3))
        self.nobles_in_play = nobles_in_play
        self.game_token_cache = game_token_cache

    def copy(self):
        return deepcopy(self)

    def get_dev_card_deck(
            self, 
            no: int) -> DevCardDeck:
        if (no-1) < 0 or (no-1) > len(self.dev_card_decks):
            raise Exception("no such dev card deck")
        return self.dev_card_deck[no-1]

    def set_dev_card_deck(
            self,
            no: int,
            new_dev_card_deck: DevCardDeck,
            ) -> None:
        if (no-1) < 0 or (no-1) > len(self.dev_card_decks):
            raise Exception("no such dev card deck")
        self.dev_card_decks[no-1] = new_dev_card_deck
        return

    def get_nobles_in_play(self) -> NoblesInPlay:
        return self.nobles_in_play

    def set_nobles_in_play(
            self, 
            new_nobles_in_play: NoblesInPlay,
            ) -> None:
        self.nobles_in_play = new_nobles_in_play
        return

    def get_token_cache(self) -> GameTokenCache:
        return self.token_cache

    def set_token_cache(self, new_token_cache: GameTokenCache) -> None:
        self.token_cache = new_token_cache
        return


class GameStateHistory:
    """
    Record of all of the historical states of the game.

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
    
    >>> game_state = GameState(dev_card_deck_1, dev_card_deck_2, dev_card_deck_3, nobles_in_play, game_token_cache)

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
 
def clone_gameState_new_dev_card_deck(
    old_game_state: GameState, 
    new_deck_no: int,
    new_dev_card_deck: DevCardDeck,
) -> GameState:
    """
    Create a new GameState from an existing one but using the updated
    DevCardDeck.
    """
    ret = old_game_state.copy()
    ret.set_dev_card_deck(new_deck_no, new_dev_card_deck)
    return ret

def clone_gameState_new_nobles_in_play(
        old_game_state: GameState, 
        new_nobles_in_play: NoblesInPlay,
) -> GameState:
    """
    Create a new GameState from an existing one but using the updated
    NoblesInPlay.
    """
    ret = old_game_state.copy()
    ret.set_nobles_in_play(new_nobles_in_play)
    return ret

def clone_gameState_new_token_cache(
    old_game_state: GameState, 
    new_token_cache: GameTokenCache
) -> GameState:
    """
    Create a new GameState from an existing one but using the updated
    TokenCache.
    """
    ret = old_game_state.copy()
    ret.set_token_cache(new_token_cache)
    return ret

def clone_gameState(
    old_game_state: GameState,
    new_deck_no: int = 0,
    new_dev_card_deck: DevCardDeck = None,
    new_nobles_in_play: NoblesInPlay = None,
    new_token_cache: GameTokenCache = None,
) -> GameState:
    """
    Create a new GameState from an existing one but using the updated
    TokenCache, DevCardCache, and/or DevCardReserve (any or all can be None).
    """
    ret = old_game_state.copy()
    if new_dev_card_deck and new_deck_no != 0:
        ret.set_dev_card_deck(new_deck_no, new_dev_card_deck)
    if new_nobles_in_play:
        ret.set_nobles_in_play(new_nobles_in_play)
    if new_token_cache:
        ret.set_token_cache(new_token_cache)
    return ret
 

class Game:
    """
    A game.  Includes game states and players.
    """

    number_of_players: int
    players: List[Player] # list b/c order of play matters
    current_player_idx: int
    game_state_history: GameStateHistory
    round_number_idx: int
    
    def __init__(self, number_of_players: int) -> None:
        """
        Set up new game
        """
        self.number_of_players = number_of_players
        self.players = list()
        self.current_player_idx = 0
        self.game_state_history = GameStateHistory()
        self.round_number_idx = 0
        return

    def add_player(self, player: Player) -> None:
        self.players.append(player)
        return

    def get_game_state_history(self) -> GameStateHistory:
        return self.game_state_history

    def append_game_state(self, new_state) -> None:
        self.game_state_history.append(new_state)
        return

    def get_current_game_state(self) -> GameState:
        return self.game_state_history.get_current_state()

    def get_current_dev_card_deck(self, no: int) -> DevCardDeck:
        return self.get_current_game_state().get_dev_card_deck(no)

    def get_current_nobles_in_play(self) -> NoblesInPlay:
        return self.get_current_game_state().get_nobles_in_play()
    
    def get_current_token_cache(self) -> PlayerTokenCache:
        return self.get_current_game_state().get_token_cache()

    def play(self) -> None:
        pass

    def action_take_three_tokens(
            self,
            player: Player,
            token_type_str_1: str,
            token_type_str_2: str,
            token_type_str_3: str,
            ) -> None:
        """
        Complete the player action of taking three tokens.

        This function makes sure that the tokens are all of different type, and that none are yellow (jokers).
        """
        if (
            token_type_str_1 == token_type_str_2
            or token_type_str_1 == token_type_str_3
            or token_type_str_2 == token_type_str_3
        ):
            raise Exception("action not allowed: chosen tokens must be all different")
        if is_joker(token_type_str_1) or is_joker(token_type_str_2) or is_joker(token_type_str_3):
            raise Exception("action not allowed: chosen tokens must not be jokers")

        # make sure player isn't over his/her max
        if not player.can_fit_tokens(len(token_type_str_add_list)):
            raise Exception(
                f"not enough space in player's token cache to add {len(token_type_add_list)} tokens"
            )
            # instead of above, we need to allow the player to get rid of some of his/her current tokens

        current_game_state = self.get_current_game_state()
        game_token_cache = current_game_state.get_token_cache()
        
        # make sure game has the right tokens
        if game_token_cache.count_type(token_type_str_1) < 1:
            raise Exception(f"not enough tokens of type {token_type_str_1} in the game's token cache")
        if game_token_cache.count_type(token_type_str_2) < 1:
            raise Exception(f"not enough tokens of type {token_type_str_2} in the game's token cache")
        if game_token_cache.count_type(token_type_str_3) < 1:
            raise Exception(f"not enough tokens of type {token_type_str_3} in the game's token cache")

        # update player
        player.action_take_three_tokens(
                token_type_str_1,
                token_type_str_2,
                token_type_str_3,
                )

        # update game
        for token_type_str_to_remove in token_type_str_add_list:
            token_cache.remove(token_type_str_to_remove)
        new_state = clone_gameState_new_token_cache(
            current_game_state,
            token_cache,
        )
        self.append_game_state(new_state)
        return

    def action_take_two_tokens(
            self,
            token_type_str: str,
            ) -> None:
        """
        Complete the player action of taking two tokens.
        """
        if is_joker(token_type_str):
            raise Exception("action not allowed: chosen tokens must not be jokers")
        
        # make sure player isn't over his/her max
        if not player.can_fit_tokens(len(token_type_str_add_list)):
            raise Exception(
                f"not enough space in player's token cache to add {len(token_type_add_list)} tokens"
            )
            # instead of above, we need to allow the player to get rid of some of his/her current tokens
        
        current_game_state = self.get_current_game_state()
        game_token_cache = current_game_state.get_token_cache()
        
        # make sure game has the right tokens
        if game_token_cache.count_type(token_type_str) < 2:
            raise Exception(f"not enough tokens of type {token_type_str_1} in the game's token cache")

        # make sure we're not breaking a rule
        if token_cache.count_type(token_type_str) < TAKE_TWO_TOKENS_MINIMUM:
            raise Exception(f"cannot take two tokens from a stack with fewer than {TAKE_TWO_TOKENS_MINIMUM}")

        # update player
        player.action_take_two_tokens(
                token_type_str,
                )

        # update game
        for token_type_str_to_remove in token_type_str_add_list:
            token_cache.remove(token_type_str_to_remove)
        new_state = clone_gameState_new_token_cache(
            current_game_state,
            token_cache,
        )
        self.append_game_state(new_state)
        return

    def action_reserve_dev_card(
            self,
            player: Player,
            dev_card: DevCard, # instead of dev_card, args could include deck_no and idx into deck
            ) -> None:
        """
        Complete the action of a player reserving a dev card.
        """
        # make sure player isn't over his/her max tokens and reserve cards
        if player.get_dev_card_reserve().is_max():
            raise Exception(f"player at max reserve cards")

        if not player.can_fit_tokens(1):
            raise Exception(
                f"not enough space in player's token cache to add 1 token"
            )
            # instead of above, we need to allow the player to get rid of some of his/her current tokens
        
        current_game_state = self.get_current_game_state()
        dev_card_level = dev_card.get_level()
        dev_card_deck = current_game_state.get_dev_card_deck(dev_card_level)
        
        # make sure card actually exists in the deck
        found_idx = dev_card_deck.find_card(dev_card)
        if found_idx == -1:
            raise Exception(f"could not find card in given deck")

        # remove card from deck
        # we ignore the return since we already have the card
        # note that the popping essentially deals out a new facing card
        dev_card_deck.pop_by_idx(found_idx)
        new_state = close_gameState_new_dev_card_deck(
                current_game_state,
                dev_card_level,
                dev_card_deck
                )
        self.append_game_state(new_state)

        # add card to player's reserve, and yellow token to player's token cache
        player.action_reserve_dev_card(dev_card)

        return


    def action_purchase_dev_card(
            self,
            player: Player,
            dev_card: DevCard, # instead of dev_card, args could include deck_no and idx into deck
            ) -> None:
        """
        Complete the action of a player purchasing a dev card.
        """

        # make sure player has the required tokens to spend
        # TODO: handle use of jokers too
        if not player.get_token_cache().can_purchase_dev_card(dev_card_to_add):
            raise Exception(f"cannot purchase dev card: insufficient tokens")
        
        # make sure card actually exists in the deck
        current_game_state = self.get_current_game_state()
        dev_card_level = dev_card.get_level()
        dev_card_deck = current_game_state.get_dev_card_deck(dev_card_level)
        found_idx = dev_card_deck.find_card(dev_card)
        if found_idx == -1:
            raise Exception(f"could not find card in given deck")

        # remove card from deck
        # we ignore the return since we already have the card
        # note that the popping essentially deals out a new facing card
        dev_card_deck.pop_by_idx(found_idx)
        new_state = close_gameState_new_dev_card_deck(
                current_game_state,
                dev_card_level,
                dev_card_deck
                )
        self.append_game_state(new_state)

        # add card to player's dev card cache
        player.action_purchase_dev_card(dev_card)

        return

