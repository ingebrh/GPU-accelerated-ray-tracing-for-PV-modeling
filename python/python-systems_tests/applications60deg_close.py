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
s_date = pd.to_datetime('1983-06-06')
e_date = pd.to_datetime('1983-06-07')

metdata = run.readWeatherFile(epwfile, starttime=s_date, endtime=e_date)

print(metdata)

run.setGround(0.6) #Concrete albedo


"""
-------------------------------------------------------------------------------
DEFINING THE MODULE AND SCENE PARAMETERS
"""


#Module parameters
moduletype = 'custom'   #Name of module
numpanels = 1           #Modules in y-direction (slant height)
x = 0.948               #Width of module
y = 1.896               #Length of module
z = 0.002               #Thickness of module


#PV array parameters
row_modules = 6                 #The number of modules per row
nrows = 3                       #The number of rows 
tot_mods = nrows*row_modules    #The total number of modules
xgap = 0.052            #Gap in x-direction (along row width)
ygap = 0                #Gap in y-direction (along slant height)
zgap = 0                #Gap in z-direction (normal on module front face)
tilt = 60               #Angle between module and horizontal plane
# Tilts:                 10      15      20      30      45      60      90
pitch = 5               #Distance between row centers
# Pitch                   x       x       x       4       5       6       x
clearance = 0.5550      #Distance between ground and lower lip under module
# Clearance:              0.1407  0.1473  0.1529  0.3800  0.4827  0.5550  
azim = 180              #Azimuth of system

nhours = 19 #print(metdata) gives 19 entries

#Raytracing and model parameters
acc = True #Boolean, for using Accelerad or not
#Run with acc = False and nhours = 1 to check if sensors are correctly placed.
modeltype = str(tilt) #which 3D model. Used to pull the correct .rad files.
basename = modeltype +'deg_'
quadortri = 'close_quad'
PorL = 'portrait' #portrait or landscape (for mismatch and output)
bififactor = 0.9 #bifaciality factor
numcells = 72 #The number of cells per module
seny = 48 #The number of sensor points along the height of each module per side
senx = 24 #The number of sensor points along the width of each module per side
senpermod = seny*senx #The total number of sensor points per module per side








"""
CREATE SCENE

Parameters are made up.
"""

# create module:
module = run.makeModule(name = moduletype, x=x, y=y, z=z, xgap=xgap,\
                        ygap=ygap, zgap=zgap, numpanels = numpanels)

# create scene dictionary.

sceneDict = {'tilt': tilt, 'pitch': pitch, 'clearance_height': clearance,\
             'azimuth': azim, 'nMods': row_modules, 'nRows': nrows}


# make scene. Creates the .rad file
scene = run.makeScene(module = module, sceneDict = sceneDict)


import time


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
for row in range(1,nrows + 1):
    for module in range(1,row_modules + 1):
        frontscan, backscan = bogus_analysis.moduleAnalysis(scene, \
                            modWanted = module, rowWanted = row, \
                            sensorsy = seny, sensorsx = senx)
        frontpts += bogus_analysis._linePtsMakeDict(frontscan)
        backpts += bogus_analysis._linePtsMakeDict(backscan)

#REPLACE THE SCENE WITH BLENDER-MADE SCENE. EDIT SCENE NAME:
"""
#######################################EDIT EDIT EDIT EDIT EDIT EDIT###########
Replace the radiance-created scene with the blender model
"""

scene_name = modeltype + 'deg_' + quadortri + '.rad' #str(row_modules)
scene_extention = 'objects\\' + scene_name
run.radfiles =['materials\\ground.rad', scene_extention ]

time_sensors = time.time() - start_time_full



time_octfiles_start = time.time()

"""
-------------------------------------------------------------------------------
To limit temperature differences in components, we create all octree files
first, so we only need to load them for the raytracing
"""

for x in range(nhours): #there are 38 hours with daylight*
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

for x in range(nhours): #there are 38 hours with daylight*
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
                                       accelerad = acc, path = folder)

time_analysis = time.time() - time_analysis_start

"""
-------------------------------------------------------------------------------
Now, we can tidy up the output files.
"""

time_output_start = time.time()

for x in range(nhours): #there are 38 hours with daylight*
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
"""

time_mismatch_start = time.time()

resultsname = 'mismatch_results' + modeltype + '.csv'
thefolder = folder + '\\results'


br.mismatch.analysisIrradianceandPowerMismatch_2(testfolder= thefolder, \
        writefiletitle = resultsname, portraitorlandscape = PorL, \
        bififactor = bififactor, numcells = numcells)

time_mismatch = time.time() - time_mismatch_start





print('total time   :   ', time.time() - start_time_full)
print('sensors      :   ', time_sensors)
print('octfiles     :   ', time_octfiles)
print('analysis     :   ', time_analysis)
print('output       :   ', time_output)
print('mismatch     :   ', time_mismatch)








"""
Times:
    60-deg:
        Single Radiance run:
            total time   :    59.04400396347046
            sensors      :    0.5581274032592773
            octfiles     :    0.11600255966186523
            analysis     :    57.76156497001648
            output       :    0.2348930835723877
            mismatch     :    0.3734159469604492
            
        Accelerad:
            total time   :    280.9197165966034
            sensors      :    0.5709407329559326
            octfiles     :    2.2686688899993896
            analysis     :    267.091805934906
            output       :    4.189369440078735
            mismatch     :    6.79893159866333
    
    60-deg_far:
        Single Radiance run:
            total time   :    57.21486139297485
            sensors      :    0.6329371929168701
            octfiles     :    0.11951279640197754
            analysis     :    55.82103109359741
            output       :    0.23895645141601562
            mismatch     :    0.4024238586425781
            
        Accelerad:
            total time   :    271.2852313518524
            sensors      :    0.5670328140258789
            octfiles     :    2.2483508586883545
            analysis     :    257.31073665618896
            output       :    4.20934796333313
            mismatch     :    6.949763059616089
    
    60-deg_close:
        Single Radiance run:
            total time   :    58.42798614501953
            sensors      :    0.5632920265197754
            octfiles     :    0.12050867080688477
            analysis     :    57.133310079574585
            output       :    0.23717784881591797
            mismatch     :    0.37369751930236816
            
        Accelerad:
            total time   :    287.96633768081665
            sensors      :    0.5629937648773193
            octfiles     :    2.168119430541992
            analysis     :    274.0628616809845
            output       :    4.221075057983398
            mismatch     :    6.951287746429443
            
"""