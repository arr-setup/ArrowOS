import os
import re

import adrv

from components import styles as st
from components import gateway as gtw
from components import recovery as rcv

class Window:
    def __init__(self, name: str, ud: adrv.Disk, td: adrv.Disk) -> None:
        self.name = name
        self.ud = ud # User disk
        self.td = td # Temp disk
    
    def refresh(self, session: dict) -> None:
        os.system('clear')
        outData = gtw.split(self.td.read('Output.L').content.decode())
        outData = gtw.parse(outData, ('type', 'location', 'content'))
        
        def highlight(exp: str) -> str:
            text = exp.replace("\:\:", "::")

            text = re.sub(r"`(.+)`|\b(\d+)\b", fr"{st.green}\g<0>{st.r}", text)
            text = re.sub(r"(~/[a-zA-Z0-9.+$()]+|~\\[a-zA-Z0-9.+$()]+|/[a-zA-Z0-9.+$()]+|\\[a-zA-Z0-9.+$()]+|~|/|\\|\./[a-zA-Z0-9.+$()]+|\.\\[a-zA-Z0-9.+$()]+|\.\./[a-zA-Z0-9.+$()]+|\.\.\\[a-zA-Z0-9.+$()]+)|\$\.([A-Za-z]+)", fr"{st.yellow}\g<0>{st.r}", text)
            text = re.sub(r"'(.+)'|\"(.+)\"", fr"{st.cyan}\g<0>{st.r}", text)
            text = re.sub(r"--([A-Za-z]+)|-([A-Za-z]+)", fr"{st.gray}\g<0>{st.r}", text)

            return text
        
        for data in outData:
            if data['type'] == 'cmd':
                line = f"{f'{st.pink}(admin) ' if session['admin'] else ''}{st.green}{session['username']}@{self.name} {st.yellow}{data['location']}{st.r} > "

                syntax = r'\{[^}]*\}|\([^)]*\)|\[[^\]]*\]|\"(?:\\\"|[^\"])*\"|\'(?:\\\'|[^\'])*\'|`(?:\\\`|[^`])*`|\S+'

                cmd = []
                for word in re.findall(syntax, data['content']):
                    cmd.append(highlight(word))
                
                line += ' '.join(cmd)
            else:
                line = data['content']
                
            print(line)
        
    def ask(self, infos: list[tuple], prompt: str = "Choose an option: ", return_nb: bool = False):
        print(prompt)
        print()
        
        for opt in range(len(infos)):
            print(f"{st.blue}{opt + 1}-{st.r}", '\t'.join(infos[opt]), sep = "\t")

        choice = ""
        value = ""
        while value == "":
            try:
                value = infos[choice - 1]
            except:
                choice = int(input("Choose an option: "))

        if return_nb:
            return choice - 1
        else: 
            return value
        
    def boot(self):
        action = self.ask([
            ('Start ArrowOS',),
            ('Reset computer disk', 'Wipe all data',),
            ('Clean tempdisk data', 'This will clear console history, active sessions, ect'),
            ('(re)install ArrowBit', 'Unavailable')
        ], 'What do you want to do: ', True)

        if action == 0:
            return 0
        elif action == 1:
            try:
                rcv.resetData(self.ud)
                return 1
            except:
                return 2
        elif action == 2:
            try:
                self.td.format_disk()
                return 1
            except:
                return 2
        elif action == 3:
            rcv.installArrowBit(self.ud)
            return 1
        
        return 2

