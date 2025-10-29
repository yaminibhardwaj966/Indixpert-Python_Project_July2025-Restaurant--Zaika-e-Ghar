import os,sys,json
import inspect
import time
sys.path.append(os.getcwd())
from Model.conflict import tableBookingLogs_Path
ob = tableBookingLogs_Path
filepath = ob.tablebookingLogsPath

def Writelogs(errorlogs):

    log_dir = os.path.dirname(filepath)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            try:
                logs = json.load(file)
            except json.JSONDecodeError:
                logs = []
    else:
        logs = []

    currentdate=time.strftime("%d/%m/%Y , %I:%M %p"),
    current = inspect.currentframe()
    caller = current.f_back

    filename = os.path.basename(caller.f_code.co_filename)
    function = caller.f_code.co_name
    line = caller.f_lineno

    log_entry = {
        "ERROR": errorlogs,
        "DATE / TIME": currentdate,
        "MODULE": filename,
        "FUNCTION":function,
        "LINE":line
    }
    
    logs.append(log_entry)

    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(logs, file, indent=2)

    