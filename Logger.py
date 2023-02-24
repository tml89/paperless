import datetime
import Settings
from enum import Enum

class LogLevel(Enum):
    Info = 1
    Warning = 2
    Error = 3
    Debug = 4
    
def Log(text, logLevel: LogLevel  = LogLevel.Info):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if logLevel.value > Settings.LOGLEVEL:
        return
    print (now + "\t"+ logLevel.name + "\t" + text)