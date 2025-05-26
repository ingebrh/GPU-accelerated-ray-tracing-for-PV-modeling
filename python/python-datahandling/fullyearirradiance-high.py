# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 10:27:58 2024

@author: ingeb
"""

"""
params to test:

E-W 10 15 20

S 30 40 50

vert E-W

define bifacial_radiance params after blender model. Use offset.


"""







import bifacial_radiance as br
import pandas as pd
import numpy as np

#DEFINE TEST FOLDER
folder = 'C:\\Users\\ingeb\\Documents\\Master\\applications\\bf_files'

# create basis
run = br.RadianceObj('applications', path = folder)

"""
DEFINE RUN CHARACTERISTICS
"""

#epwfile = run.getEPW(lat = 59.942, lon = 10.721) #Meteorologisk institutt

flname = '\\EPWs\\NOR_Oslo.Fornebu.014880_IWEC.epw'

epwfile = folder + flname

#select some data, yyyy-mm-dd:
#s_date = pd.to_datetime('1983-06-06')
#e_date = pd.to_datetime('1983-06-07')

#metdata = run.readWeatherFile(epwfile, starttime=s_date, endtime=e_date)

metdata = run.readWeatherFile(epwfile)

print(metdata)

run.setGround(0.6) #Concrete albedo


"""
-------------------------------------------------------------------------------
DEFINING THE MODULE AND SCENE PARAMETERS
"""


#Module parameters
moduletype = '10-90'   #Name of module
numpanels = 1           #Modules in y-direction (slant height)
x = 1                   #Width of module
y = 2                   #Length of module
z = 0.002               #Thickness of module


#PV array parameters
row_modules = 1         #The number of modules per row
nrows = 1               #The number of rows 
tot_mods = 5            #The total number of modules
xgap = 0.052            #Gap in x-direction (along row width)
ygap = 0                #Gap in y-direction (along slant height)
zgap = 0                #Gap in z-direction (normal on module front face)
# Tilts:                 10      15      20      30      45      60      90
pitch = 5               #Distance between row centers
# Pitch                   x       x       x       4       5       6       x
clearance = 0.2     #Distance between ground and lower lip under module
# Clearance:              0.1407  0.1473  0.1529  0.3800  0.4827  0.5550  
azim = 180             #Azimuth of system

nhours = 1 #print(metdata) gives 4624 entries

#Raytracing and model parameters
acc = False #Boolean, for using Accelerad or not
#Run with acc = False and nhours = 1 to check if sensors are correctly placed.
modeltype = ['10', '30', '50', '70', '90'] #which 3D model. Used to pull the correct .rad files.
#basename = modeltype +'deg_very_high_'
quadortri = 'quad'
PorL = 'portrait' #portrait or landscape (for mismatch and output)
bififactor = 0.9 #bifaciality factor
numcells = 72 #The number of cells per module
seny = 48 #The number of sensor points along the height of each module per side
senx = 24 #The number of sensor points along the width of each module per side
senpermod = seny*senx #The total number of sensor points per module per side



#hours = [0, 579, 1860]
hours10 = np.array([2479, 1927, 2042, 2651, 2724, 3277, 2196, 3069, 1805, 2347, 1084, 2346, 2080, 3399, 2098, 1679, 2406, 2999, 1984, 1947])
hours30 = np.array([2098, 1519, 2078, 2116, 1986, 2022, 2478, 2850, 1711, 1679, 2027, 1365, 2077, 1366, 1517, 3217, 1965, 2651, 925, 2082])
hours50 = np.array([1929, 2061, 1967, 2116, 3249, 2478, 2289, 2040, 2741, 2653, 1927, 1711, 2309, 2615, 3231, 2850, 2080, 3003, 2899, 3171])
hours70 = np.array([2157, 2135, 1930, 2026, 1984, 3249, 2651, 2740, 3103, 2060, 2138, 3643, 1712, 1782, 925, 818, 2080, 2287, 1638, 1143])
hours90 = np.array([2005, 2158, 3885, 1676, 2593, 3070, 1286, 1711, 2740, 2025, 2518, 2135, 2724, 2595, 2310, 2591, 1588, 2023, 1501, 2882])

hourlist = [hours10, hours30, hours50, hours70, hours90]

"""
CREATE SCENE

