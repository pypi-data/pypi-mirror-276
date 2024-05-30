# -*- coding: utf-8 -*-
""" This is the CLPU module to work with data from metrology.

Please do only add or modify but not delete content.

requires explicitely {
 - os
 - tkinter
 - numpy
 - cv2
 - typing
}

import after installation of pyclpu via {
  from pyclpu import metrology
}

import without installation via {
  root = os.path.dirname(os.path.abspath(/path/to/pyclpu/metrology.py))
  sys.path.append(os.path.abspath(root))
  import metrology
  from importlib import reload 
  reload(metrology)
}

"""

# =============================================================================
# PYTHON HEADER
# =============================================================================
# EXTERNALimport cv2
import os
import sys
from inspect import getsourcefile
from importlib import reload

import math
import numpy as np

from scipy import signal
from scipy import interpolate
import cv2

import matplotlib.pyplot as plt
from tkinter import filedialog #not for the function
from typing import List, Tuple

# INTERNAL
root = os.path.dirname(os.path.abspath(getsourcefile(lambda:0))) # get environment
sys.path.append(os.path.abspath(root))                           # add environment
sys.path.append(os.path.abspath(root)+os.path.sep+"LIB")         # add library

if "constants" not in globals() or globals()['constants'] == False:
    import constants                        # import all global constants from                   constants.py
    import formats                          # import all global formats from                     formats.py
    from manager  import error               # import error() from management                    manager.py
    from manager  import message             # import message() from management                  manager.py
    from manager  import warning             # import warning() from management                  manager.py
    from waveform import wfmread             # import wfmread() from waveform                    waveform.py
    from waveform import Waveform            # import Waveform from waveform                     waveform.py
    reload(constants)
    reload(formats)

