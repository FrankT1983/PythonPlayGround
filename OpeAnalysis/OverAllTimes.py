# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
#pd.set_option('display.mpl_style', 'default') # Make the graphs a bit prettier


# In[2]:

stats = pd.read_csv('overallTimes.csv', index_col=False, sep='\t' )
stats


# In[11]:

stat_table = pd.pivot_table(stats, index=['Benchmark', "Delay", "WF"] , aggfunc=np.average)
del stat_table["Calc"]
del stat_table["Calc x times"]
del stat_table["init time"]
del stat_table["input prep"]
del stat_table["loadImage"]
del stat_table["load image x times"]
del stat_table["output"]
del stat_table["output x times"]

stat_table


# In[12]:

stat_table.to_csv("overall_averaged.csv")

