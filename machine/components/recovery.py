import os

import adrv

def resetSettings(ud: adrv.Disk):
    ud.write('.sys\\config\\usrdir', '', 'w')

def resetData(ud: adrv.Disk):
    ud.format_disk()
    os.system('cd ..')
    os.system('cmd/setup.sh')