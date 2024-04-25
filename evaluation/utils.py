from typing import Any, Callable, TypedDict
import subprocess
import threading
import time

LOCALHOST_PORT = 3000  # needs to be in sync with /environment/frontend/package.json

TASK_CATEGORY_DICT: dict[str, list[str]] = {
    "operational": ["click", "type", "select"],
    "navigational": ["menu"],
    "informational": ["find", "filter", "fill"],  # search, review
}


TASK_TO_CATEGORY_MAP: dict[str, str] = {
    task: category for category, tasks in TASK_CATEGORY_DICT.items() for task in tasks
}


def flatten(input: list[list[Any]]) -> list[Any]:
    return [item for sublist in input for item in sublist]


def get_url(localhost_port: str, task: str, test: str):
    return f"localhost:{localhost_port}/ind/{task}?test={test}"


class TestSpecificEvalDict(TypedDict):
    logs: list[str]
    submit: str


def get_evals_dict(filename: str) -> dict[str, TestSpecificEvalDict]:
    lines = ""
    with open(filename, "r") as file:
        lines = file.readlines()

    eval_dict = {}
    collecting = False
    current_key = None
    current_logs = []
    submit = None

    for line in lines:
        line = line.strip()
        if line.startswith("TEST BEGIN:"):
            collecting = True
            current_key = line.split(":")[1].strip()
        elif line.startswith("TEST FINISH"):
            if current_key:
                eval_dict[current_key] = {"logs": current_logs, "submit": submit}
            collecting = False
            current_key = None
            current_logs = []
            submit = None
        elif collecting:
            if line.startswith("SUBMIT"):
                submit = line
            else:
                current_logs.append(line)

    return eval_dict


def generate_checkpoints_from_logs(filename: str) -> dict[str, list]:
    lines = ""
    with open(filename, "r") as file:
        lines = file.readlines()

    full = {}

    checkpoints = []
    collecting = False
    current_test = None
    current_checkpoint = None
    current_logs = []

    for line in lines:
        line = line.strip()
        if line.startswith("TEST BEGIN"):
            collecting = True
            current_test = line.split(":")[1].strip()
        elif line.startswith("NAVIGATE"):
            # if checkpoint already exists, end it
            if current_checkpoint:
                checkpoints.append(
                    {
                        "url": current_checkpoint.split("//")[1].strip(),
                        "logs": current_logs,
                    }
                )

            # create new checkpoint
            current_checkpoint = line
            current_logs = []
        elif line.startswith("TEST FINISH"):
            # if currently logging checkpoint, end it
            if current_checkpoint:
                checkpoints.append(
                    {
                        "url": current_checkpoint.split("//")[1].strip(),
                        "logs": current_logs,
                    }
                )
            full[current_test] = checkpoints

            collecting = False
            current_test = None
            current_logs = []
        elif collecting:
            current_logs.append(line)

    return full


def check_log_file(
    process,
    line_threshold: int,
    log_file: str,
    custom_log_break: Callable[[list[str]], bool] | None = None,
    custom_log_break_str: str | None = None,
):
    while process.poll() is None:
        with open(log_file, "r") as file:
            lines = file.readlines()
            if len(lines) >= line_threshold:
                process.terminate()
                print("Process terminated due to excess log entries.")
                return
            if custom_log_break and custom_log_break(lines):
                process.terminate()
                print(f"Process terminated due to: {custom_log_break_str}")
                return
        time.sleep(1)


def run_with_log_monitoring(
    command: str,
    line_threshold: int,
    log_file: str,
    custom_log_break: Callable[[list[str]], bool] | None = None,
    custom_log_break_str: str | None = None,
):
    process = subprocess.Popen(command, shell=True)

    # Start thread to monitor the log file
    log_thread = threading.Thread(
        target=check_log_file,
        args=(
            process,
            line_threshold,
            log_file,
            custom_log_break,
            custom_log_break_str,
        ),
    )
    log_thread.start()

    process.wait()
    log_thread.join()


def run_agent_with_limits(
    goal: str,
    url: str,
    existing_lines: int,
    log_file: str,
    timeout: int | None = None,
    addl_lines: int | None = None,
    custom_log_break: Callable[[list[str]], bool] | None = None,
    custom_log_break_str: str | None = None,
):
    command = f"""python -m evaluation.agent "{goal}" {url} {timeout}"""
    if addl_lines is not None:
        print(f"    Running with log line threshold of {addl_lines}")
        if custom_log_break:
            print(f"    Running with custom log break: {custom_log_break_str}")
        run_with_log_monitoring(
            command,
            addl_lines + existing_lines,
            log_file,
            custom_log_break,
            custom_log_break_str,
        )
    else:
        process = subprocess.Popen(command, shell=True)
        process.wait()
