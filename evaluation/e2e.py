import os
from typing import Literal
import sys

from evaluation.utils import (
    LOCALHOST_PORT,
    TASK_TO_CATEGORY_MAP,
    generate_checkpoints_from_logs,
    run_agent_with_limits,
)
from evaluation.evaluators import Log, golden_matches_processed

PARENT_FOLDER = os.path.join(os.path.dirname(__file__), "../")
MAX_AGENT_TIME = 60


class Checkpoint:
    def __init__(self, url: str):
        self.url = url


class CheckpointFromLogs(Checkpoint):
    def __init__(self, url: str, logs: list[Log]):
        super().__init__(url)
        self.logs = logs


class GoldenCheckpoint(Checkpoint):
    def __init__(
        self, url: str, logs: list[Log], name: str, orderless_logs: bool = False
    ):
        super().__init__(url)
        self.logs = logs
        self.name = name
        self.orderless_logs = orderless_logs


class PlaygroundTest:
    def __init__(self, goal: str, checkpoints: list[GoldenCheckpoint]):
        self.goal = goal
        self.checkpoints = checkpoints


def logs_list_str_to_list_logs(logs: list[str]) -> list[Log]:
    return [Log(log) for log in logs]


playground_tests: dict[str, PlaygroundTest] = {
    "order": PlaygroundTest(
        goal="Please order a MacBook Pro M3 chip without additional customizations to be delivered to John Doe at 123 Main Street, Cambridge, MA 02138",
        checkpoints=[
            GoldenCheckpoint(
                "/playground",
                logs_list_str_to_list_logs(
                    [
                        "type/text // Search items // MacBook Pro M3 chip",
                        "click/iconbutton // Search",
                    ]
                ),
                "home",
            ),
            GoldenCheckpoint(
                "/playground/search?query=MacBook Pro M3 chip",
                logs_list_str_to_list_logs(
                    ["click/link // 2023 MacBook Pro - M3 chip, 14-inch"]
                ),
                "search",
            ),
            GoldenCheckpoint(
                "/playground/product/1",
                logs_list_str_to_list_logs(["click/button // Buy now"]),
                "item_page",
            ),
            GoldenCheckpoint(
                "/playground/checkout",
                logs_list_str_to_list_logs(
                    [
                        "type/text // First name // John",
                        "type/text // Last name // Doe",
                        "type/text // Street address // 123 Main Street",
                        "type/text // City // Cambridge",
                        "select/select // State // MA",
                        "type/text // Zip code // 02138",
                        "click/button // Order",
                    ]
                ),
                "buy",
                orderless_logs=True,
            ),
            GoldenCheckpoint(
                '/playground/thanks?submitted={"city":"Cambridge","firstName":"John","lastName":"Doe","state":"MA","streetAddress":"123 Main Street","zipCode":"02138"}',
                [],
                "ordered",
            ),
        ],
    )
}


class EvaluatedGoldenCheckpoint:
    def __init__(
        self,
        url: str,
        checkpoint_status: Literal["full_match", "partial_match", "missing"],
        correct_logs: list[Log],
        missing_logs: list[Log],
        extra_logs_processed: list[Log],
        name: str,
    ):
        self.url = url
        self.checkpoint_status = checkpoint_status
        self.correct_logs = correct_logs
        self.missing_logs = missing_logs
        self.extra_logs_processed = extra_logs_processed
        self.name = name


class EvaluatedTest:
    def __init__(
        self,
        test_name: str,
        checkpoints: list[EvaluatedGoldenCheckpoint],
        correct_logs: list[str],
        missing_logs: list[str],
        extra_checkpoints_processed: list[CheckpointFromLogs],
    ):
        self.test_name = test_name
        self.checkpoints = checkpoints
        self.correct_logs = correct_logs
        self.missing_logs = missing_logs
        self.extra_checkpoints_processed = extra_checkpoints_processed


