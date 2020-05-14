"""
game_setup.py - Initial values for setting up a Splendor game, i.e. decks, tokens, and nobles.
"""

from copy import deepcopy
from core import DevCard, DevCardDeck, GameTokenCache, Noble, NoblesInPlay
from game import GameState

DEV_CARD_DECK_1 = todo
    >>> dc0 = DevCard(level=1, t=DevCardType("black"), ppoints=2, cost={"blue": 2, "red": 1})
    >>> dc1 = DevCard(level=1, t=DevCardType("black"), ppoints=0, cost={"blue": 3})
    >>> dc2 = DevCard(level=1, t=DevCardType("blue"), ppoints=1, cost={"white": 1, "red": 1, "green": 3})
    >>> dc3 = DevCard(level=1, t=DevCardType("red"), ppoints=4, cost={"white": 1, "red": 1, "green": 3})
    >>> dc4 = DevCard(level=1, t=DevCardType("red"), ppoints=4, cost={"white": 1, "red": 1, "green": 3})
    >>> dc5 = DevCard(level=1, t=DevCardType("red"), ppoints=0, cost={"red": 1, "green": 3})
    >>> dc6 = DevCard(level=1, t=DevCardType("white"), ppoints=0, cost={"white": 1, "green": 3})
    >>> dev_card_deck_1 = DevCardDeck(1, [dc0, dc1, dc2, dc3, dc4, dc5, dc6])
DEV_CARD_DECK_2 = todo
DEV_CARD_DECK_3 = todo

NOBLES_ALL = (
        Noble(3, {'black': 3, 'blue': 3, 'white': 3}),
        Noble(3, {'black': 3, 'red': 3, 'white': 3}),
        Noble(3, {'black': 3, 'red': 3, 'green': 3}),
        Noble(3, {'blue': 3, 'red': 3, 'green': 3}),
        Noble(3, {'blue': 3, 'white': 3, 'green': 3}),
        Noble(3, {'black': 4, 'white': 4}),
        Noble(3, {'black': 4, 'red': 4}),
        Noble(3, {'blue': 4, 'white': 4}),
        Noble(3, {'red': 4, 'green': 4}),
        Noble(3, {'blue': 4, 'green': 4}),
        )

def get_dev_card_deck_shuffled(deck_no: int) -> DevCardDeck:
    if deck_no == 1:
        dev_card_deck = DEV_CARD_DECK_1.deepcopy()
    elif deck_no == 2:
        dev_card_deck = DEV_CARD_DECK_2.deepcopy()
    elif deck_no == 3:
        dev_card_deck = DEV_CARD_DECK_3.deepcopy()
    else:
        raise Exception(f"no such deck number: {deck_no}")

    dev_card_deck.shuffle()
    return dev_card_deck

def get_nobles_in_play_shuffled(players_count: int=2) -> NoblesInPlay:
    """
    """
    nobles_all = NOBLES_ALL.deepcopy()
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

def generate_initial_game_state(players_count: int=2) -> GameState:
    """
    Generate the initial state of the game, i.e. shuffle and deal out the decks, set up the tokens, etc.
    """
    dev_card_deck_1 = get_dev_card_deck_shuffled(1)
    dev_card_deck_2 = get_dev_card_deck_shuffled(2)
    dev_card_deck_3 = get_dev_card_deck_shuffled(3)
    nobles_in_play = get_nobles_in_play_shuffled(players_count)
    game_token_cache = GameTokenCache(players_count)
    game_state = GameState(dev_card_deck_1, dev_card_deck_2, dev_card_deck_3, nobles_in_play, game_token_cache)
    return game_state

