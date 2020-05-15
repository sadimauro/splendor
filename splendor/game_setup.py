"""
game_setup.py - Initial values for setting up a Splendor game, i.e. decks, tokens, and nobles.
"""

from copy import deepcopy
from core import DevCard, DevCardDeck, DevCardType, GameTokenCache, Noble, NoblesInPlay
import random

import logging
logging.basicConfig(level=logging.INFO)

GAME_INTRO = (
        """In Splendor, you take on the role of a rich merchant during the Renaissance.
        You will use your resources to acquire mines, transportation methods, and artisans
        who will allow you to turn raw gems into beautiful jewels.

        During the game, the players take gem and gold tokens. With these tokens, they purchase development cards,
        which are worth prestige points and/or bonuses. These bonuses allow players to purchase subsequent
        development cards for a lesser cost. When a player has enough bonuses, they immediately receive a visit
        from a noble (which is also worth prestige points).

        As soon as a player reaches 15 prestige points, the current turn ends and the player
        with the most prestige points is declared the winner."""
        )

# This object represents the actual level-1 Splendor game deck.
DEV_CARD_DECK_1 = DevCardDeck(1, [
        DevCard(level=1, t=DevCardType("black"), ppoints=0, cost={"green": 1, "red": 3, "black": 1}),
        DevCard(level=1, t=DevCardType("black"), ppoints=0, cost={"green": 2, "red": 1}),
        DevCard(level=1, t=DevCardType("black"), ppoints=0, cost={"green": 3}),
        DevCard(level=1, t=DevCardType("black"), ppoints=0, cost={"white": 1, "blue": 1, "green": 1, "red": 1}),
        DevCard(level=1, t=DevCardType("black"), ppoints=0, cost={"white": 1, "blue": 2, "green": 1, "red": 1}),
        DevCard(level=1, t=DevCardType("black"), ppoints=0, cost={"white": 2, "blue": 2, "red": 1}),
        DevCard(level=1, t=DevCardType("black"), ppoints=0, cost={"white": 2, "green": 2}),
        DevCard(level=1, t=DevCardType("black"), ppoints=1, cost={"blue": 4}),
        DevCard(level=1, t=DevCardType("blue"), ppoints=0, cost={"black": 3}),
        DevCard(level=1, t=DevCardType("blue"), ppoints=0, cost={"blue": 1, "green": 3, "red": 1}),
        DevCard(level=1, t=DevCardType("blue"), ppoints=0, cost={"green": 2, "black": 2}),
        DevCard(level=1, t=DevCardType("blue"), ppoints=0, cost={"white": 1, "black": 2}),
        DevCard(level=1, t=DevCardType("blue"), ppoints=0, cost={"white": 1, "green": 1, "red": 1, "black": 1}),
        DevCard(level=1, t=DevCardType("blue"), ppoints=0, cost={"white": 1, "green": 1, "red": 2, "black": 1}),
        DevCard(level=1, t=DevCardType("blue"), ppoints=0, cost={"white": 1, "green": 2, "red": 2}),
        DevCard(level=1, t=DevCardType("blue"), ppoints=1, cost={"red": 4}),
        DevCard(level=1, t=DevCardType("green"), ppoints=0, cost={"blue": 1, "red": 2, "black": 2}),
        DevCard(level=1, t=DevCardType("green"), ppoints=0, cost={"blue": 2, "red": 2}),
        DevCard(level=1, t=DevCardType("green"), ppoints=0, cost={"red": 3}),
        DevCard(level=1, t=DevCardType("green"), ppoints=0, cost={"white": 1, "blue": 1, "red": 1, "black": 1}),
        DevCard(level=1, t=DevCardType("green"), ppoints=0, cost={"white": 1, "blue": 1, "red": 1, "black": 2}),
        DevCard(level=1, t=DevCardType("green"), ppoints=0, cost={"white": 1, "blue": 3, "green": 1}),
        DevCard(level=1, t=DevCardType("green"), ppoints=0, cost={"white": 2, "blue": 1}),
        DevCard(level=1, t=DevCardType("green"), ppoints=1, cost={"black": 4}),
        DevCard(level=1, t=DevCardType("red"), ppoints=0, cost={"blue": 2, "green": 1}),
        DevCard(level=1, t=DevCardType("red"), ppoints=0, cost={"white": 1, "blue": 1, "green": 1, "black": 1}),
        DevCard(level=1, t=DevCardType("red"), ppoints=0, cost={"white": 1, "red": 1, "black": 3}),
        DevCard(level=1, t=DevCardType("red"), ppoints=0, cost={"white": 2, "blue": 1, "green": 1, "black": 1}),
        DevCard(level=1, t=DevCardType("red"), ppoints=0, cost={"white": 2, "green": 1, "black": 2}),
        DevCard(level=1, t=DevCardType("red"), ppoints=0, cost={"white": 2, "red": 2}),
        DevCard(level=1, t=DevCardType("red"), ppoints=0, cost={"white": 3}),
        DevCard(level=1, t=DevCardType("red"), ppoints=1, cost={"white": 4}),
        DevCard(level=1, t=DevCardType("white"), ppoints=0, cost={"blue": 1, "green": 1, "red": 1, "black": 1}),
        DevCard(level=1, t=DevCardType("white"), ppoints=0, cost={"blue": 1, "green": 2, "red": 1, "black": 1}),
        DevCard(level=1, t=DevCardType("white"), ppoints=0, cost={"blue": 2, "black": 2}),
        DevCard(level=1, t=DevCardType("white"), ppoints=0, cost={"blue": 2, "green": 2, "black": 1}),
        DevCard(level=1, t=DevCardType("white"), ppoints=0, cost={"blue": 3}),
        DevCard(level=1, t=DevCardType("white"), ppoints=0, cost={"red": 2, "black": 1}),
        DevCard(level=1, t=DevCardType("white"), ppoints=0, cost={"white": 3, "blue": 1, "black": 1}),
        DevCard(level=1, t=DevCardType("white"), ppoints=1, cost={"green": 4}),
        ])

