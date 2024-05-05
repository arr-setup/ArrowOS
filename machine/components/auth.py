import os
import time

import adrv
import bcrypt
import getpass


from components import styles as st
from components import gateway as gtw

def connect(userDisk: adrv.Disk, tempDisk: adrv.Disk):
    os.system('clear')
    try:
        username = ''
        while username == '':
            _users = gtw.split(userDisk.read('.sys\\$Users').content.decode())
            users = gtw.parse(_users, ('name', 'password', 'admin'))
            users = [{ 'name': user['name'], 'password': user['password'], 'admin': bool(user['admin']) } for user in users ]

            __maxlenname = 0
            for user in users:
                if len(user['name']) // 4 >= __maxlenname:
                    __maxlenname = (len(user['name']) // 4)

            print(f"{st.gray}{st.bold}Available accounts{st.r}")
            
            for user in users:
                line = f"{st.gray}{st.bold}{users.index(user) + 1}-\t{st.blue}"
                line += user['name']
                line += (__maxlenname - (len(user['name']) - 1) // 4 + 1) * '\t'
                line += f"{st.r}{f'{st.green}Admin' if user['admin'] else ''}{st.r}"

                print(line)
            
            print(f"{st.gray}{st.bold}[BLANK]\t{st.blue}New{st.r}")
            print()

            req = input(f"Enter your username: {st.yellow}")
            if req != '':
                matches = [ account for account in users if account['name'] == req ]
            else:
                create_user(userDisk, tempDisk)
                continue

            print(st.r, end ='')

            while len(matches) == 0:
                print(f"{st.red}{st.bold}err{st.r} Account not found")
                req = input(f"Enter your username: {st.yellow}")
                matches = [ account for account in users if account['name'] == req ]

            user = matches[0]
            username = user['name']
            admin = user['admin']

            print("Use [CTRL+C] to connect to another account", "\n")

            try:
                salt = userDisk.read('.sys\\s\\$Salt').content
                password = bcrypt.hashpw(getpass.getpass(f"{st.gray}> Password: {st.r}").encode('UTF-8'), salt)
                
                while password != user['password'].encode('UTF-8'):
                    print(f"{st.red}{st.bold}err{st.r} Passwords do not match. Start again.")
                    
                    password = bcrypt.hashpw(getpass.getpass(f"{st.gray}> Password: {st.r}").encode('UTF-8'), salt)
            except KeyboardInterrupt:
                username = ''

        data = [ username, password.decode(), str(admin) ]
        tempDisk.write('$Session', '\n'.join(data), 'w')
    except FileNotFoundError:
        create_user(userDisk, tempDisk)
        
    print(f"{st.r}")
    os.system("clear")
    time.sleep(5)

def create_user(userDisk: adrv.Disk, tempDisk: adrv.Disk):
    os.system('clear')
    print(f"{st.gray}{st.bold}Create an account{st.r}")

    def is_allowed(username: str) -> bool:
        allowedchars = "abcdefghijklmnopqrstuvwxyz"
        for char in username:
            if not (char.isdigit() or char.lower() in allowedchars or char in '._$'):
                return False
        
        return True

    username = input(f"{st.gray}> Username: {st.yellow}")
    while not is_allowed(username):
        print(f"{st.red}{st.bold}err{st.r} Only alphanumeric characters, periods, dollar signs and underscores (_) are allowed in usernames.")
        username = input(f"{st.gray}> Username: {st.yellow}")
    
    try:
        salt = userDisk.read('.sys\\s\\$Salt').content
    except FileNotFoundError:
        print(st.red, st.bold, f"err {st.r} SYSTEM disk not correctly configured.")
        exit()

    password = bcrypt.hashpw(getpass.getpass(f"{st.gray}> Password: {st.r}").encode('UTF-8'), salt)
    confirm = bcrypt.hashpw(getpass.getpass(f"{st.gray}> Confirm password: {st.r}").encode('UTF-8'), salt)
    while confirm != password:
        print(f"{st.red}{st.bold}err{st.r} Passwords do not match. Start again.")
        password = bcrypt.hashpw(getpass.getpass(f"{st.gray}> Password: {st.r}").encode('UTF-8'), salt)
        confirm = bcrypt.hashpw(getpass.getpass(f"{st.gray}> Confirm password: {st.r}").encode('UTF-8'), salt)

    data = [ username, confirm.decode(), "True" ]

    userDisk.write('.sys\\$Users', f"{username}::{password.decode()}::True")
    userDisk.write('.sys\\config\\usrdir', f"{username}::{userDisk.name}:\\usr\\{username}")
    tempDisk.write('$Session', '\n'.join(data), 'w')