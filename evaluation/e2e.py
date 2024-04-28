import os
from typing import Literal
import sys
from urllib.parse import urlparse, parse_qs, urlencode, quote
import json

from evaluation.utils import (
    LOCALHOST_PORT,
    TASK_TO_CATEGORY_MAP,
    generate_checkpoints_from_logs,
    run_agent_with_limits,
)
from evaluation.evaluators import Log

# HELPER CONSTANTS AND CLASSES

PARENT_FOLDER = os.path.join(os.path.dirname(__file__), "../")
MAX_AGENT_TIME = 60
LOG_FILEPATH = (
    PARENT_FOLDER + "trajectories/log.txt"
)  # needs to be in sync with environment/app.py
OUTPUT_FILEPATH = PARENT_FOLDER + "output/e2e_output.txt"


class GoldenLog(Log):
    def __init__(self, log: str, untracked_component: str | None = None):
        super().__init__(log)
        self.untracked_component = untracked_component


class Checkpoint:
    def __init__(self, url: str):
        self.url = url


class CheckpointFromLogs(Checkpoint):
    def __init__(self, url: str, logs: list[Log]):
        super().__init__(url)
        self.logs = logs


class GoldenCheckpoint(Checkpoint):
    def __init__(
        self,
        url: str,
        golden_logs: list[GoldenLog],
        name: str,
        orderless_logs: bool = False,
        full_match_verifier_next_checkpoint: str | None = None,
    ):
        super().__init__(url)
        self.golden_logs = golden_logs
        self.name = name
        self.orderless_logs = orderless_logs
        self.full_match_verifier_next_checkpoint = full_match_verifier_next_checkpoint


class EvaluatedGoldenCheckpoint(Checkpoint):
    def __init__(
        self,
        url: str,
        checkpoint_status: Literal["full_match", "partial_match", "missing"],
        correct_golden_logs: list[GoldenLog],
        missing_golden_logs: list[GoldenLog],
        extra_logs_processed: list[Log],
        name: str,
    ):
        super().__init__(url)
        self.checkpoint_status = checkpoint_status
        self.correct_golden_logs = correct_golden_logs
        self.missing_golden_logs = missing_golden_logs
        self.extra_logs_processed = extra_logs_processed
        self.name = name


class e2eTest:
    def __init__(self, path: str, params: dict):
        self.path = path
        self.params = params


class PlaygroundTest:
    def __init__(self, goal: str, checkpoints: list[GoldenCheckpoint], e2e: e2eTest):
        self.goal = goal
        self.checkpoints = checkpoints
        self.e2e = e2e


class IndEvaluatedTest:
    def __init__(
        self,
        checkpoints: list[EvaluatedGoldenCheckpoint],
        correct_logs: list[GoldenLog],
        missing_logs: list[GoldenLog],
        extra_checkpoints_processed: list[CheckpointFromLogs],
        e2e_result: bool | None,
    ):
        self.checkpoints = checkpoints
        self.correct_logs = correct_logs
        self.missing_logs = missing_logs
        self.extra_checkpoints_processed = extra_checkpoints_processed
        self.e2e_result = e2e_result


class EvaluatedTest:
    def __init__(
        self,
        test_name: str,
        ind_evaluated_tests: list[IndEvaluatedTest],
    ):
        self.test_name = test_name
        self.ind_evaluated_tests = ind_evaluated_tests


class CorrectMissingData:
    def __init__(self, correct: int, missing: int):
        self.correct = correct
        self.missing = missing


# TEST LIBRARY