# This object represents the actual level-2 Splendor game deck.
DEV_CARD_DECK_2 = DevCardDeck(2, [
        DevCard(level=2, t=DevCardType("black"), ppoints=1, cost={"white": 3, "blue": 2, "green": 2}),
        DevCard(level=2, t=DevCardType("black"), ppoints=1, cost={"white": 3, "green": 3, "black": 2}),
        DevCard(level=2, t=DevCardType("black"), ppoints=2, cost={"blue": 1, "green": 4, "red": 2}),
        DevCard(level=2, t=DevCardType("black"), ppoints=2, cost={"green": 5, "red": 3}),
        DevCard(level=2, t=DevCardType("black"), ppoints=2, cost={"white": 5}),
        DevCard(level=2, t=DevCardType("black"), ppoints=3, cost={"black": 6}),
        DevCard(level=2, t=DevCardType("blue"), ppoints=1, cost={"blue": 2, "green": 2, "red": 3}),
        DevCard(level=2, t=DevCardType("blue"), ppoints=1, cost={"blue": 2, "green": 3, "black": 3}),
        DevCard(level=2, t=DevCardType("blue"), ppoints=2, cost={"blue": 5}),
        DevCard(level=2, t=DevCardType("blue"), ppoints=2, cost={"white": 2, "red": 1, "black": 4}),
        DevCard(level=2, t=DevCardType("blue"), ppoints=2, cost={"white": 5, "blue": 3}),
        DevCard(level=2, t=DevCardType("blue"), ppoints=3, cost={"blue": 6}),
        DevCard(level=2, t=DevCardType("green"), ppoints=1, cost={"white": 2, "blue": 3, "black": 2}),
        DevCard(level=2, t=DevCardType("green"), ppoints=1, cost={"white": 3, "green": 2, "red": 3}),
        DevCard(level=2, t=DevCardType("green"), ppoints=2, cost={"blue": 5, "green": 3}),
        DevCard(level=2, t=DevCardType("green"), ppoints=2, cost={"green": 5}),
        DevCard(level=2, t=DevCardType("green"), ppoints=2, cost={"white": 4, "blue": 2, "black": 1}),
        DevCard(level=2, t=DevCardType("green"), ppoints=3, cost={"green": 6}),
        DevCard(level=2, t=DevCardType("red"), ppoints=1, cost={"blue": 3, "red": 2, "black": 3}),
        DevCard(level=2, t=DevCardType("red"), ppoints=1, cost={"white": 2, "red": 2, "black": 3}),
        DevCard(level=2, t=DevCardType("red"), ppoints=2, cost={"black": 5}),
        DevCard(level=2, t=DevCardType("red"), ppoints=2, cost={"white": 1, "blue": 4, "green": 2}),
        DevCard(level=2, t=DevCardType("red"), ppoints=2, cost={"white": 3, "black": 5}),
        DevCard(level=2, t=DevCardType("red"), ppoints=3, cost={"red": 6}),
        DevCard(level=2, t=DevCardType("white"), ppoints=1, cost={"green": 3, "red": 2, "black": 2}),
        DevCard(level=2, t=DevCardType("white"), ppoints=1, cost={"white": 2, "blue": 3, "red": 3}),
        DevCard(level=2, t=DevCardType("white"), ppoints=2, cost={"green": 1, "red": 4, "black": 2}),
        DevCard(level=2, t=DevCardType("white"), ppoints=2, cost={"red": 5}),
        DevCard(level=2, t=DevCardType("white"), ppoints=2, cost={"red": 5, "black": 3}),
        DevCard(level=2, t=DevCardType("white"), ppoints=3, cost={"white": 6}),
        ])

