"""
core.py - Core splendor classes/functions.  Used heavily by the other splendor modules.
"""

from enum import Enum
import json
import random
from typing import List, Dict, Set, Tuple

import logging
logging.basicConfig(level=logging.INFO)

GEM_NAME_COMMON_STR_DICT = {
    "black": "onyx",
    "blue": "sapphire",
    "green": "emerald",
    "red": "ruby",
    "white": "diamond",
}

GEM_NAME_ALL_STR_DICT = {
    "black": "onyx",
    "blue": "sapphire",
    "green": "emerald",
    "red": "ruby",
    "white": "diamond",
    "yellow": "gold",
}

def is_joker(gem_str: str) -> bool:
    return gem_str == "yellow"

# class GemType:
#     """
#     Hashable class representing the type of a gem.

#     >>> gem_type_a = GemType("black")
#     >>> gem_type_a.get_desc()
#     'black'
#     >>> gem_type_a.get_desc_long()
#     'black (onyx)'
#     >>> gem_type_a.is_joker()
#     False
    
#     >>> gem_type_b = GemType("black")
#     >>> gem_type_c = GemType("yellow")
#     >>> gem_type_a == gem_type_b
#     True
#     >>> gem_type_a == gem_type_c
#     False
#     >>> gem_type_c.is_joker()
#     True
#     """

#     desc: str

#     def __init__(self, desc: str,) -> None:
#         self.desc = desc

#     def __eq__(self, other) -> bool:
#         return self.desc == other.desc

#     def __hash__(self) -> int:
#         return hash(self.desc)

#     def __str__(self) -> str:
#         return self.desc
    
#     def __repr__(self) -> str:
#         return f"<GemType: {self.desc}>"

#     def get_desc(self) -> str:
#         return self.__str__()

#     def get_desc_long(self) -> str:
#         retstr = ""
#         retstr += f"{self.desc} "
#         retstr += f"({GEM_TYPE_ALL_STR_DICT.get(self.desc)})"
#         return retstr

#     def is_joker(self) -> bool:
#         return self.get_desc() == "yellow"

class Gem:
    """
    Hashable class representing a gem.  Used by other classes.

    >>> gem_a = Gem("black")
    >>> gem_a.get_name()
    'black'
    >>> gem_a.get_name_long()
    'black (onyx)'
    >>> gem_a.is_joker()
    False
    
    >>> gem_b = Gem("black")
    >>> gem_c = Gem("yellow")
    >>> gem_a == gem_b
    True
    >>> gem_a == gem_c
    False
    >>> gem_c.is_joker()
    True
    """

    name: str

    def __init__(self, name: str,) -> None:
        self.name = name

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f"<Gem: {self.name}>"

    def get_name(self) -> str:
        return self.__str__()

    def get_name_long(self) -> str:
        retstr = ""
        retstr += f"{self.name} "
        retstr += f"({GEM_NAME_ALL_STR_DICT.get(self.name)})"
        return retstr

    def is_joker(self) -> bool:
        return self.get_name() == "yellow"

# class DevCardType(GemType):
#     """
#     Hashable class representing the type of a development card.  Inherits from GemType.

#     >>> dev_card_type_a = DevCardType("black")
#     >>> dev_card_type_a.get_desc()
#     'black'
#     >>> dev_card_type_a.get_desc_long()
#     'black (onyx)'
    
#     >>> dev_card_type_b = DevCardType("black")
#     >>> dev_card_type_c = DevCardType("blue")
#     >>> dev_card_type_a == dev_card_type_b
#     True
#     >>> dev_card_type_a == dev_card_type_c
#     False
#     """

#     def __repr__(self) -> str:
#         return f"<DevCardType: {self.desc}>"


