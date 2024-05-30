# -*- coding: utf-8 -*-
""" This is the CLPU module for management tasks.

Please do only add or modify but not delete content.

requires explicitely {
 - os
 - sys
 - numpy
}

import after installation of pyclpu via {
  from pyclpu import manager
}

import without installation via {
  root = os.path.dirname(os.path.abspath(/path/to/pyclpu/manager.py))
  sys.path.append(os.path.abspath(root))
  import manager
  from importlib import reload 
  reload(manager)
}

"""

# =============================================================================
# PYTHON HEADER
# =============================================================================
# EXTERNAL
import os
import sys
import shutil
import threading
import time

from inspect import getsourcefile
from importlib import reload

import tkinter as tk

import math
import numpy as np

# INTERNAL
root = os.path.dirname(os.path.abspath(getsourcefile(lambda:0))) # get environment
sys.path.append(os.path.abspath(root))                           # add environment
sys.path.append(os.path.abspath(root)+os.path.sep+"LIB")         # add library

if "constants" not in globals() or globals()['constants'] == False:
    import constants            # import all global constants from                   constants.py
    import formats              # import all global formats from                     formats.py
    from s33293804 import *     # import zoom PanZoomWindow for display images from  s33293804.py
    reload(constants)
    reload(formats)

# STYLE

# =============================================================================
# CONSTANTS
# =============================================================================
# INTEGRATION AND TESTING
test = True

# PARAMETERS

# METHODOLOGY SELECTORS
# define method used to load images, 
# possible values are
# opencv   :: use the module opencv
# tifffile :: use the module tifffile # !!! tifffile not part of the project !!!
global_load_method = 'opencv'

# CONSTANTS

# =============================================================================
# METHODS
# =============================================================================
# INTEGRATION AND TESTING
def test_pingpong(*args, **kwargs):
    try:
        for arg in args:
            print(arg)
        for key, value in kwargs.items():
            print(str(key) + " : "+ str(value))
    except:
        return False
    return True
    
# GUI MANAGEMENT
def error(source,string,code = None):
    print("\nError ............. "+source+" : "+string)
    lead_string = "                    "
    intend_string = "      "
    if code != None:
        if code == 0:
            print(lead_string+'ERROR_DIVISION_BY_ZERO\n'+intend_string+'The system cannot divide by zero.')
        elif code == 2:
            print(lead_string+'ERROR_FILE_NOT_FOUND\n'+intend_string+'The system cannot find the file specified.')
        elif code == 5:
            print(lead_string+'ERROR_ACCESS_DENIED\n'+intend_string+'Access is denied.')
        elif code == 13:
            print(lead_string+'ERROR_INVALID_DATA\n'+intend_string+'The data is invalid.')
        elif code == 161:    
            print(lead_string+'ERROR_BAD_PATHNAME\n'+intend_string+'The specified path is invalid.')
        elif code == 232:
            print(lead_string+'ERROR_NO_DATA\n'+intend_string+'The pipe is being closed.')
        elif code == 677:
            print(lead_string+'ERROR_EXTRANEOUS_INFORMATION\n'+intend_string+'Too Much Information.')
        elif code == 1160:
            print(lead_string+'ERROR_SOURCE_ELEMENT_EMPTY\n'+intend_string+'The indicated source element has no media.')
        elif code == 1169:
            print(lead_string+'ERROR_NO_MATCH\n'+intend_string+'There was no match for the specified key in the index.')
        elif code == 1287:
            print(lead_string+'ERROR_UNIDENTIFIED_ERROR\n'+intend_string+'Insufficient information exists to identify the cause of failure.')
        elif code == 8322:
            print(lead_string+'ERROR_DS_RANGE_CONSTRAINT\n'+intend_string+'A value for the attribute was not in the acceptable range of values.')
        else:
            print('ERROR\nNo idea what happened.\n')
    print("\n")
    return None
    
def message(source,string,headline = ""):
    print("\nMessage ........... "+source+" :")
    lead_string = "                    "
    if headline != "": print(lead_string+headline)
    intend_string = "      "
    string_list = string.split("\n")
    for s in string_list:
        print(intend_string + s)
    return None