def compare_processed_and_golden_checkpoints(
    golden_checkpoints: list[GoldenCheckpoint],
    processed_checkpoints: list[CheckpointFromLogs],
):
    golden_index = 0
    processed_index = 0

    evaluated_checkpoints: list[EvaluatedGoldenCheckpoint] = []
    extra_checkpoints_processed: list[CheckpointFromLogs] = []

    while True:
        # if both golden index and processed index are out of bounds, we are done
        if golden_index >= len(golden_checkpoints) and processed_index >= len(
            processed_checkpoints
        ):
            break

        # if golden index is out of bounds, but processed index is not, then we mark rest of processed_checkpoints as extra
        if golden_index >= len(golden_checkpoints):
            for processed_index in range(processed_index, len(processed_checkpoints)):
                extra_checkpoints_processed.append(
                    processed_checkpoints[processed_index]
                )
            break

        # if processed index is out of bounds, but golden index is not, then we mark rest of golden_checkpoints as missing
        if processed_index >= len(processed_checkpoints):
            for golden_index in range(golden_index, len(golden_checkpoints)):
                evaluated_checkpoints.append(
                    EvaluatedGoldenCheckpoint(
                        url=golden_checkpoints[golden_index].url,
                        checkpoint_status="missing",
                        correct_logs=[],
                        missing_logs=golden_checkpoints[golden_index].logs,
                        extra_logs_processed=[],
                        name=golden_checkpoints[golden_index].name,
                    )
                )
            break

        # if both golden index and processed index are in bounds, we compare the urls. if match...
        if (
            golden_checkpoints[golden_index].url.strip()
            == processed_checkpoints[processed_index].url.strip()
        ):
            # identify the correct, missing, incorrect, extra logs
            correct_logs = []
            missing_logs = []
            extra_logs_processed = []

            golden_logs = golden_checkpoints[golden_index].logs
            processed_logs = processed_checkpoints[processed_index].logs

            # basic parsing of logs if order doesn't matter
            if golden_checkpoints[golden_index].orderless_logs:
                for golden in golden_logs:
                    if any(
                        golden_matches_processed(golden, processed)
                        for processed in processed_logs
                    ):
                        correct_logs.append(golden)
                    else:
                        missing_logs.append(golden)

                for processed in processed_logs:
                    if not any(
                        golden_matches_processed(golden, processed)
                        for golden in golden_logs
                    ):
                        extra_logs_processed.append(processed)

            # complex parsing of logs if order matches
            else:
                golden_logs_index = 0
                processed_logs_index = 0

                while True:
                    # if both log indexes are out of bounds, we are done
                    if golden_logs_index >= len(
                        golden_logs
                    ) and processed_logs_index >= len(processed_logs):
                        break

                    # if golden_logs out of bound but not procesed_logs, then mark rest of processed_logs as extra
                    if golden_logs_index >= len(golden_logs):
                        for processed_logs_index in range(
                            processed_logs_index, len(processed_logs)
                        ):
                            extra_logs_processed.append(
                                processed_logs[processed_logs_index]
                            )
                        break

                    # if processed_logs out of bound but not golden_logs, then mark rest of golden_logs as missing
                    if processed_logs_index >= len(processed_logs):
                        for golden_logs_index in range(
                            golden_logs_index, len(golden_logs)
                        ):
                            missing_logs.append(golden_logs[golden_logs_index])
                        break

                    # if both are in bounds, we compare the logs
                    if golden_matches_processed(
                        golden_logs[golden_logs_index],
                        processed_logs[processed_logs_index],
                    ):
                        correct_logs.append(golden_logs[golden_logs_index])
                        golden_logs_index += 1
                        processed_logs_index += 1
                    else:
                        future_processed_logs = [
                            processed_logs[i]
                            for i in range(processed_logs_index, len(processed_logs))
                        ]

                        if any(
                            [
                                golden_matches_processed(
                                    golden_logs[golden_logs_index], log
                                )
                                for log in future_processed_logs
                            ]
                        ):
                            indices = [
                                index
                                for index, log in enumerate(future_processed_logs)
                                if golden_matches_processed(
                                    golden_logs[golden_logs_index], log
                                )
                            ]
                            i_index = indices[0]

                            for i in range(
                                processed_logs_index, processed_logs_index + i_index
                            ):
                                extra_logs_processed.append(processed_logs[i])
                            processed_logs_index += i_index
                        else:
                            missing_logs.append(golden_logs[golden_logs_index])
                            golden_logs_index += 1

            full_match = len(correct_logs) == len(golden_logs) == len(processed_logs)

            evaluated_checkpoints.append(
                EvaluatedGoldenCheckpoint(
                    url=golden_checkpoints[golden_index].url,
                    checkpoint_status="full_match" if full_match else "partial_match",
                    correct_logs=correct_logs,
                    missing_logs=missing_logs,
                    extra_logs_processed=extra_logs_processed,
                    name=golden_checkpoints[golden_index].name,
                )
            )

            golden_index += 1
            processed_index += 1

        # if don't match the current golden_checkpoint
        else:
            future_processed_checkpoint_urls = [
                processed_checkpoints[i].url
                for i in range(processed_index, len(processed_checkpoints))
            ]

            # if golden_checkpoint exists farther down the processed logs
            if golden_checkpoints[golden_index].url in future_processed_checkpoint_urls:
                i_index = future_processed_checkpoint_urls.index(
                    golden_checkpoints[golden_index].url
                )
                for i in range(processed_index, processed_index + i_index):
                    extra_checkpoints_processed.append(processed_checkpoints[i])
                processed_index += i_index

            # if we look ahead and doesn't exist later, then we mark current golden as missing
            else:
                evaluated_checkpoints.append(
                    EvaluatedGoldenCheckpoint(
                        url=golden_checkpoints[golden_index].url,
                        checkpoint_status="missing",
                        correct_logs=[],
                        missing_logs=golden_checkpoints[golden_index].logs,
                        extra_logs_processed=[],
                        name=golden_checkpoints[golden_index].name,
                    )
                )
                golden_index += 1

    return evaluated_checkpoints, extra_checkpoints_processed


