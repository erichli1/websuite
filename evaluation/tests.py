import subprocess
import os
import csv
from typing import Callable

PARENT_FOLDER = os.path.join(os.path.dirname(__file__), "../")
LOG_FILEPATH = PARENT_FOLDER + "trajectories/log.txt"
IND_OUTPUT_FILEPATH = PARENT_FOLDER + "output/ind_output.csv"
E2E_OUTPUT_FILEPATH = PARENT_FOLDER + "output/e2e_output.csv"
E2E_TASK_OUTPUT_FILEPATH = PARENT_FOLDER + "output/e2e_task_output.csv"


# SCAFFOLDING TO SET UP THE TEST


def initialize_log_file(content: str):
    with open(LOG_FILEPATH, "w") as file:
        file.write(content)


def run_evaluation_e2e_evalonly():
    command = f"""python -m evaluation.e2e -evalonly"""
    process = subprocess.Popen(command, shell=True)
    process.wait()


def run_evaluation_ind_evalonly():
    command = f"""python -m evaluation.ind -evalonly"""
    process = subprocess.Popen(command, shell=True)
    process.wait()


def evaluate_e2e_outputs(eval_rows: Callable[[list[str]], bool]):
    rows = []

    with open(E2E_OUTPUT_FILEPATH, "r") as file:
        reader = csv.reader(file)

        for row in reader:
            rows.append(row)

    return eval_rows(rows)


def evaluate_e2e_task_outputs(eval_rows: Callable[[list[str]], bool]):
    rows = []

    with open(E2E_TASK_OUTPUT_FILEPATH, "r") as file:
        reader = csv.reader(file)

        for row in reader:
            rows.append(row)

    return eval_rows(rows)


def evaluate_ind_outputs(eval_rows: Callable[[list[str]], bool]):
    rows = []

    with open(IND_OUTPUT_FILEPATH, "r") as file:
        reader = csv.reader(file)

        for row in reader:
            rows.append(row)

    return eval_rows(rows)


# SCAFFOLDING TO RUN THE TEST AND EVALUATE OUTPUTS


class Test:
    def __init__(
        self, name: str, log_content: str, evaluate: Callable[[list[str]], bool]
    ):
        self.name = name
        self.log_content = log_content
        self.evaluate = evaluate


class E2ETest:
    def __init__(
        self,
        name: str,
        log_content: str,
        evaluate_output: Callable[[list[str]], bool],
        evaluate_summary: Callable[[list[str]], bool] | None,
    ):
        self.name = name
        self.log_content = log_content
        self.evaluate_output = evaluate_output
        self.evaluate_summary = evaluate_summary


