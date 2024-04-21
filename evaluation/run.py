from typing import Any, Callable, Dict, TypeAlias
import sys
import os
import re
from evaluation.evaluators import Eval as eval, Log
from evaluation.utils import flatten, get_evals_dict, get_url
import subprocess
import threading
import time


## HELPFUL TYPES AND CONSTANTS


class Test:
    def __init__(
        self,
        goal: str,
        eval: Callable[[list[str]], bool],
        name: str = None,
        max_lines: int | None = None,
    ):
        self.goal = goal
        self.eval = eval
        self.name = "default" if name is None else name
        self.max_lines = max_lines

    def eval(self, response: list[str]) -> bool:
        return self.eval(response)


TestsAndMetadata: TypeAlias = tuple[list[Test], tuple[str, str]]


PARENT_FOLDER = os.path.join(os.path.dirname(__file__), "../")
LOCALHOST_PORT = 3000  # needs to be in sync with /environment/frontend/package.json
MAX_AGENT_TIME = 30  # seconds


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
        "confirmbutton": [
            Test(
                "Delete the item",
                lambda logs: eval.ordered(
                    logs, [eval.exact_match(component="click/confirmbutton")]
                ),
            )
        ],
        "iconbutton": [
            Test(
                "Delete the item",
                lambda logs: eval.ordered(
                    logs, [eval.exact_match(component="click/iconbutton")]
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
        "snackbar": [
            Test(
                "Dismiss the notification",
                lambda logs: eval.ordered(
                    logs,
                    [
                        eval.exact_match(
                            component="click/snackbar",
                            newValue="closed",
                            oldValue="open",
                        ),
                    ],
                ),
            ),
        ],
        "switch": [
            Test(
                "Turn on do not disturb",
                lambda logs: eval.ordered(
                    logs, [eval.exact_match(component="click/switch", newValue="true")]
                ),
                "on-from-off",
            ),
            Test(
                "Turn off do not disturb",
                lambda logs: eval.no_logs(logs),
                "off-from-off",
            ),
        ],
        "dropdownmenu": [
            Test(
                "Open the menu",
                lambda logs: eval.ordered(
                    logs, [eval.exact_match(component="click/iconbutton", label="Menu")]
                ),
            ),
        ],
        "accordion": [
            Test(
                "Please open the accordion to see more",
                lambda logs: eval.ordered(
                    logs,
                    [eval.exact_match(component="click/accordion", newValue="open")],
                ),
            )
        ],
    },
    "type": {
        "text": [
            Test(
                "Enter the name John",
                lambda logs: eval.ordered(
                    logs, [eval.exact_match(component="type/text", newValue="John")]
                ),
            )
        ],
        "date": [
            Test(
                "Enter the date April 3rd, 2024",
                lambda logs: eval.ordered(
                    logs,
                    [
                        eval.all_log(
                            [
                                eval.exact_match(component="type/date"),
                                eval.contains_match(newValue="03 Apr 2024"),
                            ]
                        )
                    ],
                ),
            )
        ],
        "phone": [
            Test(
                "Please enter 617-495-1000",
                lambda logs: eval.ordered(
                    logs,
                    [
                        eval.exact_match(
                            component="type/phone", newValue="(617) 495-1000"
                        )
                    ],
                ),
            )
        ],
    },
    "select": {
        "select": [
            Test(
                "Select Canada",
                lambda logs: eval.ordered(
                    logs,
                    [eval.exact_match(component="select/select", newValue="Canada")],
                ),
            ),
        ],
        "checkbox": [
            Test(
                "Please accept the terms and conditions",
                lambda logs: eval.ordered(
                    logs,
                    [eval.exact_match(component="select/checkbox", newValue="true")],
                ),
            )
        ],
        "multicheck": [
            Test(
                "Please accept the terms and conditions and privacy policy",
                lambda logs: eval.unordered(
                    logs,
                    [
                        eval.all_log(
                            [
                                eval.exact_match(
                                    component="select/checkbox", newValue="true"
                                ),
                                eval.contains_match(label="terms and conditions"),
                            ]
                        ),
                        eval.all_log(
                            [
                                eval.exact_match(
                                    component="select/checkbox", newValue="true"
                                ),
                                eval.contains_match(label="privacy policy"),
                            ]
                        ),
                    ],
                ),
            )
        ],
        "grid": [
            # Can the agent literally select the row?
            Test(
                "Please select the row corresponding to Jane Smith",
                lambda logs: eval.ordered(
                    logs,
                    [
                        eval.exact_match(
                            component="click/gridselect", newValue="Jane Smith"
                        )
                    ],
                ),
                max_lines=1,
                name="select-one",
            ),
            # Can the agent precisely select two rows in order and then stop?
            Test(
                "Please select the row corresponding to Jane Smith and then the row corresponding to John Doe",
                lambda logs: eval.ordered(
                    logs,
                    [
                        eval.exact_match(
                            component="click/gridselect", newValue="Jane Smith"
                        ),
                        eval.exact_match(
                            component="click/gridselect", newValue="John Doe"
                        ),
                    ],
                ),
                name="linearly-select-two",
            ),
        ],
    },
    "menu": {
        "basic": [
            Test(
                "Please navigate to the page where I can change my privacy settings",
                lambda logs: eval.ordered(
                    logs, [eval.exact_match(component="click/button", label="Settings")]
                ),
                max_lines=1,
            )
        ],
        "nested": [
            Test(
                "Please navigate to the page where I can change my privacy settings",
                lambda logs: eval.ordered(
                    logs,
                    [
                        eval.exact_match(component="click/button", label="Settings"),
                        eval.exact_match(component="click/menu", label="Data privacy"),
                    ],
                ),
                max_lines=2,
            )
        ],
    },
    "info": {
        "gridfilter": [
            Test(
                "Please filter for orders where the country is USA",
                lambda logs: eval.at_least_one(
                    logs,
                    [
                        eval.exact_match(
                            component="click/gridfilter",
                            newValue='[{"field":"country","operator":"equals","value":"USA"}]',
                        )
                    ],
                ),
            )
        ],
        "gridsort": [
            Test(
                "Please sort the table by the name column in ascending order",
                lambda logs: eval.ordered(
                    logs,
                    [
                        eval.exact_match(
                            component="click/gridsort",
                            newValue='[{"field":"name","sort":"asc"}]',
                        )
                    ],
                ),
            )
        ],
        "findbasic": [
            Test(
                "Please find when the AGI Research Lab was founded and enter the year into the answer box",
                lambda logs: eval.ordered(
                    logs, [eval.exact_match(component="type/text", newValue="2032")]
                ),
            )
        ],
        "findtooltip": [
            Test(
                "Please find what state Aurora City is located in and enter the state into the answer box",
                lambda logs: eval.ordered(
                    logs,
                    [eval.exact_match(component="type/text", newValue="California")],
                ),
            )
        ],
        "finddialog": [
            Test(
                "Please find when the Prometheus Project was launched and enter the year into the answer box",
                lambda logs: eval.at_least_one(
                    logs, [eval.exact_match(component="type/text", newValue="2036")]
                ),
            ),
        ],
        "findaccordion": [
            Test(
                "Please find when the AGI Research Lab was founded and enter the year into the answer box",
                lambda logs: eval.at_least_one(
                    logs, [eval.exact_match(component="type/text", newValue="2032")]
                ),
            )
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


## AGENT RUNNING SCAFFOLDING


def check_log_file(process, line_threshold: int):
    while process.poll() is None:
        with open(PARENT_FOLDER + "trajectories/log.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= line_threshold:
                process.terminate()
                print("Process terminated due to excess log entries.")
                return
        time.sleep(1)


def run_with_log_monitoring(command: str, line_threshold: int):
    process = subprocess.Popen(command, shell=True)

    # Start thread to monitor the log file
    log_thread = threading.Thread(target=check_log_file, args=(process, line_threshold))
    log_thread.start()

    process.wait()
    log_thread.join()


def run_agent_with_limits(
    goal: str,
    url: str,
    existing_lines: int,
    timeout: int | None = None,
    addl_lines: int | None = None,
):
    command = f"""python -m evaluation.agent "{goal}" {url} {timeout}"""
    if addl_lines is not None:
        print(f"    Running with log line threshold of {addl_lines}")
        run_with_log_monitoring(command, addl_lines + existing_lines)
    else:
        process = subprocess.Popen(command, shell=True)
        process.wait()


## RUNNING THE EVALUATION


if __name__ == "__main__":
    # Identify the right goals and urls to iterate through
    skip_to_evaluate = False
    tests_and_metadatas = []
    if len(sys.argv) > 1:
        for i, arg in enumerate(sys.argv[1:]):
            if arg == "evaluate_logs":
                skip_to_evaluate = True
                break

            parts = arg.split("/", 1)
            if len(parts) == 1:
                new = get_tests_and_metadatas_from_task(parts[0])
                if new is not None:
                    tests_and_metadatas.extend(new)
            elif len(parts) == 2:
                new = get_tests_and_metadata(parts[0], parts[1])
                if new is not None:
                    tests_and_metadatas.append(new)
    else:
        new = get_all_tests_and_metadatas()
        if new is not None:
            tests_and_metadatas = new

    if not skip_to_evaluate:
        # Clear the log file
        with open(PARENT_FOLDER + "trajectories/log.txt", "w") as file:
            pass

        # Run the tests
        for tests, metadata in tests_and_metadatas:
            for test in tests:
                with open(PARENT_FOLDER + "trajectories/log.txt", "a") as file:
                    file.write(f"TEST BEGIN: {metadata[0]}/{metadata[1]} {test.name}\n")

                existing_lines = 0
                with open(PARENT_FOLDER + "trajectories/log.txt", "r") as file:
                    existing_lines = len(file.readlines())
                run_agent_with_limits(
                    goal=test.goal,
                    url=get_url(LOCALHOST_PORT, *metadata),
                    existing_lines=existing_lines,
                    timeout=MAX_AGENT_TIME,
                    addl_lines=test.max_lines,
                )

                with open(PARENT_FOLDER + "trajectories/log.txt", "a") as file:
                    file.write("TEST FINISH\n")

    # Evaluate the log file
    eval_dict = get_evals_dict(PARENT_FOLDER + "trajectories/log.txt")
    for key, items in eval_dict.items():
        logs = [Log(item) for item in items]
        test, metadata = get_specific_test_and_metadata(*re.split(r"[ /]", key))
        print(f"{key}: {test.eval(logs)}")
