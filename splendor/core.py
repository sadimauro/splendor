"""
core.py - Core splendor classes/functions.  Used heavily by the other splendor modules.
"""

from enum import Enum
import json
import logging
import random
from typing import List, Dict, Set

logging.basicConfig(level=logging.INFO)

GEM_TYPE_COMMON_STR_DICT = {
    "black": "onyx",
    "blue": "sapphire",
    "green": "emerald",
    "red": "ruby",
    "white": "diamond",
}

GEM_TYPE_ALL_STR_DICT = {
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
    >>> a.is_joker()
    False
    
    >>> b = GemType("black")
    >>> c = GemType("yellow")
    >>> a == b
    True
    >>> a == c
    False
    >>> c.is_joker()
    True
    """

    t: str

    def __init__(self, t: str,) -> None:
        self.t = t

    def __eq__(self, other) -> bool:
        return self.t == other.t

    def __hash__(self) -> int:
        return hash(self.t)

    def __str__(self) -> str:
        return self.get_desc()

    def get_type(self) -> str:
        return self.get_desc()

    def get_desc(self) -> str:
        return f"{self.t}"

    def get_desc_long(self) -> str:
        retstr = ""
        retstr += f"{self.t} "
        retstr += f"({GEM_TYPE_ALL_STR_DICT.get(self.t)})"
        return retstr

    def is_joker(self) -> bool:
        return self.get_type() == "yellow"


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
    A particular instance of a development card.  Includes level (1, 2, or 3), type, points (>= 0), and cost.

    >>> a = DevCard(level=1, t=DevCardType("black"), ppoints=2, cost={"blue": 2, "red": 1})
    >>> a.__str__()
    "l1p2black/{'blue': 2, 'red': 1}"

    >>> a.get_cost_str()
    "{'blue': 2, 'red': 1}"
    """

    level: int  # 1, 2, or 3
    t: DevCardType  # also bonus
    ppoints: int
    cost: Dict[str, int]  # str -> count

    def __init__(
        self, level: int, t: DevCardType, ppoints: int, cost: Dict[str, int],
    ):
        self.level = level
        self.t = t
        self.ppoints = ppoints
        self.cost = cost

    # def is_purchasable(dev_card_cache: DevCardCache, token_player_cache: TokenPlayerCache) -> bool:
    #    pass

    def get_cost_dict(self) -> Dict[str, int]:
        return self.cost

    def get_cost_str(self) -> str:
        return self.cost.__str__()

    def __str__(self) -> str:
        return f"l{self.level}p{self.ppoints}{self.t.__str__()}/{self.get_cost_str()}"

    def __repr__(self) -> str:
        return self.__str__()

    # def get_image(self) -> bytes:
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

    def add(self, dev_card: DevCard,) -> None:
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

    def count(self) -> int:
        """
        Return the number of dev cards in the cache.
        """
        total_count = 0
        for typ in self.d.keys():
            total_count += len(self.d[typ])
        return total_count

    def size(self) -> int:
        """
        Same as count().
        """
        return self.count()

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
    The reserve of development cards held by a player, which have yet to be purchased by the player.
    
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

    s: Set[DevCard]

    def __init__(self, s: Set[DevCard] = None) -> None:
        if s is None:
            s = set()
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

    def count(self) -> int:
        return len(self.s)

    def size(self) -> int:
        """
        Same as count().
        """
        return self.count()

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
    l: list  # indices 0..3 are the face-up cards; 4..n are the face-down, where 4 is the top-most

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

# class DevCardDecks:
#    l: list # indices 0..2 are decks #1..3

# DEV_CARD_DECKS = [set(), set(), set()] # to fill in with actual cards


class Noble:
    """
    A Noble.

    >>> a = Noble(3, {'black': 4, 'white': 4})
    >>> a.get_ppoints()
    3
    >>> a.get_cost() == {'black': 4, 'white': 4}
    True
    """

    ppoints: int
    cost: Dict[DevCardType, int]
    image: bytes

    def __init__(self, ppoints: int, cost: Dict[DevCardType, int], image: bytes = None):
        self.ppoints = ppoints
        self.cost = cost
        self.image = image

    def get_ppoints(self) -> int:
        return self.ppoints

    def get_cost(self) -> Dict[DevCardType, int]:
        return self.cost

    def get_cost_str(self) -> str:
        return self.cost.__str__()

    def __str__(self) -> str:
        return f"p{self.ppoints}/{self.get_cost_str()}"


#    get_image() -> bytes


class NoblesInPlay:
    """ 
    The set of face-up Nobles.

    >>> n1 = Noble(3, {'black': 4, 'white': 4})
    >>> n2 = Noble(3, {'black': 3, 'white': 3, 'blue': 3})
    >>> n3 = Noble(3, {'black': 4, 'green': 4})
    >>> a = NoblesInPlay(set((n1, n2, n3)))
    >>> a.count()
    3
    """

    s: Set[Noble]

    def __init__(self, s: Set[Noble] = set()) -> None:
        self.s = s

    def count(self) -> int:
        return len(self.s)

    def __str__(self) -> str:
        retstr = ""
        retstr += f"Nobles in play ({self.count()}):"
        for noble in self.s:
            retstr += noble.__str__() + "\n"
        return retstr


# NOBLES_DECK = set(...) # to fill in with actual noble cards


class TokenType(GemType):
    """
    Hashable class representing the type of a token.  Inherits from GemType.

    >>> a = TokenType("black")
    >>> a.get_desc()
    'black'
    >>> a.get_desc_long()
    'black (onyx)'
    
    >>> b = TokenType("black")
    >>> c = TokenType("blue")
    >>> a == b
    True
    >>> a == c
    False
    """

    pass


class Token:
    """
    A token.

    >>> a = Token("black")
    >>> a.__str__()
    'black'
    """

    t: TokenType
    image: bytes

    def __init__(self, token_type_str: str, image: bytes = None) -> None:
        self.t = TokenType(token_type_str)
        self.image = image

    def get_type(self) -> TokenType:
        return self.t.get_type()

    def is_joker(self) -> bool:
        return self.t.is_joker()

    def __str__(self) -> str:
        return self.t.__str__()

        #    get_image() -> bytes


class TokenCache:
    """
    The set of Tokens currently held by a player (PlayerTokenCache) or game (GameTokenCache).

    >>> t0 = Token("black")
    >>> t1 = Token("black")
    >>> t2 = Token("yellow")
    >>> t3 = Token("blue")
    >>> a = TokenCache(set((t0, t1, t2, t3)))
    
    >>> a.count()
    4
    >>> a.count_type(TokenType("black"))
    2
    >>> a.count_type(TokenType("red"))
    0
    >>> a.is_type_empty(TokenType("black"))
    False
    >>> a.is_type_empty(TokenType("red"))
    True

    >>> t4 = Token("black")
    >>> t5 = Token("red")
    >>> a.add(t4)
    >>> a.add(t5)
    >>> a.count()
    6
    >>> a.count_type(TokenType("black"))
    3
    >>> a.is_type_empty(TokenType("red"))
    False

    >>> a.remove(TokenType("yellow"))
    >>> a.count()
    5
    >>> a.count_type(TokenType("yellow"))
    0
    >>> a.remove(TokenType("yellow")) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    Exception:...
    >>> a.count()
    5
    """

    d: Dict[TokenType, int]

    def __init__(self, s: Set[Token] = set()) -> None:
        self.d = {}
        for item in s:
            self.d[item.t] = self.d.setdefault(item.t, 0) + 1

    def empty(self) -> None:
        self.d = {}

    def add(self, token: Token) -> None:
        self.d[token.t] = self.d.setdefault(token.t, 0) + 1

    def remove(self, token_type: TokenType, how_many: int = 1) -> None:
        if self.d.get(token_type) and self.d.get(token_type) >= how_many:
            self.d[token_type] -= how_many
            return
        else:
            raise Exception(
                f"{how_many} of token type {token_type} not found in token cache"
            )

    def count(self) -> int:
        count = 0
        for key in self.d.keys():
            count += self.d[key]
        return count

    def size(self) -> int:
        """
        Same as count().
        """
        return self.count()

    def count_type(self, token_type: TokenType) -> int:
        count = self.d.get(token_type)
        if count:
            return count
        else:
            return 0

    def is_type_empty(self, token_type: TokenType) -> bool:
        if not self.d.get(token_type) or self.d.get(token_type) < 0:
            return True
        return False


PLAYER_TOKEN_CACHE_MAX = 10


class PlayerTokenCache(TokenCache):
    """
    The set of tokens currently held by a player.
    
    >>> a = PlayerTokenCache()
    >>> a.count()
    0
    >>> a.count_type(TokenType("black"))
    0

    >>> a.add(Token("black"))
    >>> a.add(Token("black"))
    >>> a.add(Token("black"))
    >>> a.add(Token("black"))
    >>> a.add(Token("black"))
    >>> a.add(Token("red"))
    >>> a.add(Token("red"))
    >>> a.add(Token("red"))
    >>> a.add(Token("blue"))
    >>> a.count()
    9
    >>> a.count_type(TokenType("black"))
    5
    >>> a.count_type(TokenType("red"))
    3
    >>> a.is_type_empty(TokenType("black"))
    False
    >>> a.is_type_empty(TokenType("white"))
    True
    >>> a.is_max()
    False
    >>> a.is_over_max()
    False

    >>> a.add(Token("red"))
    >>> a.count() == PLAYER_TOKEN_CACHE_MAX
    True
    >>> a.is_max()
    True
    >>> a.is_over_max()
    False
    >>> a.add(Token("red"))
    >>> a.count() == PLAYER_TOKEN_CACHE_MAX + 1
    True
    >>> a.is_max()
    False
    >>> a.is_over_max()
    True

    >>> a.remove(TokenType("red"))
    >>> a.count()
    10
    >>> a.count_type(TokenType("red"))
    4
    >>> a.remove(TokenType("yellow")) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    Exception:...
    >>> a.count()
    10
    """

    def is_max(self) -> bool:
        if self.count() == PLAYER_TOKEN_CACHE_MAX:
            return True
        return False

    def is_over_max(self) -> bool:
        if self.count() > PLAYER_TOKEN_CACHE_MAX:
            return True
        return False

    def can_purchase_dev_card(self, dev_card) -> bool:
        """
        Return True if dev_card can be purchased given the tokens in this token cache.
        
        TODO: how to handle jokers?
        """
        cost_dict = dev_card.get_cost_dict()
        for typ_str in cost_dict.keys():
            if cost_dict[typ_str] > self.count_type(TokenType(typ_str)):
                return False
        return True

    def purchase_dev_card(self, dev_card) -> None:
        """
        Remove tokens needed to purchase dev card.  Raise exception if there aren't enough tokens.
        
        TODO: how to handle jokers?
        """
        if not self.can_purchase_dev_card(dev_card):
            raise Exception(f"insufficient tokens to purchase dev card {dev_card}")
        cost_dict = dev_card.get_cost_dict()
        for typ_str in cost_dict.keys():
            self.remove(TokenType(typ_str), cost_dict[typ_str])
        return


# players count -> tokens count per type
TOKEN_COUNT_MAP = {2: 4, 3: 6, 4: 7}


class GameTokenCache(TokenCache):
    """
    The set of tokens available within a game.  The initial counts depend on the number of players.
    
    >>> a = GameTokenCache(players_count=2)
    >>> a.count()
    25
    >>> a.count_type(TokenType("black"))
    4
    >>> a.count_type(TokenType("yellow"))
    5

    >>> a.remove(TokenType("red"))
    >>> a.count_type(TokenType("red"))
    3
    >>> a.is_type_empty(TokenType("red"))
    False
    >>> a.remove(TokenType("red"))
    >>> a.remove(TokenType("red"))
    >>> a.remove(TokenType("red"))
    >>> a.count_type(TokenType("red"))
    0
    >>> a.is_type_empty(TokenType("red"))
    True
    >>> a.remove(TokenType("red")) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    Exception:...

    >>> a.add(Token("red"))
    >>> a.count_type(TokenType("red"))
    1
    """

    def __init__(self, players_count: int) -> None:
        self.d = {}
        self.fill(players_count)

    def fill(self, players_count: int) -> None:
        if players_count not in TOKEN_COUNT_MAP.keys():
            raise Exception("invalid players_count")
        for typ in GEM_TYPE_COMMON_STR_DICT.keys():
            self.d[TokenType(typ)] = TOKEN_COUNT_MAP[players_count]
        self.d[TokenType("yellow")] = 5

    # def can_action_take_three_tokens(token_types_set: Set[TokenType]) -> bool
    # def can_action_take_two_tokens(token_types_set: Set[TokenType]) -> bool


WINNING_SCORE = 15
