# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 10:27:58 2024

@author: ingeb
"""

import bifacial_radiance as br
import pandas as pd

#DEFINE TEST FOLDER
folder = 'C:\\Users\\ingeb\\Documents\\Master\\timetest2\\bf_files'

# create basis
timetest = br.RadianceObj('timetest2', path = folder)

"""
DEFINE RUN CHARACTERISTICS
"""
scan_method = 'new' #either 'new' or 'old'
scene_type = 'complex' #either 'simple' or 'complex' ('simple' or something else)
row_modules = 7 # 3, 5, 7, 9, 11, 13, 15, 17, 19, 21
acc = True #Boolean, for using Accelerad or not

#create name start 'xx_mods'
if len(str(row_modules)) == 1:
    namestart = '0' + str(row_modules) + '_mods'
else:
    namestart = str(row_modules) + '_mods'

if acc == True:
    quadortri = 'tri'
else:
    quadortri = 'quad'

#epwfile = run.getEPW(lat = 59.06, lon = 10.07)

flname = '\\EPWs\\shinyweatherdata-2022.epw'

epwfile = folder + flname

#select some data, yyyy-mm-dd:
s_date = pd.to_datetime('2022-06-06')
e_date = pd.to_datetime('2022-06-08')

metdata = timetest.readWeatherFile(epwfile, starttime=s_date, endtime=e_date)

timetest.setGround(0.6) #Concrete albedo


"""
DEFINING THE MODULE
MODEL AS TWO 72-cell modules!
"""

moduletype = 'BIPRO' # name of module
numpanels = 2 # modules in y-direction (slant height)
xgap = 0.072 # 7.2cm gap in x-direction (east-west)
ygap = 0.04 # 4cm gap in y-direction (slant height)
zgap = 0

x = 0.958 # width of module
y = 0.97 # length of module
z = 0.005 # thickness of module


"""
CREATE SCENE

Parameters are made up.
"""
#run.radfiles.append('materials\\ground.rad')
print(timetest.getfilelist())
# create module:
module = timetest.makeModule(name = moduletype, x=x, y=y, z=z, xgap=xgap,\
                        ygap=ygap, zgap=zgap, numpanels = numpanels)

# create scene dictionary.
if scene_type == 'simple':
    sceneDict = {'tilt': 35, 'pitch': 3.5, 'clearance_height': 0.602869,\
             'azimuth': 175, 'nMods': row_modules, 'nRows': 5}
else: #complex scene is on a 4m tall building
    sceneDict = {'tilt': 35, 'pitch': 3.5, 'clearance_height': 4.602869,\
             'azimuth': 175, 'nMods': row_modules, 'nRows': 5}

        
    
# make scene. Creates the .rad file
scene = timetest.makeScene(module = module, sceneDict = sceneDict)


import time


if scan_method == 'new':
    start_time = time.time()
    """
    THE SCAN DICTIONARIES DO NOT CHANGE, SO WE ONLY NEED TO MAKE ONE DICTIONARY
    AND USE IT IN THE LOOP, INSTEAD OF RECREATING THE WHOLE DICTIONARY EVERY
    TIME AN OCTREE IS MADE. WE MAKE A BOGUS OCTREE FOR THIS PURPOSE
    """
    timetest.gendaylit(0, metdata)
    bogus_oct = timetest.makeOct(timetest.getfilelist(), 'bogus')
    bogus_analysis = br.AnalysisObj(bogus_oct, 'bogus')
    frontpts = ''
    backpts = ''
    for module in range(1,row_modules + 1): #CHANGE RANGE
        frontscan, backscan = bogus_analysis.moduleAnalysis(scene, \
                              modWanted = module, sensorsy = 48, sensorsx = 24)
        frontpts += bogus_analysis._linePtsMakeDict(frontscan)
        backpts += bogus_analysis._linePtsMakeDict(backscan)
    
    #REPLACE THE SCENE WITH BLENDER-MADE SCENE. EDIT SCENE NAME:
    if scene_type == 'complex':
        scene_name = '19' + 'modules_' + quadortri + '.rad' #str(row_modules)
        scene_extention = 'objects\\' + scene_name
        timetest.radfiles =['materials\\ground.rad', scene_extention ]
    
    
    for x in range(38): #there are 38 hours with daylight*
    # *from print(metdata), one gets 114 entries
        
        timetest.gendaylit(x, metdata)
        
        
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
        
        
        fullname = namestart + '_' + str(scene_type) + '_' + str(acc) +  '_new_'
        
        if len(str(x)) == 1:
            name = '000' + str(x)
        elif len(str(x)) == 2:
            name = '00' + str(x)
        elif len(str(x)) == 3:
            name = '0' + str(x)
        else:
            name = str(x)
        
        fullname += name
        
        # create .oct file
        octfile = timetest.makeOct(timetest.getfilelist(), fullname) 
    
        analysis = br.AnalysisObj(octfile, timetest.basename)
        
        results = analysis.analysis_custom_2(octfile, fullname, frontpts, backpts,
                                           accelerad = acc)
    
    print(time.time() - start_time)






elif scan_method == 'old':
    start_time = time.time()

    #REPLACE THE SCENE WITH BLENDER-MADE SCENE. EDIT SCENE NAME:
    if scene_type == 'complex':
        scene_name = str(row_modules) + 'modules_' + quadortri + '.rad'
        scene_extention = 'objects\\' + scene_name
        timetest.radfiles =['materials\\ground.rad', scene_extention ]
    
    
    for x in range(38): #there are 38 hours with daylight*
        # *from print(metdata), one gets 114 entries
        
        timetest.gendaylit(x, metdata)
        
        
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
        
        
        fullname = namestart + '_' + str(scene_type) + '_' + str(acc) +  '_old_'
        
        if len(str(x)) == 1:
            name = '000' + str(x)
        elif len(str(x)) == 2:
            name = '00' + str(x)
        elif len(str(x)) == 3:
            name = '0' + str(x)
        else:
            name = str(x)
        
        fullname += name
        
        # create .oct file
        octfile = timetest.makeOct(timetest.getfilelist(), fullname) 
        
        analysis = br.AnalysisObj(octfile, timetest.basename)
        
        results = analysis.analyzeRow_custom(octfile, scene, name = fullname,
                                                sensorsy = 48, sensorsx = 24,
                                                accelerad = acc)
    
    print(time.time() - start_time)

"""
Times:
---------------------------------------------------NEW TYPE-time(sensor, faces)
        ACCELERAD (running on RTX 4070 Ti SUPER)
        simple
        name                t_cust       t_cust_2
