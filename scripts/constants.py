from enum import Enum

DEBUG = False

class WeaponType(Enum):
      # Starting Pistols
    GLOCK_18 = "Glock-18"
    USP_S = "USP-S"
    P2000 = "P2000"

    # Pistols
    DUAL_BERETTAS = "Dual Berettas"
    P250 = "P250"
    TEC_9 = "Tec-9"
    FIVE_SEVEN = "Five-SeveN"
    CZ75_AUTO = "CZ75-Auto"
    DESERT_EAGLE = "Desert Eagle"
    R8_REVOLVER = "R8 Revolver"

    # Mid-Tier (SMGs)
    MAC_10 = "MAC-10"
    MP9 = "MP9"
    MP7 = "MP7"
    MP5_SD = "MP5-SD"
    UMP_45 = "UMP-45"
    P90 = "P90"
    PP_BIZON = "PP-Bizon"

    # Mid-Tier (Shotguns & Machine Guns)
    NOVA = "Nova"
    XM1014 = "XM1014"
    MAG_7 = "MAG-7"
    SAWED_OFF = "Sawed-Off"
    M249 = "M249"
    NEGEV = "Negev"

    # Rifles
    GALIL_AR = "Galil AR"
    FAMAS = "FAMAS"
    AK_47 = "AK-47"
    M4A4 = "M4A4"
    M4A1_S = "M4A1-S"
    SG_553 = "SG 553"
    AUG = "AUG"

    # Sniper Rifles
    SSG_08 = "SSG 08"
    AWP = "AWP"
    G3SG1 = "G3SG1"
    SCAR_20 = "SCAR-20"

    # Other
    ZEUS_X27 = "Zeus x27"

class Rarity(Enum):
    # White
    CONSUMER_GRADE = "Consumer Grade"
    # Light Blue
    INDUSTRIAL_GRADE = "Industrial Grade"
    # Blue
    MIL_SPEC = "Mil-Spec"
    # Purple
    RESTRICTED = "Restricted"
    # Pink
    CLASSIFIED = "Classified"
    # Red
    COVERT = "Covert"
    # Orange
    CONTRABAND = "Contraband"

