from typing import Dict

LOCALHOST_PORT = 3000  # needs to be in sync with /environment/frontend/package.json


goals: Dict[str, Dict[str, str]] = {
    "click": {
        "button": "Click the button",
        "link": "Click the link",
    },
}


def get_test_goals(task: str, test: str):
    task_dict = goals.get(task)
    if task_dict is None:
        print(f"ERROR: unable to find task {task}")
        return None

    test_goal = task_dict.get(test)
    if test_goal is None:
        print(f"ERROR: unable to find test {task}/{test}")
        return None

    return (test_goal, f"localhost:{LOCALHOST_PORT}/ind/{task}?test={test}")
