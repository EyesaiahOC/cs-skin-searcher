from typing import List
from scripts.constants import WeaponType, Rarity, Source

skin_template = {

    "name": str,
    "weapon": WeaponType,
    "rarity": Rarity,
    "source": Source,
    "is_patterned_based": bool,
    "webm_url":str,
    "in_game_url":str,
    "workshop_url":str,
    "tags":List[str],
    "colors":List[str]

}
