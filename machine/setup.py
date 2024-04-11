import adrv
import bcrypt
import getpass
import os
import tempfile
import time
import warnings

from components import styles as st
from components import auth

userDisk = adrv.Disk('ARR', './disks', 512000000000)
tempDisk = adrv.Disk('TMP', './disks', 1024000000)
tempDisk.format_disk()

os.system('cls')
time.sleep(1)

def config():
    print(f"{st.yellow}{st.bold}Welcome to ArrowBit !{st.r}")
    
    available_disks = []
    for _root, _, _files in os.walk('.'):
        for _name in _files:
            _file = os.path.join(_root, _name)
            if _name.endswith('.adrv'):
                with tempfile.TemporaryDirectory('r') as tmp:
                    test_disk = adrv.Disk(_name, tmp)
                    if test_disk.diagnosis(snooze = True):
                        available_disks.append({ 'path': _file, 'size': test_disk.size, 'maxSize': test_disk.max_size })
    
    new_disk = input(f"{st.gray}Should we create a new virtual disk ? (Y/N){st.r} ") in ['Y', 'y', 'yes']
    
    if new_disk:
        userDisk.format_disk()
        userDisk.write('.sys\\s\\$Salt', bcrypt.gensalt(), 'w')
        print("Should we install...")

        tempDisk.write('.sys\\$Bootexec.ar', 'req -g https://bowandarrow.pages.dev/modules/bow/installer.ar --save-on res;\nfile -n /.sys/bow/modules/bow/installer.ar res.content;', 'w')
        if input(f"{st.t}{st.gray}> Custom themes (Y/N){st.r} ") in ['Y', 'y', 'yes']:
            tempDisk.write('\\$Bootexec.ar', 'bow -i "themes";')
        if input(f"{st.t}{st.gray}> Console (Y/N){st.r} ") in ['Y', 'y', 'yes']:
            tempDisk.write('\\$Bootexec.ar', 'bow -i "console";')
    else:
        print()
        print(f"{st.gray}{st.bold}All disks found in the working directory:{st.r}")

        __maxlensize = 0
        __maxlenpath = 0

        for disk in available_disks:
            if len(disk['path']) // 4 >= __maxlenpath:
                __maxlenpath = (len(disk['path']) // 4)
            
            if len(disk['size'].literal()) // 4 >= __maxlensize:
                __maxlensize = (len(disk['size'].literal()) // 4)
        
        for disk in available_disks:
            line = f"{st.t}{st.gray}{st.bold}{available_disks.index(disk) + 1}-\t{st.r}{st.yellow}"
            line += disk['path']
            line += (__maxlenpath - (len(disk['path']) - 1) // 4 + 1) * '\t'
            line += f"{st.r}{st.red if disk['size'].raw >= disk['maxSize'].raw else st.green}"
            line += disk['size'].literal()
            line += st.r

            print(line)

        print(f"{st.t}{st.gray}{st.bold}Custom\t{st.r}{st.yellow}Pick somewhere else{st.r}")

        choice = input(f"Disk path or position: {st.yellow}")
        if choice.isnumeric() and 1 <= int(choice) <= len(available_disks):
            disk_path = available_disks[int(choice) - 1]['path']
        else:
            disk_path = os.path.normpath(choice)
        
        while not os.path.exists(disk_path):
            print(f"{st.red}{st.bold}err{st.r} <{st.yellow}{disk_path}{st.r}> Not Found.")
            choice = input(f"Disk path or position: {st.yellow}")
            if choice.isnumeric():
                disk_path = available_disks[int(choice) - 1]['path']
            else:
                disk_path = os.path.normpath(choice)
        
        print()
        print(f"{st.gray}Copying new disk... - {st.r}", end = '')
        userDisk.format_disk(disk_path)
        print(f"{st.bold}{st.green}Done{st.r}")

    if userDisk.diagnosis(True):
        print(f"{st.green}{st.bold}Your disk has been initialized with success.{st.r}")
    else:
        print(f"{st.red}{st.bold}err{st.r} There was a problem when we tried to initialize your disk, the old one may be broken.")
        print("The disk will be formatted")
        userDisk.format_disk()
    
    userDisk.write('$')

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category = UserWarning, module = 'zipfile')
    try:
        if '$' not in userDisk.f_list() or '.sys\\s\\$Salt' not in userDisk.f_list():
            config()
    except KeyboardInterrupt as kb:
        print(st.r)
        print("Configuration has been interrupted. Initializing machine... - ", end = "")
        userDisk.format_disk()
        print(st.green, st.bold, 'Done', st.r, sep = "")

    print()

    os.system('cls')
    time.sleep(1)
    try:
        auth.connect(userDisk, tempDisk)
        print("Setup done ! Rebooting...")
    except FileNotFoundError:
        auth.create_user(userDisk, tempDisk)