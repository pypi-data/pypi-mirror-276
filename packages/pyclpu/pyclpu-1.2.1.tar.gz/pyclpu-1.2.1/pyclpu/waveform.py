# -*- coding: utf-8 -*-
""" This is the CLPU module for waveform manipulation.

Please do only add or modify but not delete content.

requires explicitely {
 - os
 - sys
 - numpy
}

import after installation of pyclpu via {
  from pyclpu import waveform
}

import without installation via {
  root = os.path.dirname(os.path.abspath(/path/to/pyclpu/waveform.py))
  sys.path.append(os.path.abspath(root))
  import waveform
  from importlib import reload 
  reload(waveform)
}

"""

# =============================================================================
# PYTHON HEADER
# =============================================================================
# EXTERNAL
import os
import sys
from inspect import getsourcefile
from importlib import reload

import math
import numpy as np
import scipy
import matplotlib.pyplot as plt

# INTERNAL
root = os.path.dirname(os.path.abspath(getsourcefile(lambda:0))) # get environment
sys.path.append(os.path.abspath(root))                           # add environment
sys.path.append(os.path.abspath(root)+os.path.sep+"LIB")         # add library

if "constants" not in globals() or globals()['constants'] == False:
    import constants                        # import all global constants from                   constants.py
    import formats                          # import all global formats from                     formats.py
    from manager import error               # import error() from management                     manager.py
    from manager import message             # import message() from management                   manager.py
    from manager import warning             # import warning() from management                   manager.py
    from manager import give_extension      # import give_extension() from management            manager.py
    from manager import give_dirlst         # import give_dirlst() from management               manager.py
    reload(constants)
    reload(formats)

# STYLE

# =============================================================================
# CONSTANTS
# =============================================================================
# INTEGRATION AND TESTING
test = True

# PARAMETERS

# CONSTANTS

# =============================================================================
# METHODS
# =============================================================================
# INTEGRATION AND TESTING
def test_pingpong(*args, **kwargs):
    """ Tests functionality of functions. 
 
    Function prints any input.
 
    Args:
        `*args`   : Any number of positional arguments.
        `**kwargs`: Any number of named keyval arguments.
    
    Returns:
        exit_stat (bool) : True in case of success and False else.
    
    Examples:
        ```python
        test_pingpong(True,kwa=True)
        ```
        returns
        ```
        True
        kwa : True
        ```
    """
    try:
        for arg in args:
            print(arg)
        for key, value in kwargs.items():
            print(str(key) + " : "+ str(value))
    except:
        return False
    return True

# WAVEFORM T/I/O
def iswfm(path: str) -> bool:
    """ Checks for waveform file. 
 
    The function looks up if the argument of type string describes the path to a waveform file.
 
    Args:
        path (str) : The path which is to be checked.
    
    Returns:
        exit_stat (bool) : True in case there is an waveform file and False else.
    
    Examples:
        ```python
        iswfm("")
        ```
        returns
        ```
        False
        ```
        
    Todo:
        * accept waveform object as input as well
    """
    try:
        extension = give_extension(path)
        if extension in formats.acceptedinput["waveform"]:
            return True
        else:
            return False
    except:
        error(iswfm.__name__,"",code=1287)

