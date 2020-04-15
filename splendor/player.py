"""
"""

from core import DevCard, DevCardCache, DevCardReserve, DevCardType, PlayerTokenCache, Token, TokenType, WINNING_SCORE

from copy import deepcopy
from enum import Enum
import json
import logging
import random
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
    >>> dev_card_reserve.add(DevCard(level=1, t=DevCardType("red"), ppoints=4, cost={"white": 1, "red": 1, "green": 3}))
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

    def get_dev_card_cache(self) -> DevCardCache:
        return self.dev_card_cache

    def get_dev_card_reserve(self) -> DevCardReserve:
        return self.dev_card_reserve

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
    >>> dev_card_reserve.add(DevCard(level=1, t=DevCardType("red"), ppoints=4, cost={"white": 1, "red": 1, "green": 3}))
    >>> state_1 = PlayerState(token_cache, dev_card_cache, dev_card_reserve)

    >>> token_cache.add(Token(TokenType("blue")))
    >>> state_2 = PlayerState(token_cache, dev_card_cache, dev_card_reserve)
    
    >>> dev_card_reserve.add(DevCard(level=2, t=DevCardType("red"), ppoints=5, cost={"white": 3, "red": 4, "green": 3}))
    >>> state_3 = PlayerState(token_cache, dev_card_cache, dev_card_reserve)

    >>> psh = PlayerStateHistory()
    >>> psh.get_current_state_idx()
    0
    >>> psh.add(state_1)
    >>> psh.get_current_state_idx()
    1
    >>> psh.add(state_2)
    >>> psh.add(state_3)
    >>> psh.get_current_state_idx()
    3
    >>> psh.get_current_state().get_token_cache()
    todo

    >>> psh.revert(1)
    >>> psh.get_current_state_idx()
    1
    >>> psh.get_current_state().get_token_cache()
    todo

    """
    l: List[PlayerState]
    current_state_idx: int
    def __init__(self) -> None:
        pass

    def get_current_state(self) -> PlayerState:
        pass

    def revert(state_no: int) -> None: # revert history to state at idx; remove newer states
        pass

class Player:
    name: str
    player_state_history: PlayerStateHistory
    
    def __init__(self, name: str=None) -> None: # if name=None, make a random one
        pass

    def get_name(self) -> str:
        return self.name

    def get_player_state_history(self) -> PlayerStateHistory:
        return self.player_state_history

    def calc_score() -> int: # call PlayerState.calc_score()
        return self.player_state_history.get_current_state().calc_score()

    def action_take_three_gems(self) -> None: # analyze current state; if applicable, create new state
        pass

    def action_take_two_gems(self) -> None:
        pass

    def action_reserve(self) -> None:
        pass

    def action_purchase(self) -> None:
        pass