# =============================================================================
# CLASSES
# =============================================================================
class ThomsonParabola():
    """ Interactive Thomson Parabola diagnostics.
    The class allows interactive work with data from a 2D particle spectrometer in the scheme of a Thomson Parabola. The interpretation of input waveforms is done relativistically. 
    
    Args:
        dispersion_relation (str, optional) :  Absolute path to dispersion relation. Expect a file with lines ``[energy,space]``.
        pixel_per_space (float, optional) : Conversion ratio of how many pixels correspond to one unit of space used in the dispersion relation.
        source_directory (str, optional) : Path to directory with source files. If not given, file dialog will start.
        source_files (list, optional) : List of filenames within ``source_directory``. If not given, file dialog will start.
        X_ray_spot (tupple, optional) : Coordinates of the X-ray spot as tupple ``(x,y)``.
        local_threshold (int, optional) : Threshold for finding local maxima next to local minima, defaults to ``1%`` of difference between minimum and maximum.
        local_wake (int, optional) : Row-by-row wake, defaults to `10%` of the length of one row.
        local_quality (int,optinal) : Minimum number of points in a valid trace, discard traces with smaller point lists. Defaults to 100.
    
    Attributes:
        status (bool) : True if processing was successfull, else False.
            Initializes to False.
    
    Returns:
        filename (str) : Name of input file.
        Xfiltered (`np.ndarray`) : Input image filtered from X-ray spots.
        rowmaxs (`np.ndarray`) : Local maxima which were detected in each row.
        trace (`np.ndarray`) : Detected trace.
        superposition (`np.ndarray`) : Filtered input image superposed with trace.
        trace_array (list) : Result list with all detected traces as ``[trace,X,Y]``
        trace_array_energy (list) : Result list with all converted traces as ``[energy,spectral_count]``.
        
    Note:
        The default trace width is assumed to be 5 pixels. There is currently no build in option to change this.
        
    Examples:
        The class can be used in a functional way

        ```python 
        from pyclpu import metrology
        TP = metrology.ThomsonParabola(source_directory = 'C:\\bin', source_files = ['shot_426.tiff'])
        ```

        A more object oriented use case demonstrates how a run can be started after initialization

        ```python
        import cv2
        from pyclpu import metrology

        TP = metrology.ThomsonParabola()
        TP.analyse()
        ```
        
        The following example shows how the results from a single analysis can be saved.
        
        ```python
        import os
        from pyclpu import manager
        
        output_dir = 'C:\\bin'

        outA = os.path.join(output_dir, 'A_no-X')
        outB = os.path.join(output_dir, 'B_row-by-row-maxs')
        outC = os.path.join(output_dir, 'C_trace')
        outD = os.path.join(output_dir, 'D_superposition')

        if not os.path.exists(outA):
            os.makedirs(outA)
        if not os.path.exists(outB):
            os.makedirs(outB)
        if not os.path.exists(outC):
            os.makedirs(outC)    
        if not os.path.exists(outD):
            os.makedirs(outD)

        if TP.status:
            cv2.imwrite(os.path.join(outA, TP.filename), TP.Xfiltered)
            cv2.imwrite(os.path.join(outB, TP.filename), TP.rowmaxs)
            cv2.imwrite(os.path.join(outC, TP.filename), TP.trace)
            cv2.imwrite(os.path.join(outD, TP.filename), TP.superposition)
            for n in range(len(TP.trace_array)):
                # coordinates
                with open(os.path.join(outC,manager.strip_extension(TP.filename) + '_trace_' + str(n) + '.csv'),'w') as f:
                    f.write('X/[pix], Y/[pix], COUNT\n')
                    for line in TP.trace_array[n]:
                        f.write(', '.join(map(str,line))+'\n')
                # spectrum
                if hasattr(TP, 'trace_array_energy'):
                    with open(os.path.join(outC,manager.strip_extension(TP.filename) + '_spectrum_' + str(n) + '.csv'),'w') as f:
                        f.write('E/[MeV], COUNT*dx/dE\n')
                        for line in TP.trace_array_energy[n]:
                            f.write(', '.join(map(str,line))+'\n')
                    array = np.array(TP.trace_array_energy[n])
                    plt.plot(array[:,0],array[:,1])
                    plt.xlabel('Energy / [MeV]')
                    plt.ylabel('Number-density / [arb.u./MeV]')
                    plt.savefig(os.path.join(outC,manager.strip_extension(TP.filename) + '_spectrum_' + str(n) + '.png'),dpi=300)
                    plt.close('all')
        ```
        
        It is also possible to analyse a batch of data in a loop.
        
        ```python
        import os
        import cv2
        import numpy as np
        import matplotlib.pyplot as plt
        from pyclpu import metrology
        from pyclpu import manager

        TP = metrology.ThomsonParabola()

        TP.X_ray_spot = (1081,1108)
        TP.pixel_per_space = 14875. # with unit of space: [m]
        TP.dispersion_relation = 'C:\\bin\\dispersion_relation.dat'

        TP.source_directory = 'C:\\bin'

        output_trace_numbers = [0] # only protons, which are presumably the 1st trace

        output_dir = 'C:\\bin'
        outA = os.path.join(output_dir, 'A_no-X')
        outB = os.path.join(output_dir, 'B_row-by-row-maxs')
        outC = os.path.join(output_dir, 'C_trace')
        outD = os.path.join(output_dir, 'D_superposition')
        if not os.path.exists(outA):
            os.makedirs(outA)
        if not os.path.exists(outB):
            os.makedirs(outB)
        if not os.path.exists(outC):
            os.makedirs(outC)    
        if not os.path.exists(outD):
            os.makedirs(outD)

        data = os.listdir(TP.source_directory)
        for entry in data:
            if os.path.isfile(os.path.join(TP.source_directory,entry)):
                TP.source_files = [entry]
                TP.analyse()
                if TP.status:
                    cv2.imwrite(os.path.join(outA, TP.filename), TP.Xfiltered)
                    cv2.imwrite(os.path.join(outB, TP.filename), TP.rowmaxs)
                    cv2.imwrite(os.path.join(outC, TP.filename), TP.trace)
                    cv2.imwrite(os.path.join(outD, TP.filename), TP.superposition)
                    for n in range(len(TP.trace_array)):
                        if n in output_trace_numbers:
                            # coordinates
                            with open(os.path.join(outC,manager.strip_extension(TP.filename) + '_trace_' + str(n) + '.csv'),'w') as f:
                                f.write('X/[pix], Y/[pix], COUNT\n')
                                for line in TP.trace_array[n]:
                                    f.write(', '.join(map(str,line))+'\n')
                            # spectrum
                            if hasattr(TP, 'trace_array_energy'):
                                with open(os.path.join(outC,manager.strip_extension(TP.filename) + '_spectrum_' + str(n) + '.csv'),'w') as f:
                                    f.write('E/[MeV], COUNT*dx/dE\n')
                                    for line in TP.trace_array_energy[n]:
                                        f.write(', '.join(map(str,line))+'\n')
                                array = np.array(TP.trace_array_energy[n])
                                plt.plot(array[:,0],array[:,1])
                                plt.xlabel('Energy / [MeV]')
                                plt.ylabel('Number-density / [arb.u./MeV]')
                                plt.savefig(os.path.join(outC,manager.strip_extension(TP.filename) + '_spectrum_' + str(n) + '.png'),dpi=300)
                                plt.close('all')
        ```
    """
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
        self.status = False
        # INTEGRITY
        if not hasattr(self, 'dispersion_relation'):
            warning(self.__class__.__name__,"No source file for the dispersion relation ``energy(space)`` defined, expect key `dispersion_relation` as type `str` pointing to a file with lines [energy,space].")
        if not hasattr(self, 'source_directory'):
            warning(self.__class__.__name__,"No source directory defined, expect key `source_directory` as type `string`.")
        if not hasattr(self, 'source_files'):
            warning(self.__class__.__name__,"No source files defined for data, expect key `source_files` as type `list`.")
        # IN PLACE
        if hasattr(self, 'source_directory') and hasattr(self, 'source_files'):
            self.__run__()
        return None
    
    @staticmethod
    def Select_source_directory() -> str:
        """
        This function open a folder dialog and allow select a destination folder that contains source files.
        Args: 
            none
        Returns: 
            (unnamed value, string) : path to folder with source files
        """
        source_directory = filedialog.askdirectory(title="Select source directory.")
        return source_directory

    @staticmethod
    def Select_files(source_directory = None) -> List[str]:
        """
        This function opens a multiple filedialog and allow to select source files.
        Args: 
            source_directory (string, optional) : Open file dialogue in this directory, defaults to ``None``.
        Returns: 
            (unnamed value, list) : List of string with the file path.
        Note:
            Change of ``askopenfilename`` to ``askopenfilenames`` is intended for a future version, such as the organization of the string within a list is hopefully more clear.
        """
        file = filedialog.askopenfilename(
            initialdir = source_directory, 
            title="Select files", 
            filetypes = (
                ("TIFF Files", "*.tiff;*.tif"),
                ("All files", "*.*")
            )
        )
        source_files = [os.path.basename(file)]
        #source_files.extend(files)
        return source_files

    @staticmethod
    def _searchpoint(img, pointlist, previousvalue, actualX):
        """
        Auxiliar function in case that the trace is lost allow to search forward one pixel more selecting the best value in the next five pixels adjacent.
        Args: 
            (1st positional argument `img`, array) : image that is analysed
            (2nd positional argument `pointlist`, list) : list of selected point for this trace
            (3rd positional argument `previousvalue`, float) : previous value for the Y coordinate
            (4th positional argument `actualX`, float) : actual x value in the scan
        Returns: 
            (unnamed value, float) : the previous value of y
        """
        try:
            # create a dictionary
            asa = {}
            # load the adjacent values
            for l in range(3):
                asa[l] = img[actualX, int(previousvalue) + l]
            # select the maximum values
            max_value = max(asa.values())
            # append the best value
            for key, value in asa.items():
                if value == max_value:
                    pointlist.append((int(key + previousvalue), actualX))
                    previousvalue = key + previousvalue
                    break
            return previousvalue
        except Exception as ex:
            raise Exception("searchpoint fail!")

    @staticmethod
    def _rows(img, clone, actualX, threshold):
        """
        Auxiliar function searches the local maximum in one row
        Args:
            (1st positional argument `img`, array) : image that is anlizing
            (2nd positional argument `clone`, array)  : copy of image, the function will add highlighting of local maximuma
            (3rd positional argument `previousvalue`, float) : previous value for the Y coordinate
            (4th positional argument `actualX`, float) : actual row
            (5th positional argument `threshold`, float) : the difference between two point in order to be considered a local maximum
        Returns:
            (unnamed value, float) : Sorted list of local maxima.
        """
        # initialize variables
        #  set to save the maximum
        localmax = set()
        #  row of the image proccesed
        row = img[actualX:actualX + 1, :]
        #  rest
        localMaxima = []
        oldstatus = 0
        newstatus = 0
        maxvalue = 0
        maxvalex = 0
        # scan the row.  Works as a states machine searching for flanks
        for x in range(row.shape[1] - 1):
            centerValue = int(row[0, x])
            rightValue = int(row[0, x + 1])
            if rightValue - centerValue > threshold:
                if newstatus == 0 and oldstatus == 0:
                    minx = x
                    oldstatus = 0
                    newstatus = 1
            elif centerValue - rightValue > threshold:
                if newstatus == 1 and oldstatus == 1:
                    oldstatus = 1
                    newstatus = 0
            else:
                if newstatus == 1 and oldstatus == 0:
                    oldstatus = 1
                    newstatus = 1
                    if maxvalue < centerValue:
                        maxvalue = centerValue
                        maxvalex = x
                elif newstatus == 0 and oldstatus == 1:
                    maxx = x
                    oldstatus = 0
                    newstatus = 0
                    p = (maxvalex, actualX)
                    localMaxima.append(p)
                    localmax.add(maxvalex)
                    maxvalue = 0
                    maxvalex = 0
                elif newstatus == 1 and oldstatus == 1:
                    if maxvalue < centerValue:
                        maxvalue = centerValue
                        maxvalex = x
        # highlight the local maximum
        for maxima in localMaxima:
            cv2.circle(clone, maxima, 1, (255, 255, 0))
        # return the local maximum ordered
        return sorted(localmax)

    def ThompsomParabolaImageprocessingV2(self, pathDestinationSelected: str, picturesSelected: List[str],
                                          threshold: int = 0, wake: int = 0, quality_n: int = 100):
        """ Tracefinder for Thomson Parabola Ion Spectrometer
        This function search for the different traces in a Thomson parabola image.
        For output, five folders are created:
        1) folder input save the original image
        2) folder output save the original image where the traces are painted with different colours
        3) folder mask save the traces with different colours
        4) folder ouput gray save the traces without discrimination
        5) folder text save the sum of the 5 adjacent values in a csv
   
        Args: 
            pathDestinationSelected (str): output folder
            picturesSelected (list): List of path for the different pictures
            threshold (int, optional): the difference between two point in order to be considered a local maximum, initializes to ``0`` and defaults to ``(max(img)-min(img))/100``.
            wake (int, optional): The maximum number of points tha can be founded with searchpoint function, initializes to ``0`` and defaults to ``size(row)/10``.
            quality_n: the minimum number of real point admmited in a trace
        
        """
        # intialize variables
        self.filename = ""
        
        # fit dispersion relation if available
        if hasattr(self, 'dispersion_relation') and hasattr(self, 'pixel_per_space') and hasattr(self, 'X_ray_spot'):
            conversion = True
            # build unit conversion for spectrum
            disprelprot = np.loadtxt(self.dispersion_relation,skiprows=1)[1:]
            dxde=np.array([[0, 0]])
            for x in range(0, len(disprelprot)-1):
               dxde=np.append(dxde, [[(disprelprot[x, 1]-disprelprot[x+1, 1])/(disprelprot[x+1,0]-disprelprot[x,0]),disprelprot[x, 0]]],axis=0)
            dxde = dxde.T
            dxde_of_energy = interpolate.interp1d(dxde[1], dxde[0], fill_value="extrapolate")
            # define funtion energy(space) for lookup of coordinates
            disrel = disprelprot.T
            energy_of_y = interpolate.interp1d(disrel[1] * self.pixel_per_space, disrel[0], fill_value="extrapolate")
        else:
            conversion = False

        # start the proccess
        try:
            # scan each file in the List
            for file in picturesSelected:

                # inicialize variables
                memory = {}
                quality = {}
                trazas = {}

                # get the name of the file
                self.filename = os.path.basename(file)

                # read the file
                img = cv2.imread(os.path.join(pathDestinationSelected,file), cv2.IMREAD_ANYDEPTH | cv2.IMREAD_GRAYSCALE)

                # filter the X ray in the image
                cv2.medianBlur(img, 5, img)

                # prepare the different output images
                #  filtered
                self.Xfiltered = img.copy()
                #  prepare canvas for image with highlightened maxima
                self.rowmaxs = np.zeros_like(img, dtype=np.uint8)
                #  RGB copy canvas for later trace add in
                self.superposition = img.copy()
                self.superposition = cv2.convertScaleAbs(self.superposition, alpha=(255.0 / self.superposition.max()))
                self.superposition = cv2.cvtColor(self.superposition, cv2.COLOR_GRAY2RGB)
                #  grayscale canvas for later trace add in
                self.trace = np.zeros_like(img, dtype=np.uint8)

                # range of row scans
                range_iter = range(np.shape(img)[0]-1, -1, -1)
                
                # find or fix threshold
                if threshold == 0:
                    threshold = max(int((np.nanmax(img)-np.nanmin(img))/100.),1)

                # search the local maximum
                for i in range_iter:
                    sort = self._rows(img, self.rowmaxs, i, threshold)
                    if len(sort) != 0:
                        memory[i] = sort
                memory = {k: memory[k] for k in sorted(memory.keys())}
                
                # combinin the different maximum to find the nearest if doesnt exist search with sarchpoint function a point
                init2 = list(memory.keys())
                counter = 1
                
                if wake == 0:
                    wake = max(int(img.shape[1] / 10.),1)
                
                if memory:
                    for j in range(init2[0], init2[-1]):
                        a = []
                        rem = {}

                        # check the actual y in memory
                        if j in memory:
                            qul = 0
                            flse = 0
                            # select all the local maximum in a row
                            for prev in memory[j]:
                                flse = 0
                                a = []
                                a.append((prev, j))
                                me = prev
                                meme = prev
                                qul += 1
                                if j in rem:
                                    rem[j].append(int(meme))
                                else:
                                    aux = []
                                    aux.append(int(me))
                                    rem[j] = aux
                                # compare with the next row to find the closest maximum
                                for k in range(j + 1, init2[-1]):
                                    if k in memory:
                                        if len(memory[k]) != 0:
                                            c1 = 0
                                            for sea in memory[k]:
                                                if sea + 3 >= me and sea - 3 <= me:
                                                    a.append((sea, k))
                                                    c1 = 1
                                                    meme = sea
                                                    me = sea
                                                    qul += 1
                                                    flse = 0
                                                    break
                                                elif sea + 6 >= me and sea <= me:
                                                    meme = sea
                                                    qul += 1
                                                    c1 = 1
                                                    me = self._searchpoint(img, a, sea, k)
                                                    break
                                                else:
                                                    c1 = 2
                                            if c1 == 1:
                                                if k in rem:
                                                    rem[k].append(int(meme))
                                                else:
                                                    aux = []
                                                    aux.append(int(meme))
                                                    rem[k] = aux
                                                c1 = 0
                                            elif c1 == 2:
                                                me = self._searchpoint(img, a, me, k)
                                                flse += 1
                                                if flse > wake:
                                                    break
                                        else:
                                            me = self._searchpoint(img, a, me, k)
                                            flse += 1
                                            if flse > wake:
                                                break
                                    else:
                                        me = self._searchpoint(img, a, me, k)
                                        flse += 1
                                        if flse > wake:
                                            break
                                    if me > 1200:
                                        break
                                    if flse > wake and len(a) == wake:
                                        for l in range(wake):
                                            a.pop()

                                        break
                                # save the trace and the quality of the trace
                                trazas[counter] = a
                                quality[counter] = qul
                                if counter == 162:
                                    counter = counter
                                qul = 0
                                counter += 1
                                # remove the local maximum already used in this trace
                                for kk in rem.keys():
                                    for kkk in rem[kk]:
                                        if kkk in memory[kk]:
                                            memory[kk].remove(kkk)

                                # remove the traces with not enough quality
                                for a in quality.items():
                                    if a[1] < quality_n:
                                        trazas.pop(a[0], None)
                # image creation proccess and trace array per trace
                c3 = 0
                trace_array = []
                if conversion:
                    trace_array_energy = []
                for trazalist in trazas.keys():
                    trazasarray = trazas[trazalist]
                    trace_array.append([])
                    if conversion:
                        trace_array_energy.append([])
                    # write trace and prepare the other outputs
                    for l in range(len(trazasarray) - 1):
                        self.superposition = cv2.line(self.superposition, trazasarray[l], trazasarray[l + 1], (255, 0, 0), 4)
                        self.trace = cv2.line(self.trace, trazasarray[l], trazasarray[l + 1], 255, 3)
                        X = trazasarray[l][0]
                        Y = trazasarray[l][1]

                        Summa = int(self.Xfiltered[Y, X - 2]) + int(self.Xfiltered[Y, X - 1]) + int(self.Xfiltered[Y, X]) + int(self.Xfiltered[Y, X + 1]) + int(self.Xfiltered[Y, X + 2])
                        trace_array[-1].append([X,Y,Summa])
                        
                        if conversion:
                            space_var = self.X_ray_spot[1] - Y
                            energy_var = energy_of_y(space_var)
                            trace_array_energy[-1].append([energy_var,Summa*dxde_of_energy(energy_var)])

                    c3 += 1
                # save the other files
                print(" > "+self.filename + " processed\n")
                self.trace_array = trace_array
                if conversion:
                    self.trace_array_energy = trace_array_energy

        # in case of fail the processed picturs are removed and the proccess is restarted
        except Exception as ex:
            print(ex)
            print(" > "+self.filename + " failed\n")

        return None
        
    def __run__(self):
        # INTEGRITY
        if not hasattr(self, 'source_directory'):
            self.source_directory = self.Select_source_directory()
        if not hasattr(self, 'source_files'):
            self.source_files = self.Select_files(source_directory = self.source_directory)
        if not hasattr(self, 'local_threshold'):
            warning(self.__class__.__name__,"No threshold defined for search of local maxima, expect key `local_threshold` as type `int`. Defaults to `1%` of the difference between maximum and minimum.")
            self.local_threshold = 0
        if not hasattr(self, 'local_wake'):
            warning(self.__class__.__name__,"No row-by-row wake defined, expect key `local_wake` as type `int`. Defaults to `10%` of the length of one row.")
            self.local_wake = 0
        if not hasattr(self, 'local_quality'):
            warning(self.__class__.__name__,"Minimum number of points before a trace is identified as valid, expect key `local_quality` as type `int`. Defaults to ``100``")
            self.local_quality = 100
        # MAIN
        self.ThompsomParabolaImageprocessingV2(
            pathDestinationSelected = self.source_directory,
            picturesSelected = self.source_files,
            threshold = self.local_threshold,
            wake = self.local_wake, 
            quality_n = self.local_quality
        )
        # housekeeping
        if hasattr(self, 'trace_array'):
            self.status = True
    def analyse(self):
        # START
        self.__run__()
            