def wfmread(path):
    """ Reads waveform file. 
 
    The function tries to read a waveform file to a numpy array as `[channel,amplitude,timebase]`.
 
    Args:
        path (str) : The path to a waveform file.
    
    Returns:
        wfm (:obj: `numpy.array`) : Matrix of values as ``[channel,amplitude,timebase]``
        
    Examples:
        ```python
        from pyclpu import waveform
        wfm = waveform.wfmread("")
        ```
        returns
        ```
        None
        ```
    """
    # METHODS
    def loader(from_file):
        if give_extension(from_file) == "bin":
            try:
                from RSRTxReadBin import RTxReadBin
            except:
                path_to_module = os.path.join(*give_dirlst(root)[:-1],"lib","RTxReadBin-1.0-py3-none-any.whl")
                error(wfmread.__name__,"RTxReadBin not installed. Run pip install "+path_to_module,1169)
                return None
            # load all
            y, x, S = RTxReadBin(from_file)
            vertical = np.transpose(y[:,0,:]) # assume the zeroth acquisition to be the only one and build [channel,amplitude]
            #print(S['MultiChannelVerticalOffset'])
            horizontal = x
        else:
            # find data
            skiplines = 0
            with open(from_file, 'r') as file:
                lines = file.readlines()
            for number,line in enumerate(lines):
                try:
                    first_character = line.strip()[0]
                    if (first_character.isnumeric() or first_character == "-"):
                        skiplines = number
                        break
                except:
                    continue
            # load data
            try:
                contents = np.loadtxt(from_file,skiprows=skiplines)
            except:
                try:
                    contents = np.genfromtxt(from_file,skip_header=skiplines,delimiter=",",filling_values=np.NaN)
                except:
                    contents = np.genfromtxt(from_file,skip_header=skiplines,delimiter=";",filling_values=np.NaN)
                contents = contents[:, ~np.isnan(contents).any(axis=0)]
            if contents.size == 0 :
                try:
                    bin_contents = []
                    with open(from_file,"r") as fh:
                        for line in fh:
                            line = line.strip()
                            line = line.split(",")
                            array = []
                            for lin in line:
                                li = lin.split(";")
                                for l in li:
                                    array.append(float(l))
                            bin_contents.append(array)
                        del line,array,lin,li,l
                    contents = np.array(bin_contents)
                    del bin_contents
                except:
                    error(wfmread.__name__,"",code=1287)
            # try to find timebase in first column or as constant
            if all(np.isclose(np.diff(contents[:,0]),np.diff(contents[:,0])[0])):
                horizontal = contents[:,0]
                vertical = np.transpose(contents[:,1:]) # build [channel,amplitude]
            else:
                vertical = np.transpose(contents) # build [channel,amplitude]
                # known exception: R&S
                timebase_known = False
                if ".wfm." in from_file.lower():
                    meta_file = from_file.lower().replace(".wfm.",".")
                    # known keywords
                    with open(meta_file, 'r') as file:
                        lines = file.readlines()
                    for line in lines:
                        if "resolution" in line.lower():
                            try:
                                find_increment = line.lower().replace("resolution","").strip().strip(":;,")
                                horizontal = np.arange(vertical.shape[1]) * float(find_increment)
                                timebase_known = True
                                break
                            except:
                                continue
                # unknown exception: manual input
                if not timebase_known:
                    ask_increment = input("Please enter the increment of timesteps in units of [s]:\n")
                    horizontal = np.arange(vertical.shape[1]) * float(ask_increment)
                # housekeeping
                del timebase_known
        return {"horizontal" : horizontal, "vertical" : vertical}
    # EXECUTE
    if iswfm(path):
        wfm = loader(path)
    else:
        return None
    if wfm["vertical"].ndim == 1:
        wfm["vertical"] =np.array([wfm["vertical"]])
    # RETURN
    if wfm is None: # happens if there is trouble with the waveform format or the path
        error(wfmread.__name__,"",code=667)
        return None
    else:
        return wfm
        
def wfmshow(wfm, *args, **kwargs):
    """ Displays waveform. 
 
    The function shows the content of a waveform.
 
    Args:
        wfm (:obj: `numpy.array`) : Wafeform array.
    
    Returns:
        exit_stat (bool) : True in case of a completed run and False else.
    
    Examples:
        ```python
        wfmshow("")
        ```
        returns
        ```
        False
        ```
    """
    name = kwargs.get('name', "ANONYMOUS")
    nolabel = kwargs.get('nolabel', False)
    # Routine
    #try:
    if np.ndim(wfm["vertical"]) == 1:
        wfm["vertical"] = [wfm["vertical"]]
    for ai,active_channel in enumerate(wfm["vertical"]):
        if nolabel:
            label = ""
        else:
            label = str(ai+1)
        plt.plot(wfm["horizontal"],active_channel,label=label)
    if not nolabel:
        plt.legend()
    plt.show()
    plt.close('all')
    return True
    #except:
    #    error(wfmshow.__name__,"",13)
    #    return False
 
def wfmwrite(full_name, wfm):
    """ Writes waveform array to disk.
    The function writes the content of a waveform array to a disk loaction.
    It also generates a plot that is saved next to the data.
    
    Args:
        full_name (str) : Absolute path and filename in one string.
        wfm (:obj: `numpy.array`) : Wafeform array.
    
    Returns:
        exit_stat (bool) : True in case of a completed run and False else.
    """
    try:
        # data
        output = [wfm["horizontal"]]
        if np.ndim(wfm["vertical"]) == 1:
            wfm["vertical"] = [wfm["vertical"]]
        header = "Time/[s],"
        i = 1
        for active_channel in wfm["vertical"]:
            output.append(active_channel)
            header = header + "CH" + str(i) + "/[V],"
            i = i + 1
        header = header[:-1]
        np.savetxt(full_name, np.array(output).T, delimiter=",",header=header)
        # visual feedback
        for active_channel in wfm["vertical"]:
            plt.plot(wfm["horizontal"],active_channel)
        plt.xlabel("time / [s]")
        plt.ylabel("signal / [V]")
        plt.tight_layout()
        plt.savefig(full_name+".png", dpi = 600)
        plt.close('all')
        return True
    except:
        error(wfmwrite.__name__,"",13)
        return False
        
