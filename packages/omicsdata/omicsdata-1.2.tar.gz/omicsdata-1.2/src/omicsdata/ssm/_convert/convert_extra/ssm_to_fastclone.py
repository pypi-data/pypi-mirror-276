import pandas as pd 
import json, argparse, os

# CONSTANTS 
FASTCLONE_COLUMNS = ["mutation_id", 
                      "sample_id", 
                      "ref_counts", 
                      "var_counts", 
                      "major_cn", 
                      "minor_cn", 
                      "normal_cn"]


def fastclone_fmt(fastclone_path, ssm_fn, params_fn):
    """
    Processes ssm dataframe into a set tsv that can be used by fastclone
    """

    dataframe = pd.read_csv(ssm_fn, sep="\t")
    samples = json.load(open(params_fn))["samples"]

    fastclone_df = pd.DataFrame(columns=FASTCLONE_COLUMNS)

    for row_idx in range(0, len(dataframe)):

        row = dataframe.iloc[row_idx]

        name = row["name"]

        # iterate through all var_read, ref_reads, var_read_prob per row
        for var_reads, ref_reads, sample in zip([int(cnt) for cnt in row["var_reads"].split(",")],
                                                               [int(cnt) for cnt in row["total_reads"].split(",")],
                                                               samples):
            # assume everything is either diploid or haploid and in a non-CNA effected region
            major_cn, minor_cn = 1, 1
            if name[:2] == "X_" or name[:2] == "Y_":
                normal_cn = 1
            else:
                normal_cn = 2

            if normal_cn == 1 and minor_cn >= 1:
                minor_cn = 1

            fastclone_values = [name, sample, ref_reads, var_reads, major_cn, minor_cn, normal_cn]
            fastclone_df = pd.concat([fastclone_df, pd.DataFrame.from_records([dict(zip(FASTCLONE_COLUMNS, fastclone_values))])], ignore_index=True)

    for s in samples:
        temp_df = fastclone_df.loc[fastclone_df["sample_id"] == s].drop("sample_id", axis=1).copy()
        temp_df.to_csv(os.path.join(fastclone_path, str(s) + ".tsv"), sep="\t", index=False)


def _parse_args():
    """
    Parses command line arguments.
    """
    parser = argparse.ArgumentParser(

        description="convert ssm file to be used by pyclone-vi",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter

    )

    parser.add_argument('fastclone_path', help='Path to write fastclone files to.')
    parser.add_argument('params_fn', help='Parameters file')
    parser.add_argument('ssm_fn', help='Simple somatic mutation file.')



    args = parser.parse_args()

    return args


def main():
    """
    Performs checks on command line arguments, then attempts to process all files.
    """
    args = _parse_args()

    fastclone_fmt(args.fastclone_path, args.params_fn, args.ssm_fn)


if __name__ == '__main__':
  main()
