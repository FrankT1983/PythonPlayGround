
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
from scipy import stats
#pd.set_option('display.mpl_style', 'default') # Make the graphs a bit prettier


# In[2]:

data = pd.read_csv('overallTime.txt', index_col=False, sep='\t')
del data["Run"]
del data["Start"]
# In[11]:

keys = data["Nodes"].unique()
keys.sort()
result = []
for i in keys:
    nodeData = data[data["Nodes"] == i]
    runtimeData = nodeData["RuntimeInMillis"]
    runtimeDataMin = runtimeData / (60*1000)
    res_mean, res_var, res_std = stats.bayes_mvs(runtimeDataMin, alpha=0.95)
    result.append([i,res_mean[0],res_mean[1][0],res_mean[1][0]])




# In[12]:
res_Dataframe = pd.DataFrame(result)
res_Dataframe.to_csv("overall_averaged.csv",header=None, index=False)

