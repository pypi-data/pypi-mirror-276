import pandas as pd 
import json, argparse, os
import numpy as np 


def viber_fmt(output_path, ssm_fn, params_fn):
    """
    Processes ssm dataframe into a tsv that can be used by VIBER
    """

    dataframe = pd.read_csv(ssm_fn, sep="\t")
    params = json.load(open(params_fn))
    samples = params["samples"]
    clusters = params["clusters"]
    ssms = [c[0] for c in clusters]

    DP = []
    NV = []

    for vid in ssms:

        row = dataframe[dataframe["id"] == vid].iloc[0]

        row_DP = []
        row_NV = []

        # iterate through all var_read, ref_reads, var_read_prob per row
        for var_reads, total_reads, var_read_prob, _ in zip([int(cnt) for cnt in row["var_reads"].split(",")],
                                                               [int(cnt) for cnt in row["total_reads"].split(",")],
                                                               [float(prob) for prob in row["var_read_prob"].split(",")],
                                                               samples):

            # make everything diploid
            total_reads_diploid = int(2*total_reads*var_read_prob)
            var_reads_diploid = np.minimum(int(var_reads), total_reads_diploid)
            row_DP.append(total_reads_diploid)
            row_NV.append(var_reads_diploid)

        DP.append(row_DP)
        NV.append(row_NV)

    pd.DataFrame(ssms, columns=["id"]).to_csv(os.path.join(output_path, "id.tsv"), sep="\t", index=False)
    pd.DataFrame(DP, columns=samples).to_csv(os.path.join(output_path, "DP.tsv"), sep="\t", index=False)
    pd.DataFrame(NV, columns=samples).to_csv(os.path.join(output_path, "NV.tsv"), sep="\t", index=False)


def _parse_args():
    """
    Parses command line arguments.
    """
    parser = argparse.ArgumentParser(

        description="convert ssm file to be used by VIBER",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter

    )

    parser.add_argument('output_path', help='Path to output VIBER data files to')
    parser.add_argument('params_fn', help='Parameters file')
    parser.add_argument('ssm_fn', help='Simple somatic mutation file.')

    args = parser.parse_args()

    return args


def main():
    """
    Performs checks on command line arguments, then attempts to process all files.
    """
    args = _parse_args()

    viber_fmt(args.output_path, args.params_fn, args.ssm_fn)


if __name__ == '__main__':
  main()
