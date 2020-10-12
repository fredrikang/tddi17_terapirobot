import json
import os
from pathlib import Path

# -----------------------------------------------------------
# Class handling all Furhat log files in the /usr/FurhatLogs folder
#
# Used for the Furhat robot to read all .json log files.
# -----------------------------------------------------------
class Log:   
    """
    Represents all furhat logs. Allows for reading logs and printing them in a formatted manner.
    """
    def __init__(self):
        self.data = { }
        try:
            logFolder = os.path.join(str(Path.home()), 'FurhatLogs', 'logs')
            for logName in os.listdir(logFolder):
                file = os.path.join(logFolder, logName, 'dialog.json')
                self.formatJsonFile(file = file)
                with open(file, 'r') as f:
                    self.data[logName] = json.load(f)
                    if len(self.data[logName]) <= 1:
                        del(self.data[logName])
        except:
            print('\"Failed to find folder FurhatLogs\"')

    def formatJsonFile(self, file):
        """
        Formats the Furhat created log file to be readable with json. Encapulates log with [].
        """
        needFormatting = False
        with open(file, 'r+') as f:
            content = f.read()

            if content[0] != '[':
                needFormatting = True
            f.close()

        with open(file, 'w') as f:
            f.seek(0, 0)
            if needFormatting == True:
                f.write('[' + content + ']')
            else:
                f.write(content)
            f.close()


    def getMessage(self, selected, index, maxLength = -1):
        """
        Get the message(text) of the json object. If maxLength is > 0 the resulting string will try to fit maxLength characters per line.

        If maxlength is -1 it will return non edited string.
        If maxLength = 0 ony one word will be written per line.
        If maxlength > 0 it will try to only let maxLength amount of characters be on a single line.
        Will add newlines based on words so that if a full word and a half word can be printed on one line only one word will be allowed.
    
        i.e. wordLength of 5: 
            string = Hey Mister! => formatted = Hey\\nMister!
          
        As can be seen it will not take into account if a single word is larger than maxLength but only if two or more words can be on the same line. 

        @param selected  - Selected log (filename)
        @param index     - Index of the json object from selected.
        @param maxLength - Maximum amount of characters per line. -1 => all characters per line. 
        """
        if self.data[selected][index]['text'] == '':
            return "[SILENT]"
        elif maxLength < 0:
            return self.data[selected][index]['text']
        else:
            stok = self.data[selected][index]['text'].split(' ')
            formatted = []
            curLen = 0
            for s in stok:
                if curLen + len(s) + 1 > maxLength:
                    formatted.append('\n')
                    curLen = 0

                formatted.append(s)
                curLen += len(s)         
            
            return ' '.join(formatted) 
    
    def getTimeStamp(self, selected, index):
        """
        Get the timestamp of the json object. Will return the 'endTime' value if no 'startTime' exists.

        @param selected - Selected log (filename)
        @param index    - Index of the json object from selected
        """
        if 'startTime' in self.data[selected][index]:
            return self.data[selected][index]['startTime'].split('.')[0]
        else:
            return self.data[selected][index]['endTime'].split('.')[0]

    def getUser(self, selected, index):
        """
        Get the user based on type (either user or robot).

        @param selected - Selected log (filename)
        @param index    - Index of the json object from selected
        """
        stok = self.data[selected][index]['type'].split('.')
        if stok[1] == 'response':
            return 'null'
        else:
            return stok[0]

    def toString():
        return ""