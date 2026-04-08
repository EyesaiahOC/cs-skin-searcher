from typing import List
from constants import WeaponType, Rarity, Collections

skin_template = {

    "name": str,
    "weapon": WeaponType,
    "rarity": Rarity,
    "collection": Collections,
    "is_patterned_based": bool,
    "webm_url":str,
    "in_game_url":str,
    "workshop_url":str,
    "tags":List[str],
    "colors":List[str]

}