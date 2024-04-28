from typing import Any, Callable, TypedDict
import subprocess
import threading
import time

LOCALHOST_PORT = 3000  # needs to be in sync with /environment/frontend/package.json

TASK_CATEGORY_DICT: dict[str, list[str]] = {
    "operational": ["click", "type", "select"],
    "navigational": ["menu"],
    "informational": ["find", "filter", "fill", "search"],  # review
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


def get_evals_dict(filename: str) -> dict[str, list[TestSpecificEvalDict]]:
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
                if current_key not in eval_dict:
                    eval_dict[current_key] = [{"logs": current_logs, "submit": submit}]
                else:
                    eval_dict[current_key].append(
                        {"logs": current_logs, "submit": submit}
                    )
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


def generate_checkpoints_from_logs(
    filename: str,
) -> dict[str, list[list[dict[str, Any]]]]:
    """Parses a log file into a dictionary mapping test names to a list of test trajectories, each of which is a list of checkpoints (each checkpoint is a dictionary with a url and logs)"""
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

            if current_test not in full:
                full[current_test] = [checkpoints]
            else:
                full[current_test].append(checkpoints)

            collecting = False
            current_test = None
            current_logs = []
            checkpoints = []
        elif collecting:
            current_logs.append(line)

    return full


def check_limits(
    process,
    log_file: str,
    line_threshold: int | None,
    timeout: int | None = None,
    custom_log_break: Callable[[list[str]], bool] | None = None,
    custom_log_break_str: str | None = None,
):
    start_time = time.time()
    while process.poll() is None:
        if timeout is not None and time.time() - start_time > timeout:
            process.terminate()
            print("Process terminated due to timeout.")
            return

        with open(log_file, "r") as file:
            lines = file.readlines()
            if line_threshold is not None and len(lines) >= line_threshold:
                process.terminate()
                print("Process terminated due to excess log entries.")
                return
            if custom_log_break is not None and custom_log_break(lines):
                process.terminate()
                print(f"Process terminated due to: {custom_log_break_str}")
                return
        time.sleep(1)


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
    command = f"""python -m evaluation.agent "{goal}" "{url}" """
    # if addl_lines is not None:
    if addl_lines:
        print(f"    Running with log line threshold of {addl_lines}")
    if timeout:
        print(f"    Running with timeout limit of {timeout}s")
    if custom_log_break:
        print(f"    Running with custom log break: {custom_log_break_str}")

    process = subprocess.Popen(command, shell=True)

    # Start thread to monitor the log file
    log_thread = threading.Thread(
        target=check_limits,
        args=(
            process,
            log_file,
            (addl_lines + existing_lines) if addl_lines is not None else None,
            timeout,
            custom_log_break,
            custom_log_break_str,
        ),
    )
    log_thread.start()

    process.wait()
    log_thread.join()
    # else:
    #     process = subprocess.Popen(command, shell=True)
    #     process.wait()