# Uses [...] in URL to specify that during evaluation, that string is a placeholder (logic implemented in "matching_urls()"). These brackets will be removed if running from a particular checkpoint.
PLAYGROUND_TESTS: dict[str, PlaygroundTest] = {
    "order": PlaygroundTest(
        goal="Please order a MacBook Pro M3 chip without additional customizations to be delivered to John Doe at 123 Main Street, Cambridge, MA 02138",
        checkpoints=[
            GoldenCheckpoint(
                url="/playground",
                golden_logs=[
                    GoldenLog(
                        "type/text // Search items",
                    ),
                    GoldenLog("click/iconbutton // Search"),
                ],
                name="search_for_item",
                full_match_verifier_next_checkpoint="/playground/search?query=[]",
            ),
            GoldenCheckpoint(
                "/playground/search?query=[MacBook Pro M3 chip]",
                [
                    GoldenLog(
                        "click/link // 2023 MacBook Pro - M3 chip, 14-inch",
                        "search/appropriate",
                    )
                ],
                "select_item_from_search",
            ),
            GoldenCheckpoint(
                url="/playground/product/1",
                golden_logs=[GoldenLog("click/button // Buy now")],
                name="purchase_item",
                full_match_verifier_next_checkpoint='/playground/checkout?cart={"id":"1","customizations":{"memory":"8GB","storage":"512GB"},"price":1599}',
            ),
            GoldenCheckpoint(
                url='/playground/checkout?cart=[{"id":"1","customizations":{"memory":"8GB","storage":"512GB"},"price":1999}]',
                golden_logs=[
                    GoldenLog("type/text // First name // John", "fill/complex"),
                    GoldenLog("type/text // Last name // Doe", "fill/complex"),
                    GoldenLog(
                        "type/text // Street address // 123 Main Street",
                        "fill/complex",
                    ),
                    GoldenLog("type/text // City // Cambridge", "fill/complex"),
                    GoldenLog("select/select // State // MA", "fill/complex"),
                    GoldenLog("type/text // Zip code // 02138", "fill/complex"),
                    GoldenLog("click/button // Order", "fill/complex"),
                ],
                name="fill_shipping_info",
                orderless_logs=True,
                full_match_verifier_next_checkpoint='/playground/thanks?cart=[]&location={"city":"Cambridge","firstName":"John","lastName":"Doe","state":"MA","streetAddress":"123 Main Street","zipCode":"02138"}',
            ),
        ],
        e2e=e2eTest(
            path="/playground/thanks",
            params={
                "cart": {
                    "customizations": {
                        "memory": "8GB",
                        "storage": "512GB",
                    },
                    "id": "1",
                },
                "location": {
                    "city": "Cambridge",
                    "firstName": "John",
                    "lastName": "Doe",
                    "state": "MA",
                    "streetAddress": "123 Main Street",
                    "zipCode": "02138",
                },
            },
        ),
    ),
    "add_custom_to_cart": PlaygroundTest(
        goal="Please add a Macbook Pro with M3 Pro Chip to the cart with highest-tier customizations.",
        checkpoints=[
            GoldenCheckpoint(
                url="/playground",
                golden_logs=[
                    GoldenLog("type/text // Search items"),
                    GoldenLog("click/iconbutton // Search"),
                ],
                name="search_for_item",
                full_match_verifier_next_checkpoint="/playground/search?query=[]",
            ),
            GoldenCheckpoint(
                url="/playground/search?query=[Macbook Pro M3 Pro Chip]",
                golden_logs=[
                    GoldenLog(
                        "click/link // 2023 MacBook Pro - M3 Pro chip, 14-inch",
                        "search/appropriate",
                    )
                ],
                name="select_item_from_search",
            ),
            GoldenCheckpoint(
                url="/playground/product/2",
                golden_logs=[
                    GoldenLog("click/button // 36GB (+400.00)"),
                    GoldenLog("click/button // 2TB (+600.00)"),
                ],
                name="select_customizations",
                orderless_logs=True,
                full_match_verifier_next_checkpoint='/playground/checkout?cart={"id":"2","customizations":{"memory":"36GB","storage":"2TB"},"price":2999}',
            ),
        ],
        e2e=e2eTest(
            path="/playground/checkout",
            params={
                "cart": {
                    "customizations": {
                        "memory": "36GB",
                        "storage": "2TB",
                    },
                    "id": "2",
                    "price": 2999,
                }
            },
        ),
    ),
}

# EVALUATING THE TRAJECTORIES


