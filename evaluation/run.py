import csv
from typing import Any, Callable, Dict, TypeAlias
import sys
import os
import re
from evaluation.evaluators import Eval as eval, Log
from evaluation.utils import (
    LOCALHOST_PORT,
    TASK_TO_CATEGORY_MAP,
    PassStats,
    display_pass_stats,
    flatten,
    get_evals_dict,
    get_url,
    run_agent_with_limits,
)


## HELPFUL TYPES AND CONSTANTS

PARENT_FOLDER = os.path.join(os.path.dirname(__file__), "../")
SHORT_MAX_TIME = 90
LONG_MAX_TIME = 300
LOG_FILEPATH = (
    PARENT_FOLDER + "trajectories/log.txt"
)  # needs to be in sync with environment/app.py
OUTPUT_FILEPATH = PARENT_FOLDER + "output/ind_output.csv"
SUMMARY_FILEPATH = PARENT_FOLDER + "output/ind_summary.txt"


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
        self.max_time = LONG_MAX_TIME if max_time is None else max_time
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
                max_lines=1,
                max_time=SHORT_MAX_TIME,
            )
        ],
        "confirmbutton": [
            Test(
                "Delete the item",
                lambda logs: eval.ordered(
                    logs, [eval.exact_match(component="click/confirmbutton")]
                ),
                max_lines=1,
                max_time=SHORT_MAX_TIME,
            )
        ],
        "iconbutton": [
            Test(
                "Delete the item",
                lambda logs: eval.ordered(
                    logs, [eval.exact_match(component="click/iconbutton")]
                ),
                max_lines=1,
                max_time=SHORT_MAX_TIME,
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
                max_lines=1,
                max_time=SHORT_MAX_TIME,
            )
        ],
        "slider": [
            Test(
                "Adjust the volume to be the maximum",
                lambda logs: eval.ordered(
                    logs, [eval.exact_match("click/slider", "100")]
                ),
                name="max",
                max_lines=1,
                max_time=SHORT_MAX_TIME,
            ),
            Test(
                "Adjust the volume to be the minimum",
                lambda logs: eval.ordered(
                    logs, [eval.exact_match("click/slider", "0")]
                ),
                name="min",
                max_lines=1,
                max_time=SHORT_MAX_TIME,
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
                max_lines=1,
                max_time=SHORT_MAX_TIME,
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
                max_lines=1,
                max_time=SHORT_MAX_TIME,
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
                max_lines=1,
                max_time=SHORT_MAX_TIME,
            ),
        ],
        "switch": [
            Test(
                "Turn on do not disturb",
                lambda logs: eval.ordered(
                    logs, [eval.exact_match(component="click/switch", newValue="true")]
                ),
                "on-from-off",
                max_lines=1,
                max_time=SHORT_MAX_TIME,
            ),
            Test(
                "Turn off do not disturb",
                lambda logs: eval.no_logs(logs),
                "off-from-off",
                max_lines=1,
                max_time=SHORT_MAX_TIME,
            ),
        ],
        "dropdownmenu": [
            Test(
                "Open the menu",
                lambda logs: eval.ordered(
                    logs, [eval.exact_match(component="click/iconbutton", label="Menu")]
                ),
                max_lines=1,
                max_time=SHORT_MAX_TIME,
            ),
        ],
        "accordion": [
            Test(
                "Please open the accordion to see more",
                lambda logs: eval.ordered(
                    logs,
                    [eval.exact_match(component="click/accordion", newValue="open")],
                ),
                max_lines=1,
                max_time=SHORT_MAX_TIME,
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
                max_lines=1,
                max_time=SHORT_MAX_TIME,
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
                max_lines=1,
                max_time=SHORT_MAX_TIME,
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
                max_lines=1,
                max_time=SHORT_MAX_TIME,
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
                max_lines=1,
                max_time=SHORT_MAX_TIME,
            ),
        ],
        "checkbox": [
            Test(
                "Please accept the terms and conditions",
                lambda logs: eval.ordered(
                    logs,
                    [eval.exact_match(component="select/checkbox", newValue="true")],
                ),
                max_lines=1,
                max_time=SHORT_MAX_TIME,
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
                max_lines=2,
                max_time=SHORT_MAX_TIME,
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
                max_time=SHORT_MAX_TIME,
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
                max_lines=2,
                name="linearly-select-two",
                max_time=SHORT_MAX_TIME,
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
                max_time=SHORT_MAX_TIME,
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
                max_time=SHORT_MAX_TIME,
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
                max_lines=1,
                max_time=SHORT_MAX_TIME,
            )
        ],
        "findtooltip": [
            Test(
                "Please find what state Aurora City is located in and enter the state into the answer box",
                lambda logs: eval.ordered(
                    logs,
                    [eval.exact_match(component="type/text", newValue="California")],
                ),
                max_lines=1,
                max_time=SHORT_MAX_TIME,
            )
        ],
        "finddialog": [
            Test(
                "Please find when the Prometheus Project was launched and enter the year into the answer box",
                lambda logs: eval.at_least_one(
                    logs, [eval.exact_match(component="type/text", newValue="2036")]
                ),
                max_lines=10,
                max_time=SHORT_MAX_TIME,
            ),
        ],
        "findaccordion": [
            Test(
                "Please find when the AGI Research Lab was founded and enter the year into the answer box",
                lambda logs: eval.at_least_one(
                    logs, [eval.exact_match(component="type/text", newValue="2032")]
                ),
                max_lines=10,
                max_time=SHORT_MAX_TIME,
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
                max_lines=10,
                max_time=LONG_MAX_TIME,
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
                max_lines=1,
                max_time=SHORT_MAX_TIME,
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
                max_lines=10,
                max_time=LONG_MAX_TIME,
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
                max_time=LONG_MAX_TIME,
                submit_eval=lambda log: eval.check_one(
                    log,
                    [
                        eval.exact_match(
                            label='{"birthday":"Sat, 01 Jan 2000 05:00:00 GMT","city":"Cambridge","email":"johndoe@gmail.com","firstName":"John","lastName":"Doe","phoneNumber":"(617) 000-0000","state":"MA","streetAddress":"123 Main St","zipCode":"02138"}'
                        )
                    ],
                ),
                max_lines=20,
            )
        ],
    },
}


