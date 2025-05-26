    def analysis_custom(self, octfile, name, frontscans, backscans,
                     plotflag=False, accuracy='low', RGB=False, accelerad = False):
            """
            
            Edited version of analysis. Edited by ingebrh. The change is that
            the function takes in a list of frontscan and backscan dictionaries
            instead of single ones. All the different linepts are added together
            to be analyzed simultaneously, excellent for parallell processing.
            
            Changes from original analysis function:
                - Name changed from 'analysis' to 'analysis_custom'
                - Inputs 'frontscan' and 'backscan', and Parameters description
                changed to plural, with added note 'list of'
                - Added 'linepts = '' 'infront of original linepts statements.
                - Added for-loops to loop through lists of frontscans/backscans
                - Moved original linepts statements into for-loop and changed
                equality signs in these with '+='
                - Changed original linepts statements to take the i'th element
                of the scans lists.
                - Changed the call to _irrplot to _irrplot_custom
                - Added accelerad parameter for using accelerad or not in
                _irrplot_custom, and added description in docstring
            
            
            General analysis function, where linepts are passed in for calling the
            raytrace routine :py:class:`~bifacial_radiance.AnalysisObj._irrPlot` 
            and saved into results with 
            :py:class:`~bifacial_radiance.AnalysisObj._saveResults`.

            
            Parameters
            ------------
            octfile : string
                Filename and extension of .oct file
            name : string 
                Name to append to output files
            frontscans : list of scene.frontscan objects
                Objects with the sensor location information for the 
                front of the modules
            backscans : list of scene.backscan objects
                Objects with the sensor location information for the 
                rear side of the modules
            plotflag : boolean
                Include plot of resulting irradiance
            accuracy : string 
                Either 'low' (default - faster) or 'high' (better for low light)
            RGB : Bool
                If the raytrace is a spectral raytrace and information for the three channe
                wants to be saved, set RGB to True.
            accelerad : Bool
                Use accelerad rtrace or not

                
            Returns
            -------
             File saved in `\\results\\irr_name.csv`

            """

            if octfile is None:
                print('Analysis aborted - no octfile \n')
                return None, None
            
            linepts = ''
            for ifront in range(len(frontscans)):
                linepts += self._linePtsMakeDict(frontscans[ifront])
            
            frontDict = self._irrPlot_custom(octfile, linepts, name+'_Front',
                                        plotflag=plotflag, accuracy=accuracy,
                                        accelerad = accelerad)

            #bottom view.
            linepts = ''
            for iback in range(len(backscans)):
                linepts += self._linePtsMakeDict(backscans[iback])
            
            backDict = self._irrPlot_custom(octfile, linepts, name+'_Back',
                                       plotflag=plotflag, accuracy=accuracy,
                                       accelerad = accelerad)
           
            # don't save if _irrPlot returns an empty file.
            if frontDict is not None:
                if len(frontDict['Wm2']) != len(backDict['Wm2']):
                    self.Wm2Front = np.mean(frontDict['Wm2'])
                    self.Wm2Back = np.mean(backDict['Wm2'])
                    self.backRatio = self.Wm2Back / (self.Wm2Front + .001)
                    self._saveResults(frontDict, reardata=None, savefile='irr_%s.csv'%(name+'_Front'), RGB=RGB)
                    self._saveResults(data=None, reardata=backDict, savefile='irr_%s.csv'%(name+'_Back'), RGB=RGB)
                else:
                    self._saveResults(frontDict, backDict,'irr_%s.csv'%(name), RGB=RGB)

            return frontDict, backDict