def print_evaluated_checkpoints(evaluated_checkpoints: list[EvaluatedGoldenCheckpoint]):
    for evaluated_checkpoint in evaluated_checkpoints:
        print(evaluated_checkpoint.checkpoint_status + " " + evaluated_checkpoint.name)
        if (
            evaluated_checkpoint.checkpoint_status == "partial_match"
            or evaluated_checkpoint.checkpoint_status == "extra_in_logs"
        ):
            print(
                "    CORRECT: "
                + str([str(log) for log in evaluated_checkpoint.correct_golden_logs])
            )
            print(
                "    MISSING: "
                + str([str(log) for log in evaluated_checkpoint.missing_golden_logs])
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


def golden_matches_processed(golden: GoldenLog, processed: Log):
    basic_eq = (
        golden.component == processed.component and golden.label == processed.label
    )
    new_eq = golden.newValue == processed.newValue if golden.newValue else True
    old_eq = golden.oldValue == processed.oldValue if golden.oldValue else True
    return basic_eq and new_eq and old_eq


def matching_urls(golden_url: str, processed_url: str):
    parsed_golden = urlparse(golden_url)
    parsed_processed = urlparse(processed_url)

    same_path = parsed_golden.path == parsed_processed.path
    if same_path:
        golden_qp = parse_qs(parsed_golden.query)
        processed_qp = parse_qs(parsed_processed.query)

        # Account for filler params
        for key in list(golden_qp.keys()):
            if golden_qp[key][0].startswith("[") and golden_qp[key][0].endswith("]"):
                golden_qp[key] = processed_qp[key]

        return golden_qp == processed_qp

    return False


def compare_processed_and_golden_checkpoints(
    golden_checkpoints: list[GoldenCheckpoint],
    processed_checkpoints: list[CheckpointFromLogs],
):
    """Compares the golden checkpoints with the processed checkpoints and returns the evaluated golden checkpoints as well as any extra checkpoints in processed."""
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
                        correct_golden_logs=[],
                        missing_golden_logs=golden_checkpoints[
                            golden_index
                        ].golden_logs,
                        extra_logs_processed=[],
                        name=golden_checkpoints[golden_index].name,
                    )
                )
            break

        # if both golden index and processed index are in bounds, we compare the urls. if match...
        if matching_urls(
            golden_checkpoints[golden_index].url.strip(),
            processed_checkpoints[processed_index].url.strip(),
        ):
            # identify the correct, missing, incorrect, extra logs
            correct_golden_logs = []
            missing_golden_logs = []
            extra_logs_processed = []

            golden_logs = golden_checkpoints[golden_index].golden_logs
            processed_logs = processed_checkpoints[processed_index].logs

            # basic parsing of logs if order doesn't matter
            if golden_checkpoints[golden_index].orderless_logs:
                for golden in golden_logs:
                    if any(
                        golden_matches_processed(golden, processed)
                        for processed in processed_logs
                    ):
                        correct_golden_logs.append(golden)
                    else:
                        missing_golden_logs.append(golden)

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
                            missing_golden_logs.append(golden_logs[golden_logs_index])
                        break

                    # if both are in bounds, we compare the logs
                    if golden_matches_processed(
                        golden_logs[golden_logs_index],
                        processed_logs[processed_logs_index],
                    ):
                        correct_golden_logs.append(golden_logs[golden_logs_index])
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
                            missing_golden_logs.append(golden_logs[golden_logs_index])
                            golden_logs_index += 1

            full_match = False
            if (
                golden_checkpoints[golden_index].full_match_verifier_next_checkpoint
                is not None
            ):
                next_url = (
                    ""
                    if processed_index + 1 >= len(processed_checkpoints)
                    else processed_checkpoints[processed_index + 1].url
                )
                full_match = matching_urls(
                    golden_checkpoints[
                        golden_index
                    ].full_match_verifier_next_checkpoint,
                    next_url,
                )
            else:
                full_match = (
                    len(correct_golden_logs) == len(golden_logs) == len(processed_logs)
                )

            evaluated_checkpoints.append(
                EvaluatedGoldenCheckpoint(
                    url=golden_checkpoints[golden_index].url,
                    checkpoint_status="full_match" if full_match else "partial_match",
                    correct_golden_logs=correct_golden_logs,
                    missing_golden_logs=missing_golden_logs,
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
            if any(
                matching_urls(golden_checkpoints[golden_index].url, future)
                for future in future_processed_checkpoint_urls
            ):
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
                        correct_golden_logs=[],
                        missing_golden_logs=golden_checkpoints[
                            golden_index
                        ].golden_logs,
                        extra_logs_processed=[],
                        name=golden_checkpoints[golden_index].name,
                    )
                )
                golden_index += 1

    return evaluated_checkpoints, extra_checkpoints_processed


def evaluate_e2e(e2e: e2eTest, log: CheckpointFromLogs) -> bool:
    parsed_url = urlparse(log.url)
    if parsed_url.path == e2e.path:
        parsed_query_raw = parse_qs(parsed_url.query)

        parsed_query = {}
        for key, value in parsed_query_raw.items():
            parsed_query[key] = json.loads(value[0])

        if parsed_query == e2e.params:
            return True

    return False


