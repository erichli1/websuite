from typing import Any, Callable, Dict, TypeAlias
from evaluation.agents.natbot.natbot import run_natbot
import sys
import os
import re
from evaluation.evaluators import Eval as eval, Log
from evaluation.utils import flatten, get_evals_dict, get_url


## HELPFUL TYPES AND CONSTANTS


class Test:
    def __init__(self, goal: str, eval: Callable[[list[str]], bool], name: str = None):
        self.goal = goal
        self.eval = eval
        self.name = "default" if name is None else name

    def eval(self, response: list[str]) -> bool:
        return self.eval(response)


TestsAndMetadata: TypeAlias = tuple[list[Test], tuple[str, str]]


PARENT_FOLDER = os.path.join(os.path.dirname(__file__), "../")
LOCALHOST_PORT = 3000  # needs to be in sync with /environment/frontend/package.json


ind_tests: Dict[str, Dict[str, list[Test]]] = {
    "click": {
        "button": [
            Test(
                "Click the button",
                lambda logs: eval.ordered(
                    logs, [eval.exact_match(component="click/button")]
                ),
            )
        ],
        "link": [
            Test(
                "Click the link",
                lambda logs: eval.ordered(
                    logs,
                    [
                        eval.exact_match(component="click/link"),
                    ],
                ),
            )
        ],
        "slider": [
            Test(
                "Adjust the volume to be the maximum",
                lambda logs: eval.ordered(
                    logs, [eval.exact_match("click/slider", "100")]
                ),
                name="max",
            ),
            Test(
                "Adjust the volume to be the minimum",
                lambda logs: eval.ordered(
                    logs, [eval.exact_match("click/slider", "0")]
                ),
                name="min",
            ),
            Test(
                "Make the volume louder",
                lambda logs: eval.ordered(
                    logs,
                    [
                        eval.all_log(
                            [
                                eval.exact_match("click/slider"),
                                eval.compare_values(lambda x, y: int(x) > int(y)),
                            ]
                        )
                    ],
                ),
                name="louder",
            ),
            Test(
                "Make the volume quieter",
                lambda logs: eval.ordered(
                    logs,
                    [
                        eval.all_log(
                            [
                                eval.exact_match("click/slider"),
                                eval.compare_values(lambda x, y: int(x) < int(y)),
                            ]
                        )
                    ],
                ),
                name="quieter",
            ),
        ],
    },
}


## HELPER FUNCTIONS RELYING ON INDIVIDUAL TESTS


def get_specific_test_and_metadata(task: str, test: str, name: str):
    task_dict = ind_tests.get(task)
    if task_dict is None:
        print(f"ERROR: unable to find task {task}")
        return None

    test_obj = task_dict.get(test)
    if test_obj is None:
        print(f"ERROR: unable to find test {task}/{test}")
        return None

    for test in test_obj:
        if test.name == name:
            return (test, (task, test))

    print(f"ERROR: unable to find test {task}/{test}/{name}")
    return None


def get_tests_and_metadata(task: str, test: str) -> TestsAndMetadata | None:
    task_dict = ind_tests.get(task)
    if task_dict is None:
        print(f"ERROR: unable to find task {task}")
        return None

    test_obj = task_dict.get(test)
    if test_obj is None:
        print(f"ERROR: unable to find test {task}/{test}")
        return None

    return (test_obj, (task, test))


def get_tests_and_metadatas_from_task(task: str) -> list[TestsAndMetadata] | None:
    task_dict = ind_tests.get(task)
    if task_dict is None:
        print(f"ERROR: unable to find task {task}")
        return None

    return [get_tests_and_metadata(task, test) for test in task_dict.keys()]


def get_all_tests_and_metadatas() -> list[TestsAndMetadata] | None:
    return flatten(
        [get_tests_and_metadatas_from_task(task) for task in ind_tests.keys()]
    )


## RUNNING THE EVALUATION


if __name__ == "__main__":
    # Identify the right goals and urls to iterate through
    tests_and_metadatas = []
    if len(sys.argv) > 1:
        for i, arg in enumerate(sys.argv[1:]):
            parts = arg.split("/", 1)
            if len(parts) == 1:
                tests_and_metadatas.extend(get_tests_and_metadatas_from_task(parts[0]))
            elif len(parts) == 2:
                tests_and_metadatas.append(get_tests_and_metadata(parts[0], parts[1]))
    else:
        tests_and_metadatas = get_all_tests_and_metadatas()

    # Clear the log file
    with open(PARENT_FOLDER + "trajectories/log.txt", "w") as file:
        pass

    # Run the tests
    for tests, metadata in tests_and_metadatas:
        for test in tests:
            with open(PARENT_FOLDER + "trajectories/log.txt", "a") as file:
                file.write(f"TEST BEGIN: {metadata[0]}/{metadata[1]} {test.name}\n")
            run_natbot(test.goal, get_url(LOCALHOST_PORT, *metadata))
            with open(PARENT_FOLDER + "trajectories/log.txt", "a") as file:
                file.write("TEST FINISH\n")

    # Evaluate the log file
    eval_dict = get_evals_dict(PARENT_FOLDER + "trajectories/log.txt")
    for key, items in eval_dict.items():
        logs = [Log(item) for item in items]
        test, metadata = get_specific_test_and_metadata(*re.split(r"[ /]", key))
        print(f"{key}: {test.eval(logs)}")