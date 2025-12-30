import random
def generate_new_game_cards(user, rare_item, total_cards):

    cards = []

    if rare_item:
        cards.append(rare_item)
        total_cards -= 1
    
    for _ in range(total_cards):
        cards.append(f"common_item_{random.randint(1, 1000)}")

    random.shuffle(cards)

    return cards