def evaluate_logs():
    """Pulls the logs from LOG_FILEPATH and then evaluates them against the golden checkpoints. Returns a list of EvaluatedTest objects."""
    evaluated_tests = []
    logs = generate_checkpoints_from_logs(LOG_FILEPATH)
    for test, items in logs.items():
        ind_evaluated_tests = []

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

        for checkpoints in items:
            if curr_test_name in PLAYGROUND_TESTS:
                processed_checkpoints: list[CheckpointFromLogs] = []
                for checkpoint in checkpoints:
                    processed_checkpoints.append(
                        CheckpointFromLogs(
                            checkpoint["url"],
                            [Log(log) for log in checkpoint["logs"]],
                        )
                    )

                golden_checkpoints = PLAYGROUND_TESTS[curr_test_name].checkpoints
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

                evaluated_checkpoints, extra_checkpoints = (
                    compare_processed_and_golden_checkpoints(
                        golden_checkpoints, processed_checkpoints
                    )
                )

                all_correct_logs: list[GoldenLog] = []
                all_missing_logs: list[GoldenLog] = []

                for evaluated_checkpoint in evaluated_checkpoints:
                    all_correct_logs.extend(evaluated_checkpoint.correct_golden_logs)
                    all_missing_logs.extend(evaluated_checkpoint.missing_golden_logs)

                # print_evaluated_checkpoints(evaluated_logs)
                # print_extra_checkpoints(extra_logs)

                e2e_result = None
                if not curr_test_checkpoint_only:
                    e2e_result = any(
                        evaluate_e2e(PLAYGROUND_TESTS[curr_test_name].e2e, extra)
                        for extra in extra_checkpoints
                    )

                ind_evaluated_tests.append(
                    IndEvaluatedTest(
                        checkpoints=evaluated_checkpoints,
                        correct_logs=all_correct_logs,
                        missing_logs=all_missing_logs,
                        extra_checkpoints_processed=extra_checkpoints,
                        e2e_result=e2e_result,
                    )
                )

        evaluated_tests.append(EvaluatedTest(curr_test_name, ind_evaluated_tests))
    return evaluated_tests


# GENERATING SUMMARY AND EXPORTING RESULTS


def get_summary_line(text: str, correct: int, missing: int):
    return f"{text}: {correct}/{correct + missing} ({round(correct * 100 / (correct + missing))}%)\n"


def update_summary(summary: dict, components: list, type: str):
    """Given the summary dictionary, it updates according to the list of components (from logs) and type of list (either correct or missing)"""
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


class CheckpointMatchStats:
    def __init__(self):
        self.full_match = 0
        self.partial_match = 0
        self.missing = 0

    def __str__(self):
        total = self.full_match + self.partial_match + self.missing

        return f"full_match ({self.full_match}/{total}), partial_match ({self.partial_match}/{total}), missing ({self.missing}/{total})"


def get_pass_stats(pass_count: int, fail_count: int):
    return f"{pass_count}/{pass_count + fail_count} ({round(pass_count * 100 / (pass_count + fail_count))}%)"


def export_results(evaluated_tests: list[EvaluatedTest]):
    """Exports the results of the evaluated tests into OUTPUT_FILEPATH"""
    with open(OUTPUT_FILEPATH, "w") as file:
        total_correct: list[GoldenLog] = []
        total_missing: list[GoldenLog] = []

        for evaluated_test in evaluated_tests:
            evaluated_e2e = False
            e2e_pass = 0
            e2e_fail = 0

            extra_checkpoints_str = ""

            evaluated_checkpoints_to_print: dict[str, CheckpointMatchStats] = {}

            for index, ind_evaluated_test in enumerate(
                evaluated_test.ind_evaluated_tests
            ):
                if ind_evaluated_test.e2e_result is not None:
                    evaluated_e2e = True
                    if ind_evaluated_test.e2e_result:
                        e2e_pass += 1
                    else:
                        e2e_fail += 1

                for evaluated_checkpoint in ind_evaluated_test.checkpoints:
                    if evaluated_checkpoint.name not in evaluated_checkpoints_to_print:
                        evaluated_checkpoints_to_print[evaluated_checkpoint.name] = (
                            CheckpointMatchStats()
                        )

                    if evaluated_checkpoint.checkpoint_status == "full_match":
                        evaluated_checkpoints_to_print[
                            evaluated_checkpoint.name
                        ].full_match += 1
                    elif evaluated_checkpoint.checkpoint_status == "partial_match":
                        evaluated_checkpoints_to_print[
                            evaluated_checkpoint.name
                        ].partial_match += 1
                    elif evaluated_checkpoint.checkpoint_status == "missing":
                        evaluated_checkpoints_to_print[
                            evaluated_checkpoint.name
                        ].missing += 1

                    total_correct.extend(evaluated_checkpoint.correct_golden_logs)
                    total_missing.extend(evaluated_checkpoint.missing_golden_logs)

                for extra_checkpoint in ind_evaluated_test.extra_checkpoints_processed:
                    extra_checkpoints_str += (
                        "    EXTRA (" + str(index) + "): " + extra_checkpoint.url + "\n"
                    )

            file.write(
                evaluated_test.test_name
                + (
                    ""
                    if not evaluated_e2e
                    else (" pass " + get_pass_stats(e2e_pass, e2e_fail))
                )
                + "\n"
            )

            for checkpoint_name, stats in evaluated_checkpoints_to_print.items():
                file.write("    " + checkpoint_name + " " + str(stats) + "\n")

            file.write(extra_checkpoints_str)

        file.write("\n\n")

        total_correct_components = []
        total_missing_components = []
        for correct in total_correct:
            total_correct_components.append(correct.component)
            if correct.untracked_component is not None:
                total_correct_components.append(correct.untracked_component)
        for missing in total_missing:
            total_missing_components.append(missing.component)
            if missing.untracked_component is not None:
                total_missing_components.append(missing.untracked_component)

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


