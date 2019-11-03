"""
"""

from enum import Enum
import json
import logging
import random
from typing import List, Dict, Set

logging.basicConfig(level=logging.INFO)

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
    Hashable class representing the type of a gem.

    >>> a = GemType("black")
    >>> a.get_desc()
    'black'
    >>> a.get_desc_long()
    'black (onyx)'
    
    >>> b = GemType("black")
    >>> c = GemType("blue")
    >>> a == b
    True
    >>> a == c
    False
    """

    t: str
    
    def __init__(
            self,
            t: str,
            ) -> None:
        self.t = t
   
    def __eq__(self, other) -> bool:
        return self.t == other.t

    def __hash__(self) -> int:
        return hash(self.t)

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
    Hashable class representing the type of a development card.  Inherits from GemType.

    >>> a = DevCardType("black")
    >>> a.get_desc()
    'black'
    >>> a.get_desc_long()
    'black (onyx)'
    
    >>> b = DevCardType("black")
    >>> c = DevCardType("blue")
    >>> a == b
    True
    >>> a == c
    False
    """
    pass

class DevCard:
    """
    >>> a = DevCard(level=1, t=DevCardType("black"), ppoints=2, cost={"blue": 2, "red": 1})
    >>> a.__str__()
    "l1p2black/{'blue': 2, 'red': 1}"

    >>> a.get_cost_str()
    "{'blue': 2, 'red': 1}"
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

    def __repr__(self) -> str:
        return self.__str__()

    #def get_image(self) -> bytes:
    #    pass

class DevCardCache:
    """
    A cache of DevCards, which have already been purchased by a player.

    >>> dc1 = DevCard(level=1, t=DevCardType("black"), ppoints=2, cost={"blue": 2, "red": 1})
    >>> dc2 = DevCard(level=2, t=DevCardType("black"), ppoints=0, cost={"blue": 3})
    >>> dc3 = DevCard(level=1, t=DevCardType("blue"), ppoints=1, cost={"white": 1, "red": 1, "green": 3})
    >>> a = DevCardCache()
    >>> a.__str__()
    'Dev cards on hand: {}'

    >>> a.add(dc1)
    >>> a.__str__()
    'Dev cards on hand: {"black": 1}'
    >>> a.add(dc2)
    >>> a.__str__()
    'Dev cards on hand: {"black": 2}'
    >>> a.add(dc3)
    >>> a.__str__()
    'Dev cards on hand: {"black": 2, "blue": 1}'

    >>> a.calc_ppoints()
    3

    >>> a.calc_discount(DevCardType("black"))
    2
    >>> a.calc_discount(DevCardType("blue"))
    1
    >>> a.calc_discount(DevCardType("red"))
    0

    >>> a.remove(dc1)
    >>> a.__str__()
    'Dev cards on hand: {"black": 1, "blue": 1}'
    >>> a.remove(dc1)
    Traceback (most recent call last):
    Exception: cannot remove card from DevCardCache: card not found
    >>> dc4 = DevCard(level=1, t=DevCardType("red"), ppoints=4, cost={"white": 1, "red": 1, "green": 3})
    >>> a.remove(dc4)
    Traceback (most recent call last):
    Exception: cannot remove card from DevCardCache: card not found

    """
    d: Dict[DevCardType, Set[DevCard]]

    def __init__(self):
        self.d = {}

    def add(
            self,
            dev_card: DevCard,
            ) -> None:
        if self.d.get(dev_card.t) is None:
            logging.debug("creating new key within self.d")
            self.d[dev_card.t] = set()
        logging.debug("adding card to self.d")
        self.d[dev_card.t].add(dev_card)
        return

    def remove(self, dev_card: DevCard) -> None:
        """
        Remove dev_card matching some DevCard in the Cache, or raise exception.  For undoing.
        """
        if dev_card.t not in self.d.keys():
            raise Exception("cannot remove card from DevCardCache: card not found")
        try:
            self.d.get(dev_card.t).remove(dev_card)
        except KeyError:
            raise Exception("cannot remove card from DevCardCache: card not found")
        except Exception as e:
            raise Exception(f"cannot remove card from DevCardCache: {e}")
        return

    def calc_ppoints(self) -> int:
        """
        Calculate ppoints across this cache
        """
        ret = 0
        for key in self.d.keys():
            for dc in self.d.get(key):
                ret += dc.ppoints
        return ret

    def calc_discount(self, dev_card_type: DevCardType) -> int:
        """
        Return current discount for DevCardType arg
        """
        if self.d.get(dev_card_type) is not None:
            return len(self.d.get(dev_card_type))
        else:
            return 0

    def __str__(self) -> str:
        ret = ""
        ret += "Dev cards on hand: "
        ret_dict = {}
        for key in self.d:
            ret_dict[key.__str__()] = len(self.d.get(key))
        ret += json.dumps(ret_dict, sort_keys=True)
        return ret

    def __repr__(self) -> str:
        ret_list = []
        for t in self.d:
            ret_list.append(self.d.get(t).__repr__() + "\n")
        return "\n".join(ret_list)

#    get_image() -> bytes

DEV_CARD_RESERVE_COUNT_MAX = 3

class DevCardReserve:
    """
    The reserve of development cards held by a player.
    
    >>> dc1 = DevCard(level=1, t=DevCardType("black"), ppoints=2, cost={"blue": 2, "red": 1})
    >>> dc2 = DevCard(level=2, t=DevCardType("black"), ppoints=0, cost={"blue": 3})
    >>> dc3 = DevCard(level=1, t=DevCardType("blue"), ppoints=1, cost={"white": 1, "red": 1, "green": 3})
    >>> dc4 = DevCard(level=1, t=DevCardType("red"), ppoints=4, cost={"white": 1, "red": 1, "green": 3})

    >>> a = DevCardReserve()
    >>> a.add(dc1)
    >>> a.count()
    1
    >>> a.__str__()
    "Dev cards in reserve (1):\\nl1p2black/{'blue': 2, 'red': 1}"
    >>> a.add(dc2)
    >>> a.count()
    2
    >>> a.is_max()
    False
    >>> a.can_action_reserve()
    True

    >>> a.add(dc3)
    >>> a.count()
    3
    >>> a.is_max()
    True
    >>> a.can_action_reserve()
    False

    >>> a.add(dc4)
    Traceback (most recent call last):
    Exception: cannot add card to DevCardReserve: at max
    >>> a.count()
    3

    >>> a.remove(dc3)
    >>> a.count()
    2
    >>> a.remove(dc4)
    Traceback (most recent call last):
    Exception: cannot remove card from DevCardReserve: not found
    >>> a.count()
    2
    """

    s: set

    def __init__(self, s: Set[DevCard] = set()) -> None:
        self.s = s

    def add(self, dev_card: DevCard) -> None:
        if self.is_max():
            raise Exception("cannot add card to DevCardReserve: at max")
        self.s.add(dev_card)
        return

    def remove(self, dev_card: DevCard) -> None:
        """
        Remove dev_card matching some DevCard in the Cache, or raise exception.  For undoing.
        """
        try:
            self.s.remove(dev_card)
        except KeyError:
            raise Exception("cannot remove card from DevCardReserve: not found")
        return

    def count(self):
        return len(self.s)

    def is_max(self) -> bool:
        return len(self.s) >= DEV_CARD_RESERVE_COUNT_MAX

    def can_action_reserve(self) -> bool:
        return not self.is_max()

    def __str__(self) -> str:
        ret_str = ""
        ret_str += "Dev cards in reserve "
        ret_str += "(" + str(len(self.s)) + "):\n"

        ret_list = []
        for entry in self.s:
            ret_list.append(entry.__str__())
        ret_str += "\n".join(ret_list)

        return ret_str

UPFACING_CARDS_LEN = 4

class DevCardDeck: 
    """
    A list of all the dev cards of one level, representing one of the three game decks.

    >>> dc0 = DevCard(level=1, t=DevCardType("black"), ppoints=2, cost={"blue": 2, "red": 1})
    >>> dc1 = DevCard(level=1, t=DevCardType("black"), ppoints=0, cost={"blue": 3})
    >>> dc2 = DevCard(level=1, t=DevCardType("blue"), ppoints=1, cost={"white": 1, "red": 1, "green": 3})
    >>> dc3 = DevCard(level=1, t=DevCardType("red"), ppoints=4, cost={"white": 1, "red": 1, "green": 3})
    >>> dc4 = DevCard(level=1, t=DevCardType("red"), ppoints=4, cost={"white": 1, "red": 1, "green": 3})
    >>> dc5 = DevCard(level=1, t=DevCardType("red"), ppoints=0, cost={"red": 1, "green": 3})
    >>> dc6 = DevCard(level=1, t=DevCardType("white"), ppoints=0, cost={"white": 1, "green": 3})

    >>> a = DevCardDeck(1, [dc0, dc1, dc2, dc3, dc4, dc5, dc6])
    >>> a.get_level()
    1
    >>> len(a.get_list())
    7
    >>> a.count()
    7
    >>> a.get_facing() == [dc0, dc1, dc2, dc3]
    True
    >>> a.is_empty()
    False
    >>> a.is_hidden_empty()
    False

    >>> a.pop_by_idx(2) == dc2
    True
    >>> a.count()
    6
    >>> a.get_facing() == [dc0, dc1, dc3, dc4]
    True

    >>> a.pop_hidden_card() == dc5
    True
    >>> a.count()
    5
    >>> a.is_hidden_empty()
    False
    >>> a.get_facing() == [dc0, dc1, dc3, dc4]
    True

    >>> a.pop_hidden_card() == dc6
    True
    >>> a.is_hidden_empty()
    True
    >>> a.is_empty()
    False
    """

    level: int
    l: list # indices 0..3 are the face-up cards; 4..n are the face-down, where 4 is the top-most
    def __init__(self, level: int, l: List[DevCard] = None) -> None:
        """
        Load all of this level's cards
        """
        self.level = level
        self.l = l

    def get_level(self) -> int:
        return self.level

    def get_list(self) -> List[DevCard]:
        return self.l

    def get_facing(self) -> List[DevCard]:
        """
        Return cards at indices 0..3, which are the facing ones, as a List
        """
        if len(self.l) < UPFACING_CARDS_LEN:
            raise Exception("not enough cards remain to get facing ones")
        return self.l[0:UPFACING_CARDS_LEN]

    def shuffle(self) -> None:
        random.shuffle(self.l)
        return

    def pop_by_idx(self, idx: int) -> DevCard:
        """
        Remove DevCard at index idx and return it, or raise exc if oob
        """
        try:
            return self.l.pop(idx)
        except IndexError:
            raise

    def pop_hidden_card(self) -> DevCard:
        """
        Remove DevCard at index 4, which is the top of the deck, and return it
        """
        if len(self.l) < UPFACING_CARDS_LEN + 1:
            raise Exception("not enough cards remain to get hidden one")
        return self.l.pop(UPFACING_CARDS_LEN)

    def is_hidden_empty(self) -> bool:
        if len(self.l) < UPFACING_CARDS_LEN + 1:
            return True
        return False

    def is_empty(self) -> bool:
        if len(self.l) <= 0:
            return True
        return False

    def count(self) -> int:
        return len(self.l)

    def __str__(self) -> str:
        ret_str = ""
        ret_str += f"Dev cards in deck "
        ret_str += f"(level {self.level}, count {len(self.l)}):\n"

        ret_list = []
        for card in self.l:
            ret_list.append(card.__str__())
        ret_str += "\n".join(ret_list)

        return ret_str

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