def warning(source,string):
    try:
        print("\nWarning ........... "+source+" : "+string+"\n")
    except:
        error(warning.__name__,"Fail to print.")
    return None
    
# FILE MANAGEMENT
    
def give_extension(filename):
    """
    Function returns extension of a filename as string or `None`.
    """
    try:
        extension = filename.rsplit(".",1)[1]
    except:
        extension = None
    return extension
    
def strip_extension(filename):
    """
    Function returns a filename without extension as string or `None`.
    """
    try:
        extension = give_extension(filename)
        if extension != None:
            noextension = filename[0:-(len(extension)+1)]
        else:
            noextension = filename
    except:
        noextension = None
    return noextension
    
def give_dirlst(path):
    """
    Function returns a list with the order of folder names from a directory.
    
    References:
        * stackoverflow answer 3167684
    """
    return os.path.split(path)[0].split(os.sep)
    
# SYSTEM MANAGEMENT

def screensize():
    root = tk.Tk()
    root.update_idletasks()
    root.attributes('-fullscreen', True)
    root.state('iconic')
    geometry = root.winfo_geometry()
    root.destroy()
    wxh = geometry.split('+')[0]
    return wxh
    
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

# INTERACTIVE
class Catch():
    """ Responsive file catcher
    This class waits for new files in a directory and keeps track of processed files.
    
    Args:
        directory (str) : Path to directory where new files are expected.
        loop (bool, optional) : Activity status of the catcher. Inactive if `False`, active if `True`.
        leap (bool) : Leaps over existing files if set True. Defaults to False. 
            With leap = False, routine will treat exisiting files as new files.
            With leap = True, routine will ignore exisiting files that are in the directory the moment the loop is started.
        
    Attributes:
        status (bool) : True if processing was successfull, else False.
            Initializes to False.
        
    Returns:
        new (list) : Names of new files which have been found. Initializes according to value of `leap`.
        processed (list) : Names of files which have been processed. Initializes as empty list.
        ident (int) : Identity of thread. If more than one thread is started, a list is created that contains the identities in chronologic order, with the newest one last.
    
    Notes:
        Start searching for new files when loop is activated by setting the input parameter `loop = True`. If elements from the list `processed` are purged during `loop = True`, then corresponding files will be recognized as new.
        
    Examples:
        
    """
    # INI
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    def __init__(self, *args, **kwargs):
        # INPUT
        self.__dict__.update(kwargs)
        # VARIABLES
        if not hasattr(self,"leap"):
            self.leap = False
        self.status = False
        # INTEGRITY
        if not hasattr(self, 'loop'):
            warning(self.__class__.__name__,"Find no loop request status, expect key `loop` as boolean and start if `loop = True`.")
        # IN PLACE
        if hasattr(self, 'loop') and self.loop == True:
            self.__run__()
        return None
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == "loop" and value == True:
            self.__run__()
        if name == "loop" and value == False:
            #os.chdir(self.cwd)
            self.stop()
        return None
    def __run__(self):
        # INTEGRITY
        if not hasattr(self, 'directory'):
            warning(self.__class__.__name__,"No source directory defined, expect key `directory` as `directory=path/to/directorty`.")
            return None
        if not hasattr(self, 'leap'):
            warning(self.__class__.__name__,"No decission made for leaping, expect key `leap` as `leap.type=bool`.")
            return None
        # METHODS
        #@classmethod
        def _worker(event):
            self.ident = threading.get_ident()
            while not self._event.is_set():
                file_list = os.listdir(self.directory)
                for file in file_list:
                    if os.path.isfile(os.path.join(self.directory,file)):
                        if file in self.processed or file in self.new:
                            continue
                        else:
                            self.new.append(file)
                            self.status = True
        # MAIN
        self.new = []
        if self.leap:
            self.processed = os.listdir(self.directory)
        else:
            self.processed = []
        if not hasattr(self,"_event"):
            self._event = threading.Event()
            self._process = threading.Thread(target=_worker, args=(self._event,))
        self.start()
    
    def start(self):
        # START
        if hasattr(self,"_process"):
            self._process.start()
        else:
            warning(self.__class__.__name__,"THREAD ALREADY STARTED: DO NOTHING")
    
    def stop(self):
        self._event.set()
        self._process.join()
        # integrity of results
        # ..
        # housekeeping
        try:
            del self.ident
            del self._event
            del self._process
        except:
            pass
        return None
        
    def next(self):
        # get file from list `new` by order of arrival, remove it and add it to list `processed`, returns filename
        if len(self.new) > 0:
            file = self.new.pop(0)
            self.processed.append(file)
        return file
        
