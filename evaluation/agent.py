import sys

from evaluation.agents.natbot.natbot import run_natbot

# from evaluation.agents.seeact.script import run_seeact

if __name__ == "__main__":
    goal = sys.argv[1]
    url = sys.argv[2]

    run_natbot(goal, url, auto=True)
    # run_seeact(goal, url)