class Source(Enum):
    # Cases - Armory
    FEVER_CASE = "Fever Case"
    # Cases - Weekly Drop
    SEALED_DEAD_HAND_TERMINAL = "Sealed Dead Hand Terminal"
    SEALED_GENESIS_TERMINAL = "Sealed Genesis Terminal"
    KILOWATT_CASE = "Kilowatt Case"
    REVOLUTION_CASE = "Revolution Case"
    DREAMS_AND_NIGHTMARES_CASE = "Dreams & Nightmares Case"
    # Cases - All
    CHROMA_2_CASE = "Chroma 2 Case"
    CHROMA_3_CASE = "Chroma 3 Case"
    CHROMA_CASE = "Chroma Case"
    CLUTCH_CASE = "Clutch Case"
    CS20_CASE = "CS20 Case"
    CSGO_WEAPON_CASE = "CS:GO Weapon Case"
    CSGO_WEAPON_CASE_2 = "CS:GO Weapon Case 2"
    CSGO_WEAPON_CASE_3 = "CS:GO Weapon Case 3"
    DANGER_ZONE_CASE = "Danger Zone Case"
    ESPORTS_2013_CASE = "eSports 2013 Case"
    ESPORTS_2013_WINTER_CASE = "eSports 2013 Winter Case"
    ESPORTS_2014_SUMMER_CASE = "eSports 2014 Summer Case"
    FALCHION_CASE = "Falchion Case"
    FRACTURE_CASE = "Fracture Case"
    GALLERY_CASE = "Gallery Case"
    GAMMA_2_CASE = "Gamma 2 Case"
    GAMMA_CASE = "Gamma Case"
    GLOVE_CASE = "Glove Case"
    HORIZON_CASE = "Horizon Case"
    HUNTSMAN_WEAPON_CASE = "Huntsman Weapon Case"
    OPERATION_BRAVO_CASE = "Operation Bravo Case"
    OPERATION_BREAKOUT_WEAPON_CASE = "Operation Breakout Weapon Case"
    OPERATION_BROKEN_FANG_CASE = "Operation Broken Fang Case"
    OPERATION_HYDRA_CASE = "Operation Hydra Case"
    OPERATION_PHOENIX_WEAPON_CASE = "Operation Phoenix Weapon Case"
    OPERATION_RIPTIDE_CASE = "Operation Riptide Case"
    OPERATION_VANGUARD_WEAPON_CASE = "Operation Vanguard Weapon Case"
    OPERATION_WILDFIRE_CASE = "Operation Wildfire Case"
    PRISMA_2_CASE = "Prisma 2 Case"
    PRISMA_CASE = "Prisma Case"
    RECOIL_CASE = "Recoil Case"
    REVOLVER_CASE = "Revolver Case"
    SHADOW_CASE = "Shadow Case"
    SHATTERED_WEB_CASE = "Shattered Web Case"
    SNAKEBITE_CASE = "Snakebite Case"
    SPECTRUM_2_CASE = "Spectrum 2 Case"
    SPECTRUM_CASE = "Spectrum Case"
    WINTER_OFFENSIVE_WEAPON_CASE = "Winter Offensive Weapon Case"
    X_RAY_P250_PACKAGE = "X-Ray P250 Package"
    # Collections - Armory
    THE_TRAIN_2025_COLLECTION = "The Train 2025 Collection"
    THE_OVERPASS_2024_COLLECTION = "The Overpass 2024 Collection"
    THE_SPORT_AND_FIELD_COLLECTION = "The Sport & Field Collection"
    LIMITED_EDITION_ITEM = "Limited Edition Item"
    # Collections - Weekly Drop
    THE_HARLEQUIN_COLLECTION = "The Harlequin Collection"
    THE_ACHROMA_COLLECTION = "The Achroma Collection"
    THE_ASCENT_COLLECTION = "The Ascent Collection"
    THE_BOREAL_COLLECTION = "The Boreal Collection"
    THE_RADIANT_COLLECTION = "The Radiant Collection"
    # Collections - All
    THE_2018_INFERNO_COLLECTION = "The 2018 Inferno Collection"
    THE_2018_NUKE_COLLECTION = "The 2018 Nuke Collection"
    THE_2021_DUST_2_COLLECTION = "The 2021 Dust 2 Collection"
    THE_2021_MIRAGE_COLLECTION = "The 2021 Mirage Collection"
    THE_2021_TRAIN_COLLECTION = "The 2021 Train Collection"
    THE_2021_VERTIGO_COLLECTION = "The 2021 Vertigo Collection"
    THE_ALPHA_COLLECTION = "The Alpha Collection"
    THE_ANCIENT_COLLECTION = "The Ancient Collection"
    THE_ANUBIS_COLLECTION = "The Anubis Collection"
    THE_ASSAULT_COLLECTION = "The Assault Collection"
    THE_AZTEC_COLLECTION = "The Aztec Collection"
    THE_BAGGAGE_COLLECTION = "The Baggage Collection"
    THE_BANK_COLLECTION = "The Bank Collection"
    THE_BLACKSITE_COLLECTION = "The Blacksite Collection"
    THE_CACHE_COLLECTION = "The Cache Collection"
    THE_CANALS_COLLECTION = "The Canals Collection"
    THE_CHOP_SHOP_COLLECTION = "The Chop Shop Collection"
    THE_COBBLESTONE_COLLECTION = "The Cobblestone Collection"
    THE_CONTROL_COLLECTION = "The Control Collection"
    THE_DUST_2_COLLECTION = "The Dust 2 Collection"
    THE_DUST_COLLECTION = "The Dust Collection"
    THE_GODS_AND_MONSTERS_COLLECTION = "The Gods and Monsters Collection"
    THE_GRAPHIC_DESIGN_COLLECTION = "The Graphic Design Collection"
    THE_HAVOC_COLLECTION = "The Havoc Collection"
    THE_INFERNO_COLLECTION = "The Inferno Collection"
    THE_ITALY_COLLECTION = "The Italy Collection"
    THE_LAKE_COLLECTION = "The Lake Collection"
    THE_MILITIA_COLLECTION = "The Militia Collection"
    THE_MIRAGE_COLLECTION = "The Mirage Collection"
    THE_NORSE_COLLECTION = "The Norse Collection"
    THE_NUKE_COLLECTION = "The Nuke Collection"
    THE_OFFICE_COLLECTION = "The Office Collection"
    THE_OVERPASS_COLLECTION = "The Overpass Collection"
    THE_RISING_SUN_COLLECTION = "The Rising Sun Collection"
    THE_SAFEHOUSE_COLLECTION = "The Safehouse Collection"
    THE_ST_MARC_COLLECTION = "The St. Marc Collection"
    THE_TRAIN_COLLECTION = "The Train Collection"
    THE_VERTIGO_COLLECTION = "The Vertigo Collection"

