PLAYERS_COUNT_MAX = 4
PLAYERS_COUNT_MIN = 2

class GameState:
    dev_card_decks: DevCardDecks
    nobles_in_play: NoblesInPlay
    token_game_cache: TokenGameCache
    __init__()
    action

class GameStateHistory:
    l: List[GameState]
    current_state_idx: int
    __init__()
    __str__() # needed?
    get_current_state() -> GameState
    revert(idx: int) -> None # revert history to state at idx; remove newer states

class Game:
    players: list[Player] # list b/c order of play matters
    game_state_history: GameStateHistory
    round_number: int
    __init__(players_count: int) # set up new game
    add_player(player: Player)
    play()
    action_take_three_gems(player: Player, gem_types_set: Set(3)) -> None # analyze current state; if applicable, create new state
    action_take_two_gems(player: Player, gem_type: GemType) -> None
    action_reserve() -> None
    action_purchase() -> None

