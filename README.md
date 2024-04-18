# benchmark for web agents

## setup

1. Make sure `.env` and `frontend/.env.local` have the same `FLASK_RUN_PORT`
2. Install python requirements with `pip install -r requirements.txt`
3. Install Next requirements with `cd frontend && npm i`
4. Run with `./start.sh`

## evaluation

1. Add agent as a package under agents/
2. Import your agent and replace `run_natbot(goal, url)` in `evaluation/run`
3. Run `python -m evaluation.run` to run the entire individual test suite. You can add `click` as an arg to run all the click tests or specify specific tests with `click/button` or `click/link`