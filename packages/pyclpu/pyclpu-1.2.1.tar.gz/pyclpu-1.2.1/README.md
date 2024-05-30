**This file describes the module of CLPU utilities and related aspects to users and maintainers.**

# CLPU Utilities

**Abstract:** This module bundels functions which are frequently used for applications at the Centro de Laseres Pulsados, Villamayor, Spain. Although we intend to deliver reliable software solutions, we can not guarantee that every implementation is flawless. We encourage the user to re-read the code and alert us if bugs are found.

:paperclip: The documentation is available in [`html`](http://pyclpu.physicaetmetaphysica.eu/) by on a third party server.

## Installation

Run `pip install pyclpu` when connected to the internet; or if not connected to the internet `pip install .` within the main folder of the project (where you find also files like `README.md`, `setup.py`, `LICENCE`).

## Use-cases

The following use cases have occured and led to debugged implementations.

### Rename Autosaved Images and Apply Warp Transform

The following code sniffes in a directory `bin` for new files by means of `manager.CatchAndRename` and performs a Warp Transform by means of `image.PerspectiveTransform`. Results are stored in `bin/output_warp` if such directory exists (else in the current working directory).

```
import os
import numpy as np

from pyclpu import image
from pyclpu import manager

chase = manager.CatchAndRename()

chase.directory = "C:\\bin"
chase.prefix = "shot_"
chase.number = 1

warp_it = image.PerspectiveTransform()
warp = []

chase.loop = True
chase.leap = True

while True:
    if chase.flag_new:
        chase.flag_new = False
        warp_it.source = image.imread(os.path.join(chase.directory,chase.filename))
    if warp_it.flag_new:
        warp_it.flag_new = False
        image.imwrite(
            os.path.join(
                chase.directory,
                'output_warp',
                chase.filename
            ),
            warp_it.warped
        )
        np.savetxt(
            os.path.join(
                chase.directory,
                'output_warp',
                manager.strip_extension(chase.filename)+".dat"
            ),
            warp_it.sourcecorners.point_list
        )
```

### Rename Many Files ...

### ... changing the filenames

```
import time
from pyclpu import manager
chase = manager.CatchAndRename()
chase.directory = "path/to/dir"
chase.prefix = "shot_"
chase.number = 504
chase.leap = False
chase.loop = True
time.sleep(1)
chase.ignored = []
time.sleep(100)
chase.loop = False
```


#### ... changing only the extension

```
import os
import math

from pyclpu import manager


chase = manager.CatchAndRename()

chase.directory = "path/to/directory"
chase.prefix = ""
chase.extension = "md"
chase.number = math.nan
chase.loop = True
chase.ignored = []
chase.loop = False
```

#### ... changing only their location

```
from pyclpu import manager
        
detector_to_server = manager.Pipeline()
detector_to_server.source = "C:\\bin"
detector_to_server.destination = "C:\\bin\\pipe"
detector_to_server.start()
```

### Time-of-Flight Analysis

Data of Time-of-Flight detectors comprises a timeline and an amplitude for every recorded temporal bin. The `ToF` class is ment to make data analysis easier. After input of the data and the geometrical situation (location of the detector with respect to the source), it is possible to obtain a spectrum. The x-axis of the output is normalized to be in units of `gamma -1`, where `gamma` is the Lorenz factor. This way the result of the analysis is kept universal without further interpretation regarding the type of particles. If the type of projectiles is known: To obtain the kinetic energy of projectiles it is sufficient to multiply the values with the rest mass energy of the projectiles, e.g. in units of MeV.

```
from pyclpu import metrology

tof_detector = metrology.ToF()
tof_detector.distance = 100
tof_detector.channel = 1
tof_detector.polarity = -1

tof_detector.waveform = "path/to/data.csv"

tof_detector.analyse()
tof_detector.show()
```

The following code sniffes in a directory `bin` for new files by means of `manager.Catch` and performs a Warp Transform by means of `image.PerspectiveTransform`. Results are stored in `bin/output_warp` if such directory exists (else in the current working directory).

```
import os
import numpy as np

from pyclpu import manager
from pyclpu import metrology

chase = manager.Catch()
chase.directory = "C:\\bin"

tof_detector = metrology.ToF()
tof_detector.distance = 100
tof_detector.channel = 1
tof_detector.polarity = -1

chase.loop = True

while True:
    if len(chase.new) > 0:
        new_file = chase.next()
        tof_detector.waveform = os.path.join(chase.directory,new_file)
        print("WORK "+tof_detector.waveform)
        tof_detector.analyse()
        if tof_detector.status:
            np.savetxt(
                os.path.join(
                    chase.directory,
                    'output_spectrum',
                    manager.strip_extension(new_file)+".spec.dat"
                ),
                np.array([tof_detector.Gminus1,tof_detector.dN_dGminus1]).T,
                header='gamma-1 dN/d(gamma-1)'
            )
```

### Work with Waveforms

#### ... visualize and dsave data

The following sniplet allows to see results of a channel from one single waveform file, and saves them to a destination.

```
from pyclpu import waveform

wfm = waveform.wfmread("C:\\bin\\emp_2023-07-10_44_122214.Wfm.bin")
waveform.wfmshow(wfm)

channel = 1
trace = waveform.Waveform(wfm = wfm, channel = channel)

trace.show()
trace.save("C:\\bin\\output.csv")
```

## Changelog
...