class Pipeline():
    """ Responsive file pipeline
    This class looks up files in a directory and moves them to a destination. Existing files are moved to begin with, new files are moved after they are written into the source directory. Files are not moved if a file with the same name is already in the destination.
    
    Args:
        source (str) : Path to directory where new files are expected.
        destination (str) : Path to directory where new files are moved.
        
    Attributes:
        status (bool) : True if the pipeline is open, else False.
            Initializes to False.
    
    Examples:
        A object oriented use case is described below. The chase for new files is activated by setting the input parameter `loop = True` and paused by setting `loop = False`.
        ```
        from pyclpu import manager
        
        detector_to_server = manager.Pipeline()
        detector_to_server.lsource = "C:\\bin"
        detector_to_server.destination = "C:\\bin\\pipe"
        detector_to_server.start()
        ```
    """
    # INI
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    def __init__(self, *args, **kwargs):
        # INPUT
        self.__dict__.update(kwargs)
        # VARIABLES
        self.status = False
        # INTEGRITY
        if not hasattr(self, 'source'):
            warning(self.__class__.__name__,"Find no source directory, expect key `source` as string.")
        if not hasattr(self, 'destination'):
            warning(self.__class__.__name__,"Find no destination directory, expect key `destination` as string.")
        return None
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == "status" and value == True:
            self.start()
        if name == "status" and value == False:
            self.stop()
        return None
    def __run__(self):
        # INTEGRITY
        if not hasattr(self, 'source'):
            warning(self.__class__.__name__,"No source directory defined, expect key `source` as `source=path/to/directorty`.")
            return None
        if not hasattr(self, 'destination'):
            warning(self.__class__.__name__,"No destination directory defined, expect key `destination` as `destination=path/to/directorty`.")
            return None
        # METHODS
        #@classmethod
        def _worker(event):
            self.ident = threading.get_ident()
            while not self._event.is_set():
                if len(self.chase.new) > 0:
                    new_file = self.chase.next()
                    origin = os.path.join(self.chase.directory,new_file)
                    moveto = os.path.join(self.destination,new_file)
                    if os.path.isfile(origin) and not os.path.isfile(moveto):
                        shutil.move(origin, moveto)
                    del new_file, origin, moveto
        # MAIN
        self.chase = Catch()
        self.chase.directory = self.source
        self.chase.leap = False
        self.chase.loop = True
        if not os.path.isdir(self.destination):
            os.makedirs(self.destination)
        if not hasattr(self,"_event"):
            self._event = threading.Event()
            self._process = threading.Thread(target=_worker, args=(self._event,))
        if hasattr(self,"_process"):
            self._process.start()
        else:
            warning(self.__class__.__name__,"THREAD ALREADY STARTED: DO NOTHING")                  
        
    def start(self):
        # START
        self.__run__()
    
    def stop(self):
        try:
            self._event.set()
            self._process.join()
        except:
            warning(self.__class__.__name__,"THREAD ALREADY STOPPED: DO NOTHING")  
        # integrity of results
        # ..
        # housekeeping
        try:
            del self.ident, self._event, self._process
            self.chase.stop()
            del self.chase
        except:
            pass
        return None
        