class DevCard:
    """
    A particular instance of a development card.  Includes level (1, 2, or 3), gem, points (>= 0), and cost.

    >>> cost_dict = {"blue": 2, "red": 1}
    >>> dev_card = DevCard(level=1, gem=Gem("black"), ppoints=2, cost=cost_dict)

    >>> dev_card.get_level()
    1
    >>> dev_card.get_gem().__str__()
    'black'
    >>> dev_card.get_ppoints()
    2
    >>> dev_card.get_cost_dict() == cost_dict
    True

    >>> cost_dict_2 = {"blue": 2, "red": 1}
    >>> dev_card_2 = DevCard(level=1, gem=Gem("black"), ppoints=2, cost=cost_dict_2)
    >>> dev_card == dev_card_2
    True

    >>> cost_dict_3 = {"white": 2, "red": 2, "black": 1}
    >>> dev_card_3 = DevCard(level=2, gem=Gem("white"), ppoints=0, cost=cost_dict_3)
    >>> dev_card == dev_card_3
    False
    """

    level: int  # 1, 2, or 3
    gem: Gem  # also bonus
    ppoints: int
    cost: Dict[str, int]  # str -> count

    def __init__(
        self, 
        level: int, 
        gem: Gem, 
        ppoints: int, 
        cost: Dict[str, int],
        ):
        self.level = level
        self.gem = gem
        self.ppoints = ppoints
        self.cost = cost

    def get_level(self) -> int:
        return self.level

    def get_gem(self) -> Gem:
        return self.gem

    def get_ppoints(self) -> int:
        return self.ppoints

    def get_cost_dict(self) -> Dict[str, int]:
        return self.cost

    def get_cost_str(self) -> str:
        return self.cost.__str__()

    def __eq__(self, other) -> bool:
        return (
                self.level == other.level
                and self.gem == other.gem
                and self.ppoints == other.ppoints
                and self.cost == other.cost
                )             

    def __str__(self) -> str:
        return f"Development card: level {self.level}, ppoints {self.ppoints}, gem {self.gem.__str__()}, cost {self.get_cost_str()}"

    def __repr__(self) -> str:
        return f"<DevCard: l{self.level} p{self.ppoints} g{self.gem.__str__()} c{self.get_cost_str()}>"


class DevCardCache:
    """
    A cache of DevCards, which have already been purchased by a player.

    >>> dc1 = DevCard(level=1, gem=Gem("black"), ppoints=2, cost={"blue": 2, "red": 1})
    >>> dc2 = DevCard(level=2, gem=Gem("black"), ppoints=0, cost={"blue": 3})
    >>> dc3 = DevCard(level=1, gem=Gem("blue"), ppoints=1, cost={"white": 1, "red": 1, "green": 3})
    >>> dev_card_cache = DevCardCache()

    >>> dev_card_cache.add(dc1)
    >>> dev_card_cache.add(dc2)
    >>> dev_card_cache.add(dc3)

    >>> dev_card_cache.calc_ppoints()
    3
    >>> dev_card_cache.calc_discount(Gem("black"))
    2
    >>> dev_card_cache.calc_discount(Gem("blue"))   
    1
    >>> dev_card_cache.calc_discount(Gem("red"))
    0

    >>> dev_card_cache.remove(dc1)
    >>> dev_card_cache.remove(dc1) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    Exception:...
    >>> dc4 = DevCard(level=1, gem=Gem("red"), ppoints=4, cost={"white": 1, "red": 1, "green": 3})
    >>> dev_card_cache.remove(dc4) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    Exception:...
    """

    d: Dict[Gem, List[DevCard]]

    def __init__(self):
        self.d = {}

    def add(self, dev_card: DevCard,) -> None:
        dc_gem = dev_card.get_gem()
        if self.d.get(dc_gem) is None:
            logging.debug("creating new key within self.d")
            self.d[dc_gem] = list()
        logging.debug("adding card to self.d")
        self.d[dc_gem].append(dev_card)
        return

    def remove(self, dev_card: DevCard,) -> None:
        """
        Remove dev_card matching some DevCard in the Cache, or raise exception.  For undoing.
        """
        dc_gem = dev_card.get_type()
        if dc_gem not in self.d.keys():
            raise Exception("cannot remove card from DevCardCache: card not found")
        try:
            self.d.get(dc_gem).remove(dev_card)
        except KeyError:
            raise Exception("cannot remove card from DevCardCache: gem not found")
        except ValueError:
            raise Exception("cannot remove card from DevCardCache: card not found")
        except Exception as e:
            raise Exception(f"cannot remove card from DevCardCache: {e}")
        return

    def count(self) -> int:
        """
        Return the number of dev cards in the cache.
        """
        total_count = 0
        for gem in self.d.keys():
            total_count += len(self.d[gem])
        return total_count

    def calc_ppoints(self) -> int:
        """
        Calculate ppoints across this cache
        """
        ret = 0
        for gem in self.d.keys():
            for dc in self.d.get(gem):
                ret += dc.ppoints
        return ret

    def calc_discount(self, gem: Gem) -> int:
        """
        Return current discount for DevCardType arg
        """
        if self.d.get(gem) is not None:
            return len(self.d.get(gem))
        else:
            return 0

    def __str__(self) -> str:
        ret = ""
        ret += "Dev cards on hand: "
        ret_dict = {}
        for gem in self.d:
            ret_dict[gem.__str__()] = len(self.d.get(gem))
        ret += json.dumps(ret_dict, sort_keys=True)
        return ret

    def __repr__(self) -> str:
        ret = ""
        ret += f"<DevCardCache: ({self.count()})"
        if self.count() > 0:
            ret += ": "
            ret_list = []
            for gem in self.d:
                ret_list.append(self.d.get(gem).__repr__())
            ret += ",".join(ret_list)
        ret += ">"
        return ret