def print_evaluated_checkpoints(evaluated_checkpoints: list[EvaluatedGoldenCheckpoint]):
    for evaluated_checkpoint in evaluated_checkpoints:
        print(evaluated_checkpoint.checkpoint_status + " " + evaluated_checkpoint.name)
        if (
            evaluated_checkpoint.checkpoint_status == "partial_match"
            or evaluated_checkpoint.checkpoint_status == "extra_in_logs"
        ):
            print(
                "    CORRECT: "
                + str([str(log) for log in evaluated_checkpoint.correct_logs])
            )
            print(
                "    MISSING: "
                + str([str(log) for log in evaluated_checkpoint.missing_logs])
            )
            print(
                "    EXTRA: "
                + str([str(log) for log in evaluated_checkpoint.extra_logs_processed])
            )
        print()


def print_extra_checkpoints(extra_checkpoints: list[CheckpointFromLogs]):
    for extra_checkpoint in extra_checkpoints:
        print("EXTRA: " + extra_checkpoint.url)
        print("    LOGS: " + str([str(log) for log in extra_checkpoint.logs]))
        print()


def evaluate_logs():
    evaluated_tests = []
    logs = generate_checkpoints_from_logs(PARENT_FOLDER + "trajectories/log.txt")
    for test, checkpoints in logs.items():
        test_and_checkpoint = test.split("/")[1].strip().split(" ")

        curr_test_name = test_and_checkpoint[0]
        curr_starting_checkpoint = (
            test_and_checkpoint[1] if len(test_and_checkpoint) > 1 else None
        )
        curr_test_checkpoint_only = (
            test_and_checkpoint[2] == "-checkpointonly"
            if len(test_and_checkpoint) > 2
            else False
        )

        if curr_test_name in playground_tests:
            processed_checkpoints: list[CheckpointFromLogs] = []
            for checkpoint in checkpoints:
                processed_checkpoints.append(
                    CheckpointFromLogs(
                        checkpoint["url"],
                        logs_list_str_to_list_logs(checkpoint["logs"]),
                    )
                )

            golden_checkpoints = playground_tests[curr_test_name].checkpoints
            if curr_starting_checkpoint is not None:
                indices = [
                    index
                    for index, checkpoint in enumerate(golden_checkpoints)
                    if checkpoint.name == curr_starting_checkpoint
                ]
                golden_checkpoints = golden_checkpoints[indices[0] :]

            if curr_test_checkpoint_only:
                golden_checkpoints = golden_checkpoints[:1]
                processed_checkpoints = processed_checkpoints[:1]

            evaluated, extra = compare_processed_and_golden_checkpoints(
                golden_checkpoints, processed_checkpoints
            )

            all_correct_logs = []
            all_missing_logs = []

            for evaluated_checkpoint in evaluated:
                all_correct_logs.extend(evaluated_checkpoint.correct_logs)
                all_missing_logs.extend(evaluated_checkpoint.missing_logs)

            print_evaluated_checkpoints(evaluated)
            print_extra_checkpoints(extra)

            evaluated_tests.append(
                EvaluatedTest(
                    test_name=test,
                    checkpoints=evaluated,
                    correct_logs=all_correct_logs,
                    missing_logs=all_missing_logs,
                    extra_checkpoints_processed=extra,
                )
            )
    return evaluated_tests


class CorrectMissingData:
    def __init__(self, correct: int, missing: int):
        self.correct = correct
        self.missing = missing


def get_summary_line(text: str, correct: int, missing: int):
    return f"{text}: {correct}/{correct + missing} ({round(correct * 100 / (correct + missing))}%)\n"


def update_summary(summary: dict, components: list, type: str):
    for component in components:
        task = component.split("/")[0].strip()
        category = TASK_TO_CATEGORY_MAP[task]
        test = component.split("/")[1].strip()

        if category not in summary:
            summary[category] = {}

        if task not in summary[category]:
            summary[category][task] = {}

        if test not in summary[category][task]:
            summary[category][task][test] = CorrectMissingData(0, 0)

        if type == "correct":
            summary[category][task][test].correct += 1
        elif type == "missing":
            summary[category][task][test].missing += 1


