import random
import uuid

# PROBABILITY
def get_rare_item_probability(user, goal_card):
    # TODO
    return 0.5

def get_jackpot_probability(user, goal_card):
    # TODO
    return 0.5

# HASH

def search_game_hash(user, goal_card):
    # TODO
    return None

def create_game_hash(user, goal_card):
    game_uuid  = str(uuid.uuid4())
    # TODO registrar no bd
    return game_uuid 

def get_game_hash(user, goal_card):
    hash = search_game_hash(user, goal_card)
    if not hash:
        hash = create_game_hash(user, goal_card)
    return hash