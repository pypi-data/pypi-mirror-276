import os
from pathlib import Path
from .function04 import Eimes
from .collections import SMessage
#=================================================================

class Files:

    async def get01(directory, stored):
        for item in Path(directory).rglob('*'):
            if os.path.isdir(item):
                continue
            else:
                stored.append(str(item))

        stored.sort()
        return SMessage(allfiles=stored, numfiles=len(stored))

#=================================================================

    async def get02(directory, stored, skip=Eimes.DATA00):
        for patho in directory:
            if patho.upper().endswith(skip):
                continue
            else:
                stored.append(patho)

        stored.sort()
        return SMessage(allfiles=stored, numfiles=len(stored))

#=================================================================
