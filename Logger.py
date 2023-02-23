import datetime
from enum import Enum

class LogLevel(Enum):
    Info = 1
    Warning = 2
    Error = 3
    Debug = 4
    
LOGLEVEL = LogLevel.Info

def Log(text, logLevel: LogLevel  = LogLevel.Info):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if logLevel.value > LOGLEVEL.value:
        return
    print (now + "\t"+ logLevel.name + "\t" + text)