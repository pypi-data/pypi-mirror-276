##############################################################################
# parse.py
#
# Source file containing functions for reading/writing simple somatic mutation
# files and parameters files.
##############################################################################

import csv
import json
import numpy as np
import numpy.ma as ma
from .constants import Variants_Keys
from .columns import SSM_Columns, PARAMS_Columns
from .common import extract_vids


def extract_nums(S, dtype):
    """Extracts and converts values from a comma delimited string"""
    return np.array(S.split(','), dtype=dtype)

def load_ssm(ssm_fn, rescale_depth=False):
    """Loads a ssm file and extracts the read count and copy number data for each variant
    
    Parameters
    ----------
    ssm_fn : str
        The simple somatic mutation file

    rescale_depth : bool, optional
        A flag for whether or not to rescale the read depth for each variant using the average across each sample.

    Returns
    -------
    dictionary
        A dictionary where the keys are unique variant 'id' values and the value is a dictionary for each variant
        containing the variant's 'id' (unique identifier), 'name' (string identifier), 
        'var_reads' (array of variants reads for each sample),  'total_reads' (array of total reads for each sample)
        'omega_v' (array of variant read probabilities for each sample)

    """
    variants = {}

    with open(ssm_fn) as f:
        reader = csv.DictReader(f, delimiter='\t')

        for row in reader:

            variant = {
                Variants_Keys.ID: row[SSM_Columns.ID],
                Variants_Keys.NAME: row[SSM_Columns.NAME],
                Variants_Keys.VAR_READS: extract_nums(row[SSM_Columns.VAR_READS], np.int32),
                Variants_Keys.TOTAL_READS: extract_nums(row[SSM_Columns.TOTAL_READS], np.int32),
                Variants_Keys.OMEGA_V: extract_nums(row[SSM_Columns.VAR_READ_PROB], np.float32),
            }

            assert np.all(variant[Variants_Keys.TOTAL_READS] >= variant[Variants_Keys.VAR_READS]), \
                    "var_reads cannot be larger than total_reads"
            assert np.all(0 <= variant[Variants_Keys.OMEGA_V]) and np.all(variant[Variants_Keys.OMEGA_V] <= 1), \
                    "omega_v must be some float between 0 and 1"

            variant[Variants_Keys.REF_READS] = variant[Variants_Keys.TOTAL_READS] - variant[Variants_Keys.VAR_READS]
            T = ma.masked_equal(variant[Variants_Keys.TOTAL_READS], 0)
            variant[Variants_Keys.VAF] = np.array(variant[Variants_Keys.VAR_READS] / T)

            assert variant[Variants_Keys.ID] not in variants, \
                    "Cannot have variants with the same ID, variant %s occurs more than once" % variant[Variants_Keys.ID]
            variants[variant[Variants_Keys.ID]] = variant

    # rescale read depth using average across samples
    if rescale_depth:
        vids = extract_vids(variants)
        V = np.array([variants[vid][Variants_Keys.VAR_READS] for vid in vids])
        T = np.array([variants[vid][Variants_Keys.TOTAL_READS] for vid in vids])
        
        VAFs = np.divide(V, T, where=T>0)
        T = np.maximum(0,np.rint(np.tile(T.mean(axis=0), (T.shape[0],1))).astype(np.int32))
        V = np.maximum(0,np.rint(VAFs*T).astype(np.int32))

        for idx,vid in enumerate(vids):
            variants[vid][Variants_Keys.VAR_READS] = V[idx,:]
            variants[vid][Variants_Keys.TOTAL_READS] = T[idx,:]

    S = len(next(iter(variants.values()))[Variants_Keys.VAR_READS])
    for vid, V in variants.items():
        for K in (Variants_Keys.VAR_READS, Variants_Keys.TOTAL_READS, Variants_Keys.OMEGA_V):
            assert len(V[K]) == S, '%s for %s is of length %s, but %s expected' % (K, vid, len(V[K]), S)

    return variants