# MISC HELPERS


def remove_placeholders_from_url_query_params(url: str, encode_url: bool = False):
    parsed_url = urlparse(url)
    parsed_query_raw = parse_qs(parsed_url.query)

    parsed_query = {}
    for key, value in parsed_query_raw.items():
        if value[0].startswith("[") and value[0].endswith("]"):
            parsed_query[key] = value[0][1:-1]

    if len(parsed_query) == 0:
        return parsed_url.path
    else:
        query_string = "&".join(
            [f"{key}={value}" for key, value in parsed_query.items()]
        )
        return parsed_url.path + "?" + query_string


def encode_url_query_params(url: str):
    return quote(url, safe="/=?&")


# E2E test scaffolding


if __name__ == "__main__":
    tests = []
    skip_to_evaluate = False
    checkpoint_only = False
    num_times = 1

    if len(sys.argv) > 1:
        for i, arg in enumerate(sys.argv[1:]):
            if arg == "-evalonly":
                skip_to_evaluate = True
                break

            if arg == "-checkpointonly":
                checkpoint_only = True
                continue

            if arg.startswith("-n="):
                num_times = int(arg.split("=")[1])
                continue

            parts = arg.split("/", 1)

            if parts[0] in PLAYGROUND_TESTS:
                if len(parts) == 1:
                    tests.append(
                        {
                            "test": parts[0],
                            "starting_checkpoint": None,
                            "path": "/playground",
                        }
                    )
                elif len(parts) == 2:
                    for checkpoint in PLAYGROUND_TESTS[parts[0]].checkpoints:
                        if parts[1] == checkpoint.name:
                            tests.append(
                                {
                                    "test": parts[0],
                                    "starting_checkpoint": parts[1],
                                    "path": remove_placeholders_from_url_query_params(
                                        checkpoint.url
                                    ),
                                }
                            )
                            break
            else:
                print(f"ERROR: unable to find test {parts[0]}")
    else:
        tests = [
            {
                "test": key,
                "starting_checkpoint": None,
                "path": "/playground",
            }
            for key in PLAYGROUND_TESTS.keys()
        ]

    # Run the agent
    if not skip_to_evaluate:
        with open(LOG_FILEPATH, "w") as file:
            pass

        for test in tests:
            for _ in range(num_times):
                with open(LOG_FILEPATH, "a") as file:
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
                with open(LOG_FILEPATH, "r") as file:
                    existing_lines = len(file.readlines())

                run_agent_with_limits(
                    goal=PLAYGROUND_TESTS[test["test"]].goal,
                    url=f"localhost:{LOCALHOST_PORT}"
                    + encode_url_query_params(test["path"]),
                    existing_lines=existing_lines,
                    log_file=LOG_FILEPATH,
                    timeout=MAX_AGENT_TIME,
                    addl_lines=100,
                    custom_log_break=(
                        (
                            lambda lines: len(
                                [
                                    line
                                    for line in lines[existing_lines:]
                                    if "NAVIGATE" in line
                                ]
                            )
                            >= 1
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

                with open(LOG_FILEPATH, "a") as file:
                    file.write("TEST FINISH\n")

    # Evaluate the logs that exist
    evaluated_tests = evaluate_logs()
    export_results(evaluated_tests)
