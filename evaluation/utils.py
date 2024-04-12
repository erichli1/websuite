from typing import Dict
from evaluation.agents.natbot.natbot import run_natbot
import sys

LOCALHOST_PORT = 3000  # needs to be in sync with /environment/frontend/package.json


goals: Dict[str, Dict[str, str]] = {
    "click": {
        "button": "Click the button",
        "link": "Click the link",
    },
}


def get_url(task: str, test: str):
    return f"localhost:{LOCALHOST_PORT}/ind/{task}?test={test}"


def get_goal_and_url(task: str, test: str):
    task_dict = goals.get(task)
    if task_dict is None:
        print(f"ERROR: unable to find task {task}")
        return None

    test_goal = task_dict.get(test)
    if test_goal is None:
        print(f"ERROR: unable to find test {task}/{test}")
        return None

    return (test_goal, get_url(task, test))


def get_goals_and_urls_from_task(task: str):
    task_dict = goals.get(task)
    if task_dict is None:
        print(f"ERROR: unable to find task {task}")
        return None

    return [(task_dict[test], get_url(task, test)) for test in task_dict.keys()]


def get_all_goals_and_urls():
    return [(goals[task][test], get_url(task, test)) for task in goals.keys() for test in goals[task].keys()]


if (__name__ == "__main__"):
    # Identify the right goals and urls to iterate through
    goals_urls = []
    if len(sys.argv) > 1:
        for i, arg in enumerate(sys.argv[1:]):
            parts = arg.split("/", 1)
            if len(parts) == 1:
                goals_urls = get_goals_and_urls_from_task(parts[0])
            elif len(parts) == 2:
                goals_urls = [get_goal_and_url(parts[0], parts[1])]
    else:
        goals_urls = get_all_goals_and_urls()

    # Run agent as appropriate
    for goal, url in goals_urls:
        run_natbot(goal, url)
