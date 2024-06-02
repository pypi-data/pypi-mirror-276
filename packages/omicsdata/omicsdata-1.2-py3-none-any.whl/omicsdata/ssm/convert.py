##############################################################################
# ssm_to_viber.py
#
# Contains code to convert a simple somatic mutation file to a 
# tab separated file that can be used by VIBER.
##############################################################################

import pandas as pd 
import json, sys, os
import numpy as np 
from warnings import showwarning

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from omicsdata.ssm.columns import SSM_Columns, PARAMS_Columns

# CONSTANTS 
PYCLONE_VI_COLUMNS = ["mutation_id", 
                      "sample_id", 
                      "ref_counts", 
                      "alt_counts", 
                      "major_cn", 
                      "minor_cn", 
                      "normal_cn"]

def ssm_to_viber(viber_dir, ssm_fn, params_fn):
    """Processes simple somatic mutation (ssm) file to a tab separated file (tsv) that can be used by VIBER (https://github.com/caravagnalab/VIBER)

    Parameters
    ----------
    viber_dir : str
        path to a directory to store all VIBER format files
    ssm_fn : str
        The simple somatic mutation file
    params_fn : str
        The parameters file 

    Returns
    -------
    None
    """

    # make sure directory exists
    if not os.path.exists(viber_dir):
        os.mkdir(viber_dir)

    dataframe = pd.read_csv(ssm_fn, sep="\t")
    params = json.load(open(params_fn))
    samples = params[PARAMS_Columns.SAMPLES]
    clusters = params[PARAMS_Columns.CLUSTERS]
    ssms = [c[0] for c in clusters]

    DP = []
    NV = []

    for vid in ssms:

        row = dataframe[dataframe["id"] == vid].iloc[0]

        row_DP = []
        row_NV = []

        # iterate through all var_read, ref_reads, var_read_prob per row
        for var_reads, total_reads, var_read_prob in zip([int(cnt) for cnt in row[SSM_Columns.VAR_READS].split(",")],
                                                               [int(cnt) for cnt in row[SSM_Columns.TOTAL_READS].split(",")],
                                                               [float(vrp) for vrp in row[SSM_Columns.VAR_READ_PROB].split(",")]):

            # make everything diploid
            total_reads_diploid = int(2*total_reads*var_read_prob)
            var_reads_diploid = np.minimum(int(var_reads), total_reads_diploid)
            row_DP.append(total_reads_diploid)
            row_NV.append(var_reads_diploid)

        DP.append(row_DP)
        NV.append(row_NV)

    pd.DataFrame(ssms, columns=["id"]).to_csv(os.path.join(viber_dir, "id.tsv"), sep="\t", index=False)
    pd.DataFrame(DP, columns=samples).to_csv(os.path.join(viber_dir, "DP.tsv"), sep="\t", index=False)
    pd.DataFrame(NV, columns=samples).to_csv(os.path.join(viber_dir, "NV.tsv"), sep="\t", index=False)


def ssm_to_pyclone(pyclone_fn, ssm_fn, params_fn):
    """Processes simple somatic mutation (ssm) file to a tab separated file (tsv) that can be used by PyClone-VI (https://github.com/Roth-Lab/pyclone-vi)

    Parameters
    ----------
    pyclone_fn : str
        path to a file to a tsv file to output the convert ssm file data
    ssm_fn : str
        The simple somatic mutation file
    params_fn : str
        The parameters file 

    Returns
    -------
    None
    """
    showwarning("We do not have a good way to estimate the major and minor copy numbers for PyClone" 
                "-- if your data contains mutations from sex chromosomes, we do not know if the organism" 
                "is male or female. If complex copy number changes have occurred, we also don't have a clear " 
                "way to determine how many copies of each allele there are. You've been warned!", Warning, "ssm_to_pyclone.py", 42)
    dataframe = pd.read_csv(ssm_fn, sep="\t")
    params = json.load(open(params_fn))
    samples = params[PARAMS_Columns.SAMPLES]
    clusters = params[PARAMS_Columns.CLUSTERS]
    ssms = [c[0] for c in clusters]

    pyclone_df = pd.DataFrame(columns=PYCLONE_VI_COLUMNS)

    for vid in ssms:

        row = dataframe[dataframe[SSM_Columns.ID] == vid].iloc[0]

        name = row[SSM_Columns.NAME]

        # iterate through all var_read, ref_reads, var_read_prob per row
        for var_reads, total_reads, var_read_prob, sample in zip([int(cnt) for cnt in row[SSM_Columns.VAR_READS].split(",")],
                                                               [int(cnt) for cnt in row[SSM_Columns.TOTAL_READS].split(",")],
                                                               [float(vrp) for vrp in row[SSM_Columns.VAR_READ_PROB].split(",")],
                                                               samples):
            # assume everything is either diploid or haploid and in a non-CNA effected region
            major_cn, minor_cn = 1, 1
 
            if (name[:2] == "Y_") or var_read_prob > 0.90: # this is a guess that the copy number is 1, this is not accurate if your data has complex copy number changes 
                normal_cn = 1
            else:
                normal_cn = 2

            if normal_cn == 1 and minor_cn >= 1:
                minor_cn = 1

            pyclone_values = [name, sample, total_reads - var_reads, var_reads, major_cn, minor_cn, normal_cn]
            pyclone_df = pd.concat([pyclone_df, pd.DataFrame.from_records([dict(zip(PYCLONE_VI_COLUMNS, pyclone_values))])], ignore_index=True)

    pyclone_df.to_csv(pyclone_fn, sep="\t", index=False)
