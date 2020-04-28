"""
"""

from core import DevCard, DevCardCache, DevCardReserve, DevCardType, PlayerTokenCache, Token, TokenType, PLAYER_TOKEN_CACHE_MAX, WINNING_SCORE

from copy import deepcopy
from enum import Enum
import json
import logging
import random
import string
from typing import List, Dict, Set

logging.basicConfig(level=logging.INFO)

class PlayerState:
    """
    The state of a player at some point during a game.
   
    >>> token_cache = PlayerTokenCache()
    >>> token_cache.add(Token(TokenType("black")))
    >>> token_cache.add(Token(TokenType("black")))
    >>> token_cache.add(Token(TokenType("red")))
    >>> dev_card_cache = DevCardCache()
    >>> dev_card_cache.add(DevCard(level=1, t=DevCardType("black"), ppoints=2, cost={"blue": 2, "red": 1}))
    >>> dev_card_cache.add(DevCard(level=2, t=DevCardType("black"), ppoints=0, cost={"blue": 3}))
    >>> dev_card_cache.add(DevCard(level=1, t=DevCardType("blue"), ppoints=1, cost={"white": 1, "red": 1, "green": 3}))
    >>> dev_card_reserve = DevCardReserve()
    >>> dev_card_reserve.add(DevCard(level=1, t=DevCardType("red"), ppoints=4, cost={"white": 1, "red": 1, "green": 1}))
    >>> a = PlayerState(token_cache, dev_card_cache, dev_card_reserve)

    >>> a.calc_score()
    3

    >>> a.is_winning_state()
    False

    >>> b = a.copy()
    >>> a.calc_score() == b.calc_score()
    True

    """
    token_cache: PlayerTokenCache
    dev_card_cache: DevCardCache
    dev_card_reserve: DevCardReserve

    def __init__(self, token_cache: PlayerTokenCache, dev_card_cache: DevCardCache, dev_card_reserve: DevCardReserve) -> None:
        self.token_cache = token_cache
        self.dev_card_cache = dev_card_cache
        self.dev_card_reserve = dev_card_reserve

    def copy(self):
        return deepcopy(self)

    def get_token_cache(self) -> PlayerTokenCache:
        return self.token_cache
    
    def set_token_cache(self, new_token_cache) -> None:
        self.token_cache = new_token_cache
        return

    def get_dev_card_cache(self) -> DevCardCache:
        return self.dev_card_cache

    def set_dev_card_cache(self, new_dev_card_cache) -> None:
        self.dev_card_cache = new_dev_card_cache
        return
    
    def get_dev_card_reserve(self) -> DevCardReserve:
        return self.dev_card_reserve

    def set_dev_card_reserve(self, new_dev_card_reserve) -> None:
        self.dev_card_reserve = new_dev_card_reserve
        return
    
    def calc_score(self) -> int:
        return self.dev_card_cache.calc_ppoints()

    def is_winning_state(self) -> bool:
        return self.calc_score() >= WINNING_SCORE

    def __str__(self) -> str:
        ret = ""
        ret += "Player state:\n"
        ret += self.token_cache + "\n"
        ret += self.dev_card_cache + "\n"
        ret += self.dev_card_reserve + "\n"
        return ret

def clone_playerState_new_token_cache(
        old_player_state: PlayerState,
        new_token_cache: PlayerTokenCache
        ) -> PlayerState:
    """
    Create a new PlayerState from an existing one but using the updated
    TokenCache.
    """
    ret = old_player_state.copy()
    ret.set_token_cache(new_token_cache)
    return ret

def clone_playerState_new_dev_card_cache(
        old_player_state: PlayerState,
        new_dev_card_cache: DevCardCache,
        ) -> PlayerState:
    """
    Create a new PlayerState from an existing one but using the updated
    DevCardCache.
    """
    ret = old_player_state.copy()
    ret.set_dev_card_cache(new_dev_card_cache)
    return ret

def clone_playerState_new_dev_card_reserve(
        old_player_state: PlayerState,
        new_dev_card_reserve: DevCardReserve,
        ) -> PlayerState:
    """
    Create a new PlayerState from an existing one but using the updated
    DevCardReserve.
    """
    ret = old_player_state.copy()
    ret.set_dev_card_reserve(new_dev_card_reserve)
    return ret

