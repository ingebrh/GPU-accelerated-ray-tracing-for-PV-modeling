    def _irrPlot_custom(self, octfile, linepts, mytitle=None, plotflag=None,
                   accuracy='low', accelerad = False):
        """
        Edited version of _irrPlot. Edited by ingebrh. Made for use with
        Accelerad by Nathaniel L Jones.
        
        Changes from original analysis function:
            - Name changed from '_irrPlot' to '_irrPlot_custom'
            - Added 'accelerad' parameter which will determine whether
              Radiance rtrace or Accelerad rtrace is to be used, and added
              a description for it in the docstring.
            - Added if-test to check the accelerad parameter and create a new
              argument for rtrace
            - Added the new argument to the rtrace 'cmd'-line
        
        
        (plotdict) = _irrPlot_custom(linepts,title,time,plotflag, accuracy)
        irradiance plotting using rtrace
        pass in the linepts structure of the view along with a title string
        for the plots.  
    
        Parameters
        ------------
        octfile : string
            Filename and extension of .oct file
        linepts : 
            Output from :py:class:`bifacial_radiance.AnalysisObj._linePtsMake3D`
        mytitle : string
            Title to append to results files
        plotflag : Boolean
            Include plot of resulting irradiance
        accuracy : string
            Either 'low' (default - faster) or 'high'
            (better for low light)
        accelerad : Boolean
            Use accelerad (True) or not (False)
    
        Returns
        -------
        out : dictionary
            out.x,y,z  - coordinates of point
            .r,g,b     - r,g,b values in Wm-2
            .Wm2            - equal-weight irradiance
            .mattype        - material intersected
            .title      - title passed in
        """
        
        if mytitle is None:
            mytitle = octfile[:-4]
    
        if plotflag is None:
            plotflag = False
    
        
        if self.hpc :
            import time
            time_to_wait = 10
            time_counter = 0
            while not os.path.exists(octfile):
                time.sleep(1)
                time_counter += 1
                if time_counter > time_to_wait:
                    print('Warning: OCTFILE NOT FOUND')
                    break
    
        if octfile is None:
            print('Analysis aborted. octfile = None' )
            return None
    
        keys = ['Wm2','x','y','z','r','g','b','mattype']
        out = {key: [] for key in keys}
        #out = dict.fromkeys(['Wm2','x','y','z','r','g','b','mattype','title'])
        out['title'] = mytitle
        print ('Linescan in process: %s' %(mytitle))
        #rtrace ambient values set for 'very accurate':
        #cmd = "rtrace -i -ab 5 -aa .08 -ar 512 -ad 2048 -as 512 -h -oovs "+ octfile
        
        
        if accelerad == True:
            arg = '-g+ ' #Enable GPU raytracing (default)
        elif accelerad == False:
            arg = '-g- ' #Disable GPU raytracing (run on CPU)
        else:
            print('Parameter "accelerad" must be boolean')
            return None
        
        
        if accuracy == 'low':
            #rtrace optimized for faster scans: (ab2, others 96 is too coarse)
            cmd = "rtrace -i -ab 2 -aa .1 -ar 256 -ad 2048 -as 256 -h -oovs "+ arg + octfile
        elif accuracy == 'high':
            #rtrace ambient values set for 'very accurate':
            cmd = "rtrace -i -ab 5 -aa .08 -ar 512 -ad 2048 -as 512 -h -oovs "+ arg + octfile
        else:
            print('_irrPlot accuracy options: "low" or "high"')
            return({})
    
    
    
        temp_out,err = _popen(cmd,linepts.encode())
        if err is not None:
            if err[0:5] == 'error':
                raise Exception(err[7:])
            else:
                print(err)
    
        # when file errors occur, temp_out is None, and err message is printed.
        if temp_out is not None:
            for line in temp_out.splitlines():
                temp = line.split('\t')
                out['x'].append(float(temp[0]))
                out['y'].append(float(temp[1]))
                out['z'].append(float(temp[2]))
                out['r'].append(float(temp[3]))
                out['g'].append(float(temp[4]))
                out['b'].append(float(temp[5]))
                out['mattype'].append(temp[6])
                out['Wm2'].append(sum([float(i) for i in temp[3:6]])/3.0)
    
    
            if plotflag is True:
                import matplotlib.pyplot as plt
                plt.figure()
                plt.plot(out['Wm2'])
                plt.ylabel('Wm2 irradiance')
                plt.xlabel('variable')
                plt.title(mytitle)
                plt.show()
        else:
            out = None   # return empty if error message.
    
        return(out)