class CatchAndRename():
    """ Responsive file catcher
    This class waits for new files in a directory and renames them upon arrival. Renaming results in `str(prefix+"_"+number+"."+extension)` according to 
    - an optional input variable `prefix` with default `""`, 
    - counting up from an optional input variable `number` that defaults to `number = 0`, 
    - and without changing the original extension.
    
    Args:
        directory (str) : Path to directory where new files are expected.
        prefix (str, optional) : Prefix of renamed filename. Defaults to `""`.
        number (int, optional) : Suffix of renamed filename. Defaults to `0`.
        extension (str, optional) : Extension of renamed files. Defaults to the old extension.
        loop (bool, optional) : Activity status of the catcher. Inactive if `False`, active if `True`.
        leap (bool) : Leaps over existing files if set True. Defaults to False. 
            With leap = False, routine will overwrite exisiting files and exists if an attempt is made.
            With leap = True, routine will not overwrite exisiting files but use the next possible number, counting up.
        
    Attributes:
        filename (str) : Name of last file which was written. Initializes as empty string.
        flag_new (bool) : True if processing was successfull, else False.
            Initializes to False.
            Intended to be modified from outside in use cases where this routine delivers output for another process.
        status (bool) : True if processing was successfull, else False.
            Initializes to False.
        
    Returns:
        ident (int) : Identity of thread. If more than one thread is started, a list is created that contains the identities in chronologic order, with the newest one last.
        ignored (list) : List of files which is ignored.
    
    Notes:
        Rename freshly arriving files to `str(prefix+number+"."+extension)` when loop is activated by setting the input parameter `loop = True`. If elements from the list `inored` are purged during `loop = True`, then corresponding files will be renamed as they are recognized as new.
        
    Examples:
        The class can be used in a functional way
        ```
        from pyclpu import manager
        chase = manager.CatchAndRename(directory = "path/to/directory/", prefix = "any_string", number = 42, loop=True)
        ```
        A more object oriented use case is described below. The chase for new files is activated by setting the input parameter `loop = True` and paused by setting `loop = False`.
        ```
        from pyclpu import manager
        import time

        chase = manager.CatchAndRename()

        chase.directory = "path/to/test"
        chase.prefix = "any_string"
        chase.number = 42

        chase.loop = True
        time.sleep(100)
        chase.loop = False`
        ```
        Files that arrive in the directory during a pause will be ignored when switching on the loop again with `loop = True`.
    """
    # INI
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    def __init__(self, *args, **kwargs):
        # INPUT
        self.__dict__.update(kwargs)
        # VARIABLES
        #self.cwd = os.getcwd()
        self.timeout = 2
        self.filename = ""
        self.flag_new = False
        self.status = False
        self.leap = False
        self.ident = None
        # INTEGRITY
        if not hasattr(self, 'loop'):
            warning(self.__class__.__name__,"Find no loop request status, expect key `loop` as boolean and start if `loop = True`.")
        # IN PLACE
        if hasattr(self, 'loop') and self.loop == True:
            self.__run__()
        return None
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == "loop" and value == True:
            self.__run__()
        if name == "loop" and value == False:
            #os.chdir(self.cwd)
            self.stop()
        return None
    def __run__(self):
        # INTEGRITY
        if not hasattr(self, 'directory'):
            warning(self.__class__.__name__,"No source directory defined, expect key `directory` as `directory=path/to/directorty`.")
            return None
        if not hasattr(self, 'number'):
            warning(self.__class__.__name__,"No starting integer defined, expect key `number` as `number=integer`. Set `number = 0`.")
            self.number = 0
        if not hasattr(self, 'extension'):
            warning(self.__class__.__name__,"No extension defined, expect key `extension`. Remain with original extension.")
            self.extension = ""
        if not hasattr(self, 'prefix'):
            warning(self.__class__.__name__,"No prefix defined, expect key `prefix` as `prefix=any_string`. Set `prefix = ''`.")
            self.prefix = ""
        # METHODS
        #@classmethod
        def _worker(event):
            self.ident = threading.get_ident()
            self.ignored = os.listdir(self.directory)
            while not self._event.is_set():
                time.sleep(self.timeout)
                dir_list = os.listdir(self.directory)
                cwd = os. getcwd()
                os.chdir(self.directory)
                sorted_file_list = sorted(filter(os.path.isfile, dir_list), key=os.path.getmtime)
                os.chdir(cwd)
                for file in sorted_file_list:
                    if file in self.ignored:
                        continue
                    else:
                        message(self.__class__.__name__,"WORK ON  "+file)
                        try:
                            filename_and_extension = file.rsplit( ".", 1 )
                            old_extension = filename_and_extension[1]
                            old_basename  = filename_and_extension[0]
                        except:
                            old_extension = ""
                            old_basename  = file
                        if self.extension == "":
                            new_extension = old_extension
                        else:
                            new_extension = self.extension
                        if math.isnan(self.number):
                            new_file = self.prefix+old_basename+'.'+new_extension
                        else:
                            new_file = self.prefix+str(self.number).zfill(3)+'.'+new_extension
                            self.number = self.number + 1
                        self.ignored.append(new_file)
                        old_name = os.path.join(self.directory,file)
                        new_name = os.path.join(self.directory,new_file)
                        if os.path.isfile(new_name):
                            message(self.__class__.__name__,"FILE ALREADY EXISTS: "+new_name)
                            find_next_free_number_for_pattern = self.number
                            while True:
                                find_next_free_number_for_pattern = find_next_free_number_for_pattern + 1
                                test_file = self.prefix+str(find_next_free_number_for_pattern).zfill(3)+'.'+new_extension
                                if os.path.isfile(os.path.join(self.directory,test_file)):
                                    continue
                                else:
                                    break
                            new_file = test_file
                            new_name = os.path.join(self.directory,new_file)
                            message(self.__class__.__name__,"FIND NEXT POSSIBLE: "+new_name)
                            if self.leap == True:
                                pass
                            else:
                                warning(self.__class__.__name__,"FILE ALREADY EXISTS: DO NOTHING FOR "+old_name)
                                message(self.__class__.__name__,"EXIT LOOP: loop = False")
                                self.status = False
                                self.loop = False
                                break
                        message(self.__class__.__name__,"CREATE  "+new_name)
                        os.rename(old_name, new_name)
                        self.filename = new_file
                        self.flag_new = True
                        self.status = True
        # MAIN
        if not hasattr(self,"_event"):
            self._event = threading.Event()
            self._process = threading.Thread(target=_worker, args=(self._event,))
        self.start()
    
    def start(self):
        # START
        if hasattr(self,"_process"):
            self._process.start()
        else:
            warning(self.__class__.__name__,"THREAD ALREADY STARTED: DO NOTHING")
    
    def stop(self):
        self._event.set()
        self._process.join()
        # integrity of results
        # ..
        # housekeeping
        try:
            del self.ident
            del self._event
            del self._process
        except:
            pass
        return None
        