# This object represents the actual level-3 Splendor game deck.
DEV_CARD_DECK_3 = DevCardDeck(3, [
        DevCard(level=3, t=DevCardType("black"), ppoints=3, cost={"white": 3, "blue": 3, "green": 5, "red": 3}),
        DevCard(level=3, t=DevCardType("black"), ppoints=4, cost={"green": 3, "red": 6, "black": 3}),
        DevCard(level=3, t=DevCardType("black"), ppoints=4, cost={"red": 7}),
        DevCard(level=3, t=DevCardType("black"), ppoints=5, cost={"red": 7, "black": 3}),
        DevCard(level=3, t=DevCardType("blue"), ppoints=3, cost={"white": 3, "green": 3, "red": 3, "black": 5}),
        DevCard(level=3, t=DevCardType("blue"), ppoints=4, cost={"white": 6, "blue": 3, "black": 3}),
        DevCard(level=3, t=DevCardType("blue"), ppoints=4, cost={"white": 7}),
        DevCard(level=3, t=DevCardType("blue"), ppoints=5, cost={"white": 7, "blue": 3}),
        DevCard(level=3, t=DevCardType("green"), ppoints=3, cost={"white": 5, "blue": 3, "red": 3, "black": 3}),
        DevCard(level=3, t=DevCardType("green"), ppoints=4, cost={"blue": 7}),
        DevCard(level=3, t=DevCardType("green"), ppoints=4, cost={"white": 3, "blue": 6, "green": 3}),
        DevCard(level=3, t=DevCardType("green"), ppoints=5, cost={"blue": 7, "green": 3}),
        DevCard(level=3, t=DevCardType("red"), ppoints=3, cost={"white": 3, "blue": 5, "green": 3, "black": 3}),
        DevCard(level=3, t=DevCardType("red"), ppoints=4, cost={"blue": 3, "green": 6, "red": 3}),
        DevCard(level=3, t=DevCardType("red"), ppoints=4, cost={"green": 7}),
        DevCard(level=3, t=DevCardType("red"), ppoints=5, cost={"green": 7, "red": 3}),
        DevCard(level=3, t=DevCardType("white"), ppoints=3, cost={"blue": 3, "green": 3, "red": 5, "black": 3}),
        DevCard(level=3, t=DevCardType("white"), ppoints=4, cost={"black": 7}),
        DevCard(level=3, t=DevCardType("white"), ppoints=4, cost={"white": 3, "red": 3, "black": 6}),
        DevCard(level=3, t=DevCardType("white"), ppoints=5, cost={"white": 3, "black": 7}),
        ])

# This object represents the actual Splendor game nobles.
NOBLES_ALL_LIST = [
        Noble(3, {'black': 3, 'blue': 3, 'white': 3}),
        Noble(3, {'black': 3, 'red': 3, 'green': 3}),
        Noble(3, {'black': 3, 'red': 3, 'white': 3}),
        Noble(3, {'black': 4, 'red': 4}),
        Noble(3, {'black': 4, 'white': 4}),
        Noble(3, {'blue': 3, 'red': 3, 'green': 3}),
        Noble(3, {'blue': 3, 'white': 3, 'green': 3}),
        Noble(3, {'blue': 4, 'green': 4}),
        Noble(3, {'blue': 4, 'white': 4}),
        Noble(3, {'red': 4, 'green': 4}),
        ]

def create_dev_card_deck_shuffled(deck_no: int) -> DevCardDeck:
    """
    Create a dev card deck of the specified level, by copying the actual deck and shuffling it.
    """
    if deck_no == 1:
        dev_card_deck = deepcopy(DEV_CARD_DECK_1)
    elif deck_no == 2:
        dev_card_deck = deepcopy(DEV_CARD_DECK_2)
    elif deck_no == 3:
        dev_card_deck = deepcopy(DEV_CARD_DECK_3)
    else:
        raise Exception(f"no such deck number: {deck_no}")

    dev_card_deck.shuffle()
    return dev_card_deck

def create_nobles_in_play_shuffled(players_count: int) -> NoblesInPlay:
    """
    Shuffle the set of nobles and select some based on the number of players.
    """
    nobles_all = deepcopy(NOBLES_ALL_LIST)
    if players_count == 2:
        nobles_count = 3
    elif players_count == 3:
        nobles_count = 4
    elif players_count == 4:
        nobles_count = 5
    else:
        raise Exception(f"unexpected number of players: {players_count}")
    random.shuffle(nobles_all)
    return NoblesInPlay(set(nobles_all[:nobles_count]))

