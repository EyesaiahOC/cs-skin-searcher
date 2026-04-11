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


