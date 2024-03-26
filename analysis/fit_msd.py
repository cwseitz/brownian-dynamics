import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def fit_log_msd(tau,imsds,ndim=3):
    thetas = []
    ntau,ntraj = imsds.shape
    for n in range(ntraj):
        y = np.log10(imsds[:,n])
        slope, intercept, r, p, stderr = \
        stats.linregress(np.log10(tau),y)
        D = np.power(10, intercept) / (2 * ndim)
        alpha = slope; thetas.append([D,alpha])
        yhat = np.log10(2*ndim*D) + alpha*np.log10(tau)
    return np.array(thetas)