## HELPER FUNCTIONS RELYING ON INDIVIDUAL TESTS


def get_specific_test_and_metadata(task: str, test: str, name: str):
    task_dict = ind_tests.get(task)
    if task_dict is None:
        raise Exception(f"ERROR: unable to find task {task}")
        return None

    tests_obj = task_dict.get(test)
    if tests_obj is None:
        raise Exception(f"ERROR: unable to find test {task}/{test}")
        return None

    for test_obj in tests_obj:
        if test_obj.name == name:
            return (test_obj, (task, test))

    raise Exception(f"ERROR: unable to find test {task}/{test}/{name}")
    return None


def get_tests_and_metadata(task: str, test: str) -> TestsAndMetadata | None:
    task_dict = ind_tests.get(task)
    if task_dict is None:
        raise Exception(f"ERROR: unable to find task {task}")
        return None

    test_obj = task_dict.get(test)
    if test_obj is None:
        raise Exception(f"ERROR: unable to find test {task}/{test}")
        return None

    return (test_obj, (task, test))


def get_tests_and_metadatas_from_task(task: str) -> list[TestsAndMetadata] | None:
    task_dict = ind_tests.get(task)
    if task_dict is None:
        raise Exception(f"ERROR: unable to find task {task}")
        return None

    return [get_tests_and_metadata(task, test) for test in task_dict.keys()]


def get_all_tests_and_metadatas() -> list[TestsAndMetadata] | None:
    return flatten(
        [get_tests_and_metadatas_from_task(task) for task in ind_tests.keys()]
    )


def bool_to_pass_fail(b: bool) -> str:
    return "pass" if b else "fail"


def calc_pass_stats(pass_count: int, total_count: int) -> str:
    return f"{pass_count}/{total_count} ({round(pass_count * 100 / (total_count))}%)"


## RUNNING THE EVALUATION


# class PassStats:
#     def __init__(self):
#         self.pass_count = 0
#         self.total_count = 0
#         self.track_process = False
#         self.process_pass_count = 0
#         self.process_total_count = 0