def clone_playerState(
        old_player_state: PlayerState,
        new_token_cache: PlayerTokenCache=None,
        new_dev_card_cache: DevCardCache=None,
        new_dev_card_reserve: DevCardReserve=None,
        ) -> PlayerState:
    """
    Create a new PlayerState from an existing one but using the updated
    TokenCache, DevCardCache, and/or DevCardReserve (any or all can be None).
    """
    ret = old_player_state.copy()
    if new_token_cache:
        ret.set_token_cache(new_token_cache)
    if new_dev_card_cache:
        ret.set_dev_card_cache(new_dev_card_cache)
    if new_dev_card_reserve:
        ret.set_dev_card_reserve(new_dev_card_reserve)
    return ret


class PlayerStateHistory:
    """
    The ordered list of a player's states.  PlayerState at index 0 is the player's first PlayerState, and subsequent indices are later states.

    >>> token_cache = PlayerTokenCache()
    >>> token_cache.add(Token(TokenType("black")))
    >>> token_cache.add(Token(TokenType("black")))
    >>> token_cache.add(Token(TokenType("red")))
    >>> dev_card_cache = DevCardCache()
    >>> dev_card_cache.add(DevCard(level=1, t=DevCardType("black"), ppoints=2, cost={"blue": 2, "red": 1}))
    >>> dev_card_cache.add(DevCard(level=2, t=DevCardType("black"), ppoints=0, cost={"blue": 3}))
    >>> dev_card_cache.add(DevCard(level=1, t=DevCardType("blue"), ppoints=1, cost={"white": 1, "red": 1, "green": 3}))
    >>> dev_card_reserve = DevCardReserve()
    >>> dev_card_reserve.is_max()
    False

    >>> dev_card_reserve.add(DevCard(level=1, t=DevCardType("red"), ppoints=4, cost={"white": 1, "red": 1, "green": 3}))
    >>> state_1 = PlayerState(token_cache, dev_card_cache, dev_card_reserve)

    >>> token_cache.add(Token(TokenType("blue")))
    >>> state_2 = PlayerState(token_cache, dev_card_cache, dev_card_reserve)
    
    >>> dev_card_reserve.add(DevCard(level=2, t=DevCardType("red"), ppoints=5, cost={"white": 3, "red": 4, "green": 3}))
    >>> state_3 = PlayerState(token_cache, dev_card_cache, dev_card_reserve)

    >>> psh = PlayerStateHistory()
    >>> psh.get_current_state_no()
    0
    >>> psh.append(state_1)
    >>> psh.get_current_state_no()
    1
    >>> psh.append(state_2)
    >>> psh.append(state_3)
    >>> psh.get_current_state_no()
    3
    >>> psh.get_current_state() #doctest: +ELLIPSIS
    <player.PlayerState object at ...

    >>> psh.revert(1)
    >>> psh.get_current_state_no()
    1

    """
    l: List[PlayerState]

    def __init__(self) -> None:
        self.l = list()

    def append(self, new_state) -> None:
        self.l.append(new_state)
        return

    def get_current_state(self) -> PlayerState:
        """ Retrieve the current state within this PlayerStateHistory. """
        if len(self.l) == 0:
            return None
        return self.l[len(self.l)-1]
    
    def get_current_state_no(self) -> int:
        """ Return the one-based state number (or zero, if the list is empty)."""
        return len(self.l)

    def revert(self, state_no: int) -> None: 
        """ Revert history to state at state_no, and remove newer states. """
        if state_no <= 0:
            raise Exception("state number cannot be negative")
        if state_no > len(self.l):
            raise Exception("state number cannot be greater than the current state number")
        self.l = self.l[0:state_no]
        return

