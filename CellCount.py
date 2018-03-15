#!/usr/bin/python

import sys
import pandas
import numpy as np

# Auto Detect working matplotlib backend
# see: https://stackoverflow.com/questions/3285193/how-to-switch-backends-in-matplotlib-python
import matplotlib
gui_env = ['TKAgg','GTKAgg','Qt4Agg','WXAgg','agg']
for gui in gui_env:
    try:
        print ("testing " +  gui)
        matplotlib.use(gui,warn=False, force=True)
        from matplotlib import pyplot as plt
        print ("++++ Working: " +  gui)
        break
    except:
        continue


csvPath = "9b50c76c-45d1-429c-8cbb-f8583584bdfd.txt"
savePath = "foo.png"

if (len(sys.argv) > 3):
    csvPath =sys.argv[1]
    savePath = sys.argv[2]
else:
    print("use default parameters, not enough args: " + str(sys.argv))

print("scvPaht: " + csvPath)
print("savePath: " + savePath)


df = pandas.read_csv(csvPath)
count = df[["Z","T"]].groupby(["T"]).count()
nparray = count.reset_index().as_matrix()

print(str(count))

fig, ax = plt.subplots()
ax.plot(nparray[:,0],nparray[:,1] )
fig.savefig(savePath)

plt.show()