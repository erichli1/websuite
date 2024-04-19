import signal
import sys

from evaluation.agents.natbot.natbot import run_natbot


class TimeoutException(Exception):  # Custom exception class
    pass


def timeout_handler(signum, frame):  # Custom signal handler
    raise TimeoutException


signal.signal(signal.SIGALRM, timeout_handler)

if __name__ == "__main__":
    goal = sys.argv[1]
    url = sys.argv[2]

    if sys.argv[3] != "None":
        timeout = int(sys.argv[3])
        signal.alarm(timeout)
        print(f"    Running with timeout limit of {timeout}s")

    try:
        run_natbot(goal, url, auto=True)
    except TimeoutException:
        print("Process timed out.")
    else:
        # Reset the alarm
        signal.alarm(0)