DEV_CARD_RESERVE_COUNT_MAX = 3

class DevCardReserve:
    """
    The reserve of development cards held by a player, which have yet to be purchased by the player.
    
    >>> dc1 = DevCard(level=1, gem=Gem("black"), ppoints=2, cost={"blue": 2, "red": 1})
    >>> dc2 = DevCard(level=2, gem=Gem("black"), ppoints=0, cost={"blue": 3})
    >>> dc3 = DevCard(level=1, gem=Gem("blue"), ppoints=1, cost={"white": 1, "red": 1, "green": 3})
    >>> dc4 = DevCard(level=1, gem=Gem("red"), ppoints=4, cost={"white": 1, "red": 1, "green": 3})

    >>> dev_card_reserve = DevCardReserve()
    >>> dev_card_reserve.add(dc1)
    >>> dev_card_reserve.count()
    1
    >>> dev_card_reserve.add(dc2)
    >>> dev_card_reserve.count()
    2
    >>> dev_card_reserve.is_max()
    False
    >>> dev_card_reserve.can_action_reserve()
    True

    >>> dev_card_reserve.add(dc3)
    >>> dev_card_reserve.count()
    3
    >>> dev_card_reserve.is_max()
    True
    >>> dev_card_reserve.can_action_reserve()
    False

    >>> dev_card_reserve.add(dc4)
    Traceback (most recent call last):
    Exception: cannot add card to DevCardReserve: at max
    >>> dev_card_reserve.count()
    3

    >>> dev_card_reserve.remove(dc3)
    >>> dev_card_reserve.count()
    2
    >>> dev_card_reserve.remove(dc4) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    Exception:...
    >>> dev_card_reserve.count()
    2
    """

    l: List[DevCard]

    def __init__(self, l: List[DevCard] = None) -> None:
        if l is None:
            l = list()
        self.l = l

    def add(self, dev_card: DevCard) -> None:
        if self.is_max():
            raise Exception("cannot add card to DevCardReserve: at max")
        self.l.append(dev_card)
        return

    def remove(self, dev_card: DevCard) -> None:
        """
        Remove dev_card matching some DevCard in the Cache, or raise exception.  For undoing.
        """
        try:
            self.l.remove(dev_card)
        except KeyError:
            raise Exception("cannot remove card from DevCardReserve: not found")
        except Exception as e:
            raise Exception(f"cannot remove card from DevCardReserve: {e}")

        return

    def count(self) -> int:
        return len(self.l)

    def is_max(self) -> bool:
        return len(self.l) >= DEV_CARD_RESERVE_COUNT_MAX

    def can_action_reserve(self) -> bool:
        return not self.is_max()

    def __str__(self) -> str:
        ret_str = ""
        ret_str += "Dev cards in reserve "
        ret_str += "(" + str(len(self.l)) + "):\n"

        ret_list = []
        for entry in self.l:
            ret_list.append(entry.__str__())
        ret_str += "\n".join(ret_list)

        return ret_str
    
    def __repr__(self) -> str:
        ret = ""
        ret += f"<DevCardReserve: ({self.count()})"
        if self.count() > 0:
            ret += ": "
            ret_list = []
            for t in self.l:
                ret_list.append(self.l.get(t).__repr__())
            ret += ",".join(ret_list)
        ret += ">"
        return ret


UPFACING_CARDS_LEN = 4

