"""
"""

from enum import Enum
from typing import List, Dict, Set

GEM_TYPE_STR_DICT = {
        "black": "onyx",
        "blue": "sapphire",
        "green": "emerald",
        "red": "ruby",
        "white": "diamond",
        "yellow": "gold",
        }

class GemType:
    """
    >>> a = GemType("black")
    >>> a.get_desc()
    'black'
    >>> a.get_desc_long()
    'black (onyx)'
    """

    t: str
    
    def __init__(
            self,
            t: str,
            ) -> None:
        self.t = t
    
    def __str__(self) -> str:
        return self.get_desc()
    
    def get_desc(self) -> str:
        return f"{self.t}"
    
    def get_desc_long(self) -> str:
        retstr = ""
        retstr += f"{self.t} "
        retstr += f"({GEM_TYPE_STR_DICT.get(self.t)})"
        return retstr


class DevCardType(GemType):
    """
    >>> a = DevCardType("black")
    >>> a.get_desc()
    'black'
    >>> a.get_desc_long()
    'black (onyx)'
    """
    pass

class DevCard:
    """
    >>> a = DevCard(level=1, t=DevCardType("black"), ppoints=2, cost={"blue": 2, "red": 1})
    >>> a.__str__()
    "l1p2black/{'blue': 2, 'red': 1}"
    """
    
    level: int # 1, 2, or 3
    t: DevCardType # also bonus
    ppoints: int
    cost: Dict[str, int] # str -> count
    def __init__(
            self,
            level: int, 
            t: DevCardType, 
            ppoints: int, 
            cost: Dict[str, int],
            ):
        self.level = level
        self.t = t
        self.ppoints = ppoints
        self.cost = cost

    #def is_purchasable(dev_card_cache: DevCardCache, token_player_cache: TokenPlayerCache) -> bool:
    #    pass

    def get_cost_str(self) -> str:
        return self.cost.__str__()

    def __str__(self) -> str:
        return f"l{self.level}p{self.ppoints}{self.t.__str__()}/{self.get_cost_str()}"

    #def get_image(self) -> bytes:
    #    pass

class DevCardCache:
    """
    >>> dc1 = DevCard(level=1, t=DevCardType("black"), ppoints=2, cost={"blue": 2, "red": 1})
    >>> dc2 = DevCard(level=2, t=DevCardType("black"), ppoints=0, cost={"blue": 3})
    >>> dc3 = DevCard(level=1, t=DevCardType("blue"), ppoints=1, cost={"white": 1, "red": 1, "green": 3})
    >>> a = DevCardCache()
    >>> a.__str__()
    ""
    >>> a.add(dc1)
    >>> a.__str__()
    "Dev cards on hand: {'black': 1}"
    >>> a.add(dc2)
    >>> a.add(dc3)
    >>> a.__str__()
    "Dev cards on hand: {'black': 2, 'blue': 1}"
    """
    d: Dict[DevCardType, Set[DevCard]]

    def __init__(self):
        self.d = {}

    def add(
            self,
            dev_card: DevCard,
            ) -> None:
        if not self.d.get(dev_card.t):
            self.d[dev_card.t] = set()
        self.d[dev_card.t].add(dev_card)
        return

#    remove(dev_card: DevCard) -> None # remove dev_card matching some DevCard in the Cache, or raise exception.  For undoing.                                                    
#    calc_ppoints() -> int # calc ppoints across this cache
#    calc_discount(dev_card_type: DevCardType) -> int # return current discount for DevCardType arg                                                                               
#    __str__() -> str
#    get_str() -> str # __str__()
#    get_image() -> bytes

#DEV_CARD_RESERVE_COUNT_MAX = 3

#class DevCardReserve:
#    s: set
#    __init__()
#    add(dev_card: DevCard)
#    remove(dev_card: DevCard) -> None # remove dev_card matching some DevCard in the Cache, or raise exception.  For undoing.
#    is_max() -> bool
#    can_action_reserve() -> bool
#    __str__() -> str
#    get_str() -> str # __str__()

#class DevCardDeck: # a set of all the dev cards of one level; for storing Game decks
#    level: int
#    l: list # indices 0..3 are the face-up cards; 4..n are the face-down, where 4 is the top-most
#    __init__(level: int, s: set) # load all of this level's cards
#    get_level() -> int
#    get_list() -> List
#    get_facing() -> List[4] # return cards at indices 0..3, which are the facing ones
#    shuffle() -> None
#    pop_by_idx(idx: int) -> DevCard # remove DevCard at index idx and return it, or raise exc if oob
#    pop_hidden_card() -> DevCard # remove DevCard at index 4, which is the top of the deck, and return it
#    is_empty()
#    count()
#    __str__() -> str
#    get_image() -> bytes

#class DevCardDecks:
#    l: list # indices 0..2 are decks #1..3

#DEV_CARD_DECKS = [set(), set(), set()] # to fill in with actual cards

#class Noble:
#    ppoints: int
#    cost: dict # GemType (or DevCardType?) -> count
#    image: bytes
#    __init__(ppoints: int, cost: dict, image=None: bytes)
#    __str__() -> str
#    get_image() -> bytes

#class NoblesInPlay:
#    s: Set[Noble]
#    __init__(players_count: int)
#    __str__() -> str

#NOBLES_DECK = set(...) # to fill in with actual noble cards

#class TokenType(GemType)

#class Token:
#    type: TokenType
#    desc: str
#    desc_long: str
#    image: bytes
#    __init__(token_type=TokenType.NONE: TokenType)
#    set_type_by_str(type_str)
#    __str__() # "sapphire (blue)"
#    get_image() -> bytes

#class TokenCache:
#    d: dict # TokenType -> count
#    __init__()
#    fill(players_count: int) -> None # for use by __init__()
#    empty() -> None
#    add(token_type: TokenType) -> None
#    remove(token_type: TokenType) -> None
#    count() -> int
#    count_type(token_type: TokenType) -> int
#    is_type_empty(token_type: TokenType) -> bool
#    can_action_take_three_gems(gem_types_set: Set(3)) -> bool
#    can_action_take_two_gems(gem_type: GemType) -> bool

#TOKEN_PLAYER_CACHE_MAX = 10

#class TokenPlayerCache(TokenCache)
#    __init__()
#    is_max() -> bool
#    is_over_max() -> bool

# players count -> tokens count per type
#TOKEN_COUNT_MAP = {2: 4, 3: 6, 4: 7}

#class TokenGameCache(TokenCache)
#    __init__(players_count: int)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
