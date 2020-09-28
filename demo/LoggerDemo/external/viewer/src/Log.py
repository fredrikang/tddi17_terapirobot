import json
import os
from pathlib import Path

class Log:   
    def formatJsonFile(self, file):
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

    def __init__(self):
        self.data = { }
        logFolder = os.path.join(str(Path.home()), 'FurhatLogs', 'logs')
        for logName in os.listdir(logFolder):
            file = os.path.join(logFolder, logName, 'dialog.json')
            self.formatJsonFile(file = file)
            with open(file, 'r') as f:
                self.data[logName] = json.load(f)