class DevCardDeck:
    """
    A list of all the dev cards of one level, representing one of the three game decks.

    Includes face-up and face-down cards.  Face-up cards are at lowest indices.

    >>> dc0 = DevCard(level=1, gem=Gem("black"), ppoints=2, cost={"blue": 2, "red": 1})
    >>> dc1 = DevCard(level=1, gem=Gem("black"), ppoints=0, cost={"blue": 3})
    >>> dc2 = DevCard(level=1, gem=Gem("blue"), ppoints=1, cost={"white": 1, "red": 1, "green": 3})
    >>> dc3 = DevCard(level=1, gem=Gem("red"), ppoints=4, cost={"white": 1, "red": 1, "green": 3})
    >>> dc4 = DevCard(level=1, gem=Gem("red"), ppoints=3, cost={"white": 1, "red": 1, "green": 3})
    >>> dc5 = DevCard(level=1, gem=Gem("red"), ppoints=0, cost={"red": 1, "green": 3})
    >>> dc6 = DevCard(level=1, gem=Gem("white"), ppoints=0, cost={"white": 1, "green": 3})
    >>> dev_cards_list = [dc0, dc1, dc2, dc3, dc4, dc5, dc6]
    >>> dev_card_deck = DevCardDeck(1, dev_cards_list.copy())
    >>> dev_card_deck.get_level()
    1
    >>> dev_card_deck.get_list() == dev_cards_list
    True
    >>> dev_card_deck.count()
    7
    >>> dev_card_deck.get_facing() == [dc0, dc1, dc2, dc3]
    True
    >>> dev_card_deck.count_facing()
    4
    >>> dev_card_deck.count_hidden()
    3
    >>> dev_card_deck.is_empty()
    False
    >>> dev_card_deck.is_hidden_empty()
    False

    >>> dev_card_deck.pop_by_idx(2) == dc2
    True
    >>> dev_card_deck.pop_hidden_card() == dc5
    True
    >>> dev_card_deck.count()
    5
    >>> dev_card_deck.get_facing() == [dc0, dc1, dc3, dc4]
    True
    >>> dev_card_deck.count_facing()
    4
    >>> dev_card_deck.is_hidden_empty()
    False
    >>> dev_card_deck.count_hidden()
    1

    >>> dev_card_deck.pop_by_idx(0) == dc0
    True
    >>> dev_card_deck.pop_by_idx(0) == dc1
    True
    >>> dev_card_deck.count()
    3
    >>> dev_card_deck.get_facing() == [dc3, dc4, dc6]
    True
    >>> dev_card_deck.count_facing()
    3
    >>> dev_card_deck.is_hidden_empty()
    True
    >>> dev_card_deck.count_hidden()
    0

    >>> dev_card_deck = DevCardDeck(1, dev_cards_list.copy())
    >>> dev_card_deck.shuffle()
    >>> dev_card_deck.count()
    7

    >>> dev_card_deck = DevCardDeck(1, dev_cards_list.copy())
    >>> dev_card_deck.find_card(dc0)
    0
    >>> dev_card_deck.find_card(dc4)
    4
    >>> dc7 = DevCard(level=2, gem=Gem("green"), ppoints=2, cost={"white": 4, "green": 3})
    >>> dev_card_deck.find_card(dc7)
    -1
    """
    # TODO: is there a good way to doctest shuffle()?

    level: int
    l: List[DevCard] # indices 0..3 are the face-up cards; 4..n are the face-down, where 4 is the top-most

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
        Return cards at indices 0..3 (if they exist), which are the facing ones, as a List
        """
        return self.l[0:min(self.count(), UPFACING_CARDS_LEN)]

    def count(self) -> int:
        return len(self.l)
            
    def count_facing(self) -> int:
        return min(self.count(), UPFACING_CARDS_LEN)
    
    def count_hidden(self) -> int:
        if self.count() <= UPFACING_CARDS_LEN:
            return 0
        return self.count() - UPFACING_CARDS_LEN

    def shuffle(self) -> None:
        random.shuffle(self.l)
        return

    def find_card(self, card_seeking: DevCard) -> int:
        """
        Find dev_card within this deck; return its index or -1 if not found.
        """
        for idx in range(self.count()): 
            if self.l[idx] == card_seeking:
                return idx
        return -1

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
        if self.count() < UPFACING_CARDS_LEN + 1:
            raise Exception("not enough cards remain to get hidden one")
        return self.l.pop(UPFACING_CARDS_LEN)

    def is_empty(self) -> bool:
        if self.count() <= 0:
            return True
        return False

    def is_hidden_empty(self) -> bool:
        if self.count() < UPFACING_CARDS_LEN + 1:
            return True
        return False

    def __str__(self) -> str:
        ret_str = ""
        ret_str += f"Development cards deck "
        ret_str += f"level {self.level}, total {self.count()}, hidden {self.count_hidden()}"
        ret_str += "\n"

        ret_list = []
        for card in self.get_facing():
            ret_list.append(card.__str__())
        ret_str += "\n".join(ret_list)

        return ret_str

    def __repr__(self) -> str:
        return f"<DevCardDeck: level {self.level}, total {self.count()}, hidden {self.count_hidden()}>"


class Noble:
    """
    A Noble.

    >>> cost_dict_1 = {Gem('black'): 4, Gem('white'): 4}
    >>> noble = Noble(3, cost_dict_1)
    >>> noble.get_ppoints()
    3
    >>> noble.get_cost() == cost_dict_1
    True
    >>> noble.get_image() == None
    True

    >>> noble_2 = Noble(3, cost_dict_1)
    >>> noble == noble_2
    True
    >>> noble_3 = Noble(4, cost_dict_1)
    >>> noble == noble_3
    False
    >>> cost_dict_2 = {Gem('black'): 3, Gem('white'): 3, Gem('red'): 3}
    >>> noble_4 = Noble(3, cost_dict_2)
    >>> noble == noble_4
    False
    """

    ppoints: int
    cost: Dict[Gem, int]
    image: bytes

    def __init__(self, ppoints: int, cost: Dict[Gem, int], image: bytes = None):
        self.ppoints = ppoints
        self.cost = cost
        self.image = image

    def get_ppoints(self) -> int:
        return self.ppoints

    def get_cost(self) -> Dict[Gem, int]:
        return self.cost

    def get_image(self) -> bytes:
        return self.image

    def __eq__(self, other) -> bool:
        return (
                self.ppoints == other.ppoints
                and self.cost == other.cost
                and self.image == other.image
                )

    def __hash__(self) -> int:
        return hash((self.ppoints, frozenset(self.cost.items()), self.image))

    def __str__(self) -> str:
        return f"Noble: {self.ppoints} ppoints, cost = {self.cost.__str__()}"
        
    def __repr__(self) -> str:
        return f"<Noble: points {self.ppoints}, cost {self.cost.__repr__()}>"
        

class NoblesInPlay:
    """ 
    The set of face-up Nobles.

    >>> cost_dict_1 = {Gem('black'): 4, Gem('white'): 4}
    >>> cost_dict_2 = {Gem('black'): 3, Gem('white'): 3, Gem('blue'): 3}
    >>> cost_dict_3 = {Gem('black'): 4, Gem('green'): 4}
    >>> n0 = Noble(3, cost_dict_1)
    >>> n1 = Noble(3, cost_dict_2)
    >>> n2 = Noble(3, cost_dict_3)
    >>> nobles_in_play = NoblesInPlay([n0, n1, n2])
    >>> nobles_in_play.count()
    3

    >>> nobles_in_play.find(n1)
    1
    >>> nobles_in_play.pop_by_idx(1) == n1
    True
    >>> nobles_in_play.count()
    2
    >>> nobles_in_play.find(n1)
    -1

    >>> cost_dict_4 = {Gem('black'): 4, Gem('red'): 4}
    >>> n3 = Noble(3, cost_dict_4)
    >>> nobles_in_play.find(n3)
    -1
    """

    l: List[Noble] # this can be a set, but well make it a list for ease of mutability.

    def __init__(self, l: List[Noble] = list()) -> None:
        self.l = l

    def count(self) -> int:
        return len(self.l)

    def find(self, noble_seeking: Noble) -> int:
        """
        Find noble_seeking within this list; return its index or -1 if not found.
        """
        for idx in range(self.count()): 
            if self.l[idx] == noble_seeking:
                return idx
        return -1

    def pop_by_idx(self, idx: int) -> Noble:
        """
        Remove Noble at index idx and return it, or raise exc if oob
        """
        try:
            return self.l.pop(idx)
        except IndexError:
            raise

    def __str__(self) -> str:
        retstr = ""
        retstr += f"Nobles in play ({self.count()}):\n"
        for noble in self.l:
            retstr += noble.__str__() + "\n"
        return retstr
    
    def __repr__(self) -> str:
        return f"<NoblesInPlay: {self.count()}>"


# class TokenType(GemType):
#     """
#     Hashable class representing the type of a token.  Inherits from GemType.