# WAVEFORM ANALYSYS

def FastFourierTransform(wfm, *args, **kwargs):
    """ Executes an FFT. 
 
    The function generates the Fast Fourier Transform of all available channels of a waveform.
 
    Args:
        wfm (:obj: `numpy.array`) : Wafeform array.
    
    Returns:
        fft (:obj: `numpy.array`) : FFT array.
    
    Examples:
        ```python
        FastFourierTransform("")
        ```
        returns
        ```
        None
        ```
    """
    try:
        fft = {}
        oneD = False
        if np.ndim(wfm["vertical"]) == 1:
            wfm["vertical"] = [wfm["vertical"]]
            oneD = True
        fft["timestep"]    = wfm["horizontal"][1] - wfm["horizontal"][0]
        fft["t_start"]     = wfm["horizontal"][0]
        fft["t_stop"]      = wfm["horizontal"][-1]
        fft["samples"]     = wfm["vertical"][0].size
        fft["frequencies"] = scipy.fft.rfftfreq(fft["samples"], d = fft["timestep"])
        amplitudes = []
        for ai,signal in enumerate(wfm["vertical"]):
            signal_FFT         = scipy.fft.rfft(signal,workers = os.cpu_count())
            amplitudes.append(signal_FFT)
        if oneD:
            amplitudes = amplitudes[0]
        fft["amplitudes"]  = np.array(amplitudes)
        return fft
    except:
        error(FastFourierTransform.__name__,"",13)
        return None
    
def InverseFastFourierTransform(fft, *args, **kwargs):
    """ Executes an inverse FFT. 
 
    The function generates the time-domain values of all available channels of a Fourier Transformed sgnal.
 
    Args:
        fft (:obj: `numpy.array`) : Fourier Transform dictionary ``{"timestep": real, "samples" : integer, "amplitudes" : np.array(), "frequencies" = np.array()}``.
    
    Returns:
        wfm (:obj: `numpy.array`) : Waveform array.
    
    Examples:
        ```python
        InverseFastFourierTransform("")
        ```
        returns
        ```
        None
        ```
    """
    try:
        vertical = []
        oneD = False
        if np.ndim(fft["amplitudes"]) == 1:
            fft["amplitudes"] = [fft["amplitudes"]]
            oneD = True
        for ai,amplitude in enumerate(fft["amplitudes"]):
            ifft = scipy.fft.irfft(amplitude,n=fft["samples"], workers = os.cpu_count())
            vertical.append(ifft)
        if oneD:
            vertical = vertical[0]
        horizontal = np.linspace(fft["t_start"],fft["t_stop"],num=fft["samples"])
        return {"horizontal" : horizontal, "vertical" : np.array(vertical)}
    except:
        error(InverseFastFourierTransform.__name__,"",13)
        return None
        
# WAVEFORM MANIPULATION

def bandpass(wfm, f_start, f_stop, *args, **kwargs):
    """ Applies brick-wall bandpass filter to a waveform. 
 
    The function generates the filtered time-domain values of all available channels in a waveform. The frequencies from `f_start` to ´f_stop` pass, others are supressed.
 
    Args:
        wfm (:obj: `numpy.array`) : Wafeform array.
        f_start (float) : Lower limit of bandpass.
        f_stop (float) : High limit of bandpass.
    
    Returns:
        wfm (:obj: `numpy.array`) : Filtered waveform array.
    
    Examples:
        ```python
        bandpass("")
        ```
        returns
        ```
        None
        ```
    """
    try:
        fft = FastFourierTransform(wfm)
        passed = np.where(np.logical_and(fft["frequencies"]>=f_start, fft["frequencies"]<=f_stop),True,False)
        amplitudes = []
        if np.ndim(fft["amplitudes"]) == 1:
            fft["amplitudes"] = [fft["amplitudes"]]
            oneD = True
        for ai,amps in enumerate(fft["amplitudes"]):
            fft["amplitudes"][ai] = np.where(passed,fft["amplitudes"][ai],0.+0.j)
        if oneD:
            fft["amplitudes"] = fft["amplitudes"][0]
        else:
            fft["amplitudes"] = np.array(fft["amplitudes"])
        return InverseFastFourierTransform(fft)
    except:
        error(bandpass.__name__,"",13)
        return None
    
