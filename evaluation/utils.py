from typing import Callable, Dict
from evaluation.agents.natbot.natbot import run_natbot
import sys
import os
from evaluation.evaluators import Eval as eval


parent_folder = os.path.join(os.path.dirname(__file__), "../")

LOCALHOST_PORT = 3000  # needs to be in sync with /environment/frontend/package.json


class Test:
    def __init__(self, goal: str, eval: Callable[[list[str]], bool]):
        self.goal = goal
        self.eval = eval

    def eval(self, response: list[str]) -> bool:
        return self.eval(response)


ind_tests: Dict[str, Dict[str, Test]] = {
    "click": {
        "button": Test("Click the button", lambda logs: eval.all(logs, [eval.len_match(1), eval.contains_partial_match("click/button")])),
        "link": Test("Click the link", lambda logs: eval.all(logs, [eval.len_match(1), eval.contains_partial_match("click/link")])),
        "slider": Test("Adjust the volume to be the maximum", lambda logs: eval.all(logs, [eval.len_match(1), eval.contains_partial_match("click/slider"), eval.contains_partial_match("100")])),
    },
}


def get_url(task: str, test: str):
    return f"localhost:{LOCALHOST_PORT}/ind/{task}?test={test}"


def get_test_and_metadata(task: str, test: str):
    task_dict = ind_tests.get(task)
    if task_dict is None:
        print(f"ERROR: unable to find task {task}")
        return None

    test_goal = task_dict.get(test)
    if test_goal is None:
        print(f"ERROR: unable to find test {task}/{test}")
        return None

    return (test_goal, (task, test))


def get_tests_and_metadatas_from_task(task: str):
    task_dict = ind_tests.get(task)
    if task_dict is None:
        print(f"ERROR: unable to find task {task}")
        return None

    return [(task_dict[test], (task, test)) for test in task_dict.keys()]


def get_all_tests_and_metadatas():
    return [(ind_tests[task][test], (task, test)) for task in ind_tests.keys() for test in ind_tests[task].keys()]


def get_evals_dict(filename: str) -> Dict[str, list[str]]:
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


if (__name__ == "__main__"):
    # Identify the right goals and urls to iterate through
    tests_and_metadatas = []
    if len(sys.argv) > 1:
        for i, arg in enumerate(sys.argv[1:]):
            parts = arg.split("/", 1)
            if len(parts) == 1:
                tests_and_metadatas.extend(
                    get_tests_and_metadatas_from_task(parts[0]))
            elif len(parts) == 2:
                tests_and_metadatas.append(
                    get_test_and_metadata(parts[0], parts[1]))
    else:
        tests_and_metadatas = get_all_tests_and_metadatas()

    # Clear the log file
    with open(parent_folder + "trajectories/log.txt", "w") as file:
        pass

    # Run the tests
    for test, metadata in tests_and_metadatas:
        with open(parent_folder + "trajectories/log.txt", "a") as file:
            file.write(f"TEST BEGIN: {metadata[0]}/{metadata[1]}\n")
        run_natbot(test.goal, get_url(*metadata))
        with open(parent_folder + "trajectories/log.txt", "a") as file:
            file.write("TEST FINISH\n")

    # Evaluate the log file
    eval_dict = get_evals_dict(parent_folder + "trajectories/log.txt")
    for key, items in eval_dict.items():
        test, metadata = get_test_and_metadata(*key.split("/"))
        print(f"{key}: {test.eval(items)}")