#     >>> token_type_a = TokenType("black")
#     >>> token_type_a.get_desc()
#     'black'
#     >>> token_type_a.get_desc_long()
#     'black (onyx)'
    
#     >>> token_type_b = TokenType("black")
#     >>> token_type_c = TokenType("blue")
#     >>> token_type_a == token_type_b
#     True
#     >>> token_type_a == token_type_c
#     False
#     """

#     def __repr__(self) -> str:
#         return f"<TokenType: {self.desc}>"


class Token:
    """
    A token.

    >>> token = Token("black")
    >>> token.get_gem_str()
    'black'
    >>> token.get_image() == None
    True
    >>> token.is_joker()
    False

    >>> token = Token("yellow")
    >>> token.get_gem_str()
    'yellow'
    >>> token.is_joker()
    True
    """

    gem: Gem
    image: bytes

    def __init__(self, gem_str: str, image: bytes=None) -> None:
        """
        Init a Token from a string describing the TokenType.
        """
        self.gem = Gem(gem_str)
        self.image = image

    def get_gem(self) -> Gem:
        return self.gem
    
    def get_gem_name(self) -> str:
        return self.gem.__str__()

    def get_image(self) -> bytes:
        return self.image

    def is_joker(self) -> bool:
        return self.gem.is_joker()

    def __str__(self) -> str:
        return self.gem.__str__()
    
    def __repr__(self) -> str:
        return f"<Token: {self.gem.__repr__()}, image {len(self.image)} bytes>"


