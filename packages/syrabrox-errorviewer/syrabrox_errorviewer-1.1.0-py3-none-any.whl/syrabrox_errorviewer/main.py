import sys
import os
import traceback
from datetime import datetime

def errorlaw(exception, intents, filename="Error_Logs.txt"):
    print("!! Error Logs !!")
    intents_str = str(intents)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    file_path = exc_tb.tb_frame.f_code.co_filename
    file_name = os.path.basename(file_path)
    log = []

    if '1' in intents_str:
        print(f"An error occurred: {exception}")
        log.append(f"An error occurred: {exception}")
    if '2' in intents_str:
        print(f"Error type: {exc_type.__name__}")
        log.append(f"Error type: {exc_type.__name__}")
    if '3' in intents_str:
        print(f"Error message: {exc_obj}")
        log.append(f"Error message: {exc_obj}")
    if '4' in intents_str:
        print(f"Error occurred in file: {file_name}")
        log.append(f"Error occurred in file: {file_name}")
    if '5' in intents_str:
        print(f"Full file path: {file_path}")
        log.append(f"Full file path: {file_path}")
    if '6' in intents_str:
        print(f"Error in line: {exc_tb.tb_lineno}\n")
        log.append(f"Error in line: {exc_tb.tb_lineno}")
    if '7' in intents_str:
        # print("\nTraceback details:")
        # traceback.print_tb(exc_tb)
        print(f"Traceback details: {tb_str}\n")
        tb_str = ''.join(traceback.format_tb(exc_tb))
        log.append(f"\nTraceback details: {tb_str}")
    if '8' in intents_str:
        with open(filename, 'a') as logFile:
            logFile.write(f"Logs Information: {datetime.now()}\n")
            for errors in log:
                logFile.write(f"{errors}\n")