##############################################################################
# common.py
#
# Source file containing commonly used functions.
##############################################################################

def sort_vids(vids):
    """Extracts the unique numerical value of a variant id (vid).
    Assumes that all vids match the regular expression r's\d+'.
    
    Parameters
    ----------
    vids : list 
        list of 'id' values for variants

    Returns
    -------
    list
        sorted list of only the numeric values of each 'id' from the inputted list of variant 'id' values
    """
    return sorted(vids, key = lambda V: int(V[1:]))

def extract_vids(variants):
    """Extracts the unique numerical value of all variants and sorts them"
    
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
        list of sorted variant 'id' values
    """
    return sort_vids(variants.keys())