class ToF():
    """ Interactive Time-of-Flight diagnostics.
    The class allows interactive work with data from a 1D Time-of-Flight detector. The interpretation of input waveforms is done relativistically. 
    
    Args:
        distance  (float,optional) : Source to detector distance in units of [m].
        waveform  (str,optional) : Absolute path to measurement in a waveform file.
        channel   (int,optional) : If more than one channel is contained in the waveform file,
            channel number `channel` is chosen for analyisis. Defaults to `1`.
        polarity  (int,optional) : Polarity is `+1` for positive amplitudes of peaks and `-1` else. 
            Defaults to `+1`.
        bandwidth  (list of floats,optional) : Bandwidth of detection circuit. 
            Defaults to `[None,None]` - without limits.
        warnings  (bool,optional) : display warning messages, defaults to TRUE
    
    Attributes:
        signaltonoise (int) : Assumed signal to noise ratio, initializes to 4.
        prenoiseperiods (int) : Assumed number of noise periods that can be used for averaging, initializes to 5.
        status (bool) : True if processing was successfull, else False.
            Initializes to False.
    
    Returns:
        Xrise (float) : Arrival time of X-rays with respect to the time base of the waveform, evaluated when the noise-filtered signal surpases signal to noise ratio, likely in units of [s].
        Xfall (float) : Time, with respect to the time base of the waveform, when signal of X-rays decayed under the signal to noise ratio, evaluated on the noise filtered trace, likely in units of [s].
        Prise (float) : Arrival time of Projectiles with respect to the time base of the waveform, evaluated when the noise-filtered signal surpases signal to noise ratio, likely in units of [s].
        Pfall (float) : Time, with respect to the time base of the waveform, when signal of Projectiles decayed under the signal to noise ratio, evaluated on the noise filtered trace, likely in units of [s].
        tof (:obj: ``numpy.array``) : Time of flight from source position to detector for all data-bins between Prise and Pfall.
        Gminus1 (:obj: ``numpy.array``) : Ratio of relativistic kinethic energy and rest mass energy (equals gamma-factor minus 1) for all data-bins between Prise and Pfall. For conversion to kinethic energy, multiply rest mass of species under regard.
        dN_dGminus1 (:obj: ``numpy.array``) : Detector signal in practical units of `dN/d(gamma-1)`, where N is in units of the amplitude of the measurement.
        dN_dGminus1_lowpass (:obj: ``numpy.array``) : Low pass of detector signal in practical units of `dN/d(gamma-1)`, where N is in units of the amplitude of the measurement.
        
    Note:
        The original data array is not part of the object after processing. If `Xrise` is set, no automatic search is performed, reset with the `reset("Xrise")` class method.
        
    Examples:
        The class can be used in a functional way

        ```python 
        from pyclpu import metrology
        spectrum = metrology.ToF(distance = 100, waveform = "path/to/data.csv", channel = 1)
        ```

        A more object oriented use case demonstrates how a run can be started after initialization

        ```python 
        from pyclpu import metrology

        tof_detector = metrology.ToF()
        tof_detector.distance = 100
        tof_detector.channel = 1
        tof_detector.polarity = -1

        tof_detector.waveform = "path/to/data.csv"

        tof_detector.analyse()
        tof_detector.show()
        ```
        returns a non-blocking plot that can be refreshed through further calls to `show()`.
    """
    # INI
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
        self.signaltonoise = 4
        self.prenoiseperiods = 5
        self.status = False
        # INTEGRITY
        if not hasattr(self, 'warnings'):    
            self.warnings = True
        if not hasattr(self, 'distance'):
            if self.warnings: warning(self.__class__.__name__,"No source to detector distance defined, expect key `distance` as type `float`.")
        if not hasattr(self, 'waveform'):
            if self.warnings: warning(self.__class__.__name__,"No source file defined for data, expect key `waveform` as type `str`.")
        if not hasattr(self, 'channel'):
            if self.warnings: warning(self.__class__.__name__,"No source channel defined for data, expect key `channel` as type `int`.")
        if not hasattr(self, 'polarity'):    
            self.polarity = 1
        if not hasattr(self, 'bandwidth'):    
            self.bandwidth = [None,None]
        # IN PLACE
        if hasattr(self, 'distance') and hasattr(self, 'waveform') and hasattr(self, 'channel'):
            self.__run__()
        return None
    def __run__(self):
        # INTEGRITY
        if not hasattr(self, 'distance'):
            error(self.__class__.__name__,"No source to detector distance defined, expect key `distance` as type `float`. DO NOTHING.",1169)
            self.status = False
            return None
        if not hasattr(self, 'waveform'):
            error(self.__class__.__name__,"No source file defined for data, expect key `waveform` as type `str`. DO NOTHING.",1169)
            self.status = False
            return None
        if not hasattr(self, 'channel'):
            if self.warnings: warning(self.__class__.__name__,"No source channel defined for data, expect key `channel` as type `int`. Set `channel = 1`.")
            self.channel = 1
        if len(self.bandwidth) != 2:
            if self.warnings: warning(self.__class__.__name__,"No valid bandwidth defined, expect key `bandwidth` as type `list` of floats. Set `bandwidth = [None,None]`.")
            self.bandwidth = [None,None]
        # VARIABLES

        # METHODS

        # MAIN
        # load data
        if self.bandwidth[0] == None and self.bandwidth[1] == None:
            trace = Waveform(wfm = wfmread(self.waveform), channel = self.channel, warnings = False)
        elif self.bandwidth[0] is not None and self.bandwidth[1] is not None:
            trace = Waveform(wfm = wfmread(self.waveform), channel = self.channel, lowest_frequency = self.bandwidth[0], highest_frequency = self.bandwidth[1], warnings = False)
        elif self.bandwidth[0] is not None:
            trace = Waveform(wfm = wfmread(self.waveform), channel = self.channel, lowest_frequency = self.bandwidth[0], warnings = False)
        elif self.bandwidth[1] is not None:
            trace = Waveform(wfm = wfmread(self.waveform), channel = self.channel, highest_frequency = self.bandwidth[1], warnings = False)
        if trace.status == False:
            error(self.__class__.__name__,"Can not build trace from waveform data.",1160)
            self.status = False
            return None
        trace.vertical = trace.vertical * self.polarity
        # find arrival time of X-rays
        # a) with peak detection
        #    - find peaks in bandpass-corrected signal
        # Xtime = signal.find_peaks_cwt(trace.vertical, np.arange(1,self.typicalpeakwidth), min_snr = 3)
        # b) assuming clear rising edge (fast method, least accuracy)
        #    - calculate typical length of one "noise wave"
        typical_noise = int(trace.noise_period/trace.dt) * self.prenoiseperiods
        #    - calculate average noise level within typical length
        noise = np.sum(np.abs(trace.vertical[0:typical_noise])) / typical_noise
        #    - calculate moving average with a bin size equal to the typical length
        ret = np.cumsum(trace.vertical, dtype=float)
        ret[typical_noise:] = ret[typical_noise:] - ret[:-typical_noise]
        moving_average = np.zeros(np.shape(ret))
        moving_average[int(typical_noise/2) - 1:-int(typical_noise/2)] = ret[typical_noise - 1:] / typical_noise
        #    - get tips which are above the noise (i.e. noise multiplied with signal to noise ratio)
        islands = np.where(np.abs(moving_average) > np.abs(self.signaltonoise * noise))[0]
        tips = []
        for l,land in enumerate(list(islands)):
            if l == 0:
                tips.append(land)
            elif l + 1 == islands.size:
                break
            elif land + 1 != islands[l + 1]:
                tips.append(land)
        print("signal starts at",trace.horizontal[tips[0]],"for",trace.horizontal[tips[-1]]-trace.horizontal[tips[0]])
        #    - check for input parameter /
        if not hasattr(self, 'Xrise'):
            #    - get rising edge as first element of the first tip
            try:
                self.Xrise = trace.horizontal[tips[0]] + trace.noise_period * self.prenoiseperiods/2.
            except:
                error(self.__class__.__name__,"Can not find X-ray peak from waveform data.",1160)
                self.status = False
                return None
        else:
            if self.warnings: warning(self.__class__.__name__,"X-ray peak from input variable, ignore auto-search.")
        #    - get falling edge as last element of the first tip
        self.Xfall = trace.horizontal[tips[1]]
        # find slower projectiles (if there is no gap between X-rays and projectiles, maybe there is a problem with leaking electrons)
        try:
            N_Prise = tips[2]
            N_Pfall = tips[-1]
            self.Prise = trace.horizontal[N_Prise]
            self.Pfall = trace.horizontal[N_Pfall]
        except:
            warning(self.__class__.__name__,"Detect no gap between X-ray peak and peak of massive projectiles. See plot and tune, e.g. signal to noise ratio. Exits after pop-up window is closed.")
            plt.plot(moving_average)
            plt.plot(trace.vertical)
            plt.hlines([tips[0],tips[-1]])
            plt.show()
            return None
        # transform time base to base in units of kinetic-energy/rest-mass-energy for times larger than Ptime (ratio equal to gamma - 1)
        tof = trace.horizontal[N_Prise:N_Pfall] - self.Xrise + self.distance / constants.speed_of_light
        T_m = 1./np.sqrt(1. - (self.distance/constants.speed_of_light/tof)**2) - 1.
        # transform the signal amplitude in spectral counts (so far without multiplying a calibration factor)
        dT_dt = (T_m[1:]-T_m[:-1])/(tof[1:]-tof[:-1])
        dT_dt = np.append(dT_dt, [dT_dt[-1]])
        dN_dT = trace.vertical[N_Prise:N_Pfall] / ( - dT_dt)
        dN_dT_lowpass = moving_average[N_Prise:N_Pfall] / ( - dT_dt)
        # publication
        self.tof = tof
        self.amp = trace.vertical[N_Prise:N_Pfall]
        self.Gminus1 = T_m
        self.dN_dGminus1 = dN_dT
        self.dN_dGminus1_lowpass = dN_dT_lowpass
        # integrity of results
        if isinstance(dN_dT,np.ndarray):
            self.status = True
        else:
            message(self.__class__.__name__,"Output stream invalid.")
            self.status = False
        # housekeeping
        del noise, trace, moving_average, tof, T_m, dT_dt, dN_dT, dN_dT_lowpass
        return None
    def analyse(self):
        # START
        self.__run__()
    def show(self):
        if self.status:
            # use open frame or create new
            new_plt_id = True
            try:
                if hasattr(self, 'plot'):
                    if "num" in self.plot.keys():
                        if plt.fignum_exists(self.plot['num']):
                            fig = self.plot['fig']
                            ax0 = self.plot['axs']
                            ax0.clear()
                            new_plt_id = False
                            plt.figure(fig.number)
            except:
                pass
            if new_plt_id:    
                plt.ion()
                fig = plt.figure(figsize=(15,10), dpi=100)
                ax0 = fig.add_subplot()
                self.plot = {}
                self.plot['num'] = fig.number
                self.plot['fig'] = fig
                self.plot['axs'] = ax0
            # plotting
            ax0.plot(self.Gminus1,self.dN_dGminus1,label="data spectrum")
            ax0.plot(self.Gminus1,self.dN_dGminus1_lowpass,label="lowpass spectrum")
            ax0.legend()
            plt.tight_layout()
            # display
            if new_plt_id:
                plt.show()
                plt.pause(1.001)
            else:
                plt.draw()
                plt.pause(0.201)
    def reset(self,attr):
        self.__dict__.pop(attr,None)