import time
import subprocess
import threading
import os


PARENT_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/../"


def check_log_file(process, line_limit: int):
    while process.poll() is None:
        with open(PARENT_FOLDER + "trajectories/log.txt", "r") as file:
            lines = file.readlines()
            if len(lines) > line_limit:
                process.terminate()
                print("Process terminated due to excess log entries.")
                return
        time.sleep(1)


def run_with_log_monitoring(command: str, line_limit: int):
    process = subprocess.Popen(command, shell=True)

    # Start thread to monitor the log file
    log_thread = threading.Thread(target=check_log_file, args=(process, line_limit))
    log_thread.start()

    process.wait()

    log_thread.join()


command = f"""python -m evaluation.agent "Find the button" localhost:3000 5"""
run_with_log_monitoring(command, line_limit=2)