# CODE PARSER FOR SIMULATION INPUT/OUTPUT/TRANSLATION/PIPELINES
class ChoCoLaT_output():
    """
    The class allows to load output of a ChoCoLaT simulation into a class object.
    
    Args:
        source  (string, optional) : Source output file.
        
    Attributes:
        status (bool) : True if processing was successfull, else False.
            Initializes to False.
        flag_new (bool) : True if processing was successfull, else False.
            Initializes to False.
            Intended to be modified from outside in use cases where this routine delivers output for another process.
    
    Returns:
        meta  (dictionary)   : Simulation input parameters and meta information.
        data  (record array) : Simulation output in named columns of a record array (allows to see `array.keys`).
        
    Note:
        This parser refers to ChoCoLaT version 2 and younger.
    
    Examples:
        The class can be used in a functional way

        ```python 
        from pyclpu import manager
        choc = manager.ChoCoLaT_output(source = "path/to/test.dat")
        ```

        A more object oriented use case can deal with loops

        ```python 
        from pyclpu import manager
        choc_it = manager.ChoCoLaT_output()
        chocs = []
        
        simulations = ["1.dat","2.dat","3.dat"]
        for choc in image_stack:
            choc_it.source = choc
            chocs.append[{choc_it.meta["metal_id"] : choc_it.data["Q_[nC]"][-1]}]
        ```
        with selected results beeing stored in a list `chocs`.
    """
    # INI
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
        self.status = False
        self.flag_new = False
        # INTEGRITY
        if not hasattr(self, 'source'):
            warning(self.__class__.__name__,"No source path defined, expect key `source` as `source=path.dat`.")
        # IN PLACE
        if hasattr(self, 'source'):
            self.__run__()
        return None
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == "source":
            self.__run__()
        return None
    def __run__(self):
        self.status = False
        # METHODS
        def load(path):
            """
            Loads the file with simulation results into an line-by-line array
            """
            # check if file exists
            if not os.path.isfile(path):
                warning(self.__class__.__name__,"Invalid source path, expect key `source` as `source=path.dat`.")
                return None
            # open file
            with open(path) as file:
                # check if file is empty
                file.seek(0, os.SEEK_END) # go to end of file
                if file.tell():           # if current position is truish (i.e != 0)
                    file.seek(0)          # rewind the file for later use 
                else:
                    warning(self.__class__.__name__,"Invalid source, file is empty.")
                    return None           # file is empty
                # parse file line by line into array
                line_by_line = [line.rstrip() for line in file]
            return line_by_line   
        def find_sim_meta(line_by_line):
            """
            Filters the input information to the simulation and meta information from the simulation file array.
            """
            # prepare dictionary for file header information (meta and simulation input)
            meta_dict = {}
            # ChoCoLaT marks meta information about the simulation with "%",
            #  and meta information is always in the header od the output file.
            for line in line_by_line:
                if "%" in line:
                    # clean strings
                    keyed = line.replace("%","").split("=")
                    key   = keyed[0].strip()
                    value = keyed[1].strip()
                    # try to sort out for type
                    if key == "T_isol":
                        value = bool(value)
                    elif key in ["metal", "Nb Th", "diag s", "diag f", "N_iks", "Nb"] : 
                        value = int(value)
                    elif key in ["dt", "t_laser", "E_laser", "C_abs", "w_laser", "d_laser", "d_targe", "e_targe", "T_hot_e", "N_tot", "t_life"] : 
                        value = float(value)
                    else:
                        warning(self.__class__.__name__,"Unknown key in header ! `" + key +"` as `" + key +" = " + value +"`.")
                    # add to dict
                    meta_dict[key] = value
                else:
                    break
            return meta_dict
        def wumwum_parse_data(line_by_line):
            """
            Filters the data from the output file.
            """
            # prepare column header tuple
            header = ()
            # prepare data array (will have every output line in one tuple)
            rows   = []
            # find column header, located directly after the file header
            for line in line_by_line:
                if "%" in line:
                    continue
                else:
                    # column headers are separated by differing amounts of white spaces
                    words = line.split()
                    # nearly all column headers have units, always first comes the keyword and after the unit
                    keys_units  = {}
                    last_key_poition = 0
                    for p,phrase in enumerate(words):
                        # separate keywords and units based on the feature that units are in brackets
                        if "[" not in phrase and "]" not in phrase:
                            # one known header includes the keyword `all` and has no units
                            if last_key_poition == p-1 and "all" not in words[last_key_poition]:
                                keys_units.pop(words[last_key_poition], None)
                                keys_units[words[last_key_poition] + "_" + phrase] = None
                                last_key = words[last_key_poition] + "_" + phrase
                            else: 
                                keys_units[phrase] = None
                                last_key = phrase
                            # update position of last keyword in array words
                            last_key_poition = p
                        else:
                            # react to type missmatch that produces an off char in from of the unit um
                            if "Â" in phrase :
                                unit = phrase.replace("Â","")
                            else:
                                unit = phrase
                            keys_units[last_key] = unit
                    # combine keys and units to header entry for data columns
                    for key in keys_units.keys():
                        if keys_units[key] is not None:
                            header = header + (key + "_" + keys_units[key],)
                        else:
                            header = header + (key,)
                    break
            # read out data underneath column header information
            for line in line_by_line:
                if "%" in line or key in line:
                    continue
                else:
                    # data is separated by a variable amount of white spaces
                    data_row = np.array(line.split()).astype(float)
                    # check if the header and the data are consistent
                    if data_row.size != len(header):
                        warning(self.__class__.__name__,"Header and row have different length ! "+str(data_row.size)+" != "+str(len(header)))
                    # fill data into data array of tuples
                    rows.append(tuple(data_row))
            # build 32bit float dtype from keys
            dtype_info = [(key,'f4') for key in header]
            # build record array
            return np.array(rows, dtype=dtype_info)
        # MAIN
        # load file to file array
        input_array = load(self.source)
        # extract simulation input information from file array header information
        self.meta   = find_sim_meta(input_array)
        # extract timesteps
        self.data   = wumwum_parse_data(input_array)
        # housekeeping
        self.status = True
        self.flag_new = True
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
    