from typing import Any, Callable, Dict, TypeAlias
import sys
import os
import re
from evaluation.evaluators import Eval as eval, Log
from evaluation.utils import (
    LOCALHOST_PORT,
    flatten,
    get_evals_dict,
    get_url,
    run_agent_with_limits,
)
import subprocess
import threading
import time


## HELPFUL TYPES AND CONSTANTS

PARENT_FOLDER = os.path.join(os.path.dirname(__file__), "../")
MAX_AGENT_TIME = 30  # seconds


class Test:
    def __init__(
        self,
        goal: str,
        eval: Callable[[list[str]], bool],
        name: str = None,
        max_lines: int | None = None,
        max_time: int | None = None,
        submit_eval: Callable[[str], bool] | None = None,
    ):
        self.goal = goal
        self.eval = eval
        self.name = "default" if name is None else name
        self.max_lines = max_lines
        self.max_time = MAX_AGENT_TIME if max_time is None else max_time
        self.submit_eval = submit_eval

    def eval(self, response: list[str]) -> bool:
        return self.eval(response)


TestsAndMetadata: TypeAlias = tuple[list[Test], tuple[str, str]]


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
    "find": {
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
    "filter": {
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
    },
    "fill": {
        "basicform": [
            Test(
                "Please submit the form given that my name is John Doe, and my email is johndoe@gmail.com",
                lambda logs: eval.unordered(
                    logs,
                    [
                        eval.exact_match(
                            component="type/text", label="First name", newValue="John"
                        ),
                        eval.exact_match(
                            component="type/text", label="Last name", newValue="Doe"
                        ),
                        eval.exact_match(
                            component="type/text",
                            label="Email",
                            newValue="johndoe@gmail.com",
                        ),
                        eval.exact_match(component="click/button", label="Submit"),
                    ],
                ),
                submit_eval=lambda log: eval.check_one(
                    log,
                    [
                        eval.exact_match(
                            label='{"email":"johndoe@gmail.com","firstName":"John","lastName":"Doe"}'
                        )
                    ],
                ),
            )
        ],
        "complexform": [
            Test(
                "Please submit the form given this information from my ID. John Doe. johndoe@gmail.com. (617) 000-0000. 123 Main St. Cambridge, MA 02138. Born 1/1/2000.",
                lambda logs: eval.unordered(
                    logs,
                    [
                        eval.exact_match(
                            component="type/text", label="First name", newValue="John"
                        ),
                        eval.exact_match(
                            component="type/text", label="Last name", newValue="Doe"
                        ),
                        eval.exact_match(
                            component="type/text",
                            label="Email",
                            newValue="johndoe@gmail.com",
                        ),
                        eval.exact_match(
                            component="type/phone",
                            label="Phone number",
                            newValue="(617) 000-0000",
                        ),
                        eval.exact_match(
                            component="type/text",
                            label="Street address",
                            newValue="123 Main St",
                        ),
                        eval.exact_match(
                            component="type/text", label="City", newValue="Cambridge"
                        ),
                        eval.exact_match(
                            component="select/select", label="State", newValue="MA"
                        ),
                        eval.exact_match(
                            component="type/text", label="Zip code", newValue="02138"
                        ),
                        eval.all_log(
                            [
                                eval.exact_match(component="type/date"),
                                eval.contains_match(newValue="01 Jan 2000"),
                            ]
                        ),
                        eval.exact_match(component="click/button", label="Submit"),
                    ],
                ),
                max_time=60,
                submit_eval=lambda log: eval.check_one(
                    log,
                    [
                        eval.exact_match(
                            label='{"birthday":"Sat, 01 Jan 2000 05:00:00 GMT","city":"Cambridge","email":"johndoe@gmail.com","firstName":"John","lastName":"Doe","phoneNumber":"(617) 000-0000","state":"MA","streetAddress":"123 Main St","zipCode":"02138"}'
                        )
                    ],
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

    tests_obj = task_dict.get(test)
    if tests_obj is None:
        print(f"ERROR: unable to find test {task}/{test}")
        return None

    for test_obj in tests_obj:
        if test_obj.name == name:
            return (test_obj, (task, test))

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


def bool_to_pass_fail(b: bool) -> str:
    return "pass" if b else "fail"


## RUNNING THE EVALUATION


if __name__ == "__main__":
    # Identify the right goals and urls to iterate through
    skip_to_evaluate = False
    tests_and_metadatas = []
    if len(sys.argv) > 1:
        for i, arg in enumerate(sys.argv[1:]):
            if arg == "-evalonly":
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
                    log_file=PARENT_FOLDER + "trajectories/log.txt",
                    timeout=test.max_time,
                    addl_lines=test.max_lines,
                )

                with open(PARENT_FOLDER + "trajectories/log.txt", "a") as file:
                    file.write("TEST FINISH\n")

    # Evaluate the log file
    eval_dict = get_evals_dict(PARENT_FOLDER + "trajectories/log.txt")
    with open(PARENT_FOLDER + "output/ind.txt", "w") as file:
        for key, items in eval_dict.items():
            logs = [Log(item) for item in items["logs"]]
            test, metadata = get_specific_test_and_metadata(*re.split(r"[ /]", key))
            if test.submit_eval is not None:
                submit_eval_result = (
                    test.submit_eval(Log(items["submit"]))
                    if items["submit"] is not None
                    else False
                )

                file.write(
                    f"{key}: process:{bool_to_pass_fail(test.eval(logs))} submit:{bool_to_pass_fail(submit_eval_result)}\n"
                )
            else:
                file.write(f"{key}: {bool_to_pass_fail(test.eval(logs))}\n")
