##############################################################################
# constants.py
#
# Source file containing constants used to read/write/process ssm files 
##############################################################################

from dataclasses import dataclass
@dataclass(frozen=True)
class Variants_Keys:
    """Dataclass used to define variant column headers"""
    NAME: str = "name"
    ID: str = "id"
    CHROM: str = "chrom"
    POS: str = "pos"
    OMEGA_V: str = "omega_v"
    VAR_READS: str = "var_reads"
    REF_READS: str = "ref_reads"
    TOTAL_READS: str = "total_reads"
    VAF: str = "vaf"

