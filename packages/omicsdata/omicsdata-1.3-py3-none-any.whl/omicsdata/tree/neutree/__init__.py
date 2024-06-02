###############################################################################################################
# __init__.py
# 
# Contains the source code for reading/writing 'Neutree' namedtuples 
###############################################################################################################
import pickle, sys, os
from collections import namedtuple
import numpy as np

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from columns import NEUTREE_Columns

# for compatibility with Pairtree, we reuse the Neutree named tuple
Neutree = namedtuple('Neutree', (NEUTREE_Columns.STRUCTS, NEUTREE_Columns.PHIS, NEUTREE_Columns.COUNTS, NEUTREE_Columns.LOGSCORES, NEUTREE_Columns.CLUSTERINGS, NEUTREE_Columns.GARBAGE))

def save(ntree, neutree_fn):
	"""Saves the data for a bulk DNA cancer phylongeny reconstruction in a generalized format
	that's simply a zipped archive containing a namedtuple
	
	Parameters
	----------
	ntree : namedtuple
		the name tuple that will be written to a zipped archive
	neutree_fn : str
		the file name that the ntree namedtuple will be written to

	Returns
	-------
	None
	"""
	N = len(ntree.structs)
	for K in (NEUTREE_Columns.STRUCTS, NEUTREE_Columns.PHIS, NEUTREE_Columns.COUNTS, NEUTREE_Columns.LOGSCORES, NEUTREE_Columns.CLUSTERINGS):
		assert len(getattr(ntree, K)) == N, '%s has length %s instead of %s' % (K, len(getattr(ntree, K)), N)

	# we always expect data in the Neutree archive to be ndarray's
	arr_vals = {K: np.array(getattr(ntree, K)) for K in (NEUTREE_Columns.COUNTS, NEUTREE_Columns.LOGSCORES)}
	ntree = ntree._replace(**arr_vals)

	with open(neutree_fn, 'wb') as F:
		pickle.dump(ntree, F)

def load(neutree_fn):
	"""Loads the Neutree namedtuple from a zipped archive
	
	Parameters
	----------
	neutree_fn : str
		the file name that the ntree namedtuple will be loaded from

	Returns
	-------
	pickle
		a pickle file loaded into memory
	"""
	with open(neutree_fn, 'rb') as F:
		return pickle.load(F)