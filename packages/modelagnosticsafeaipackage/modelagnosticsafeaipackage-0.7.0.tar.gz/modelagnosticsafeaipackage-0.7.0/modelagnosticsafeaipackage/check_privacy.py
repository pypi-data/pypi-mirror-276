import pandas as pd
import numpy as np
import scipy
from .utils.util import _num, _den, _test_delta_function
from .check_accuracy import rga

def rgp(yhat, yhat_rm):
    """
    ### RANK GRADUATION PRIVACY (RGP) MEASURE ###
    Function for the RGP measure computation
    """      
    rgp = rga(yhat, yhat_rm)
    return rgp


def rgp_statistic_test(yhat, yhat_rm):
    """
    RGP based test for comparing the ordering of the ranks related to the full model with that of the
    reduced model without the observation of interest
    """
    yhat = np.array(yhat)
    yhat_rm = np.array(yhat_rm)
    
    # Compute the number of samples
    n = len(yhat)
    
    # Compute jackknife results
    jk_results = []
    for i in range(n):
        # Use numpy indexing to exclude the i-th sample
        jk_yhat = np.delete(yhat, i)
        jk_yhat_rm = np.delete(yhat_rm, i)
        
        # Calculate delta function using optimized approach
        delta_statistic = _test_delta_function(jk_yhat, jk_yhat_rm)
        jk_results.append(delta_statistic)
    
    se = np.sqrt(((n-1)/n)*(sum([(x-np.mean(jk_results))**2 for x in jk_results])))
    z = (_den(  yhat)-_num(  yhat,yhat_rm))/se
    p_value = 2*scipy.stats.norm.cdf(-abs(z))
    return p_value