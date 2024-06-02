##############################################################################
# columns.py
#
# Source file containing dataclasses that define columns for tree structures
##############################################################################

from dataclasses import dataclass

@dataclass(frozen=True)
class NEUTREE_Columns:
    """Dataclass used to define Neutree columns"""
    STRUCTS: str = "structs"
    PHIS: str = "phis"
    COUNTS: str = "counts"
    LOGSCORES: str = "logscores"
    CLUSTERINGS: str = "clusterings"
    GARBAGE: str = "garbage"