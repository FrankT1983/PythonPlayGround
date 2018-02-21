import sys
import pandas
import matplotlib.pyplot as plt
import numpy as np

csvPath = "9b50c76c-45d1-429c-8cbb-f8583584bdfd.csv"
savePath = "foo.png"

if (len(sys.argv) > 2):
    csvPath =sys.argv[1]

df = pandas.read_csv(csvPath)
count = df[["Z","T"]].groupby(["T"]).count()
nparray = count.reset_index().as_matrix()

fig, ax = plt.subplots()
ax.plot(nparray[:,0],nparray[:,1] )
fig.savefig("foo.png")