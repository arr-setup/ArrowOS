from adrv import Disk
import os
import time

import components.auth as auth
import components.styles as st

userDisk = Disk('ARR', './disks', 512000000000)
tempDisk = Disk('TMP', './disks', 1024000000)

session = {}
while session == {}:
    try:
        session = dict(zip(['username', 'password', 'admin'], tempDisk.read('$Session').content.replace('\r', '').split('\n')))
        # Check if the given session has a match in the disk (plus the password)
    except: # Case there is no $Session file in the tempDisk
        input(f"{st.red}{st.bold}err{st.r} Login failed, press [Enter] to reconnect.")
        os.system('cls')
        auth.connect()

session['admin'] = bool(session['admin'])

os.system('cls')
time.sleep(0.5)
print(f"{st.yellow}{st.bold}ArrowOS Terminal{st.r}")
print()
print(f"{st.gray}Welcome to ArrowOS 0.0-beta - You are on a preview version of ArrowOS, so ArrowBit is not available. Check the ArrowBit docs at https://arrowbit.vercel.app/docs")
print(st.r)
print(f"{st.blue}{st.bold}Basic commands:{st.r}")
print(f"{st.t}go {st.green}<location:str>{st.r} - Change location")
print(f"{st.t}run {st.green}<file:path>{st.r} - Run a file located on the disk or on the web")
print(f"{st.t}var {st.green}-Action(a, d) <name:id> [value:?Any]{st.r} - Assign or delete a variable")
print(f"{st.t}file {st.green}-Action(n, i, d){st.r} - Manage files")
print()

running = True
while running:
    try:
        location = os.path.normpath(os.path.join("ARR:/u/", session['username'], "work"))
        line = f"{st.yellow}${st.green}{location}{st.r} > "
        cmd = input(line)
        
        print(f"{st.red}{st.bold}err{st.r} ArrowBit is not found.")
        print(f"Check out https://arrowbit.vercel.app to install it.")
    except KeyboardInterrupt:
        os.system('cd ..')
        running = False