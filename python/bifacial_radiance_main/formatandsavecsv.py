    def formatandsavecsv(self, frontfile=None, rearfile=None, name=None,\
                         RGB=False, numsensors = 24*48, nmods = 1):
        """
        New method consisting of previously removed formatting code from
        other functions. Set up by ingebrh. To be called on by the user after
        analysis_custom_3 has been used, where pure rtrace output is saved
        in .txt format. The following script combines these files, splits them
        up by module and creates csv files in regular bifacial_radiance layout.
        
        NOTE: This has not been tested with half-cut modules. Those might need
        a little more formatting.
        

        Parameters
        ----------
        frontfile : string
            Filepath, name and extension of txt file containing raw rtrace
            output for front irradiances
        rearfile : string
            Filepath, name and extension of txt file containing raw rtrace
            output for front irradiances
        name : string
            The base name for the output csv files.
        RGB : Boolean
            If the raytrace is a spectral raytrace and information for the
            three channels wants to be saved, set RGB to True.
        numsensors : TYPE, optional
            The number of sensors per module
        nmods : TYPE, optional
            The number of modules that have been evaluated

        Returns
        -------
        None.

        """
        
        
        keys = ['Wm2','x','y','z','r','g','b','mattype']
        frontdict = {key: [] for key in keys}
        frontdict['title'] = name
        backdict = {key: [] for key in keys}
        backdict['title'] = name
        
        if frontfile is not None:
            frontfiledata = open(frontfile, 'r')
            frontdata = frontfiledata.read()
            frontfiledata.close()
        else:
            frontdata = None
        
        
        
        if rearfile is not None:
            rearfiledata = open(rearfile, 'r')
            reardata = rearfiledata.read()
            rearfiledata.close() 
        else:
            reardata = None
            
        
        if frontdata is not None and reardata is not None:
            for line in frontdata.split('\n\n'):
                temp = line.split('\t')
                if temp != ['']:
                    frontdict['x'].append(float(temp[0]))
                    frontdict['y'].append(float(temp[1]))
                    frontdict['z'].append(float(temp[2]))
                    frontdict['r'].append(float(temp[3]))
                    frontdict['g'].append(float(temp[4]))
                    frontdict['b'].append(float(temp[5]))
                    frontdict['mattype'].append(temp[6])
                    frontdict['Wm2'].append(sum([float(i) for i in temp[3:6]])/3.0)
            for line in reardata.split('\n\n'):
                temp = line.split('\t')
                if temp != ['']:
                    backdict['x'].append(float(temp[0]))
                    backdict['y'].append(float(temp[1]))
                    backdict['z'].append(float(temp[2]))
                    backdict['r'].append(float(temp[3]))
                    backdict['g'].append(float(temp[4]))
                    backdict['b'].append(float(temp[5]))
                    backdict['mattype'].append(temp[6])
                    backdict['Wm2'].append(sum([float(i) for i in temp[3:6]])/3.0)

        elif frontdata is not None and reardata is None:
            for line in frontdata.split('\n\n'):
                temp = line.split('\t')
                if temp != ['']:
                    frontdict['x'].append(float(temp[0]))
                    frontdict['y'].append(float(temp[1]))
                    frontdict['z'].append(float(temp[2]))
                    frontdict['r'].append(float(temp[3]))
                    frontdict['g'].append(float(temp[4]))
                    frontdict['b'].append(float(temp[5]))
                    frontdict['mattype'].append(temp[6])
                    frontdict['Wm2'].append(sum([float(i) for i in temp[3:6]])/3.0)
                    backdict['x'].append(0)
                    backdict['y'].append(0)
                    backdict['z'].append(0)
                    backdict['r'].append(0)
                    backdict['g'].append(0)
                    backdict['b'].append(0)
                    backdict['mattype'].append('*')
                    backdict['Wm2'].append(0)

        elif frontdata is None and reardata is not None:
            for line in reardata.split('\n\n'):
                temp = line.split('\t')
                if temp != ['']:
                    backdict['x'].append(float(temp[0]))
                    backdict['y'].append(float(temp[1]))
                    backdict['z'].append(float(temp[2]))
                    backdict['r'].append(float(temp[3]))
                    backdict['g'].append(float(temp[4]))
                    backdict['b'].append(float(temp[5]))
                    backdict['mattype'].append(temp[6])
                    backdict['Wm2'].append(sum([float(i) for i in temp[3:6]])/3.0)
                    frontdict['x'].append(0)
                    frontdict['y'].append(0)
                    frontdict['z'].append(0)
                    frontdict['r'].append(0)
                    frontdict['g'].append(0)
                    frontdict['b'].append(0)
                    frontdict['mattype'].append('*')
                    frontdict['Wm2'].append(0)
        else:
            frontdata = None
            reardata = None
            print('No data from front nor back')
        
        
        
        # don't save if _irrPlot returns an empty file.
        if frontdict is not None:
            if len(frontdict['Wm2']) != len(backdict['Wm2']):
                for mod in range(nmods):
                    if len(str(mod)) == 1:
                        namemodifier = '_mod_00' + str(mod)
                    elif len(str(mod)) == 2:
                        namemodifier = '_mod_0' + str(mod)
                    else:
                        namemodifier = '_mod_' + str(mod)
                    frontsliced = {key : frontdict[key][mod*numsensors:(mod+1)*numsensors] for key in keys}
                    backsliced = {key : backdict[key][mod*numsensors:(mod+1)*numsensors] for key in keys}
                    self.Wm2Front = np.mean(frontsliced['Wm2'])
                    self.Wm2Back = np.mean(backsliced['Wm2'])
                    self.backRatio = self.Wm2Back / (self.Wm2Front + .001)
                    self._saveResults(frontsliced, reardata=None, savefile='irr_%s.csv'%(name+namemodifier+'_Front'), RGB=RGB)
                    self._saveResults(data=None, reardata=backsliced, savefile='irr_%s.csv'%(name+namemodifier+'_Back'), RGB=RGB)
            else:
                for mod in range(nmods):
                    if len(str(mod)) == 1:
                        namemodifier = '_mod_00' + str(mod)
                    elif len(str(mod)) == 2:
                        namemodifier = '_mod_0' + str(mod)
                    else:
                        namemodifier = '_mod_' + str(mod)
                    frontsliced = {key : frontdict[key][mod*numsensors:(mod+1)*numsensors] for key in keys}
                    backsliced = {key : backdict[key][mod*numsensors:(mod+1)*numsensors] for key in keys}
                    self._saveResults(frontsliced, backsliced,'irr_%s.csv'%(name+namemodifier), RGB=RGB)

