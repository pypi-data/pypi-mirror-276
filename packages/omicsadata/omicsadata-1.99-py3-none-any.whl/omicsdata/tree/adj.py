import numpy as np

def adj_to_anc(adj, root=0):
    """Converts an adjacency matrix to an ancestry matrix
    
    Parameters
    ----------
    adj : ndarray
        a 2D numpy array that is an adjacency matrix for a graph
    root : int, optional
        the row in the inputted adjacency matrix that corresponds to the root nodes 

    Returns
    -------
    ndarray
        an ancestry matrix for the corresponding adjacency matrix 
    """
    anc = np.copy(adj)
    np.fill_diagonal(anc, 0)
    stack = [root]
    while len(stack) > 0:
        node = stack.pop()
        node_children = np.flatnonzero(anc[node])
        if len(node_children) == 0:
            continue
        node_parents = np.copy(anc[:, node])
        node_parents[node] = 1
        anc[:, node_children] = np.expand_dims(node_parents, 1)
        stack += list(node_children)
    np.fill_diagonal(anc, 1)

    return anc

def adj_to_parents(adj):
    """Converts and adjacency matrix to a parents vector. We assume the inputted adjacency matrix is for a directed graph
    
    Parameters
    ----------
    adj : ndarray
        a 2D numpy array that is an adjacency matrix for a graph 

    Returns
    -------
    ndarray
        an array where each index i represents a node in a graph, and the value at index i is which node is its direct ancestor
    """
    np.fill_diagonal(adj, 0)
    K = len(adj)
    parents = np.full(K-1, np.nan)
    for j in range(1, K):
        ancestor = np.where(adj[:,j] == 1)[0]
        assert len(ancestor) == 1, "Each node must have exactly one direct ancestor"
        parents[j-1] = ancestor
    return parents.astype(np.uint8)