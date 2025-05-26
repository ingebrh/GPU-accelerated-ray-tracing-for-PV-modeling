# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 14:11:17 2025

@author: ingeb
"""

import pandas as pd
import numpy as np


folder = 'C:\\Users\\ingeb\\Documents\\Master\\applications\\bf_files'

systems = ['10deg', '15deg', '20deg', '30deg', '45deg', '60deg', '60deg_far', '60deg_close']

for system in systems:
    filename = system + '-results.csv'
    file = folder + '\\' + filename
    df = pd.read_csv(file)
    Parray = df['pmp'].to_numpy()
    totP = []
    for time in range(19):
        totP.append(np.sum(Parray[time*18:time*18+18]))
    df2 = pd.DataFrame(totP, columns=['Pdet'])
    outfolder = folder + '\\' + 'finished'
    outfile = outfolder + '\\' + 'daily' + filename
    df2.to_csv(outfile, index_label= system)