class Player:
    """
    A Splendor player.  Includes the player's name and state history.

    >>> player_a = Player("Joe")
    >>> player_a.get_name()
    'Joe'

    >>> token_cache = PlayerTokenCache()
    >>> token_cache.add(Token("black"))
    >>> token_cache.add(Token("black"))
    >>> token_cache.add(Token("red"))
    >>> dev_card_cache = DevCardCache()
    >>> dev_card_cache.add(DevCard(level=1, t=DevCardType("black"), ppoints=2, cost={"blue": 2, "red": 1}))
    >>> dev_card_cache.add(DevCard(level=2, t=DevCardType("black"), ppoints=0, cost={"blue": 3}))
    >>> dev_card_cache.add(DevCard(level=1, t=DevCardType("blue"), ppoints=1, cost={"white": 1, "red": 1, "green": 3}))
    >>> dev_card_reserve = DevCardReserve()
    >>> dev_card_reserve.add(DevCard(level=1, t=DevCardType("red"), ppoints=4, cost={"white": 1, "red": 1, "green": 2}))
    >>> state_1 = PlayerState(token_cache, dev_card_cache, dev_card_reserve)
    >>> player_a.append_player_state(state_1)

    >>> player_a.calc_score()
    3

    >>> token_cache.add(Token("blue"))
    >>> state_2 = PlayerState(token_cache, dev_card_cache, dev_card_reserve)
    >>> dev_card_reserve.add(DevCard(level=2, t=DevCardType("red"), ppoints=5, cost={"white": 3, "red": 4, "green": 3}))
    >>> state_3 = PlayerState(token_cache, dev_card_cache, dev_card_reserve)
    >>> player_a.append_player_state(state_2)
    >>> player_a.append_player_state(state_3)

    >>> player_a.get_current_token_cache().size()
    4
    >>> player_a.action_take_three_tokens(Token("black"), Token("blue"), Token("green"))
    >>> player_a.get_current_token_cache().size()
    7
    >>> player_a.action_take_three_tokens(Token("black"), Token("black"), Token("green")) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    Exception...
    >>> player_a.action_take_three_tokens(Token("black"), Token("yellow"), Token("green")) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    Exception...

    >>> player_a.action_take_two_tokens(Token("red"), Token("red"))
    >>> player_a.get_current_token_cache().size()
    9
    >>> player_a.action_take_two_tokens(Token("red"), Token("black")) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    Exception...
    >>> player_a.action_take_two_tokens(Token("yellow"), Token("yellow")) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    Exception...

    >>> player_b = Player()
    >>> player_b.get_name() #doctest: +ELLIPSIS
    'PLAYER_...'
    >>> len(player_b.get_name())
    15
    """
    name: str
    player_state_history: PlayerStateHistory
    
    def __init__(self, name: str=None) -> None: # if name=None, make a random one
        if name:
            self.name = name
        else:
            SUFFIX_LEN = 8
            suffix = "".join(random.choice(string.ascii_uppercase) for i in range(SUFFIX_LEN))
            self.name = "PLAYER_" + suffix
        self.player_state_history = PlayerStateHistory()

    def get_name(self) -> str:
        return self.name

    def get_player_state_history(self) -> PlayerStateHistory:
        return self.player_state_history

    def append_player_state(self, new_state) -> None:
        self.player_state_history.append(new_state)
        return

    def get_current_player_state(self) -> PlayerState:
        return self.player_state_history.get_current_state()
    
    def get_current_token_cache(self) -> PlayerTokenCache:
        return self.player_state_history.get_current_state().get_token_cache()

    def calc_score(self) -> int:
        return self.player_state_history.get_current_state().calc_score()

    def _action_take_tokens(self, token_add_list) -> None:
        """
        Complete the player action of taking tokens.  

        This function does *not* make sure that the game's gem cache actually
        has the desired gems, though it will make sure that the player will not
        exceed its maximum Cache size.
        """
        token_cache = self.get_current_token_cache()
        
        # if this player's TokenCache will overflow, raise Exception.
        if token_cache.count() + len(token_add_list) > PLAYER_TOKEN_CACHE_MAX:
            raise Exception(f"not enough space in player's token cache to add {len(token_add_list)} tokens")

        # Create updated state including the updated token cache
        for token_to_add in token_add_list:
            token_cache.add(token_to_add)
        new_state = clone_playerState_new_token_cache(
                self.player_state_history.get_current_state(),
                token_cache,
                )
        self.append_player_state(new_state)
        return
    
    def action_take_three_tokens(self, token_1, token_2, token_3) -> None:
        """
        Complete the player action of taking three tokens.

        This function makes sure that the tokens are all of different type, and that none are yellow.
        """
        if token_1.get_type() == token_2.get_type() or \
                token_1.get_type() == token_3.get_type() or \
                token_2.get_type() == token_3.get_type():
            raise Exception("action not allowed: chosen tokens must be all different")
        if token_1.is_joker() or \
                token_2.is_joker() or\
                token_3.is_joker():
            raise Exception("action not allowed: chosen tokens must not be jokers")

        return self._action_take_tokens([token_1, token_2, token_3])

    def action_take_two_tokens(self, token_1, token_2) -> None:
        """
        Complete the player action of taking two tokens.
        
        This function makes sure that the tokens are of the same type, and that none are yellow.
        """
        if token_1.get_type() != token_2.get_type():
            raise Exception("action not allowed: chosen tokens must be the same")
        if token_1.is_joker() or \
                token_2.is_joker():
            raise Exception("action not allowed: chosen tokens must not be jokers")
        return self._action_take_tokens([token_1, token_2])
    
    def action_reserve(self) -> None:
        pass

    def action_purchase(self) -> None:
        pass

