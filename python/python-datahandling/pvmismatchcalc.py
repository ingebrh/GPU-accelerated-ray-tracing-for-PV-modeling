# -*- coding: utf-8 -*-
"""
Created on Mon May 12 12:24:06 2025

@author: ingeb
"""

import pandas as pd
import numpy as np
import pvmismatch as pv
import os
import matplotlib.pyplot as plt

basedir = 'C:\\Users\\ingeb\\Documents\\Master\\applications\\bf_files\\results\\'
#change as we go

standard =np.array([[0,	23,	24,	47,	48,	71],
                [1,	22,	25,	46,	49,	70],
                [2,	21,	26,	45,	50,	69],
                [3,	20,	27,	44,	51,	68],
                [4,	19,	28,	43,	52,	67],
                [5,	18,	29,	42,	53,	66],
                [6,	17,	30,	41,	54,	65],
                [7,	16,	31,	40,	55,	64],
                [8,	15,	32,	39,	56,	63],
                [9,	14,	33,	38,	57,	62],
                [10,13,	34,	37,	58,	61],
                [11,12,	35,	36,	59,	60]])








def mismatch(filedir, bififactor, xcells, ycells, xsenpcell, ysenpcell,\
             basedir = basedir, standard = standard):
    """
    Calculates pmp from module using PVMismatch, as well as average front
    and back irradiances.
    Created to read results files made with bifacial_radiance
    
    Parameters
    ----------
    filedir : string
        directory from basedir
    bififactor : TYPE
        bifaciality factor for the backside
    xcells : TYPE
        number of cells along the x-direction (width) of the module
    ycells : TYPE
        number of cells along the y-direction (slant height) of the module
    xsenpcell : TYPE
        number of sensors per cell in the x-direction of the module
    ysenpcell : TYPE
        number of sensors per cell in the y-direction of the module

    Returns
    -------
    None. Saves a file in 'bf_files' folder from the python file directory

    """
    if xcells > ycells:
        xc = ycells
        yc = xcells
        xs = xsenpcell
        ys = ysenpcell
        stdpl = standard.transpose()
    else:
        xc = xcells
        yc = ycells
        xs = xsenpcell
        ys = ysenpcell
        stdpl = standard
    
    
    #set directory
    fulldir = basedir + filedir
    nameext = str(filedir[:-1])
    
    filelist = sorted(os.listdir(fulldir))
    output = pd.DataFrame()
    
    
    for x in range(filelist.__len__()):
        #create empty dataframe
        singleout = pd.DataFrame(index = [filelist[x]])
        #get file x from directory
        df = pd.read_csv(fulldir + filelist[x])[['Wm2Front', 'Wm2Back']]
        #gather front and back irradiances
        frontirr = df['Wm2Front'].to_numpy()
        backirr = df['Wm2Back'].to_numpy()
        
        #sum over irradiances on each cell
        cell_irr_front = np.transpose(frontirr.reshape(xc, xs, yc, ys).sum(axis=(1,3)))/16
        cell_irr_back = np.transpose(backirr.reshape(xc, xs, yc, ys).sum(axis=(1,3)))/16
        
        #flip the arrays to conform to standard portrait layout
        cell_irr_front = np.flipud(cell_irr_front)
        cell_irr_back = np.flipud(cell_irr_back)
        
        avgfrontirr = cell_irr_front.sum()/72
        avgbackirr = cell_irr_back.sum()/72
        
        
        totirr = cell_irr_front + cell_irr_back*bififactor
        
        #create pvmismatch positioning of cells
        pos = pv.pvmismatch_lib.pvmodule.STD72
        #create pvmismatch module
        mod=pv.pvmismatch_lib.pvmodule.PVmodule(cell_pos=pos)
        #create pvmismatch system
        sys = pv.pvsystem.PVsystem(numberStrs=1, numberMods=1, pvmods=mod)
        #set irradiances
        sys.setSuns({0: {0: [totirr/1000, stdpl]}})
        #get power maxpoint
        pmp=sys.Pmp
        
        
        singleout['pmp'] = pmp
        singleout['avgfrontirr'] = avgfrontirr
        singleout["avgbackirr"] = avgbackirr
        
        output = pd.concat([output, singleout])
        #pd.concat
        print(x)
    
    output.to_csv('bf_files\\' + nameext +'-results.csv')
        
        

mismatch('', 0.9, 6, 12, 4, 4)

"""        
mismatch('10deg\\', 0.9, 6, 12, 4, 4)
mismatch('15deg\\', 0.9, 6, 12, 4, 4)
mismatch('20deg\\', 0.9, 6, 12, 4, 4)
mismatch('30deg\\', 0.9, 6, 12, 4, 4)
mismatch('45deg\\', 0.9, 6, 12, 4, 4)
mismatch('60deg\\', 0.9, 6, 12, 4, 4)
mismatch('60deg_close\\', 0.9, 6, 12, 4, 4)
mismatch('60deg_far\\', 0.9, 6, 12, 4, 4)
"""