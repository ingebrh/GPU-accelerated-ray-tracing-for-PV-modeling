# -*- coding: utf-8 -*-
"""
Created on Mon May 12 16:51:28 2025

@author: ingeb
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

folder = 'C:\\Users\\ingeb\\Documents\\Master\\applications\\bf_files'

systems = ['10-90-ACC', '10-90-RAD']


filename1 = '10-90-ACC' + '-results.csv'
file1 = folder + '\\' + filename1
df1 = pd.read_csv(file1)
Parray1 = df1['pmp'].to_numpy()
totPA1 = Parray1[0::5]
totPA2 = Parray1[1::5]
totPA3 = Parray1[2::5]
totPA4 = Parray1[3::5]
totPA5 = Parray1[4::5]


filename2 = '10-90-RAD' + '-results.csv'
file2 = folder + '\\' + filename2
df2 = pd.read_csv(file2)
Parray2 = df2['pmp'].to_numpy()
totPR1 = Parray2[0::5]
totPR2 = Parray2[1::5]
totPR3 = Parray2[2::5]
totPR4 = Parray2[3::5]
totPR5 = Parray2[4::5]    

data = pd.DataFrame()

data['relerrP1'] = (totPA1 - totPR1)/totPR1
data['relerrP2'] = (totPA2 - totPR2)/totPR2
data['relerrP3'] = (totPA3 - totPR3)/totPR3
data['relerrP4'] = (totPA4 - totPR4)/totPR4
data['relerrP5'] = (totPA5 - totPR5)/totPR5

data['abserrP1'] = totPA1 - totPR1
data['abserrP2'] = totPA2 - totPR2
data['abserrP3'] = totPA3 - totPR3
data['abserrP4'] = totPA4 - totPR4
data['abserrP5'] = totPA5 - totPR5

data['abserrP1'] = (totPA1 - totPR1)
data['abserrP2'] = (totPA2 - totPR2)
data['abserrP3'] = (totPA3 - totPR3)
data['abserrP4'] = (totPA4 - totPR4)
data['abserrP5'] = (totPA5 - totPR5)


fig, ax = plt.subplots(1,1)
ax.scatter()



"""
outfolder = folder + '\\' + 'finished'
outfile = outfolder + '\\' + 'RAD-ACC-pow-err.csv'
data.to_csv(outfile)
"""