class TokenCache:
    """
    The set of Tokens currently held by a player (PlayerTokenCache) or game (GameTokenCache).

    >>> t_black_2 = Token("black")
    >>> t_yellow = Token("yellow")
    >>> t_blue = Token("blue")
    >>> token_cache = TokenCache((t_black_1, t_black_2, t_yellow, t_blue))
    >>> token_cache.count()
    4
    >>> token_cache.count_token(t_black_1)
    2
    >>> token_cache.count_token(t_black_2)
    2
    >>> t_red = Token("red")
    >>> token_cache.count_token(t_red
    0
    >>> token_cache.is_token_empty(t_black_1)
    False
    >>> token_cache.is_token_empty(t_red)
    True

    >>> t_black_3 = Token("black")
    >>> t_red_2 = Token("red")
    >>> token_cache.add(t_black_3)
    >>> token_cache.add(t_red_2)
    >>> token_cache.count()
    6
    >>> token_cache.count_token(t_black_3)
    3
    >>> token_cache.is_token_empty(t_red_2)
    False

    >>> token_cache.remove(t_yellow)
    >>> token_cache.count()
    5
    >>> token_cache.count_token(t_yellow)
    0
    >>> token_cache.remove(t_yellow) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    Exception:...
    >>> token_cache.count()
    5
    """

    d: Dict[Token, int]

    def __init__(self, t: Tuple[Token] = ()) -> None:
        self.d = {}
        for item in t:
            self.d[item.get_gem()] = self.d.setdefault(item.get_gem(), 0) + 1

    def empty(self) -> None:
        self.d = {}

    def get_tokens_list(self) -> List[Token]:
        return list(self.d.keys())
 
    def add(self, token: Token, how_many: int=1) -> None:
        """
        Add how_many tokens (by Token, not by a string describing a token).
        """
        gem_name = token.get_gem_name()
        self.add_by_name(gem_name, how_many)

    def add_by_name(self, gem_name: str, how_many: int=1) -> None:
        """
        Add how_many tokens (by a string describing a token).
        """
        self.d[Token(gem_name)] = self.d.setdefault(Token(gem_name), 0) + how_many

    def remove(self, token: Token, how_many: int=1) -> None:
        """
        Remove tokens from this cache, by a string describing a token type.
        """
        if self.d.get(token) and self.d.get(token) >= how_many:
            self.d[token] -= how_many
            return
        else:
            raise Exception(
                f"{how_many} of token type {token} not found in token cache"
            )

    def count(self) -> int:
        count = 0
        for key in self.d.keys():
            count += self.d[key]
        return count

    def count_token(self, token: Token) -> int:
        count = self.d.get(token)
        if count:
            return count
        else:
            return 0

    def is_token_empty(self, token: Token) -> bool:
        if not self.d.get(token) or self.d.get(token) < 0:
            return True
        return False

    def __str__(self) -> str:
        ret = ""
        ret += f"Token cache ({self.count()} total): "
        ret_dict = {}
        for key in self.d:
            ret_dict[key.__str__()] = self.d.get(key)
        ret += json.dumps(ret_dict, sort_keys=True)
        return ret

    def __repr__(self) -> str:
        return f"<TokenCache: {self.count()} total>"


