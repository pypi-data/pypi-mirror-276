import pandas as pd 
import json, argparse
import numpy as np 


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
    VAR_READ_PROB: str = "var_read_prob"
    VAF: str = "vaf"

# CONSTANTS 
MOBSTER_COLUMNS = ["Key", 
                   "t_alt_count", 
                   "t_ref_cont", 
                   "DP"
                   "VAF"]


def mobster_fmt(mobster_fn, ssm_fn, params_fn):
    """
    Processes ssm dataframe into a tsv that can be used by MOBSTER
    """

    dataframe = pd.read_csv(ssm_fn, sep="\t")
    samples = json.load(open(params_fn))["samples"]

    mobster_df = pd.DataFrame(columns=MOBSTER_COLUMNS)

    for row_idx in range(0, len(dataframe)):

        row = dataframe.iloc[row_idx]

        name = row[Variants_Keys.NAME]

        # iterate through all var_read, ref_reads, var_read_prob per row
        for var_reads, ref_reads, var_read_prob, sample in zip([int(cnt) for cnt in row[Variants_Keys.VAR_READS].split(",")],
                                                               [int(cnt) for cnt in row[Variants_Keys.TOTAL_READS].split(",")],
                                                               [float(prob) for prob in row[Variants_Keys.VAR_READ_PROB].split(",")],
                                                               samples):

            total_reads_diploid = 2*(var_reads + ref_reads)*var_read_prob
            var_reads_diploid = np.minimum(var_reads, total_reads_diploid)
            ref_reads_diploid = total_reads_diploid - var_reads_diploid
            VAF = var_reads_diploid / ref_reads_diploid
            mobster_values = [name, var_reads_diploid, ref_reads_diploid, total_reads_diploid, VAF]
            mobster_df = pd.concat([mobster_df, pd.DataFrame.from_records([dict(zip(MOBSTER_COLUMNS, mobster_values))])], ignore_index=True)

    mobster_df.to_csv(mobster_fn, sep="\t", index=False)


def _parse_args():
    """
    Parses command line arguments.
    """
    parser = argparse.ArgumentParser(

        description="convert ssm file to be used by MOBSTER",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter

    )

    parser.add_argument('mobster_fn', help='Output tab separated file name in MOBSTER format')
    parser.add_argument('params_fn', help='Parameters file')
    parser.add_argument('ssm_fn', help='Simple somatic mutation file.')



    args = parser.parse_args()

    return args


def main():
    """
    Performs checks on command line arguments, then attempts to process all files.
    """
    args = _parse_args()

    mobster_fmt(args.mobster_fn, args.params_fn, args.ssm_fn)


if __name__ == '__main__':
  main()
