# benchmark for web agents

## setup

1. Make sure `.env` and `environment/frontend/.env.local` have the same `FLASK_RUN_PORT`
2. Make sure the port in `environment/frontend/package.json` and `evaluation/utils.py`
3. Install python requirements with `pip install -r requirements.txt`
4. Install Next requirements with `cd frontend && npm i`
5. Run with `./start.sh`

## evaluation

1. Add agent as a package under `agents/`
2. Import your agent and replace `run_natbot(goal, url)` in `evaluation/agent`
3. Run `python -m evaluation.ind` to run the entire individual test suite. You can add `click` as an arg to run all the click tests or specify specific tests with `click/button` or `click/link`. To run a test multiple times, you can specify `-n=3`.
4. Run `python -m evaluation.e2e` to run the entire E2E test suite. You can add `order` as an arg to run the order test or specify a specific checkpoint with `order/search`. To only run the checkpoint, you can specify `-checkpointonly`. To run a test multiple times, you can specify `-n=3`.