def export_results(evaluated_tests: list[EvaluatedTest]):
    with open(PARENT_FOLDER + "output/output.txt", "w") as file:
        total_correct: list[Log] = []
        total_missing: list[Log] = []

        for evaluated_test in evaluated_tests:
            file.write(evaluated_test.test_name + "\n")
            for evaluated_checkpoint in evaluated_test.checkpoints:
                if evaluated_checkpoint.checkpoint_status != "extra_in_logs":
                    file.write(
                        "    "
                        + evaluated_checkpoint.name
                        + " "
                        + evaluated_checkpoint.checkpoint_status
                        + "\n"
                    )

                    total_correct.extend(evaluated_checkpoint.correct_logs)
                    total_missing.extend(evaluated_checkpoint.missing_logs)

        file.write("\n\n")

        total_correct_components = [correct.component for correct in total_correct]
        total_missing_components = [missing.component for missing in total_missing]

        summary: dict[str, dict[str, dict[str, CorrectMissingData]]] = {}

        update_summary(summary, total_correct_components, "correct")
        update_summary(summary, total_missing_components, "missing")

        for category in summary:
            output = []

            category_correct = 0
            category_missing = 0

            for task in summary[category]:
                task_correct = 0
                task_missing = 0

                for test in summary[category][task]:
                    test_correct = summary[category][task][test].correct
                    test_missing = summary[category][task][test].missing

                    output.append(
                        get_summary_line("        " + test, test_correct, test_missing)
                    )

                    task_correct += test_correct
                    task_missing += test_missing

                output.append(
                    get_summary_line("    " + task, task_correct, task_missing)
                )

                category_correct += task_correct
                category_missing += task_missing

            output.append(
                get_summary_line(category, category_correct, category_missing)
            )

            output.reverse()
            file.write("".join(output))


if __name__ == "__main__":
    tests = []
    skip_to_evaluate = False
    checkpoint_only = False

    if len(sys.argv) > 1:
        for i, arg in enumerate(sys.argv[1:]):
            if arg == "-evalonly":
                skip_to_evaluate = True
                break

            if arg == "-checkpointonly":
                checkpoint_only = True
                continue

            parts = arg.split("/", 1)

            if parts[0] in playground_tests:
                if len(parts) == 1:
                    tests.append(
                        {
                            "test": parts[0],
                            "starting_checkpoint": None,
                            "path": "/playground",
                        }
                    )
                elif len(parts) == 2:
                    for checkpoint in playground_tests[parts[0]].checkpoints:
                        if parts[1] == checkpoint.name:
                            tests.append(
                                {
                                    "test": parts[0],
                                    "starting_checkpoint": parts[1],
                                    "path": checkpoint.url,
                                }
                            )
                            break
            else:
                print(f"ERROR: unable to find test {parts[0]}")

    if not skip_to_evaluate:
        with open(PARENT_FOLDER + "trajectories/log.txt", "w") as file:
            pass

        for test in tests:
            with open(PARENT_FOLDER + "trajectories/log.txt", "a") as file:
                starting_checkpoint_str = (
                    test["starting_checkpoint"]
                    if test["starting_checkpoint"] is not None
                    else ""
                )
                if checkpoint_only:
                    starting_checkpoint_str += " -checkpointonly"

                file.write(
                    f"TEST BEGIN: playground/{test['test']} {starting_checkpoint_str}\n"
                )
                file.write(f"NAVIGATE // {test['path']}\n")

            existing_lines = 0
            with open(PARENT_FOLDER + "trajectories/log.txt", "r") as file:
                existing_lines = len(file.readlines())

            run_agent_with_limits(
                goal=playground_tests[test["test"]].goal,
                url=f"localhost:{LOCALHOST_PORT}" + test["path"],
                existing_lines=existing_lines,
                log_file=PARENT_FOLDER + "trajectories/log.txt",
                timeout=MAX_AGENT_TIME,
                addl_lines=100,
                custom_log_break=(
                    (
                        lambda lines: len(
                            [line for line in lines if "NAVIGATE" in line]
                        )
                        >= 2
                    )
                    if (test["starting_checkpoint"] is not None and checkpoint_only)
                    else None
                ),
                custom_log_break_str=(
                    "only running for single checkpoint"
                    if (test["starting_checkpoint"] is not None and checkpoint_only)
                    else None
                ),
            )

            with open(PARENT_FOLDER + "trajectories/log.txt", "a") as file:
                file.write("TEST FINISH\n")

    # evaluate the logs that exist
    evaluated_tests = evaluate_logs()
    export_results(evaluated_tests)