IND_TESTS = [
    Test(
        name="ind_basic_pass",
        log_content="""
                    TEST BEGIN: click/button default
                    click/button // Submit
                    TEST FINISH
                    """,
        evaluate=lambda rows: len(rows) == 2
        and rows[1] == ["operational", "click", "button", "default", "1", "1"],
    ),
    Test(
        name="ind_basic_fail",
        log_content="""
                    TEST BEGIN: click/button default
                    TEST FINISH
                    """,
        evaluate=lambda rows: len(rows) == 2
        and rows[1] == ["operational", "click", "button", "default", "0", "1"],
    ),
    Test(
        name="ind_finddialog_manylogs_pass",
        log_content="""
                    TEST BEGIN: find/finddialog default
                    type/text // Answer // 2036
                    click/button // Learn more
                    type/text // Answer // 2032
                    TEST FINISH
                    """,
        evaluate=lambda rows: len(rows) == 2
        and rows[1] == ["informational", "find", "finddialog", "default", "1", "1"],
    ),
    Test(
        name="ind_gridfilter_manylogs_pass",
        log_content="""
                    TEST BEGIN: filter/gridfilter default
                    click/gridfilter // Orders // [{"field":"name","operator":"contains","value":"USA"}] // []
                    click/gridfilter // Orders // [{"field":"country","operator":"contains","value":"USA"}] // [{"field":"name","operator":"contains","value":"USA"}]
                    click/gridfilter // Orders // [{"field":"country","operator":"contains"}] // [{"field":"country","operator":"contains","value":"USA"}]
                    click/gridfilter // Orders // [{"field":"country","operator":"contains","value":"USA"}] // [{"field":"country","operator":"contains"}]
                    click/gridfilter // Orders // [{"field":"country","operator":"equals","value":"USA"}] // [{"field":"country","operator":"contains","value":"USA"}]
                    TEST FINISH
                    """,
        evaluate=lambda rows: len(rows) == 2
        and rows[1] == ["informational", "filter", "gridfilter", "default", "1", "1"],
    ),
    Test(
        name="ind_fill_basicform_fail",
        log_content="""
                    TEST BEGIN: fill/basicform default
                    type/text // First name // John // 
                    type/text // Last name // Doe // 
                    type/text // Email // johndoe@gmail.com //
                    TEST FINISH
                    """,
        evaluate=lambda rows: len(rows) == 2
        and rows[1]
        == ["informational", "fill", "basicform", "default", "0", "1", "0", "1"],
    ),
    Test(
        name="ind_fill_basicform_pass_process_fail",
        log_content="""
                    TEST BEGIN: fill/basicform default
                    type/text // First name // John Doe // 
                    type/text // Last name // Doe // 
                    type/text // Email // johndoe@gmail.com //
                    type/text // First name // John // John DOe
                    click/button // Submit
                    SUBMIT // {"email":"johndoe@gmail.com","firstName":"John","lastName":"Doe"}
                    TEST FINISH
                    """,
        evaluate=lambda rows: len(rows) == 2
        and rows[1]
        == ["informational", "fill", "basicform", "default", "1", "1", "0", "1"],
    ),
    Test(
        name="ind_fill_complexform_pass_process_pass",
        log_content="""
                    TEST BEGIN: fill/complexform default
                    type/text // First name // John // 
                    type/text // Last name // Doe // 
                    type/text // Email // johndoe@gmail.com //
                    type/phone // Phone number // (617) 000-0000 // 
                    type/text // Street address // 123 Main St // 
                    type/text // City // Cambridge // 
                    select/select // State // MA // 
                    type/text // Zip code // 02138 // 
                    type/date // Birthday // Sat, 01 Jan 2000 05:00:00 GMT //
                    click/button // Submit
                    SUBMIT // {"birthday":"Sat, 01 Jan 2000 05:00:00 GMT","city":"Cambridge","email":"johndoe@gmail.com","firstName":"John","lastName":"Doe","phoneNumber":"(617) 000-0000","state":"MA","streetAddress":"123 Main St","zipCode":"02138"}
                    TEST FINISH
                    """,
        evaluate=lambda rows: len(rows) == 2
        and rows[1]
        == ["informational", "fill", "complexform", "default", "1", "1", "1", "1"],
    ),
]

