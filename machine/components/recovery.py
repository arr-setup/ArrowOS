import math
import os
import time
import uuid

import adrv

from components import styles as st

CONFIG_VERSION = '1'

def resetSettings(ud: adrv.Disk):
    ud.write('.sys/config/usrdir', '', 'w')

def resetData(ud: adrv.Disk):
    ud.format_disk()
    os.system('cd ..')
    os.system('cmd/setup.sh')

def installArrowBit(ud: adrv.Disk):
    os.system('clear')

    print(f"{st.bold}{st.yellow}Installing ArrowOS...{st.r}\n")

    print(f"{st.gray}Writing system commands...", end = ' ')
    ud.write('.sys/cmd/shutdown', 'raise KeyboardInterrupt', 'w')
    ud.write('.sys/cmd/reboot.sh', 'py machine/main.py', 'w') # Maybe just reset the tempDisk
    ud.write('.sys/cmd/clear', "import adrv\nadrv.Disk('TMP', './disks').delete('Output.L')", 'w')
    print(f"{st.green}Done{st.r}")

    print(f"{st.gray}Configuring default settings...", end = ' ')
    ud.write('.sys/MACHINE.cfg', f'ConfigVersion={CONFIG_VERSION}\nSerialNumber={uuid.uuid4()}\nConfigDate={math.floor(time.time())}', 'w')
    ud.write('.sys/READONLY.cfg', '/\n.sys/\nusr/', 'w')
    print(f"{st.green}Done{st.r}")

    time.sleep(3)