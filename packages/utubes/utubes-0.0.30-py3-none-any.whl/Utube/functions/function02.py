import os
from ..scripts import Smbo
from .collections import SMessage
from pyrogram.enums import MessageEntityType
#=============================================================================================

class Extractors:

    async def extract03(reames, finame):
        if reames == None and finame == None:
            return SMessage(filename="Unknown")
        else:
            nameas = str(reames)
            cnames = os.path.splitext(nameas)[0]
            exexon = os.path.splitext(nameas)[1]
            exoexo = exexon if exexon else ".tmp"
            moonus = finame if finame else cnames
            return SMessage(filename=moonus, extension=exoexo)

#=============================================================================================

    async def extract04(update, incoming):
        amoend = filter(lambda o: o.type == MessageEntityType.URL, update.entities)
        amoond = list(amoend)
        neomos = amoond[0].offset
        sosmso = amoond[0].length
        linked = incoming[ neomos : neomos + sosmso ]
        return linked

#=============================================================================================
    
    async def extract01(update, incoming):
        poxwers = incoming.split(Smbo.DATA04)
        if len(poxwers) == 2 and Smbo.DATA04 in incoming:
             Username = None
             Password = None
             Flielink = poxwers[0] # INCOMING URL
             Filename = poxwers[1] # INCOMING FILENAME
        elif len(poxwers) == 3 and Smbo.DATA04 in incoming:
             Filename = None
             Flielink = poxwers[0] # INCOMING URL
             Username = poxwers[1] # INCOMING USERNAME
             Password = poxwers[2] # INCOMING PASSWORD
        elif len(poxwers) == 4 and Smbo.DATA04 in incoming:
             Flielink = poxwers[0] # INCOMING URL
             Filename = poxwers[1] # INCOMING FILENAME
             Username = poxwers[2] # INCOMING USERNAME
             Password = poxwers[3] # INCOMING PASSWORD
        else:
             Filename = None # INCOMING FILENAME
             Username = None # INCOMING USERNAME
             Password = None # INCOMING PASSWORD
             Flielink = await Extractors.extract04(update, incoming)

        moon01 = Flielink.strip() if Flielink != None else None
        moon02 = Filename.strip() if Filename != None else None
        moon03 = Username.strip() if Username != None else None
        moon04 = Password.strip() if Password != None else None
        return SMessage(filelink=moon01, filename=moon02, username=moon03, password=moon04)

#=============================================================================================

    async def extract02(update, filename, incoming):
        poxwers = incoming.split(Smbo.DATA04)
        if len(poxwers) == 2 and Smbo.DATA04 in incoming:
             Username = None
             Password = None
             Flielink = poxwers[0] # INCOMING URL
             Filename = poxwers[1] # INCOMING FILENAME
        elif len(poxwers) == 3 and Smbo.DATA04 in incoming:
             Filename = None
             Flielink = poxwers[0] # INCOMING URL
             Username = poxwers[1] # INCOMING USERNAME
             Password = poxwers[2] # INCOMING PASSWORD
        elif len(poxwers) == 4 and Smbo.DATA04 in incoming:
             Flielink = poxwers[0] # INCOMING URL
             Filename = poxwers[1] # INCOMING FILENAME
             Username = poxwers[2] # INCOMING USERNAME
             Password = poxwers[3] # INCOMING PASSWORD
        else:
             Filename = None # INCOMING FILENAME
             Username = None # INCOMING USERNAME
             Password = None # INCOMING PASSWORD
             Flielink = await Extractors.extract04(update, incoming)

        moon01 = Flielink.strip() if Flielink != None else None
        moon03 = Username.strip() if Username != None else None
        moon04 = Password.strip() if Password != None else None
        moon02 = Filename.strip() if Filename != None else filename
        return SMessage(filelink=moon01, filename=moon02, username=moon03, password=moon04)

#=============================================================================================
