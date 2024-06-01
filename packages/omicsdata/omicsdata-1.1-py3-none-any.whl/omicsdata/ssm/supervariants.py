#################################################################################
# supervariants.py
#
# Source file containing functions for creating and manipulating 'supervariants'.
#################################################################################

import numpy as np
import numpy.ma as ma
from collections import namedtuple 

from .common import extract_vids
from .constants import Variants_Keys

# namedtuple defining the fields for a 'Variant'
Variant = namedtuple('Variant', (
  'id',
  'var_reads',
  'ref_reads',
  'total_reads',
  'vaf',
  'omega_v',
))

def convert_variant_dict_to_tuple(variant):
    """Converts a dictionary of variants into a tuple of variants
    
    Parameters
    ----------
    variant : dictionary
        A dictionary containing all of the following keys for a particular variant:
        'id',
        'var_reads',
        'ref_reads',
        'total_reads',
        'vaf',
        'omega_v'

    Returns
    -------
    namedtuple
        A 'Variant' named tuple with all of the same keys as the inputted dictionary
    """
    return Variant(**{K: variant[K] for K in Variant._fields})

def convert_all_variants_to_tuples(variants):
    """Converts a dictionary of variants each of which are represented by a dictionary into a list of
    tuples
    
    Parameters
    ----------
    variants : dictionary
        A dictionary where the keys are unique variant 'id' values and the value is a dictionary for each variant
        containing the variant's 'id' (unique identifier), 'name' (string identifier), 
        'var_reads' (array of variants reads for each sample),  'total_reads' (array of total reads for each sample)
        'omega_v' (array of variant read probabilities for each sample)

    Returns
    -------
    list
        A list of namedtuples for each variant in the variants input. Each value in the list is a 'Variant'
        namedtuple with the following keys: 'id', 'var_reads', 'ref_reads', 'total_reads','vaf','omega_v'

    """
    return [convert_variant_dict_to_tuple(variants[V]) for V in list(variants.keys())]

def make_supervar(name, variants, fill_chr_pos=False):
    """Makes a supervariant given a list of variants
    
    Parameters
    ----------
    name : str
        A name/id value to give the supervariant

    variants : list
        A list of 'variant' dictionaries. Each variant dictionary contains the following keys:'id' (unique identifier), 'name' (string identifier), 
        'var_reads' (array of variants reads for each sample),  'total_reads' (array of total reads for each sample)
        'omega_v' (array of variant read probabilities for each sample)

    fill_chr_pos : bool
        A flag to fill the chromosome and position fields for each supervariant. This will only work 
        if all variant names match the pattern '{chromosome}_{position}'

    Returns
    -------
    dictionary
        A dictionary that has summarizes the information in the list of variants inputted. The supervariant
        has the following (used) keys: 'id' (unique id for supervariant), 'name' (string name of supervariant), 'var_reads' (array of variants reads for each sample),  'total_reads' (array of total reads for each sample)
        'omega_v' (array of variant read probabilities for each sample)
    """
    assert len(variants) > 0, "Cannot make supervariants from an empty list of variants"
    N = np.array([var[Variants_Keys.TOTAL_READS] for var in variants])
    V = np.array([var[Variants_Keys.VAR_READS] for var in variants])
    omega_v = np.array([var[Variants_Keys.OMEGA_V] for var in variants])

    # converts all supervariants to have an omega_v of 0.5
    _, S = N.shape
    N_hat = 2*N*omega_v
    V_hat = np.minimum(V, N_hat)
    omega_v_hat = 0.5 * np.ones(S)

    chrom = None 
    pos = None

    # fill chromosome and position if given flag and the name field matches pattern
    if fill_chr_pos:
        if all([len(var[Variants_Keys.NAME].split("_")) == 2 for var in variants]):
            chrom = np.array([var[Variants_Keys.NAME].split("_")[0] for var in variants])
            pos = np.array([var[Variants_Keys.NAME].split("_")[1] for var in variants])

    supervariant = {
        Variants_Keys.ID:          name,
        Variants_Keys.NAME:        name,
        Variants_Keys.CHROM:       chrom,
        Variants_Keys.POS:         pos,
        Variants_Keys.OMEGA_V:     omega_v_hat,
        Variants_Keys.VAR_READS:   np.round(np.sum(V_hat, axis=0)).astype(np.int32),
        Variants_Keys.TOTAL_READS: np.round(np.sum(N_hat, axis=0)).astype(np.int32),
    }
    supervariant[Variants_Keys.REF_READS] = \
        supervariant[Variants_Keys.TOTAL_READS] - supervariant[Variants_Keys.VAR_READS]
    T = ma.masked_equal(supervariant[Variants_Keys.TOTAL_READS], 0)
    supervariant[Variants_Keys.VAF] = np.array(supervariant[Variants_Keys.VAR_READS] / T)

    return supervariant

