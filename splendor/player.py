"""
player.py - Player and player-related classes.
"""

from copy import deepcopy
from splendor.core import (
    DevCard,
    DevCardCache,
    DevCardReserve,
    DevCardType,
    is_joker,
    PlayerTokenCache,
    PLAYER_TOKEN_CACHE_MAX,
    Token,
    TokenType,
)
from enum import Enum
import json
import random
import string
from typing import (
    Dict, 
    List, 
    Set,
)

import logging
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

    >>> b = a.copy()
    >>> a.calc_score() == b.calc_score()
    True

    """

    token_cache: PlayerTokenCache
    dev_card_cache: DevCardCache
    dev_card_reserve: DevCardReserve

    def __init__(
        self,
        token_cache: PlayerTokenCache,
        dev_card_cache: DevCardCache,
        dev_card_reserve: DevCardReserve,
    ) -> None:
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

    #def is_winning_state(self) -> bool:
    #    return self.calc_score() >= WINNING_SCORE

    def __str__(self) -> str:
        ret = ""
        ret += "Player state:\n"
        ret += self.token_cache + "\n"
        ret += self.dev_card_cache + "\n"
        ret += self.dev_card_reserve + "\n"
        return ret
    
    def __repr__(self) -> str:
        return f"<PlayerState>"


def clone_playerState_new_token_cache(
    old_player_state: PlayerState, new_token_cache: PlayerTokenCache
    ) -> PlayerState:
    """
    Create a new PlayerState from an existing one but using the updated
    TokenCache.
    """
    ret = old_player_state.copy()
    ret.set_token_cache(new_token_cache)
    return ret

def clone_playerState_new_dev_card_cache(
    old_player_state: PlayerState, new_dev_card_cache: DevCardCache,
    ) -> PlayerState:
    """
    Create a new PlayerState from an existing one but using the updated
    DevCardCache.
    """
    ret = old_player_state.copy()
    ret.set_dev_card_cache(new_dev_card_cache)
    return ret

def clone_playerState_new_dev_card_reserve(
    old_player_state: PlayerState, new_dev_card_reserve: DevCardReserve,
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
    new_token_cache: PlayerTokenCache = None,
    new_dev_card_cache: DevCardCache = None,
    new_dev_card_reserve: DevCardReserve = None,
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
    >>> player_a.action_take_three_tokens("black", "blue", "green")
    >>> player_a.get_current_token_cache().size()
    7
    
    >>> player_a.action_take_three_tokens("black", "black", "green") #doctest: +ELLIPSIS
    Traceback (most recent call last):
    Exception...
    >>> player_a.action_take_three_tokens("black", "yellow", "green") #doctest: +ELLIPSIS
    Traceback (most recent call last):
    Exception...

    >>> player_a.get_current_token_cache().size()
    7
    >>> player_a.action_take_two_tokens("red")
    >>> player_a.get_current_token_cache().size()
    9
    
    >>> player_a.action_take_two_tokens("yellow") #doctest: +ELLIPSIS
    Traceback (most recent call last):
    Exception...

    >>> player_a.get_current_dev_card_reserve().size()
    2
    >>> player_a.get_current_token_cache().size()
    9
    >>> player_a.action_reserve_dev_card(DevCard(level=2, t=DevCardType("blue"), ppoints=0, cost={"white": 1, "red": 1, "green": 2}))
    >>> player_a.get_current_dev_card_reserve().size()
    3
    >>> player_a.get_current_token_cache().size()
    10
    
    >>> player_a.action_reserve_dev_card(DevCard(level=1, t=DevCardType("red"), ppoints=2, cost={"white": 1, "red": 1, "green": 2})) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    Exception...
    
    >>> player_a.get_current_dev_card_cache().size()
    3
    >>> player_a.get_current_token_cache().size()
    10
    >>> player_a.action_purchase_dev_card(DevCard(level=1, t=DevCardType("blue"), ppoints=0, cost={"black": 2}))
    >>> player_a.get_current_dev_card_cache().size()
    4
    >>> player_a.get_current_token_cache().size()
    8
    
    >>> player_a.action_purchase_dev_card(DevCard(level=3, t=DevCardType("red"), ppoints=5, cost={"white": 4, "red": 4, "green": 4})) #doctest: +ELLIPSIS
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

    def __init__(self, name: str = None) -> None:  # if name=None, make a random one
        if name:
            self.name = name
        else:
            SUFFIX_LEN = 8
            suffix = "".join(
                random.choice(string.ascii_uppercase) for i in range(SUFFIX_LEN)
            )
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
        return self.get_current_player_state().get_token_cache()

    def get_current_dev_card_cache(self) -> DevCardCache:
        return self.get_current_player_state().get_dev_card_cache()
    
    def get_current_dev_card_cache_count(self) -> int:
        """
        Return the number of cards in the cache.  Used (at least) to determine the winner in the tiebreak scenario.
        """
        return self.get_current_dev_card_cache().count()

    def get_current_dev_card_reserve(self) -> DevCardReserve:
        return self.get_current_player_state().get_dev_card_reserve()

    def calc_score(self) -> int:
        return self.get_current_player_state().calc_score()

    def can_fit_tokens(
            self,
            number_of_tokens_to_add: int,
            ) -> bool:
        """
        Return true if adding number_of_tokens_to_add will not exceed the player's max.
        """
        if number_of_tokens_to_add < 0:
            raise Exception("number of tokens to add cannot be negative")
        return self.get_current_token_cache().count() + number_of_tokens_to_add <= PLAYER_TOKEN_CACHE_MAX

    def action_take_tokens(self, token_type_str_add_list) -> None:
        """
        Complete the player action of taking tokens.  

        This function does *not* make sure that the game's gem cache actually
        has the desired gems, though it will make sure that the player will not
        exceed its maximum Cache size.
        """
        token_cache = self.get_current_token_cache()

        # if this player's TokenCache will overflow, raise Exception.
        if not self.can_fit_tokens(len(token_type_str_add_list)):
            raise Exception(
                f"not enough space in player's token cache to add {len(token_type_str_add_list)} tokens"
            )

        # Create updated state including the updated token cache
        for token_type_str_to_add in token_type_str_add_list:
            token_cache.add(Token(token_type_str_to_add))
        new_state = clone_playerState_new_token_cache(
            self.get_current_player_state(), token_cache,
        )
        self.append_player_state(new_state)
        return

    def action_take_three_tokens(
            self, 
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

        return self.action_take_tokens([token_type_str_1, token_type_str_2, token_type_str_3])

    def action_take_two_tokens(
            self, 
            token_type_str: str, 
            ) -> None:
        """
        Complete the player action of taking two tokens.
        
        This function makes sure that none are yellow (jokers).
        """
        if is_joker(token_type_str):
            raise Exception("action not allowed: chosen tokens must not be jokers")
        return self.action_take_tokens([token_type_str, token_type_str])

    def action_reserve_dev_card(self, dev_card_to_add: DevCard) -> None:
        """
        Complete the player action of reserving a development card.

        This functions makes sure that the player has ample room is his/her caches to fit the card and yellow token.
        """
        # if this player's DevCardReserve will overflow, raise Exception.
        dev_card_reserve = self.get_current_dev_card_reserve()
        if dev_card_reserve.is_max():
            raise Exception(
                f"not enough space in player's dev card reserve to add a card"
            )

        # if this player's token cache will overflow, raise an exception.
        # TODO: handle this better.
        token_cache = self.get_current_token_cache()
        if token_cache.count_until_max() < 1:
            raise Exception(f"not enough space in this player's token cache to add a token")

        # Create updated state including the updated token cache
        dev_card_reserve.add(dev_card_to_add)
        token_cache.add(Token("yellow"))
        new_state = clone_playerState(
            self.get_current_player_state(), 
            new_dev_card_reserve=dev_card_reserve,
            new_token_cache=token_cache,
        )
        self.append_player_state(new_state)
        return

    def action_purchase_dev_card(self, dev_card_to_add) -> None:
        """
        Complete the player action to purchase a development card, adding it to the player's cache.
        
        This function makes sure that the player has the funds (tokens) available to purchase the card, removes them if so, or raises an Exception if not.
        """
        dev_card_cache = self.get_current_dev_card_cache()
        token_cache = self.get_current_token_cache()

        if not token_cache.can_purchase_dev_card(dev_card_to_add):
            raise Exception(f"cannot purchase dev card: insufficient tokens")

        # Create updated state including the updated token cache and dev card cache
        dev_card_cache.add(dev_card_to_add)
        token_cache.purchase_dev_card(dev_card_to_add)
        new_state = clone_playerState(
            self.get_current_player_state(),
            new_token_cache=token_cache,
            new_dev_card_cache=dev_card_cache,
        )
        self.append_player_state(new_state)
        return

        def __str__(self):
            ret = ""
            ret += f"Player: {self.get_name()}"
            ret += "\n"
            ret += "State: "
            ret += "\n"
            ret += f"{self.get_current_player_state()}"
            return ret