from typing import Any


def flatten(input: list[list[Any]]) -> list[Any]:
    return [item for sublist in input for item in sublist]


def get_url(localhost_port: str, task: str, test: str):
    return f"localhost:{localhost_port}/ind/{task}?test={test}"


def get_evals_dict(filename: str) -> dict[str, list[str]]:
    lines = ""
    with open(filename, "r") as file:
        lines = file.readlines()

    eval_dict = {}
    collecting = False
    current_key = None
    current_values = []

    for line in lines:
        line = line.strip()
        if line.startswith("TEST BEGIN:"):
            collecting = True
            current_key = line.split(":")[1].strip()
        elif line.startswith("TEST FINISH"):
            if current_key:
                eval_dict[current_key] = current_values
            collecting = False
            current_key = None
            current_values = []
        elif collecting:
            current_values.append(line)

    return eval_dict
