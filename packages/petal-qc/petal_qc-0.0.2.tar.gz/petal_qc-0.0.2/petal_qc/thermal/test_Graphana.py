#!/usr/bin/env python3
"""Test the connection with graphana to get the value at the peak."""
import sys
from pathlib import Path
import datetime
try:
    import petal_qc

except ImportError:
    cwd = Path(__file__).parent.parent.parent
    sys.path.append(cwd.as_posix())

from petal_qc.utils.readGraphana import ReadGraphana
from petal_qc.thermal.IRDataGetter import IRDataGetter
from petal_qc.thermal.IRPetalParam import IRPetalParam
from petal_qc.thermal import IRBFile


options = IRPetalParam()
options.files = ["/Users/lacasta/tmp/thermal/PPC.007.irb"]
getter = IRDataGetter.factory(options.institute, options)
DB = ReadGraphana("localhost")
irbf = IRBFile.open_file(options.files)

frames = getter.get_analysis_frame(irbf)
print(frames[0].timestamp)
the_time = datetime.fromtimestamp(timestamp, timezone.utc)
val = DB.get_temperature(frames[0].timestamp, 10)

print(val)