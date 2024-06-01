##############################################################################
# newick.py
#
# Contains code to convert an adjacency matrix to a Newick tree string.
# Format guidelines: https://en.wikipedia.org/wiki/Newick_format 
##############################################################################

import numpy as np

def adj_to_newick(adj, root=0):
    """Converts an adjacency matrix a Newick Format string
    
    Parameters
    ----------
    adj : ndarray
        a 2D numpy array that is an adjacency matrix for a graph
    root : int, optional
        the row in the inputted adjacency matrix that corresponds to the root nodes 

    Returns
    -------
    string
        a Newick Format string 
    """
    newick_string = ""
    np.fill_diagonal(adj, 0)
    stack = [root]

    while len(stack) > 0:
        node = stack.pop()

        newick_string = str(node) + newick_string

        if (node == "(") or (node == ")") or (node == ","):
            continue

        node_children = np.flatnonzero(adj[node])
        if len(node_children) == 0:
            continue
            
        stack.append("(")
        n = len(node_children)
        for i in range(n):
            stack.append(node_children[i])
            if i < n - 1:
                stack.append(",")
        stack.append(")")

    return newick_string

def save_newick(newick_fn, newick_string):
    """Saves a Newick string to a file

    Parameters
    -----------
    newick_fn : str
        a path to save the Newick file to

    newick_string : str 
        the string that follows the Newick text format

    Returns
    --------
    None
    """
    with open(newick_fn, "w") as f:
        f.write(newick_string)