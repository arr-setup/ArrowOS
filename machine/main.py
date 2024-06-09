import os
import tempfile
import time
import warnings

from adrv import Disk, bridge
import arrowbit

import components.auth as auth
import components.styles as st
import components.machine as vm
import components.gateway as gtw

userDisk = Disk('ARR', './disks', 512000000000)
tempDisk = Disk('TMP', './disks', 1024000000)



#------------------------------------- INIT COMPUTER STATE -------------------------------------
# Fetch computer infos

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

w = vm.Window(infos['name'], userDisk, tempDisk)

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category = UserWarning, module = 'zipfile')
    _boot = 2
    while _boot != 0:
        os.system('clear')
        _boot = w.boot()
        if _boot == 2:
            os.system('clear')
            print('Something went wrong...')
            time.sleep(3)

# Try login

auth.connect(userDisk, tempDisk)
session = {}
while session == {}:
    try:
        _session = gtw.split(tempDisk.read('$Session').content.decode())
        session = dict(zip(('username', 'password', 'admin'), _session))
        # Check if the given session has a match in the disk (plus the password)
    except FileNotFoundError: # Case there is no $Session file in the tempDisk
        auth.connect(userDisk, tempDisk)
        tempDisk.format_disk() # Clear data from old session

try:
    session['admin'] = bool(session['admin'])
except KeyError:
    session['admin'] = False
    time.sleep(1)


# Introduce to basics if first login

os.system('clear')
bootpath = os.path.join("usr", session['username'], "work", "$Config", "Boot")
if bootpath not in userDisk.f_list():
    time.sleep(0.5)
    input(f"""{st.yellow}{st.bold}ArrowOS Terminal{st.r}

    {st.gray}Welcome to ArrowOS 0.0-beta - You are on a preview version of ArrowOS, so ArrowBit is not available. Check the ArrowBit docs at https://arrowbit.vercel.app/docs{st.r}

    {st.yellow}{st.bold}Basic commands:{st.r}
    {st.t}{st.blue}go {st.green}<location:str>{st.r} - Change location
    {st.t}{st.blue}sysdata {st.green}<name:id> -Action(a, c, d, i){st.r} - Manage system data
    {st.t}{st.blue}run {st.green}<file:path>{st.r} - Run a file located on the disk or on the web
    {st.t}{st.blue}var {st.green}-Action(a, d) <name:id> [value?:Any]{st.r} - Assign or delete a variable
    {st.t}{st.blue}file {st.green}-Action(c, d, n){st.r} - Manage files
    {st.t}{st.blue}ls {st.green}-Options(c, d) [dir?:fp=.]{st.r} - List files in a directory
    {st.t}{st.blue}dir {st.green}-Options(d, m, n){st.r} - Manages directories

    Press {st.bold}{st.yellow}[Enter]{st.r} to continue.""")
    os.system('clear')

    userDisk.write(bootpath, 'bootcount=1')
else:
    bootcfgraw = gtw.split(userDisk.read(bootpath).content.decode())
    bootcfg = gtw.parse(bootcfgraw)
    bootcfg['bootcount'] += 1

#------------------------------------- PROCESS -------------------------------------

process = arrowbit.Process(userDisk, tempDisk, session)

running = True
while running:
    try:
        location = os.path.normpath(os.path.join("~", "work"))
        line = f"{f'{st.pink}(admin) ' if session['admin'] else ''}{st.green}{session['username']}@{infos['name']} {st.yellow}{location}{st.r} > "
        cmd = input(line)

        tempDisk.write('Output.L', '::'.join(['cmd', location, cmd.replace('::', '\:\:')]))
        w.refresh(session)

        pcmd = arrowbit.parse(cmd)
        if pcmd['module'] == 'arr' and pcmd['submodule'] in ['clear', 'reboot']:
            os.system(userDisk.read(f".sys\\cmd\\{pcmd['submodule']}.sh").content.decode())
        elif pcmd['module'] == 'arr' and pcmd['submodule'] in ['shutdown']:
            exec(userDisk.read(f".sys\\cmd\\{pcmd['submodule']}").content.decode())
        else:
            process.exec(pcmd)

    except KeyboardInterrupt:
        running = False
        os.system('cd ..')
        os.system('clear')