PLAYER_TOKEN_CACHE_MAX = 10

class PlayerTokenCache(TokenCache):
    """
    The set of tokens currently held by a player.
    
    >>> player_token_cache = PlayerTokenCache()
    >>> player_token_cache.count()
    0
    >>> player_token_cache.count_token(Token("black"))
    0

    >>> t_black = Token("black")
    >>> t_red = Token("red")
    >>> t_yellow = Token("yellow")
    >>> t_green = Token("green")
    >>> t_white = Token("white")
    >>> t_blue = Token("blue")

    >>> initial_tokens = (t_black, t_black, t_black, t_black, t_red, t_red, t_red, t_yellow)
    >>> player_token_cache = PlayerTokenCache(initial_tokens)
    >>> player_token_cache.count()
    8
    >>> player_token_cache.count_token(t_black)
    4
    >>> player_token_cache.count_token(t_red)
    3
    >>> player_token_cache.is_token_empty(t_black)
    False
    >>> player_token_cache.is_token_empty(t_white)
    True
    >>> player_token_cache.is_max()
    False
    >>> player_token_cache.is_over_max()
    False
    >>> player_token_cache.count_until_max()
    2

    >>> player_token_cache = PlayerTokenCache(initial_tokens)
    >>> player_token_cache.add(t_red)

    >>> player_token_cache.add(t_green)
    >>> player_token_cache.is_max()
    True
    >>> player_token_cache.is_over_max()
    False
    >>> player_token_cache.count_until_max()
    0
    >>> player_token_cache.add(t_red)
    >>> player_token_cache.is_max()
    False
    >>> player_token_cache.is_over_max()
    True
    >>> player_token_cache.count_until_max()
    0

    >>> player_token_cache = PlayerTokenCache(initial_tokens)
    >>> player_token_cache.remove(t_red)
    >>> player_token_cache.count()
    7
    >>> player_token_cache.count_token(t_red)
    2

    >>> player_token_cache.remove(t_blue) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    Exception:...

    >>> player_token_cache = PlayerTokenCache(initial_tokens)
    >>> cost_dict_1 = {"black": 2, "red": 1}
    >>> dev_card_1 = DevCard(level=1, gem=Gem("black"), ppoints=2, cost=cost_dict_1)
    >>> player_token_cache.can_purchase_dev_card(dev_card_1)
    True
    >>> player_token_cache.purchase_dev_card(dev_card_1)
    >>> player_token_cache.count()
    5
    >>> player_token_cache.count_token(t_black)
    2
    >>> player_token_cache.count_token(t_red)
    2
    >>> player_token_cache.count_token(t_yellow)
    1

    >>> player_token_cache = PlayerTokenCache(initial_tokens)
    >>> cost_dict_2 = {"black": 5, "red": 1}
    >>> dev_card_2 = DevCard(level=1, gem=Gem("black"), ppoints=2, cost=cost_dict_2)
    >>> player_token_cache.can_purchase_dev_card(dev_card_2)
    True
    >>> player_token_cache.purchase_dev_card(dev_card_2)
    >>> player_token_cache.count()
    2
    >>> player_token_cache.count_token(t_black)
    0
    >>> player_token_cache.count_token(t_red)
    2
    >>> player_token_cache.count_token(t_yellow)
    0

    >>> player_token_cache = PlayerTokenCache(initial_tokens)
    >>> cost_dict_3 = {"black": 6, "red": 1}
    >>> dev_card_3 = DevCard(level=1, gem=Gem("black"), ppoints=2, cost=cost_dict_3)
    >>> player_token_cache.can_purchase_dev_card(dev_card_3)
    False
    >>> player_token_cache.purchase_dev_card(dev_card_3) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    Exception:...
    """

    def is_max(self) -> bool:
        if self.count() == PLAYER_TOKEN_CACHE_MAX:
            return True
        return False

    def is_over_max(self) -> bool:
        if self.count() > PLAYER_TOKEN_CACHE_MAX:
            return True
        return False

    def count_until_max(self) -> int:
        """
        Return the number of token "space" within this cache.
        """
        return max(PLAYER_TOKEN_CACHE_MAX - self.count(), 0)

    def _purchase_dev_card_tokens_needed(self, dev_card) -> TokenCache:
        """
        Return a TokenCache of the tokens needed to purchase dev_card, or None if the card cannot be purchased.

        Considers jokers.
        """
        token_cache_needed = TokenCache()
        jokers_needed = 0

        cost_dict = dev_card.get_cost_dict()
        for gem_name in cost_dict.keys():
            cost_count_this = cost_dict[gem_name]
            cache_count_this = self.count_token(gem_name)
            token_cache_needed.add_by_name(gem_name, min(cost_count_this, cache_count_this))
            if cost_count_this > cache_count_this:
                jokers_needed += (cost_count_this - cache_count_this)
        if jokers_needed > self.count_token(Token("yellow")):
            return None
        token_cache_needed.add_by_name("yellow", jokers_needed)
        return token_cache_needed

    def can_purchase_dev_card(self, dev_card) -> bool:
        """
        Return True if dev_card can be purchased given the tokens in this token cache.
        """
        return self._purchase_dev_card_tokens_needed(dev_card) != None

    def purchase_dev_card(self, dev_card) -> None:
        """
        Remove tokens needed to purchase dev card.  Raise exception if there aren't enough tokens.
        """
        token_cache_needed = self._purchase_dev_card_tokens_needed(dev_card)
        if token_cache_needed == None:
            raise Exception(f"insufficient tokens to purchase dev card {dev_card}")
        for token in token_cache_needed.get_tokens_list():
            self.remove(token, token_cache_needed.count_token(token))
        return

    def __repr__(self) -> str:
        return f"<PlayerTokenCache: {self.count()} total>"