Parameters are made up.
"""

# create module:
module = run.makeModule(name = 'module', x=x, y=y, z=z, xgap=xgap,\
                        ygap=ygap, zgap=zgap, numpanels = numpanels)

origins = [-8, -4, 0, 4, 8] #origin on X-axis in meters
n = 0
scenes = []
for k in [10, 30, 50, 70, 90]:
    scenedict = {'tilt': k, 'pitch': pitch, 'clearance_height': clearance,\
                 'azimuth': azim, 'nMods': row_modules, 'nRows': nrows,\
                'originx' : origins[n]}
    scenes.append(run.makeScene(module = module, sceneDict = scenedict))
    n += 1

import time

for systemtestno in range(5):
    hours = hourlist[systemtestno]
    basename = modeltype[systemtestno] +'deg_very_high_'
    
    start_time_full = time.time()
    """
    -------------------------------------------------------------------------------
    THE SCAN DICTIONARIES DO NOT CHANGE, SO WE ONLY NEED TO MAKE ONE DICTIONARY
    AND USE IT IN THE LOOP, INSTEAD OF RECREATING THE WHOLE DICTIONARY EVERY
    TIME AN OCTREE IS MADE. WE MAKE A BOGUS OCTREE FOR THIS PURPOSE
    """
    run.gendaylit(0, metdata)
    bogus_oct = run.makeOct(run.getfilelist(), 'bogus')
    bogus_analysis = br.AnalysisObj(bogus_oct, 'bogus')
    frontpts = ''
    backpts = ''
    
    frontscan, backscan = bogus_analysis.moduleAnalysis(scenes[systemtestno],\
                                modWanted = 1, rowWanted = 1, \
                                sensorsy = seny, sensorsx = senx)
    frontpts += bogus_analysis._linePtsMakeDict(frontscan)
    backpts += bogus_analysis._linePtsMakeDict(backscan)
    """
        if j == 2:
            backfilename = folder + '\\_Back' + '.txt'
            file = open(backfilename, 'w')
            file.write(bogus_analysis._linePtsMakeDict(backscan))
            file.close()
            frontfilename = folder + '\\_Front' + '.txt'
            file = open(frontfilename, 'w')
            file.write(bogus_analysis._linePtsMakeDict(frontscan))
            file.close()
    """
        
        
    
    run.radfiles =['materials\\ground.rad',\
            'objects\\module_C_0.20_rtr_5.00_tilt_10_1modsx1rows_origin-8,0.rad',\
            'objects\\module_C_0.20_rtr_5.00_tilt_30_1modsx1rows_origin-4,0.rad',\
            'objects\\module_C_0.20_rtr_5.00_tilt_50_1modsx1rows_origin0,0.rad',\
            'objects\\module_C_0.20_rtr_5.00_tilt_70_1modsx1rows_origin4,0.rad',\
            'objects\\module_C_0.20_rtr_5.00_tilt_90_1modsx1rows_origin8,0.rad']
    
    """
    ------------------------------------------------------------------------------
    TEST ON WEIRD NODES:
    
    frontpts = "0.020000000000000018 -0.6188495140490987 0.2331954829563649 -0.000 0.766 -0.643"
    backpts = "0.020000000000000018 -0.6157853362766228 0.23062433251761877 0.000 -0.766 0.643"
    """
    
    #REPLACE THE SCENE WITH BLENDER-MADE SCENE. EDIT SCENE NAME:
    """
    #######################################EDIT EDIT EDIT EDIT EDIT EDIT###########
    Replace the radiance-created scene with the blender model
    
    
    scene_name = modeltype + 'deg_' + quadortri + '.rad' #str(row_modules)
    scene_extention = 'objects\\' + scene_name
    run.radfiles =['materials\\ground.rad', scene_extention ]
    """
    time_sensors = time.time() - start_time_full
    
    
    time_octfiles_start = time.time()
    
    """
    -------------------------------------------------------------------------------
    To limit temperature differences in components, we create all octree files
    first, so we only need to load them for the raytracing
    """
    
    for x in hours: #there are 38 hours with daylight*
    # *from print(metdata), one gets 114 entries
        
        run.gendaylit(x, metdata)
        
        
        """
        We have to make sure the files are in order 'alphabetically' for the
        mismatch analysis. The mismatch commands will go through all the csv
        files in a folder in such an order, going 0, 1, 10, 11, 12, ... 19, 2, 20
        and so on. This is like listing it as a, b, ba, bc, bd, ... bz, c, ca, etc.
        Since we want it as 1, 2, 3, ... and we have some thousand points, we need
        to go for 0000, 0001, 0002, 0003, analogue to aaaa, aaab, aaac...
        
        For the dates, we can later use the list of generated skies, as they
        contain the date and time of each sky that was generated.
        """
        
        
        if len(str(x)) == 1:
            name = '000' + str(x)
        elif len(str(x)) == 2:
            name = '00' + str(x)
        elif len(str(x)) == 3:
            name = '0' + str(x)
        else:
            name = str(x)
        
        fullname = basename + name
        
        # create .oct file if it does not exist (!!!)
        import os.path
        
        if not os.path.isfile(folder + '\\' + fullname+'.oct'):
            run.makeOct(run.getfilelist(), fullname)
        else:
            print(fullname+'.oct already exists, skipping')
    
    time_octfiles = time.time() - time_octfiles_start
    
    """
    -------------------------------------------------------------------------------
    We now do raytracing -without- tidying up the output files between simulations
    """
    
    time_analysis_start = time.time()
    
    for x in hours: #there are 38 hours with daylight*
    # *from print(metdata), one gets 114 entries
         
        if len(str(x)) == 1:
             name = '000' + str(x)
        elif len(str(x)) == 2:
             name = '00' + str(x)
        elif len(str(x)) == 3:
             name = '0' + str(x)
        else:
             name = str(x)
             
        fullname = basename + name
        
        octfile = fullname + '.oct'
    
        analysis = br.AnalysisObj(octfile, run.basename)
        
        
        analysis.analysis_custom_3(octfile, fullname, frontpts, backpts,
                                           accelerad = acc, path = folder, accuracy = 'very high')
    
    time_analysis = time.time() - time_analysis_start
    
    """
    -------------------------------------------------------------------------------
    Now, we can tidy up the output files.
    """
    
    time_output_start = time.time()
    
    for x in hours: #there are 38 hours with daylight*
    # *from print(metdata), one gets 114 entries
    
        if len(str(x)) == 1:
             name = '000' + str(x)
        elif len(str(x)) == 2:
             name = '00' + str(x)
        elif len(str(x)) == 3:
             name = '0' + str(x)
        else:
             name = str(x) 
        
        path = folder
        
        fullname = basename + name
        
        frontfile = folder + '\\' + fullname + '_Front.txt'
        rearfile = folder + '\\' + fullname + '_Back.txt'
        
        makefiles = bogus_analysis.formatandsavecsv(frontfile, rearfile, fullname,\
                                        numsensors = senpermod, nmods = tot_mods)
    
    time_output = time.time() - time_output_start
    
    
    """
    -------------------------------------------------------------------------------
    Calculate mismatch and power output
    
    
    time_mismatch_start = time.time()
    
    resultsname = 'mismatch_results' + modeltype + '.csv'
    thefolder = folder + '\\results'
    
    
    br.mismatch.analysisIrradianceandPowerMismatch_2(testfolder= thefolder, \
            writefiletitle = resultsname, portraitorlandscape = PorL, \
            bififactor = bififactor, numcells = numcells)
    
    time_mismatch = time.time() - time_mismatch_start
    """
    
    
    
    
    print('total time   :   ', time.time() - start_time_full)
    print('sensors      :   ', time_sensors)
    print('octfiles     :   ', time_octfiles)
    print('analysis     :   ', time_analysis)
    print('output       :   ', time_output)
    #print('mismatch     :   ', time_mismatch)








"""
Times:
    10 first hours
        Radiance:
            total time   :    67.9300057888031
            sensors      :    0.14118146896362305
            octfiles     :    0.2567589282989502
            analysis     :    65.76330900192261
            output       :    0.7154834270477295
            mismatch     :    1.0532729625701904
            -Will take around 9 hours
        
        Accelerad:
            Quads:
            total time   :    21.052953958511353
            sensors      :    0.14121794700622559
            octfiles     :    0.25653839111328125
            analysis     :    18.831793069839478
            output       :    0.7530689239501953
            mismatch     :    1.0703356266021729
            
            Tris:
            total time   :    21.01774311065674
            sensors      :    0.14519667625427246
            octfiles     :    0.28162717819213867
            analysis     :    18.748733282089233
            output       :    0.7943341732025146
            mismatch     :    1.047851800918579
            -Will take around 3 hours
        
    FULL RUN:
        Accelerad:
            total time   :    9520.07091999054
            sensors      :    0.13306140899658203
            octfiles     :    142.53994941711426
            analysis     :    8482.494874477386
            output       :    334.2342700958252
            mismatch     :    560.668764591217
        2 hours and 38 minutes SELF INTERSECTION RUN
        
        Accelerad:
            PURE BIFACIAL_RADIANCE FILES:
            total time   :    11611.058860778809
            sensors      :    0.21021556854248047
            octfiles     :    769.6953461170197
            analysis     :    9929.804150342941
            output       :    341.9447445869446
            mismatch     :    569.4044041633606
        
        Radiance:
            total time   :    25873.901760339737
            sensors      :    0.2037820816040039
            octfiles     :    770.2816445827484
            analysis     :    24189.29373025894
            output       :    332.97079277038574
            mismatch     :    581.1518106460571
        
        
        DOUBLE RUN
        Radiance:
            total time   :    35.677064657211304
            sensors      :    0.1310110092163086
            octfiles     :    0.3160386085510254
            analysis     :    34.85597372055054
            output       :    0.14151477813720703
            mismatch     :    0.23252654075622559
        
        Accelerad:
            total time   :    9.704376459121704
            sensors      :    0.1375105381011963
            octfiles     :    0.3525240421295166
            analysis     :    8.85279130935669
            output       :    0.1380138397216797
            mismatch     :    0.22353672981262207
        

50
total time   :    893.8342020511627
sensors      :    0.17751264572143555
octfiles     :    3.2344841957092285
analysis     :    889.8501288890839
output       :    0.5720763206481934


70
total time   :    877.6497313976288
sensors      :    0.16908478736877441
octfiles     :    3.163919687271118
analysis     :    873.7455832958221
output       :    0.571143627166748






"""