E2E_TESTS = [
    E2ETest(
        name="e2e_order_full_pass",
        log_content="""
                    TEST BEGIN: playground/order
                    NAVIGATE // /playground
                    type/text // Search items // laptop // 
                    click/iconbutton // Search
                    NAVIGATE // /playground/search?query=laptop
                    click/link // 2023 MacBook Pro - M3 chip, 14-inch
                    NAVIGATE // /playground/product/1
                    click/button // Buy now
                    NAVIGATE // /playground/checkout?cart={"id":"1","customizations":{"memory":"8GB","storage":"512GB"},"price":1599}
                    type/text // First name // John // 
                    type/text // Last name // Doe // 
                    type/text // Street address // 123 Main Street // 
                    type/text // City // Cambridge // 
                    select/select // State // MA // 
                    type/text // Zip code // 02138 // 
                    click/button // Order
                    NAVIGATE // /playground/thanks?cart={"customizations":{"memory":"8GB","storage":"512GB"},"id":"1"}&location={"city":"Cambridge","firstName":"John","lastName":"Doe","state":"MA","streetAddress":"123 Main Street","zipCode":"02138"}
                    TEST FINISH
                    """,
        evaluate_output=lambda rows: len(rows) == 6
        and rows[1:]
        == [
            ["order", "1", "1"],
            ["order", "", "", "1_search_for_item", "1", "0", "0", "1"],
            ["order", "", "", "2_select_item_from_search", "1", "0", "0", "1"],
            ["order", "", "", "3_purchase_item", "1", "0", "0", "1"],
            ["order", "", "", "4_fill_shipping_info", "1", "0", "0", "1"],
        ],
        evaluate_summary=lambda rows: all(
            row
            in [
                ["operational", "type", "text", "1", "1"],
                ["informational", "search", "appropriate", "1", "1"],
                ["operational", "click", "iconbutton", "1", "1"],
                ["operational", "click", "link", "1", "1"],
                ["operational", "click", "button", "1", "1"],
                ["informational", "fill", "complex", "1", "1"],
            ]
            for row in rows[1:]
        ),
    ),
    E2ETest(
        name="e2e_order_full_pass_n=3",
        log_content="""
                    TEST BEGIN: playground/order
                    NAVIGATE // /playground
                    type/text // Search items // laptop // 
                    click/iconbutton // Search
                    NAVIGATE // /playground/search?query=laptop
                    click/link // 2023 MacBook Pro - M3 chip, 14-inch
                    NAVIGATE // /playground/product/1
                    click/button // Buy now
                    NAVIGATE // /playground/checkout?cart={"id":"1","customizations":{"memory":"8GB","storage":"512GB"},"price":1599}
                    type/text // First name // John // 
                    type/text // Last name // Doe // 
                    type/text // Street address // 123 Main Street // 
                    type/text // City // Cambridge // 
                    select/select // State // MA // 
                    type/text // Zip code // 02138 // 
                    click/button // Order
                    NAVIGATE // /playground/thanks?cart={"customizations":{"memory":"8GB","storage":"512GB"},"id":"1"}&location={"city":"Cambridge","firstName":"John","lastName":"Doe","state":"MA","streetAddress":"123 Main Street","zipCode":"02138"}
                    TEST FINISH
                    TEST BEGIN: playground/order
                    NAVIGATE // /playground
                    type/text // Search items // laptop // 
                    click/iconbutton // Search
                    NAVIGATE // /playground/search?query=laptop
                    click/link // 2023 MacBook Pro - M3 chip, 14-inch
                    NAVIGATE // /playground/product/1
                    click/button // Buy now
                    NAVIGATE // /playground/checkout?cart={"id":"1","customizations":{"memory":"8GB","storage":"512GB"},"price":1599}
                    type/text // First name // John // 
                    type/text // Last name // Doe // 
                    type/text // Street address // 123 Main Street // 
                    type/text // City // Cambridge // 
                    select/select // State // MA // 
                    type/text // Zip code // 02138 // 
                    click/button // Order
                    NAVIGATE // /playground/thanks?cart={"customizations":{"memory":"8GB","storage":"512GB"},"id":"1"}&location={"city":"Cambridge","firstName":"John","lastName":"Doe","state":"MA","streetAddress":"123 Main Street","zipCode":"02138"}
                    TEST FINISH
                    TEST BEGIN: playground/order
                    NAVIGATE // /playground
                    type/text // Search items // laptop // 
                    click/iconbutton // Search
                    NAVIGATE // /playground/search?query=laptop
                    click/link // 2023 MacBook Pro - M3 chip, 14-inch
                    NAVIGATE // /playground/product/1
                    click/button // Buy now
                    NAVIGATE // /playground/checkout?cart={"id":"1","customizations":{"memory":"8GB","storage":"512GB"},"price":1599}
                    type/text // First name // John // 
                    type/text // Last name // Doe // 
                    type/text // Street address // 123 Main Street // 
                    type/text // City // Cambridge // 
                    select/select // State // MA // 
                    type/text // Zip code // 02138 // 
                    click/button // Order
                    NAVIGATE // /playground/thanks?cart={"customizations":{"memory":"8GB","storage":"512GB"},"id":"1"}&location={"city":"Cambridge","firstName":"John","lastName":"Doe","state":"MA","streetAddress":"123 Main Street","zipCode":"02138"}
                    TEST FINISH
                    """,
        evaluate_output=lambda rows: len(rows) == 6
        and rows[1:]
        == [
            ["order", "3", "3"],
            ["order", "", "", "1_search_for_item", "3", "0", "0", "3"],
            ["order", "", "", "2_select_item_from_search", "3", "0", "0", "3"],
            ["order", "", "", "3_purchase_item", "3", "0", "0", "3"],
            ["order", "", "", "4_fill_shipping_info", "3", "0", "0", "3"],
        ],
        evaluate_summary=lambda rows: all(
            row
            in [
                ["operational", "type", "text", "3", "3"],
                ["informational", "search", "appropriate", "3", "3"],
                ["operational", "click", "iconbutton", "3", "3"],
                ["operational", "click", "link", "3", "3"],
                ["operational", "click", "button", "3", "3"],
                ["informational", "fill", "complex", "3", "3"],
            ]
            for row in rows[1:]
        ),
    ),
    E2ETest(
        name="e2e_order_all_checkpoints_pass",
        log_content="""
                    TEST BEGIN: playground/order 1_search_for_item -checkpointonly
                    NAVIGATE // /playground
                    type/text // Search items // laptop // 
                    click/iconbutton // Search
                    NAVIGATE // /playground/search?query=laptop
                    TEST FINISH
                    TEST BEGIN: playground/order 2_select_item_from_search -checkpointonly
                    NAVIGATE // /playground/search?query=Macbook Pro M3 chip
                    click/link // 2023 MacBook Pro - M3 chip, 14-inch
                    NAVIGATE // /playground/product/1
                    TEST FINISH
                    TEST BEGIN: playground/order 3_purchase_item -checkpointonly
                    NAVIGATE // /playground/product/1
                    click/button // Buy now
                    NAVIGATE // /playground/checkout?cart={"id":"1","customizations":{"memory":"8GB","storage":"512GB"},"price":1599}
                    TEST FINISH
                    TEST BEGIN: playground/order 4_fill_shipping_info -checkpointonly
                    NAVIGATE // /playground/checkout?cart={"id":"1","customizations":{"memory":"8GB","storage":"512GB"},"price":1599}
                    type/text // First name // John // 
                    type/text // Last name // Doe // 
                    type/text // Street address // 123 Main Street // 
                    type/text // City // Cambridge // 
                    select/select // State // MA // 
                    type/text // Zip code // 02138 // 
                    click/button // Order
                    NAVIGATE // /playground/thanks?cart={"customizations":{"memory":"8GB","storage":"512GB"},"id":"1"}&location={"city":"Cambridge","firstName":"John","lastName":"Doe","state":"MA","streetAddress":"123 Main Street","zipCode":"02138"}
                    TEST FINISH
                    """,
        evaluate_output=lambda rows: len(rows) == 9
        and rows[1:]
        == [
            ["order", "0", "0"],
            ["order", "", "", "1_search_for_item", "1", "0", "0", "1"],
            ["order", "0", "0"],
            ["order", "", "", "2_select_item_from_search", "1", "0", "0", "1"],
            ["order", "0", "0"],
            ["order", "", "", "3_purchase_item", "1", "0", "0", "1"],
            ["order", "0", "0"],
            ["order", "", "", "4_fill_shipping_info", "1", "0", "0", "1"],
        ],
        evaluate_summary=lambda rows: all(
            row
            in [
                ["operational", "type", "text", "1", "1"],
                ["informational", "search", "appropriate", "1", "1"],
                ["operational", "click", "iconbutton", "1", "1"],
                ["operational", "click", "link", "1", "1"],
                ["operational", "click", "button", "1", "1"],
                ["informational", "fill", "complex", "1", "1"],
            ]
            for row in rows[1:]
        ),
    ),
    E2ETest(
        name="e2e_order_full_fail_pass_134_fail_2",
        log_content="""
                    TEST BEGIN: playground/order
                    NAVIGATE // /playground
                    type/text // Search items // laptop // 
                    click/iconbutton // Search
                    NAVIGATE // /playground/search?query=laptop
                    click/link // 2023 MacBook Pro - M3 Pro chip, 14-inch
                    NAVIGATE // /playground/product/2
                    click/button // Buy now
                    NAVIGATE // /playground/checkout?cart={"id":"2","customizations":{"memory":"18GB","storage":"512GB"},"price":1999}
                    type/text // First name // John // 
                    type/text // Last name // Doe // 
                    type/text // Street address // 123 Main Street // 
                    type/text // City // Cambridge // 
                    select/select // State // MA // 
                    type/text // Zip code // 02138 // 
                    click/button // Order
                    NAVIGATE // /playground/thanks?cart={"customizations":{"memory":"18GB","storage":"512GB"},"id":"2"}&location={"city":"Cambridge","firstName":"John","lastName":"Doe","state":"MA","streetAddress":"123 Main Street","zipCode":"02138"}
                    TEST FINISH
                    """,
        evaluate_output=lambda rows: len(rows) == 6
        and rows[1:]
        == [
            ["order", "0", "1"],
            ["order", "", "", "1_search_for_item", "1", "0", "0", "1"],
            [
                "order",
                "",
                "",
                "2_select_item_from_search",
                "0",
                "1",
                "0",
                "1",
            ],  # Partial match bc clicked wrong product
            [
                "order",
                "",
                "",
                "3_purchase_item",
                "0",
                "0",
                "1",
                "1",
            ],  # Missing bc never reached purchase item page for product ID 2
            ["order", "", "", "4_fill_shipping_info", "1", "0", "0", "1"],
        ],
        evaluate_summary=lambda rows: all(
            row
            in [
                ["operational", "type", "text", "1", "1"],
                ["operational", "click", "iconbutton", "1", "1"],
                ["operational", "click", "link", "0", "1"],
                ["informational", "search", "appropriate", "0", "1"],
                ["operational", "click", "button", "1", "2"],
                ["informational", "fill", "complex", "1", "1"],
            ]
            for row in rows[1:]
        ),
    ),
    E2ETest(
        name="e2e_order_full_pass_order_all_checkpoints_fail",
        log_content="""
                    TEST BEGIN: playground/order
                    NAVIGATE // /playground
                    type/text // Search items // laptop // 
                    click/iconbutton // Search
                    NAVIGATE // /playground/search?query=laptop
                    click/link // 2023 MacBook Pro - M3 chip, 14-inch
                    NAVIGATE // /playground/product/1
                    click/button // Buy now
                    NAVIGATE // /playground/checkout?cart={"id":"1","customizations":{"memory":"8GB","storage":"512GB"},"price":1599}
                    type/text // First name // John // 
                    type/text // Last name // Doe // 
                    type/text // Street address // 123 Main Street // 
                    type/text // City // Cambridge // 
                    select/select // State // MA // 
                    type/text // Zip code // 02138 // 
                    click/button // Order
                    NAVIGATE // /playground/thanks?cart={"customizations":{"memory":"8GB","storage":"512GB"},"id":"1"}&location={"city":"Cambridge","firstName":"John","lastName":"Doe","state":"MA","streetAddress":"123 Main Street","zipCode":"02138"}
                    TEST FINISH
                    TEST BEGIN: playground/order 1_search_for_item -checkpointonly
                    NAVIGATE // /playground
                    TEST FINISH
                    TEST BEGIN: playground/order 2_select_item_from_search -checkpointonly
                    NAVIGATE // /playground/search?query=Macbook Pro M3 chip
                    TEST FINISH
                    TEST BEGIN: playground/order 3_purchase_item -checkpointonly
                    NAVIGATE // /playground/product/1
                    TEST FINISH
                    TEST BEGIN: playground/order 4_fill_shipping_info -checkpointonly
                    NAVIGATE // /playground/checkout?cart={"id":"1","customizations":{"memory":"8GB","storage":"512GB"},"price":1599}
                    TEST FINISH
                    """,
        evaluate_output=lambda rows: rows[1:]
        == [
            ["order", "1", "1"],
            ["order", "", "", "1_search_for_item", "1", "0", "0", "1"],
            ["order", "", "", "2_select_item_from_search", "1", "0", "0", "1"],
            ["order", "", "", "3_purchase_item", "1", "0", "0", "1"],
            ["order", "", "", "4_fill_shipping_info", "1", "0", "0", "1"],
            ["order", "0", "0"],
            ["order", "", "", "1_search_for_item", "0", "1", "0", "1"],
            ["order", "0", "0"],
            ["order", "", "", "2_select_item_from_search", "0", "1", "0", "1"],
            ["order", "0", "0"],
            ["order", "", "", "3_purchase_item", "0", "1", "0", "1"],
            ["order", "0", "0"],
            ["order", "", "", "4_fill_shipping_info", "0", "1", "0", "1"],
        ],
        evaluate_summary=None,
    ),
    E2ETest(
        name="e2e_add_cart_pass_1_stuck_2",
        log_content="""
                    TEST BEGIN: playground/add_custom_to_cart
                    NAVIGATE // /playground
                    type/text // Search items // laptop // 
                    click/iconbutton // Search
                    NAVIGATE // /playground/search?query=laptop
                    TEST FINISH
                    """,
        evaluate_output=lambda rows: rows[1:]
        == [
            ["add_custom_to_cart", "0", "1"],
            ["add_custom_to_cart", "", "", "1_search_for_item", "1", "0", "0", "1"],
            [
                "add_custom_to_cart",
                "",
                "",
                "2_select_item_from_search",
                "0",
                "1",
                "0",
                "1",
            ],
            [
                "add_custom_to_cart",
                "",
                "",
                "3_select_customizations",
                "0",
                "0",
                "1",
                "1",
            ],
        ],
        evaluate_summary=lambda rows: all(
            row
            in [
                ["operational", "type", "text", "1", "1"],
                ["operational", "click", "iconbutton", "1", "1"],
                ["operational", "click", "link", "0", "1"],
                ["informational", "search", "appropriate", "0", "1"],
            ]
            for row in rows[1:]
        ),
    ),
]


def print_ind_test_result(name: str, result: bool):
    print(name + (" \033[32mcorrect\033[0m" if result else " \033[31mincorrect\033[0m"))


def print_e2e_test_result(name: str, output_result: bool, summary_result: bool | None):
    output_str = (
        name
        + " output"
        + (" \033[32mcorrect\033[0m" if output_result else " \033[31mincorrect\033[0m")
    )

    if summary_result is not None:
        output_str += " task_output" + (
            " \033[32mcorrect\033[0m" if summary_result else " \033[31mincorrect\033[0m"
        )

    print(output_str)


if __name__ == "__main__":
    for test in IND_TESTS:
        initialize_log_file(test.log_content)
        run_evaluation_ind_evalonly()
        result = evaluate_ind_outputs(test.evaluate)
        print_ind_test_result(test.name, result)

    print()

    for test in E2E_TESTS:
        initialize_log_file(test.log_content)
        run_evaluation_e2e_evalonly()
        output_result = evaluate_e2e_outputs(test.evaluate_output)
        summary_result = (
            evaluate_e2e_task_outputs(test.evaluate_summary)
            if test.evaluate_summary is not None
            else None
        )
        print_e2e_test_result(test.name, output_result, summary_result)