# players count -> tokens count per type
TOKEN_COUNT_MAP = {2: 4, 3: 5, 4: 7}


class GameTokenCache(TokenCache):
    """
    The set of tokens available within a game.  The initial counts depend on the number of players.
    
    >>> t_black = Token("black")
    >>> t_red = Token("red")
    >>> t_yellow = Token("yellow")
    >>> t_green = Token("green")
    >>> t_white = Token("white")
    >>> t_blue = Token("blue")

    >>> game_token_cache = GameTokenCache(players_count=2)
    >>> game_token_cache.count()
    25
    >>> game_token_cache.count_token(t_black)
    4
    >>> game_token_cache.count_token(t_yellow)
    5

    >>> game_token_cache.remove(t_red)
    >>> game_token_cache.count_token(t_red)
    3
    >>> game_token_cache.is_token_empty(t_red)
    False
    >>> game_token_cache.remove(t_red)
    >>> game_token_cache.remove(t_red)
    >>> game_token_cache.remove(t_red)
    >>> game_token_cache.count_token(t_red)
    0
    >>> game_token_cache.is_token_empty(t_red)
    True
    >>> game_token_cache.remove(t_red) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    Exception:...

    >>> game_token_cache.add(Token("red"))
    >>> game_token_cache.count_token(t_red)
    1
    """

    def __init__(self, players_count: int) -> None:
        self.d = {}
        self.fill(players_count)

    def fill(self, players_count: int) -> None:
        if players_count not in TOKEN_COUNT_MAP.keys():
            raise Exception("invalid players_count")
        for gem_name in GEM_NAME_COMMON_STR_DICT.keys():
            self.d[Token(gem_name)] = TOKEN_COUNT_MAP[players_count]
        self.d[Token("yellow")] = 5

    # def can_action_take_three_tokens(token_types_set: Set[TokenType]) -> bool
    # def can_action_take_two_tokens(token_types_set: Set[TokenType]) -> bool

    def __repr__(self) -> str:
        return f"<GameTokenCache: {self.count()} total>"
