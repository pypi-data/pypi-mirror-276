import pandas as pd 
import json, argparse

# CONSTANTS 
PYCLONE_VI_COLUMNS = ["mutation_id", 
                      "sample_id", 
                      "ref_counts", 
                      "alt_counts", 
                      "major_cn", 
                      "minor_cn", 
                      "normal_cn"]


def pyclone_vi_fmt(pyclone_fn, ssm_fn, params_fn):
    """
    Processes ssm dataframe into a tsv that can be used by PyClone-VI
    """

    dataframe = pd.read_csv(ssm_fn, sep="\t")
    params = json.load(open(params_fn))
    samples = params["samples"]
    clusters = params["clusters"]
    ssms = [c[0] for c in clusters]

    pyclone_df = pd.DataFrame(columns=PYCLONE_VI_COLUMNS)

    for vid in ssms:

        row = dataframe[dataframe["id"] == vid].iloc[0]

        name = row["name"]

        # iterate through all var_read, ref_reads, var_read_prob per row
        for var_reads, total_reads, var_read_prob, sample in zip([int(cnt) for cnt in row["var_reads"].split(",")],
                                                               [int(cnt) for cnt in row["total_reads"].split(",")],
                                                               [float(vrp) for vrp in row["var_read_prob"].split(",")],
                                                               samples):
            # assume everything is either diploid or haploid and in a non-CNA effected region
            major_cn, minor_cn = 1, 1
            if (name[:2] == "X_") or (name[:2] == "Y_") or var_read_prob > 0.90:
                normal_cn = 1
            else:
                normal_cn = 2

            if normal_cn == 1 and minor_cn >= 1:
                minor_cn = 1

            pyclone_values = [name, sample, total_reads - var_reads, var_reads, major_cn, minor_cn, normal_cn]
            pyclone_df = pd.concat([pyclone_df, pd.DataFrame.from_records([dict(zip(PYCLONE_VI_COLUMNS, pyclone_values))])], ignore_index=True)

    pyclone_df.to_csv(pyclone_fn, sep="\t", index=False)


def _parse_args():
    """
    Parses command line arguments.
    """
    parser = argparse.ArgumentParser(

        description="convert ssm file to be used by pyclone-vi",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter

    )

    parser.add_argument('pyclone_fn', help='Output tab separated file name in pyclone-vi format')
    parser.add_argument('params_fn', help='Parameters file')
    parser.add_argument('ssm_fn', help='Simple somatic mutation file.')



    args = parser.parse_args()

    return args


def main():
    """
    Performs checks on command line arguments, then attempts to process all files.
    """
    args = _parse_args()

    pyclone_vi_fmt(args.pyclone_fn, args.params_fn, args.ssm_fn)


if __name__ == '__main__':
  main()