# =============================================================================
# CLASSES
# =============================================================================
# INTEGRATION AND TESTING
class Main:
    # https://realpython.com/python-class-constructor/
    def __new__(cls, *args, **kwargs):
        #1) Create from this class as cls a new instance of an object Main
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        #2) Initialize from the instance of an object Main as self the initial state of the object Main
        for arg in args:
            warning(self.__class__.__name__,"Object does not accept unnamed arguments! Ignore: "+str(arg))
        for key, value in kwargs.items():
            self.key = value
        return None
            
    def __setattr__(self, name, value):
        #3) Set attributes of the instance during runtime, e.g. to change the initial state
        #if name in self.__dict__:
        #    print("!!! Warning...........Call to __setattr__ overwrites value of "+str(name)+ " with "+str(value))
        super().__setattr__(name, value)
        return None

    def __repr__(self) -> str:
        #anytime) representation as string, e.g. for print()
        string = "(\n"
        for att in self.__dict__:
            string = string + str(att) + " -> " + str( getattr(self,att) ) + "\n"
        return str(type(self).__name__) + string + ")"

# MAIN OBJECT  
class Waveform():
    """ Waveform object.
    The class allows interaction with a waveform object. Build-in functions allow to display the data `.show()`; to save the data `.save("path/to/file.csv")`; ...
    
    Args:
        wfm    (dict,optional) : Waveform source as dictionary ``{"horizontal": numpy.array, "vertical": numpy.array(*channels)}`` .
        channel (int,optional) : Channel of interest.
        lowest_frequency (float,optional) : Lowest frequency that can pass through the circuit, defaults to zero.
        highest_frequency (float,optional) : Highest frequency that can pass through the circuit, defaults to the maximum allowed by the sampling rate.
        crop_peak (list,optional) : Crops signal around peak by indicated amount of time before (list position 0) and after (list position 1) the peak.
        warnings  (bool,optional) : display warning messages, defaults to TRUE
    
    Attributes:
        status (bool) : True if processing was successfull, else False.
            Initializes to False.
    
    Returns:
        horizontal (float) : Array with horizontal axis.
        vertical (float) : Array with vertical axis.
        dt (float) : Timestep of vertical axis.
        noise_period (float) : Periodicity of noise (in units of `horizontal` from the beginning of the waveform.
        
    Note:
        The source of the waveform is not part of the object after processing.
        
    Examples:
        The class holds the main object of the `waveform` module.

        ```python 
        from pyclpu import waveform
        wfm_1 = waveform.Waveform()
        ```
    """
    # INI
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
        self.status = False
        # INTEGRITY
        if not hasattr(self, 'warnings'):    
            self.warnings = True
        if not hasattr(self, 'wfm'):
            if self.warnings: warning(self.__class__.__name__,"No waveform source defined, expect key `waveform` as `waveform={'horizontal': numpy.array, 'vertical': numpy.array(*channels)}`.")
        if not hasattr(self, 'channel'):
            if self.warnings: warning(self.__class__.__name__,"No source channel defined for data, expect key `channel` as type `int`.")
        if not hasattr(self, 'lowest_frequency'):
            if self.warnings: warning(self.__class__.__name__,"No lowmost frequency defined for circuit, expect key `lowest_frequency` as type `float`.")
        if not hasattr(self, 'highest_frequency'):
            if self.warnings: warning(self.__class__.__name__,"No highmost frequency defined for circuit, expect key `highest_frequency` as type `float`.")
        if not hasattr(self, 'crop_peak'):
            if self.warnings: warning(self.__class__.__name__,"No cropping intervall defined for signal, expect key `crop_peak` as type `list`.")
        # IN PLACE
        if hasattr(self, 'wfm') and hasattr(self, 'channel'):
            self.__run__()
        return None
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if hasattr(self, 'wfm') and hasattr(self, 'channel'):
            if name in ["wfm","channel"]:
                self.__run__()
        return None
    def __run__(self):
        # INTEGRITY
        if not hasattr(self, 'wfm'):
            error(self.__class__.__name__,"No waveform source defined, expect key `waveform` as `waveform={'horizontal': numpy.array, 'vertical': numpy.array(*channels)}`. DO NOTHING.",1169)
            return None
        if self.wfm is None:
            error(self.__class__.__name__,"No valid waveform source defined, expect key `waveform` as `waveform={'horizontal': numpy.array, 'vertical': numpy.array(*channels)}`. DO NOTHING.",1169)
            return None
        if not hasattr(self, 'channel'):
            if self.warnings: warning(self.__class__.__name__,"No source channel defined for data, expect key `channel` as type `int`. Set `channel = 1`.")
            self.channel = 1
        if not hasattr(self, 'lowest_frequency'):
            if self.warnings: warning(self.__class__.__name__,"No lowmost frequency defined for circuit, expect key `lowest_frequency` as type `float`. Defaults to zero.")
            self.lowest_frequency = 0.
        if not hasattr(self, 'highest_frequency'):
            self.highest_frequency = scipy.fft.rfftfreq(self.wfm["horizontal"].size, d = self.wfm["horizontal"][1] - self.wfm["horizontal"][0])[-1]
            if self.warnings: warning(self.__class__.__name__,"No highmost frequency defined for circuit, expect key `highest_frequency` as type `float`. Defaults to maximum by sampling rate: " +str("%.2E" % self.highest_frequency))
        if not hasattr(self, 'crop_peak'):
            self.crop_peak = []
            if self.warnings: warning(self.__class__.__name__,"No cropping intervall defined for signal, expect key `crop_peak` as type `list`. Defaults to `[]` ")
        elif not (len(self.crop_peak) == 2):
            self.crop_peak = []
            if self.warnings: warning(self.__class__.__name__,"Weird cropping intervall defined for signal, expect key `crop_peak` as type `list` of length 2. Defaults to `[]` ")
        # MAIN
        if not self.crop_peak:
            self.horizontal = self.wfm["horizontal"]
            self.vertical = self.wfm["vertical"][self.channel-1]
        else:
            dt = self.wfm["horizontal"][1] - self.wfm["horizontal"][0]
            minimum = np.nanargmin(self.wfm["vertical"][self.channel-1])
            maximum = np.nanargmax(self.wfm["vertical"][self.channel-1])
            before = max(0,maximum - int(self.crop_peak[0]/dt))
            after  = min(maximum + int(self.crop_peak[1]/dt),self.wfm["horizontal"].size - 1)
            self.horizontal = self.wfm["horizontal"][before:after]
            self.vertical   = self.wfm["vertical"][self.channel-1][before:after]
            del dt, maximum, minimum, before, after
        self.dt = self.horizontal[1] - self.horizontal[0]
        # CORRECTIONS
        # bandpass limited
        if not( self.highest_frequency == scipy.fft.rfftfreq(self.wfm["horizontal"].size, d = self.wfm["horizontal"][1] - self.wfm["horizontal"][0])[-1] and self.lowest_frequency == 0. ):
            self.vertical = bandpass(
                                {
                                 "horizontal":self.horizontal,
                                 "vertical"  :self.vertical
                                },
                                self.lowest_frequency,
                                self.highest_frequency
                            )["vertical"]
        
        # STATISTICS
        # delivery of periodicity of noise from the beginning of the waveform
        for n in range(1,self.vertical.size):
            if self.vertical[n-1] < self.vertical[n]:
                for m in range(n+1,self.vertical.size):
                    if self.vertical[m-1] > self.vertical[m]:
                        self.noise_period = 4 * (m-n) * self.dt
                        break
        if not hasattr(self, 'noise_period'):
            self.noise_period = self.dt
        # integrity of results
        self.status = True
        # housekeeping
        del self.wfm
        return None
    def show(self):
        wfmshow({"horizontal" : self.horizontal, "vertical" : self.vertical, "nolabel" : True })
        return None
    def save(self,path):
        wfmwrite(path,{"horizontal" : self.horizontal, "vertical" : self.vertical, "nolabel" : True })
        return None


# =============================================================================
# PYTHON MAIN
# =============================================================================
# SELF AND TEST
if globals()["__name__"] == '__main__':
    # STARTUP
    print("START TEST OF CLPU IMAGE MODULE")
    print("!!! -> expect True ")
    # parse command line
    args = sys.argv
    # TESTS
    # (001) CONSTANTS
    print("\n(001) CONSTANTS")
    print(test)
    # (002) FUNCTION CALL
    print("\n(002) FUNCTION CALL")
    print(test_pingpong(True,kwa=True))
    # (003) CLASS INIT
    print("\n(003) CLASS INIT")
    test_class = Main(kwa=True)
    test_class.add = True
    print(test_class)
    del test_class
    