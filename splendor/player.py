class PlayerState:
    token_cache: TokenCache
    dev_card_cache: DevCardCache
    dev_card_reserve: DevCardReserve
    __init__(token_cache: TokenCache, dev_card_cache: DevCardCache, dev_card_reserve: DevCardReserve)                                                                            
    get_token_cache() -> TokenCache
    get_dev_card_cache() -> DevCardCache
    get_dev_card_reserve() -> DevCardReserve
    calc_score() -> int
    is_winning_state() -> bool
    __str__() -> str

class PlayerStateHistory:
    l: List[PlayerState]
    current_state_idx: int
    __init__()
    __str__() # needed?
    get_current_state() -> PlayerState
    revert(idx: int) -> None # revert history to state at idx; remove newer states

class Player:
    name: str
    player_state_history: PlayerStateHistory
    __init__(name=None: str) # if name=None, make a random one
    get_name() -> str
    get_player_state_history() -> PlayerStateHistory
    calc_score() -> int # call PlayerState.calc_score()
    action_take_three_gems() -> None # analyze current state; if applicable, create new state                                                                                    
    action_take_two_gems() -> None
    action_reserve() -> None
    action_purchase() -> None

