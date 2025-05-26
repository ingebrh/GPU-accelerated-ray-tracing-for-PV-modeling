    def _irrPlot_custom_2(self, octfile, linepts, mytitle=None, plotflag=None,
                   accuracy='low', accelerad = False):
        """
        Edited version of _irrPlot. Edited by ingebrh. Made for use with
        Accelerad by Nathaniel L Jones. Removes all text editing of output
        to reduce time between simulations.
        
        Changes from original analysis function:
            - Name changed from '_irrPlot' to '_irrPlot_custom'
            - Added 'accelerad' parameter which will determine whether
              Radiance rtrace or Accelerad rtrace is to be used, and added
              a description for it in the docstring.
            - Added if-test to check the accelerad parameter and create a new
              argument for rtrace
            - Added the new argument to the rtrace 'cmd'-line
            - Removed the text editing for the output
        
        
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
        
        elif accuracy == "very high":
            #rtrace high but lower bounces and higher ambient divisions
            cmd = "rtrace -i -ab 3 -aa .08 -ar 512 -ad 8192 -as 1024 -h -oovs "+ arg + octfile
        
        else:
            print('_irrPlot accuracy options: "low", "high" or "very high"')
            return({})



        temp_out,err = _popen(cmd,linepts.encode())
        if err is not None:
            if err[0:5] == 'error':
                raise Exception(err[7:])
            else:
                print(err)
        # when file errors occur, temp_out is None, and err message is printed.
       
        return(temp_out)
