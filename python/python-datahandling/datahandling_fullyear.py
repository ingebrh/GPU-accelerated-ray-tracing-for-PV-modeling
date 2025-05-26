# -*- coding: utf-8 -*-
"""
Created on Sun May 11 11:01:50 2025

@author: ingeb
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

mainfolder = 'C:\\Users\\ingeb\\Documents\\Master\\applications\\bf_files\\'


"""
-------------------------------------------------------------------------------
SENSOR POINT RELATIVE ERRORS
"""
def plotsingledetailed(RADFILE, ACCFILE, frontorback = 'back', text = '', yearly = False):
    if frontorback == 'back':
        key = 'Wm2Back'
    else:
        key = 'Wm2Front'
    
    
    dfERROR = 100*(ACCFILE - RADFILE)/RADFILE
    
    backerror1 = dfERROR[key].to_numpy()
    backRAD = RADFILE[key].to_numpy()
    backACC = ACCFILE[key].to_numpy()
    
    image1 = np.transpose(backRAD.reshape(24,48))
    image2 = np.transpose(backACC.reshape(24,48))
    image3 = np.transpose(backerror1.reshape(24,48))
    
    fig, (ax0, ax1, ax2) = plt.subplots(1,3, figsize=(8.6,4.4))
    fig.suptitle('Sensor point irradiance ' + text)
    
    vmin = np.min([np.min(image1),np.min(image2)])
    vmax = np.max([np.max(image1),np.max(image2)])
    
    R = ax0.pcolor(image1, shading = 'flat', vmin = vmin, vmax = vmax, snap = True)
    ax0.set_title('RADIANCE very high \n (W/$m^2$)')
    for xi in range(4,24,4):
        ax0.axvline(xi, ymin = 0, ymax = 2, color = 'k', linewidth = 0.45)
    for yi in range(4,48,4):
        ax0.axhline(yi, xmin = 0, xmax = 1, color = 'k', linewidth = 0.45)
    fig.colorbar(R, ax = ax0, format = '%3.2f')
    ax0.set_xticks([0,6,12,18,24], ['0','$\\leftarrow$W','0.5','E$\\rightarrow$','1'])
    ax0.set_yticks([0,24,48], ['0','1','2'])
    ax0.set_xlabel('width (m)')
    ax0.set_ylabel('slant height (m)')
    
    
    
    A = ax1.pcolor(image2, shading = 'flat', vmin = vmin, vmax = vmax, snap = True)
    ax1.set_title('ACCELERAD low \n (W/$m^2$)')
    for xi in range(4,24,4):
        ax1.axvline(xi, ymin = 0, ymax = 2, color = 'k', linewidth = 0.45)
    for yi in range(4,48,4):
        ax1.axhline(yi, xmin = 0, xmax = 1, color = 'k', linewidth = 0.45)
    fig.colorbar(A, ax = ax1, format = '%3.2f')
    ax1.set_xticks([0,6,12,18,24], ['0','$\\leftarrow$W','0.5','E$\\rightarrow$','1'])
    ax1.set_yticks([0,24,48], ['0','1','2'])
    ax1.set_xlabel('width (m)')
    ax1.set_ylabel('slant height (m)')
    
    
    
    re = ax2.pcolor(image3, shading = 'flat', snap = True)
    ax2.set_title('Relative \n error (%)')
    for xi in range(4,24,4):
        ax2.axvline(xi, ymin = 0, ymax = 2, color = 'k', linewidth = 0.45)
    for yi in range(4,48,4):
        ax2.axhline(yi, xmin = 0, xmax = 1, color = 'k', linewidth = 0.45)
    fig.colorbar(re, ax = ax2, format = '% 2.3f')
    ax2.set_xticks([0,6,12,18,24], ['0','$\\leftarrow$W','0.5','E$\\rightarrow$','1'])
    ax2.set_yticks([0,24,48], ['0','1','2'])
    ax2.set_xlabel('width (m)')
    ax2.set_ylabel('slant height (m)')
    
    
    
    plt.tight_layout()
    
    plt.show()
    
    
    """
    -------------------------------------------------------------------------------
    CELL LEVEL RELATIVE ERRORS
    """
    
    #arr = np.array([[2,4,8,16], [1,3,7,15]])
    
    #avgirr = (arr_in.reshape(nycells, nysenpercel, nxcells, nxsenpercel)).sum(axis = (1,3))
    
    image4 = np.transpose(backRAD.reshape(6, 4, 12, 4).sum(axis=(1,3)))/16
    image5 = np.transpose(backACC.reshape(6, 4, 12, 4).sum(axis=(1,3)))/16
    image6 = 100*(image5 - image4)/image4
    #image6 = np.transpose(backerror1.reshape(6, 4, 12, 4).sum(axis=(1,3)))/16
    #image7 = np.transpose(backerror1.reshape(6, 4, 12, 4).std(axis=(1,3)))
    
    
    
    fig, (ax0, ax1, ax2) = plt.subplots(1,3, figsize=(8.6,4.4))
    fig.suptitle('Cell irradiance ' + text)
    
    vmin = np.min([np.min(image4),np.min(image5)])
    vmax = np.max([np.max(image4),np.max(image5)])
    
    R = ax0.pcolor(image4, shading = 'flat', vmin = vmin, vmax = vmax, snap = True)
    ax0.set_title('RADIANCE very high \n (W/$m^2$)')
    for xi in range(1,6):
        ax0.axvline(xi, ymin = 0, ymax = 2, color = 'k', linewidth = 0.45)
    for yi in range(1,12):
        ax0.axhline(yi, xmin = 0, xmax = 1, color = 'k', linewidth = 0.45)
    fig.colorbar(R, ax = ax0, format = '%3.2f')
    ax0.set_xticks([0,1.5,3,4.5,6], ['0','$\\leftarrow$W','0.5','E$\\rightarrow$','1'])
    ax0.set_yticks([0,6,12], ['0','1','2'])
    ax0.set_xlabel('width (m)')
    ax0.set_ylabel('slant height (m)')
    
    
    
    A = ax1.pcolor(image5, shading = 'flat', vmin = vmin, vmax = vmax, snap = True)
    ax1.set_title('ACCELERAD low \n (W/$m^2$)')
    for xi in range(1,6):
        ax1.axvline(xi, ymin = 0, ymax = 2, color = 'k', linewidth = 0.45)
    for yi in range(1,12):
        ax1.axhline(yi, xmin = 0, xmax = 1, color = 'k', linewidth = 0.45)
    fig.colorbar(A, ax = ax1, format = '%3.2f')
    ax1.set_xticks([0,1.5,3,4.5,6], ['0','$\\leftarrow$W','0.5','E$\\rightarrow$','1'])
    ax1.set_yticks([0,6,12], ['0','1','2'])
    ax1.set_xlabel('width (m)')
    ax1.set_ylabel('slant height (m)')
    
    
    
    re = ax2.pcolor(image6, shading = 'flat', snap = True)
    ax2.set_title('Relative \n error (%)')
    for xi in range(1,6):
        ax2.axvline(xi, ymin = 0, ymax = 2, color = 'k', linewidth = 0.45)
    for yi in range(1,12):
        ax2.axhline(yi, xmin = 0, xmax = 1, color = 'k', linewidth = 0.45)
    fig.colorbar(re, ax = ax2, format = '% 2.3f')
    ax2.set_xticks([0,1.5,3,4.5,6], ['0','$\\leftarrow$W','0.5','E$\\rightarrow$','1'])
    ax2.set_yticks([0,6,12], ['0','1','2'])
    ax2.set_xlabel('width (m)')
    ax2.set_ylabel('slant height (m)')
    
    """
    #Standard deviation doesnt really give a lot more info than can be
    #found by comparing relative and mean relative error plots.
    #It is therefore scrapped
    sd = ax3.pcolor(image7, shading = 'flat')
    ax3.set_title('Standard \n deviation (%)')
    fig.colorbar(sd, ax = ax3)
    ax3.set_xticks([0,3,6], ['0','0.5','1'])
    ax3.set_yticks([0,6,12], ['0','1','2'])
    ax3.set_xlabel('width (m)')
    ax3.set_ylabel('slant height (m)')
    """
    
    plt.tight_layout()
    
    plt.show()

#plotsingledetailed(MOD3RADirr, MOD3ACCirr)

#backerror1 = df1ERROR['Wm2Back'].to_numpy()



"""
--------------------------------------------------------------------------
import data
"""


#RADmismatch = mainfolder + 'results_old\\' + 'mismatch_results10-90-RAD.csv'
#ACCmismatch = mainfolder + 'results_old\\' + 'mismatch_results10-90-ACC.csv'

#RADmismatchdf = pd.read_csv(RADmismatch)

#ACCmismatchdf = pd.read_csv(ACCmismatch)


MOD1RADirr = pd.DataFrame()
MOD1RADtot = pd.DataFrame()

MOD1ACCirr = pd.DataFrame()
MOD1ACCtot = pd.DataFrame()


MOD2RADirr = pd.DataFrame()
MOD2RADtot = pd.DataFrame()

MOD2ACCirr = pd.DataFrame()
MOD2ACCtot = pd.DataFrame()


MOD3RADirr = pd.DataFrame()
MOD3RADtot = pd.DataFrame()

MOD3ACCirr = pd.DataFrame()
MOD3ACCtot = pd.DataFrame()


MOD4RADirr = pd.DataFrame()
MOD4RADtot = pd.DataFrame()

MOD4ACCirr = pd.DataFrame()
MOD4ACCtot = pd.DataFrame()


MOD5RADirr = pd.DataFrame()
MOD5RADtot = pd.DataFrame()

MOD5ACCirr = pd.DataFrame()
MOD5ACCtot = pd.DataFrame()





ACCfolder = mainfolder + 'results_old\\' + '10-90-ACC\\'
#ACCfolder = mainfolder + 'results\\'


#1:
#RADfolder = mainfolder + 'results_old\\' + '10-90-RAD\\'
#filenamebase = 'irr_10-90deg_'

#2:
#RADfolder = mainfolder + 'results_old\\' + 'specialhours-high\\'
#filenamebase = 'irr_10-90deg_'

#3:
RADfolder = mainfolder + 'results\\'
filenamebaseRAD = 'deg_very_high_'
filenamebase = 'irr_10-90deg_'

#cmd = "rtrace -i -ab 2 -aa .1 -ar 256 -ad 2048 -as 256 -h -oovs "

#RADfolder = mainfolder + 'results_old\\' + '10-90-RAD-SICK\\'
#cmd = "rtrace -i -ab 3 -aa .08 -ar 512 -ad 4096 -as 512 -h -oovs "


#RADfolder = mainfolder + 'results_old\\' + '10-90-RAD-INSANE\\'
#cmd = "rtrace -i -ab 3 -aa .08 -ar 512 -ad 8192 -as 1024 -h -oovs "


# list spechours as [10deg, 30deg, 50deg, 70deg, 90deg]

spechours = [2479, 1519, 2478, 2135, 2005]

datecount = 0
#dates = ['h1929', 'h2005', 'h2098', 'h2157', 'h2479']


nhours = 4624#4624 
for x in spechours:
    if len(str(x)) == 1:
         num = '000' + str(x)
    elif len(str(x)) == 2:
         num = '00' + str(x)
    elif len(str(x)) == 3:
         num = '0' + str(x)
    else:
         num = str(x) 
    
    filenamestart = filenamebase + num + '_mod_'
    
    if filenamebaseRAD == 'deg_very_high_':
        filenamestartRAD = filenamebaseRAD + num + '_mod_'
        modif1 = 'irr_10'
        modif2 = 'irr_30'
        modif3 = 'irr_50'
        modif4 = 'irr_70'
        modif5 = 'irr_90'
        
        try:
            df1RAD = pd.read_csv(RADfolder + modif1 + filenamestartRAD + '000.csv')[['Wm2Front', 'Wm2Back']]
            MOD1RADtot = MOD1RADtot.add(df1RAD, fill_value = 0)
            df1ACC = pd.read_csv(ACCfolder + filenamestart + '000.csv')[['Wm2Front', 'Wm2Back']]
            MOD1ACCtot = MOD1ACCtot.add(df1ACC, fill_value = 0)
        except FileNotFoundError:
            print('filenotfound', x, modif1)    
        try:
            df2RAD = pd.read_csv(RADfolder + modif2 + filenamestartRAD + '000.csv')[['Wm2Front', 'Wm2Back']]
            MOD2RADtot = MOD2RADtot.add(df2RAD, fill_value = 0)
            df2ACC = pd.read_csv(ACCfolder + filenamestart + '001.csv')[['Wm2Front', 'Wm2Back']]
            MOD2ACCtot = MOD2ACCtot.add(df2ACC, fill_value = 0)
        except FileNotFoundError:
            print('filenotfound', x, modif2)
        try:    
            df3RAD = pd.read_csv(RADfolder + modif3 + filenamestartRAD + '000.csv')[['Wm2Front', 'Wm2Back']]
            MOD3RADtot = MOD3RADtot.add(df3RAD, fill_value = 0)
            df3ACC = pd.read_csv(ACCfolder + filenamestart + '002.csv')[['Wm2Front', 'Wm2Back']]
            MOD3ACCtot = MOD3ACCtot.add(df3ACC, fill_value = 0)
        except FileNotFoundError:
            print('filenotfound', x, modif3)
        try:    
            df4RAD = pd.read_csv(RADfolder + modif4 + filenamestartRAD + '000.csv')[['Wm2Front', 'Wm2Back']]
            MOD4RADtot = MOD4RADtot.add(df4RAD, fill_value = 0)
            df4ACC = pd.read_csv(ACCfolder + filenamestart + '003.csv')[['Wm2Front', 'Wm2Back']]
            MOD4ACCtot = MOD4ACCtot.add(df4ACC, fill_value = 0)
        except FileNotFoundError:
            print('filenotfound', x, modif4)
        try:    
            df5RAD = pd.read_csv(RADfolder + modif5 + filenamestartRAD + '000.csv')[['Wm2Front', 'Wm2Back']]
            MOD5RADtot = MOD5RADtot.add(df5RAD, fill_value = 0)
            df5ACC = pd.read_csv(ACCfolder + filenamestart + '004.csv')[['Wm2Front', 'Wm2Back']]
            MOD5ACCtot = MOD5ACCtot.add(df5ACC, fill_value = 0)
        except FileNotFoundError:
            print('filenotfound', x, modif5)
        
    else:
        filenamestartRAD = filenamestart
        modif1 = None
        modif2 = None
        modif3 = None
        modif4 = None
        modif5 = None
    
        df1RAD = pd.read_csv(RADfolder + modif1 + filenamestartRAD + '000.csv')[['Wm2Front', 'Wm2Back']]
        MOD1RADtot = MOD1RADtot.add(df1RAD, fill_value = 0)
        df1ACC = pd.read_csv(ACCfolder + filenamestart + '000.csv')[['Wm2Front', 'Wm2Back']]
        MOD1ACCtot = MOD1ACCtot.add(df1ACC, fill_value = 0)
        
        df2RAD = pd.read_csv(RADfolder + modif2 + filenamestartRAD + '001.csv')[['Wm2Front', 'Wm2Back']]
        MOD2RADtot = MOD2RADtot.add(df2RAD, fill_value = 0)
        df2ACC = pd.read_csv(ACCfolder + filenamestart + '001.csv')[['Wm2Front', 'Wm2Back']]
        MOD2ACCtot = MOD2ACCtot.add(df2ACC, fill_value = 0)
        
        df3RAD = pd.read_csv(RADfolder + modif3 + filenamestartRAD + '002.csv')[['Wm2Front', 'Wm2Back']]
        MOD3RADtot = MOD3RADtot.add(df3RAD, fill_value = 0)
        df3ACC = pd.read_csv(ACCfolder + filenamestart + '002.csv')[['Wm2Front', 'Wm2Back']]
        MOD3ACCtot = MOD3ACCtot.add(df3ACC, fill_value = 0)
        
        df4RAD = pd.read_csv(RADfolder + modif4 + filenamestartRAD + '003.csv')[['Wm2Front', 'Wm2Back']]
        MOD4RADtot = MOD4RADtot.add(df4RAD, fill_value = 0)
        df4ACC = pd.read_csv(ACCfolder + filenamestart + '003.csv')[['Wm2Front', 'Wm2Back']]
        MOD4ACCtot = MOD4ACCtot.add(df4ACC, fill_value = 0)
        
        df5RAD = pd.read_csv(RADfolder + modif5 + filenamestartRAD + '004.csv')[['Wm2Front', 'Wm2Back']]
        MOD5RADtot = MOD5RADtot.add(df5RAD, fill_value = 0)
        df5ACC = pd.read_csv(ACCfolder + filenamestart + '004.csv')[['Wm2Front', 'Wm2Back']]
        MOD5ACCtot = MOD5ACCtot.add(df5ACC, fill_value = 0)
    
    if x == spechours[0]:
        plotsingledetailed(df1RAD, df1ACC, text = 'h' + str(x) + ' 10 degrees back')
        plotsingledetailed(df1RAD, df1ACC, 'a', text = 'h' + str(x) + ' 10 degrees front')
    elif x == spechours[1]:
        plotsingledetailed(df2RAD, df2ACC, text = 'h' + str(x) + ' 30 degrees back')
        plotsingledetailed(df2RAD, df2ACC, 'a', text = 'h' + str(x) + ' 30 degrees front')
    elif x == spechours[2]:
        plotsingledetailed(df3RAD, df3ACC, text = 'h' + str(x) + ' 50 degrees back')
        plotsingledetailed(df3RAD, df3ACC, 'a', text = 'h' + str(x) + ' 50 degrees front')
    elif x == spechours[3]: 
        plotsingledetailed(df4RAD, df4ACC, text = 'h' + str(x) + ' 70 degrees back')
        plotsingledetailed(df4RAD, df4ACC, 'a', text = 'h' + str(x) + ' 70 degrees front')        
    elif x == spechours[4]:
        plotsingledetailed(df5RAD, df5ACC, text = 'h' + str(x) + ' 90 degrees back')
        plotsingledetailed(df5RAD, df5ACC, 'a', text = 'h' + str(x) + ' 90 degrees front')
    
        
    datecount += 1
    
"""
if x in spechours:
    
    plotsingledetailed(df1RAD, df1ACC, text = dates[datecount] + ' 10 degrees back')
    plotsingledetailed(df2RAD, df2ACC, text = dates[datecount] + ' 30 degrees back')
    plotsingledetailed(df3RAD, df3ACC, text = dates[datecount] + ' 50 degrees back')
    plotsingledetailed(df4RAD, df4ACC, text = dates[datecount] + ' 70 degrees back')
    plotsingledetailed(df5RAD, df5ACC, text = dates[datecount] + ' 90 degrees back')
    
    
    plotsingledetailed(df1RAD, df1ACC, 'a', text = dates[datecount] + ' 10 degrees front')
    plotsingledetailed(df2RAD, df2ACC, 'a', text = dates[datecount] + ' 30 degrees front')
    plotsingledetailed(df3RAD, df3ACC, 'a', text = dates[datecount] + ' 50 degrees front')
    plotsingledetailed(df4RAD, df4ACC, 'a', text = dates[datecount] + ' 70 degrees front')
    plotsingledetailed(df5RAD, df5ACC, 'a', text = dates[datecount] + ' 90 degrees front')
"""        

"""
plotsingledetailed(MOD1RADtot, MOD1ACCtot, text = 'yearly 10 degrees back')
plotsingledetailed(MOD2RADtot, MOD2ACCtot, text = 'yearly 30 degrees back')
plotsingledetailed(MOD3RADtot, MOD3ACCtot, text = 'yearly 50 degrees back')
plotsingledetailed(MOD4RADtot, MOD4ACCtot, text = 'yearly 70 degrees back')
plotsingledetailed(MOD5RADtot, MOD5ACCtot, text = 'yearly 90 degrees back')


plotsingledetailed(MOD1RADtot, MOD1ACCtot, 'a', text = 'yearly 10 degrees front')
plotsingledetailed(MOD2RADtot, MOD2ACCtot, 'a', text = 'yearly 30 degrees front')
plotsingledetailed(MOD3RADtot, MOD3ACCtot, 'a', text = 'yearly 50 degrees front')
plotsingledetailed(MOD4RADtot, MOD4ACCtot, 'a', text = 'yearly 70 degrees front')
plotsingledetailed(MOD5RADtot, MOD5ACCtot, 'a', text = 'yearly 90 degrees front')
"""


