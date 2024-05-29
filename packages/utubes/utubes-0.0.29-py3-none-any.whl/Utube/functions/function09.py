import os
from .collections import SMessage
#=================================================================================================

class Finders:

    async def get01(flocation, exo):
        try:
            location = str(flocation)
            filesize = int(os.path.getsize(location))
            return SMessage(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = str(flocation) + "." + exo
            filesize = int(os.path.getsize(location))
            return SMessage(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = os.path.splitext(flocation)[0]
            filesize = int(os.path.getsize(location))
            return SMessage(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = os.path.splitext(flocation)[0] + str(".mkv")
            filesize = int(os.path.getsize(location))
            return SMessage(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = os.path.splitext(flocation)[0] + "." + str(exo)
            filesize = int(os.path.getsize(location))
            return SMessage(location=location, filesize=filesize)
        except Exception:
            return SMessage(location=None, filesize=0)

#=================================================================================================

    async def get02(dlocation, exo, exe):
        try:
            location = str(dlocation)
            filesize = int(os.path.getsize(location))
            return SMessage(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = str(dlocation) + "." + exo
            filesize = int(os.path.getsize(location))
            return SMessage(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = str(dlocation) + "." + exe
            filesize = int(os.path.getsize(location))
            return SMessage(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = os.path.splitext(dlocation)[0]
            filesize = int(os.path.getsize(location))
            return SMessage(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = os.path.splitext(dlocation)[0] + str(".mp3")
            filesize = int(os.path.getsize(location))
            return SMessage(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = os.path.splitext(dlocation)[0] + str(".mp4")
            filesize = int(os.path.getsize(location))
            return SMessage(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = os.path.splitext(dlocation)[0] + str(".mkv")
            filesize = int(os.path.getsize(location))
            return SMessage(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = os.path.splitext(dlocation)[0] + "." + str(exe)
            filesize = int(os.path.getsize(location))
            return SMessage(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = os.path.splitext(dlocation)[0] + "." + str(exo)
            filesize = int(os.path.getsize(location))
            return SMessage(location=location, filesize=filesize)
        except Exception:
            return SMessage(location=None, filesize=0)

#=================================================================================================
