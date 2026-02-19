def get_building_cost_modifier(village_id: int) -> float:
    return  1.5 ** (village_id - 1)