03mods_simple_True_new   : 100.1068     :  97.87
05mods_simple_True_new   : 119.5309     : 115.14
07mods_simple_True_new   : 136.5274     : 130.28
09mods_simple_True_new   : 152.1414     : 145.03
11mods_simple_True_new   : 170.5671     : 160.63
13mods_simple_True_new   : 185.6502     : 176.29
15mods_simple_True_new   : 203.0974     : 191.64
17mods_simple_True_new   : 220.4876     : 208.34
19mods_simple_True_new   : 236.8299     : 223.54
21mods_simple_True_new   : 266.1712     : 249.43
        complex
        name                t_cust       t_cust_2
03mods_complex_True_new  : 106.65       : 103.36
05mods_complex_True_new  : 135.21       : 130.33
07mods_complex_True_new  : 159.10       : 153.36
09mods_complex_True_new  : 182.95       : 175.67
11mods_complex_True_new  : 206.38       : 198.59
13mods_complex_True_new  : 232.69       : 222.31
15mods_complex_True_new  : 256.08       : 245.17
17mods_complex_True_new  : 281.48       : 269.79
19mods_complex_True_new  : 319.45       : 307.07
21mods_complex_True_new  : 479.09       : 460.56
OBSERVATION: GPU usage maxes out at 21 mods, see screenshots

        RADIANCE (running on i7-14700)
        simple
        name                t_cust       t_cust_2
03mods_simple_False_new  : 184.0088     : 183.97
05mods_simple_False_new  : 266.8488     : 263.54
07mods_simple_False_new  : 348.0122     : 341.82
09mods_simple_False_new  : 423.6430     : 413.43
11mods_simple_False_new  : 498.6134     : 486.35
13mods_simple_False_new  : 576.3991(89) : 563.62
15mods_simple_False_new  : 651.2064(89) : 635.21
17mods_simple_False_new  : 725.1243     : 706.92
19mods_simple_False_new  : 801.1715     : 781.03
21mods_simple_False_new  : 874.5238     : 851.85
        complex
        name                t_cust       t_cust_2
03mods_complex_False_new : 749.21       : 736.88
05mods_complex_False_new :1182.14       :1165.84
121.55 seconds for a single timestep run with 21 modules


-------------------------------------------------OLD TYPE (all simple)
        ACCELERAD
03mods_simple_True_old   : 226.11
05mods_simple_True_old   : 413.96
07mods_simple_True_old   : 638.41


        RADIANCE
03mods_simple_False_old  : 379.38
05mods_simple_False_old  : 765.44
07mods_simple_False_old  : 

    
---------------------------------------------------time(sensor)
        
        21-model
name       t_cust      t_old
01mods  :  272.94
03mods  :  292.16
05mods  :  297.96
07mods  :  299.71
09mods  :  300.98
11mods  :  303.28
13mods  :  306.59
15mods  :  309.09
17mods  :  313.15
19mods  :  326.70
21mods  :  461.18

        19-model
01mods  :  251.36
03mods  :  272.45
05mods  :  278.79
07mods  :  
09mods  :  
11mods  :  
13mods  :  
15mods  :  
17mods  :  
19mods  :  

        17-model
01mods  :  
03mods  :  
05mods  :  
07mods  :  
09mods  :  
11mods  :  
13mods  :  
15mods  :  
17mods  : 

        15-model
01mods  :  
03mods  :  
05mods  :  
07mods  :  
09mods  :  
11mods  :  
13mods  :  
15mods  :  

        13-model
01mods  :  
03mods  :  
05mods  :  
07mods  :  
09mods  :  
11mods  :  
13mods  :  

        11-model
01mods  :  
03mods  :  
05mods  :  
07mods  :  
09mods  :  
11mods  :  

        09-model
01mods  :  
03mods  :  
05mods  :  
07mods  :  
09mods  :  

        07-model
01mods  :  
03mods  :  
05mods  :  
07mods  :  

        05-model
01mods  :  
03mods  :  
05mods  :  

        03-model
01mods  :  
03mods  :  









 
"""