if __name__ == "__main__":
    # Identify the right goals and urls to iterate through
    skip_to_evaluate = False
    tests_and_metadatas = []
    num_times = 1

    for i, arg in enumerate(sys.argv[1:]):
        if arg == "-evalonly":
            skip_to_evaluate = True
            break

        if arg.startswith("-n="):
            num_times = int(arg.split("=")[1])
            continue

        parts = arg.split("/", 1)
        if len(parts) == 1:
            new = get_tests_and_metadatas_from_task(parts[0])
            if new is not None:
                tests_and_metadatas.extend(new)
        elif len(parts) == 2:
            new = get_tests_and_metadata(parts[0], parts[1])
            if new is not None:
                tests_and_metadatas.append(new)

    if len(tests_and_metadatas) == 0:
        new = get_all_tests_and_metadatas()
        if new is not None:
            tests_and_metadatas = new

    if not skip_to_evaluate:
        # Clear the log file
        with open(LOG_FILEPATH, "w") as file:
            pass

        # Run the tests
        for tests, metadata in tests_and_metadatas:
            for test in tests:
                for _ in range(num_times):
                    with open(LOG_FILEPATH, "a") as file:
                        file.write(
                            f"TEST BEGIN: {metadata[0]}/{metadata[1]} {test.name}\n"
                        )

                    existing_lines = 0
                    with open(LOG_FILEPATH, "r") as file:
                        existing_lines = len(file.readlines())
                    run_agent_with_limits(
                        goal=test.goal,
                        url=get_url(LOCALHOST_PORT, *metadata),
                        existing_lines=existing_lines,
                        log_file=LOG_FILEPATH,
                        timeout=test.max_time,
                        addl_lines=test.max_lines,
                    )

                    with open(LOG_FILEPATH, "a") as file:
                        file.write("TEST FINISH\n")

    # Evaluate the log file
    eval_dict = get_evals_dict(LOG_FILEPATH)
    output_csv_rows = [
        [
            "Category",
            "Task",
            "Test",
            "Version",
            "Pass Count",
            "Total Count",
            "Process Pass Count",
            "Process Total Count",
        ]
    ]
    summary_str = ""

    for key, items in eval_dict.items():
        basic_stats = PassStats()
        process_stats = None

        for item in items:
            logs = [Log(log) for log in item["logs"]]
            test, metadata = get_specific_test_and_metadata(*re.split(r"[ /]", key))

            if test.submit_eval is None:
                if test.eval(logs):
                    basic_stats.pass_count += 1
                else:
                    basic_stats.fail_count += 1
            else:
                if process_stats is None:
                    process_stats = PassStats()

                if test.eval(logs):
                    process_stats.pass_count += 1
                else:
                    process_stats.fail_count += 1

                submit_eval_result = (
                    test.submit_eval(Log(item["submit"]))
                    if item["submit"] is not None
                    else False
                )

                if submit_eval_result:
                    basic_stats.pass_count += 1
                else:
                    basic_stats.fail_count += 1

        split_key = key.split("/")
        split_test = split_key[1].split(" ")

        task = split_key[0]
        category = TASK_TO_CATEGORY_MAP[task]
        test = split_test[0]
        version = split_test[1]

        if process_stats is not None:
            summary_str += f"{key}: process: pass {display_pass_stats(process_stats.pass_count, process_stats.fail_count, True)} submit: pass {display_pass_stats(basic_stats.pass_count, basic_stats.fail_count, True)}\n"
            output_csv_rows.append(
                [
                    category,
                    task,
                    test,
                    version,
                    basic_stats.pass_count,
                    basic_stats.fail_count + basic_stats.pass_count,
                    process_stats.pass_count,
                    process_stats.fail_count + process_stats.pass_count,
                ]
            )
        else:
            summary_str += f"{key}: pass {display_pass_stats(basic_stats.pass_count, basic_stats.fail_count, True)}\n"
            output_csv_rows.append(
                [
                    category,
                    task,
                    test,
                    version,
                    basic_stats.pass_count,
                    basic_stats.fail_count + basic_stats.pass_count,
                ]
            )

    with open(OUTPUT_FILEPATH, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(output_csv_rows)

    with open(SUMMARY_FILEPATH, "w") as file:
        file.write(summary_str)
