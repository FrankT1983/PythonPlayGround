import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import os.path
import csv



def getData(i):
    name ='output' + str(i) + '.csv'
    if not os.path.isfile(name) :
        return np.random.random((10,10))
    with open(name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = []
        for row in reader:
            colData = []
            for col in row:
                colData.append(float(col))
            data.append(colData)
    return np.matrix(data)

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
ret = plt.imshow(getData(0), cmap='hot', interpolation='nearest')


class Index(object):
    ind = 0

    def next(self, event):
        self.ind += 1
        ret.set_data(getData(self.ind))
        plt.draw()

    def prev(self, event):
        self.ind -= 1
        ret.set_data(getData(self.ind))
        plt.draw()



callback = Index()
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous')
bprev.on_clicked(callback.prev)

plt.show()