def clusters_to_supervars(clusters, variants, fill_chr_pos=False):
    """Converts clusters into supervariants
    
    Parameters
    ----------
    clusters: list
        A list of lists, where each sublist contains the 'id' values for the variants that are in that cluster

    variants : dictionary
        A dictionary where the keys are unique variant 'id' values and the value is a dictionary for each variant
        containing the variant's 'id' (unique identifier), 'name' (string identifier), 
        'var_reads' (array of variants reads for each sample),  'total_reads' (array of total reads for each sample)
        'omega_v' (array of variant read probabilities for each sample)

    fill_chr_pos : bool
        A flag to fill the chromosome and position fields for each supervariant. This will only work 
        if all variant names match the pattern '{chromosome}_{position}'

    Returns
    -------
    dictionary
        A dictionary of supervariants, where the keys are the supervariant 'id' values and the values are a 
        dictionary containing the data for the supervariant
    """
    supervars = {}

    for cluster in clusters:
        assert len(cluster) > 0, "Cannot make a supervariant from an empty list"
        cluster_variants = [variants[vid] for vid in cluster]
        name = 'S%s' % (len(supervars) + 1)
        supervars[name] = make_supervar(name, cluster_variants, fill_chr_pos)

    return supervars

def make_superclusters(supervars):
    """Generates a clustering where each supervariant is in its own cluster
    
    Parameters
    ----------
    supervars : dictionary
        A dictionary of supervariants, where the keys are the supervariant 'id' values and the values are a 
        dictionary containing the data for the supervariant

    Returns
    -------
    list
        A list of lists where each sublist contains a single supervariant
    """
    svids = extract_vids(supervars)
    return [[S] for S in svids]

def supervars_to_binom_params(supervars):
    """Extracts the binomial parameters for each supervariant.
    
    Parameters
    ----------
    supervars : dictionary
        A dictionary of supervariants, where the keys are the supervariant 'id' values and the values are a 
        dictionary containing the data for the supervariant

    Returns
    -------
    ndarray
        An ndarray where each row i = 1,...,n is the variant reads for all m samples for supervariant i, and each column s = 1,...,m is the
        variants reads for supervariant i in sample s.
    ndarray
        An ndarray where each row i = 1,...,n is the total reads for all m samples for supervariant i, and each column s = 1,...,m is the
        total reads for supervariant i in sample s.
    ndarray
        An ndarray where each row i = 1,...,n is the variant read probability for all m samples for supervariant i, and each column s = 1,...,m is the
        variant read probability for supervariant i in sample s.
    """
    svids = extract_vids(supervars)
    V = np.array([supervars[S][Variants_Keys.VAR_READS] for S in svids])
    R = np.array([supervars[S][Variants_Keys.REF_READS] for S in svids])
    omega_v = np.array([supervars[S][Variants_Keys.OMEGA_V] for S in svids])

    assert np.all(omega_v == 0.5), "supervariant omega_v is incorrect"
    return V, R, omega_v
