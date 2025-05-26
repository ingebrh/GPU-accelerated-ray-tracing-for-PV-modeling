    def analyzeRow_custom(self, octfile, scene, rowWanted=None, name=None, 
                   sensorsy=None, sensorsx=None, accelerad = False ):
        '''
        Custom version of analyzeRow edited by ingebrh to take the accelerad
        parameter to switch between Radiance and accelerad.
        Uses analysis_custom for the same reason, and will therefore put frontscan
        and backscan into their own lists for it to work correctly.
        These changes are so minor that they should not affect computation time in
        any significant way compared to the original analyzeRow method.
        
        Changes from original analyzeRow method:
            - Name changed from analyzeRow to analyzeRow_custom
            - Added parameter 'accelerad' to allow for changing between
            running Accelerad or Radiance versions of rtrace, and added a
            description for it.
            - Changed the call to analysis to be to analysis_custom and put
            the frontscan and backscan parameters into brackets, as well as
            added the accelerad parametert to the call.
            - The line saying 'rowWanted = round(nRows / 1.99)'
            originally said   'rowWanted = round(self.nRows / 1.99)'
            but this does not work as the AnalysisObj class does not have
            the 'nRows' attribute. This was fixed by adding the
            'nRows = scene.sceneDict['nRows']' -line
        
        Function to Analyze every module in the row. 
    
        Parameters
        ----------
        octfile : string
            Filename and extension of .oct file
        scene : ``SceneObj``
            Generated with :py:class:`~bifacial_radiance.RadianceObj.makeScene`.
        rowWanted : int
            Row wanted to sample. If none, defaults to center row (rounding down)
        sensorsy : int or list 
            Number of 'sensors' or scanning points along the collector width 
            (CW) of the module(s). If multiple values are passed, first value
            represents number of front sensors, second value is number of back sensors
        sensorsx : int or list 
            Number of 'sensors' or scanning points along the length, the side perpendicular 
            to the collector width (CW) of the module(s) for the back side of the module. 
            If multiple values are passed, first value represents number of 
            front sensors, second value is number of back sensors.
        accelerad : boolean
            Choose to run accelerad rtrace (True) or Radiance rtrace (False)
    
        Returns
        -------
        df_row : dataframe
            Dataframe with all values sampled for the row.
    
        '''
        #allfront = []
        #allback = []
        
        nMods = scene.sceneDict['nMods']
        nRows = scene.sceneDict['nRows']
        
        if rowWanted == None:
            rowWanted = round(nRows / 1.99)
        df_dict_row = {}
        row_keys = ['x','y','z','rearZ','mattype','rearMat','Wm2Front','Wm2Back','Back/FrontRatio']
        dict_row = df_dict_row.fromkeys(row_keys)
        df_row = pd.DataFrame(dict_row, index = [j for j in range(nMods)])
        
        for i in range (nMods):
            temp_dict = {}
            frontscan, backscan = self.moduleAnalysis(scene, sensorsy=sensorsy, 
                                        sensorsx=sensorsx, modWanted = i+1, 
                                        rowWanted = rowWanted) 
            allscan = self.analysis_custom(octfile, name+'_Module_'+str(i),
                                           [frontscan], [backscan],
                                           accelerad = accelerad) 
            front_dict = allscan[0]
            back_dict = allscan[1]
            temp_dict['x'] = front_dict['x']
            temp_dict['y'] = front_dict['y']
            temp_dict['z'] = front_dict['z']
            temp_dict['rearZ'] = back_dict['z']
            temp_dict['mattype'] = front_dict['mattype']
            temp_dict['rearMat'] = back_dict['mattype']
            temp_dict['Wm2Front'] = front_dict['Wm2']
            temp_dict['Wm2Back'] = back_dict['Wm2']
            temp_dict['Back/FrontRatio'] = list(np.array(front_dict['Wm2'])/np.array(back_dict['Wm2']))
            df_row.iloc[i] = temp_dict
            #allfront.append(front)
        return df_row
