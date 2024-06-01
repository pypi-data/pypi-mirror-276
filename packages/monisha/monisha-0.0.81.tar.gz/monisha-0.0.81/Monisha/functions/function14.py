import os
from typing import List
from pathlib import Path
from .function04 import Eimes
from .collections import SMessage
#======================================================================

class Locations:

    @staticmethod
    async def get01(directory: str, stored: List[str]) -> SMessage:
        for item in Path(directory).rglob('*'):
            if item.is_dir():
                continue
            else:
                stored.append(str(item))

        stored.sort()
        return SMessage(allfiles=stored, numfiles=len(stored))

#======================================================================

    async def get02(directory, stored, skip=Eimes.DATA00):
        for patho in directory:
            if patho.upper().endswith(skip):
                continue
            else:
                stored.append(patho)

        stored.sort()
        return SMessage(allfiles=stored, numfiles=len(stored))

#======================================================================
