import os
from typing import Literal

from evaluation.utils import generate_checkpoints_from_logs
from evaluation.evaluators import Log, golden_matches_processed

PARENT_FOLDER = os.path.join(os.path.dirname(__file__), "../")


class PlaygroundCheckpoint:
    def __init__(self, url: str, logs: list[Log], name: str | None = None):
        self.url = url
        self.logs = logs
        self.name = name


class PlaygroundTest:
    def __init__(self, goal: str, checkpoints: list[PlaygroundCheckpoint]):
        self.goal = goal
        self.checkpoints = checkpoints


def logs_list_str_to_list_logs(logs: list[str]) -> list[Log]:
    return [Log(log) for log in logs]


playground_tests: dict[str, PlaygroundTest] = {
    "order": PlaygroundTest(
        goal="Please order a laptop to be delivered to John Doe at 123 Main Street, Cambridge, MA 02138",
        checkpoints=[
            PlaygroundCheckpoint(
                "/playground",
                logs_list_str_to_list_logs(
                    [
                        "type/text // Search items // laptop",
                        "click/iconbutton // Search",
                    ]
                ),
                "home",
            ),
            PlaygroundCheckpoint(
                "/playground/search?query=laptop",
                logs_list_str_to_list_logs(
                    [
                        'click/link // OTVOC Laptop 16 inch Windows 11 Pro, VocBook 16, Intel 12th Gen N95, Up to 3.4GHz, 16GB DDR5 RAM, 1TB PCIE NVME SSD, 16" FHD IPS 1920x1200, 2.0MP, 2.4G+5G WiFi, BT 5.0, HDMI, RJ45, Type C, Gray'
                    ]
                ),
                "search",
            ),
            PlaygroundCheckpoint(
                "/playground/product/2",
                logs_list_str_to_list_logs(["click/button // Buy now"]),
                "item_page",
            ),
            PlaygroundCheckpoint(
                "/playground/checkout",
                logs_list_str_to_list_logs(
                    [
                        "type/text // First name // John",
                        "type/text // Last name // Doe",
                        "type/text // Street address // 123 Main St",
                        "type/text // City // Cambridge",
                        "select/select // State // MA",
                        "type/text // Zip code // 02138",
                        "click/button // Order",
                    ]
                ),
                "buy",
            ),
            PlaygroundCheckpoint(
                '/playground/thanks?submitted={"city":"Cambridge","firstName":"John","lastName":"Doe","state":"MA","streetAddress":"123 Main St","zipCode":"02138"}',
                [],
                "ordered",
            ),
        ],
    )
}


class EvaluatedCheckpoint:
    def __init__(
        self,
        url: str,
        checkpoint_status: Literal[
            "full_match", "partial_match", "missing", "extra_in_logs"
        ],
        correct_logs: list[str],
        missing_logs: list[str],
        extra_logs_processed: list[str],
        name: str | None = None,
    ):
        self.url = url
        self.checkpoint_status = checkpoint_status
        self.correct_logs = correct_logs
        self.missing_logs = missing_logs
        self.extra_logs_processed = extra_logs_processed
        self.name = name


def compare_processed_and_golden_checkpoints(
    golden_checkpoints: list[PlaygroundCheckpoint],
    processed_checkpoints: list[PlaygroundCheckpoint],
):
    golden_index = 0
    processed_index = 0

    evaluated_checkpoints: list[EvaluatedCheckpoint] = []

    while True:
        # if both golden index and processed index are out of bounds, we are done
        if golden_index >= len(golden_checkpoints) and processed_index >= len(
            processed_checkpoints
        ):
            break

        # if golden index is out of bounds, but processed index is not, then we mark rest of processed_checkpoints as extra
        if golden_index >= len(golden_checkpoints):
            for processed_index in range(processed_index, len(processed_checkpoints)):
                evaluated_checkpoints.append(
                    EvaluatedCheckpoint(
                        url=processed_checkpoints[processed_index].url,
                        checkpoint_status="extra_in_logs",
                        correct_logs=[],
                        missing_logs=[],
                        extra_logs_processed=processed_checkpoints[
                            processed_index
                        ].logs,
                    )
                )
            break

        # if processed index is out of bounds, but golden index is not, then we mark rest of golden_checkpoints as missing
        if processed_index >= len(processed_checkpoints):
            for golden_index in range(golden_index, len(golden_checkpoints)):
                evaluated_checkpoints.append(
                    EvaluatedCheckpoint(
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
                    for golden_logs_index in range(golden_logs_index, len(golden_logs)):
                        missing_logs.append(golden_logs[golden_logs_index])
                    break

                # if both are in bounds, we compare the logs
                if golden_matches_processed(
                    golden_logs[golden_logs_index], processed_logs[processed_logs_index]
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
                EvaluatedCheckpoint(
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
                    evaluated_checkpoints.append(
                        EvaluatedCheckpoint(
                            url=processed_checkpoints[i].url,
                            checkpoint_status="extra_in_logs",
                            correct_logs=[],
                            missing_logs=[],
                            extra_logs_processed=processed_checkpoints[i].logs,
                        )
                    )
                processed_index += i_index

            # if we look ahead and doesn't exist later, then we mark current golden as missing
            else:
                evaluated_checkpoints.append(
                    EvaluatedCheckpoint(
                        url=golden_checkpoints[golden_index].url,
                        checkpoint_status="missing",
                        correct_logs=[],
                        missing_logs=golden_checkpoints[golden_index].logs,
                        extra_logs_processed=[],
                        name=golden_checkpoints[golden_index].name,
                    )
                )
                golden_index += 1

    return evaluated_checkpoints


if __name__ == "__main__":
    logs = generate_checkpoints_from_logs(PARENT_FOLDER + "trajectories/log.txt")
    for test, checkpoints in logs.items():
        test_name = test.split("/")[1].strip()
        if test_name in playground_tests:
            processed_checkpoints = []
            for checkpoint in checkpoints:
                processed_checkpoints.append(
                    PlaygroundCheckpoint(
                        checkpoint["url"],
                        logs_list_str_to_list_logs(checkpoint["logs"]),
                    )
                )

            evaluated = compare_processed_and_golden_checkpoints(
                playground_tests[test_name].checkpoints, processed_checkpoints
            )

            for evaluated_checkpoint in evaluated:
                print(
                    evaluated_checkpoint.checkpoint_status
                    + " "
                    + (
                        evaluated_checkpoint.name
                        if evaluated_checkpoint.name is not None
                        else evaluated_checkpoint.url
                    )
                )
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
                        + str(
                            [
                                str(log)
                                for log in evaluated_checkpoint.extra_logs_processed
                            ]
                        )
                    )
                print()
