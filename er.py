import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd

from eralchemy import render_er

from sqlalchemy import (MetaData, Table, Column)    
metadata = MetaData()

filename = 'mymodel.png'
render_er(metadata, filename)
imgplot = plt.imshow(mpimg.imread(filename))
plt.rcParams["figure.figsize"] = (15,10)
plt.show()
