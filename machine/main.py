from adrv import Disk
import os
import time

import components.auth as auth
import components.styles as st
import components.machine as vm
import components.gateway as gtw

userDisk = Disk('ARR', './disks', 512000000000)
tempDisk = Disk('TMP', './disks', 1024000000)
tempDisk.format_disk() # Clear the ancient state

auth.connect(userDisk, tempDisk)
session = {}
while session == {}:
    try:
        _session = gtw.split(tempDisk.read('$Session').content.decode())
        session = dict(zip(('username', 'password', 'admin'), _session))
        # Check if the given session has a match in the disk (plus the password)
    except FileNotFoundError: # Case there is no $Session file in the tempDisk
        input(f"{st.red}{st.bold}err{st.r} Login failed, press [Enter] to reconnect.")
        os.system('clear')
        auth.connect(userDisk, tempDisk)

infos = {}
while infos == {}:
    try:
        _infos = gtw.split(userDisk.read('.sys\\$Info').content.decode())
        infos = dict(zip(('name', 'version'), _infos))
    except FileNotFoundError:
        print(f"{st.red}{st.bold}err{st.r} Your disk is not totally configured for this version.")
        input("Please press [Enter] and run setup.")
        os.system('clear')
        exit()

try:
    session['admin'] = bool(session['admin'])
except KeyError:
    session['admin'] = False
    time.sleep(1)

os.system('clear')
if os.path.join("usr", session['username'], "work", "$Settings") not in userDisk.f_list():
    time.sleep(0.5)
    input(f"""{st.yellow}{st.bold}ArrowOS Terminal{st.r}

    {st.gray}Welcome to ArrowOS 0.0-beta - You are on a preview version of ArrowOS, so ArrowBit is not available. Check the ArrowBit docs at https://arrowbit.vercel.app/docs{st.r}

    {st.yellow}{st.bold}Basic commands:{st.r}
    {st.t}{st.blue}go {st.green}<location:str>{st.r} - Change location
    {st.t}{st.blue}run {st.green}<file:path>{st.r} - Run a file located on the disk or on the web
    {st.t}{st.blue}var {st.green}-Action(a, d) <name:id> [value:?Any]{st.r} - Assign or delete a variable
    {st.t}{st.blue}file {st.green}-Action(n, i, d){st.r} - Manage files

    Press {st.bold}{st.yellow}[Enter]{st.r} to continue.""")
    os.system('clear')

    userDisk.write(os.path.join("usr", session['username'], "work", "$Settings"), 'FirstBoot=True')

w = vm.Window(infos['name'], userDisk, tempDisk, session)

running = True
while running:
    try:
        location = os.path.normpath(os.path.join("~", "work"))
        line = f"{f'{st.pink}(admin) ' if session['admin'] else ''}{st.green}{session['username']}@{infos['name']} {st.yellow}{location}{st.r} > "
        cmd = input(line)

        tempDisk.write('Output.L', '::'.join(['cmd', location, cmd.replace('::', '\:\:')]))
        w.refresh()
    except KeyboardInterrupt:
        running = False
        os.system('cd ..')
        os.system('clear')