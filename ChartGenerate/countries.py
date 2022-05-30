import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import ticker
from io import BytesIO
import ctypes
import pandas as pd


d = pd.read_csv('../test/owid-covid-data.csv')
for i in d:
    print(i, end=' ')
# countries = d.loc[:, 'iso_code']
# countries = countries.drop_duplicates()

print(d.shape)
print(len(d.index))

