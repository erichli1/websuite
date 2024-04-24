from typing import Any, TypedDict


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
