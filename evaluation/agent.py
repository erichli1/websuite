import sys

from evaluation.agents.natbot.natbot import run_natbot

if __name__ == "__main__":
    goal = sys.argv[1]
    url = sys.argv[2]

    run_natbot(goal, url, auto=True)