def remove_garbage(variants, garbage):
    """Removes garbage variants from dictionary of variants
    
    Parameters
    ----------
    variants : dictionary
        A dictionary where the keys are unique variant 'id' values and the value is a dictionary for each variant
        containing the variant's 'id' (unique identifier), 'name' (string identifier), 
        'var_reads' (array of variants reads for each sample),  'total_reads' (array of total reads for each sample)
        'omega_v' (array of variant read probabilities for each sample)
    garbage : list 
        A list of variant 'id' values to be removed from the 'variants' dictionary

    Returns
    -------
    dictionary
        A 'variants' dictionary (same as what's returned by load_ssms) 
        with the variants listed in the garbage parameter removed
    """
    assert set(garbage).issubset(set(variants.keys())), \
           "Garbage variants must be in the dictionary of variants"
    cleaned = dict(variants)
    for vid in garbage:
        del cleaned[vid]
    return cleaned

def load_params(params_fn):
    """Loads a params file into a dictionary
    
    Parameters
    ----------
    params_fn : str
        The parameters file 

    Returns
    -------
    dictionary
        A dictionary where each of the key, value pairs are the same as those listed in the params_fn file
    """
    if params_fn is None:
        return {}
    with open(params_fn) as P:
        return json.load(P)

def load_ssms_and_params(ssm_fn, params_fn, remove_garb=True, rescale_depth=False):
    """Loads ssm file and params file
    
    Parameters
    ----------
    ssm_fn : str
        The simple somatic mutation file
    params_fn : str
        The parameters file 

    remove_garb : bool, optional
        A flag to remove garbage from the 'variants' dictionary (default is True)
    """
    variants = load_ssm(ssmfn, rescale_depth)
    params = load_params(paramsfn)
    if PARAMS_Columns.GARBAGE not in params:
        params[PARAMS_Columns.GARBAGE] = []
    if remove_garb:
        variants = remove_garbage(variants, params[PARAMS_Columns.GARBAGE])
    return (variants, params)

def write_ssms(variants, ssm_fn):
    """Writes a set of variants along with their associated read 
    count and copy number information to an ssm file
    
    Parameters
    ----------
    variants : dictionary 
        A dictionary where the keys are unique variant 'id' values and the value is a dictionary for each variant
        containing the variant's 'id' (unique identifier), 'name' (string identifier), 
        'var_reads' (array of variants reads for each sample),  'total_reads' (array of total reads for each sample)
        'omega_v' (array of variant read probabilities for each sample)

    ssm_fn : str
        The simple somatic mutation file

    Returns
    -------
    None
    """
    keys = (
            SSM_Columns.ID, 
            SSM_Columns.NAME, 
            SSM_Columns.VAR_READS, 
            SSM_Columns.TOTAL_READS, 
            SSM_Columns.VAR_READ_PROB
    )
    with open(ssm_fn, 'w') as f:
        print(*keys, sep='\t', file=f)
        for variant in variants.values():
            variant = dict(variant)
            for k in (Variants_Keys.VAR_READS, Variants_Keys.TOTAL_READS, Variants_Keys.OMEGA_V):
                variant[k] = ','.join([str(val) for val in variant[k]])
            variant[SSM_Columns.VAR_READ_PROB] = variant[Variants_Keys.OMEGA_V]
            print(*[variant[k] for k in keys], sep='\t', file=f)

def write_params(params, params_fn):
    """Writes a set of variants along with their associated read 
    count and copy number information to an ssm file
    
    Parameters
    ----------
    params : dictionary 
        A dictionary that contains a set of key/value pairs to write to a file as a JSON string

    params_fn : str
        The parameters file (.params.json) to write the params to

    Returns
    -------
    None
    """
    json_params = json.dumps(params)
    with open(params_fn, "w") as outfile:
        outfile.write(json_params)