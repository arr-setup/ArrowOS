import os
import re

import adrv

from components import styles as st
from components import gateway as gtw

class Window:
    def __init__(self, name: str, ud: adrv.Disk, td: adrv.Disk, session: dict) -> None:
        self.name = name
        self.ud = ud # User disk
        self.td = td # Temp disk
        self.session = session
        self.location = []
    
    def refresh(self) -> None:
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
                line = f"{f'{st.pink}(admin) ' if self.session['admin'] else ''}{st.green}{self.session['username']}@{self.name} {st.yellow}{data['location']}{st.r} > "

                syntax = r'\{[^}]*\}|\([^)]*\)|\[[^\]]*\]|\"(?:\\\"|[^\"])*\"|\'(?:\\\'|[^\'])*\'|`(?:\\\`|[^`])*`|\S+'

                cmd = []
                for word in re.findall(syntax, data['content']):
                    cmd.append(highlight(word))
                
                line += ' '.join(cmd)
            else:
                line = data['content']
                
            print(line)