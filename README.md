# WebSuite: Diagnostic Benchmark for Generalist Web Agents

## Set up web environment
1. Make sure `.env` and `environment/frontend/.env.local` have the same `FLASK_RUN_PORT`
2. Make sure the port in `environment/frontend/package.json` and `evaluation/utils.py`
3. Install python requirements with `pip install -r requirements.txt`
4. Install Next requirements with `cd frontend && npm i`
5. Run with `./start.sh`

## Evaluate an agent

1. Add agent as a package under `agents/`
2. Import your agent and replace `run_natbot(goal, url)` in `evaluation/agent`
3. Run `python -m evaluation.ind` to run the entire individual test suite. You can add `click` as an arg to run all the click tests or specify specific tests with `click/button` or `click/link`. To run a test multiple times, you can specify `-n=8`.
4. Run `python -m evaluation.e2e` to run the entire E2E test suite. You can add `order` as an arg to run the order test or specify a specific checkpoint with `order/search`. To run a test multiple times, you can specify `-n=8`.

## Analze agent performance
1. After running the individual test suite, move `output/ind_output.csv` to be `analyze/outputs/ind/<agent name>.csv`.
2. After running the E2E test suite, move `output/e2e_output.csv` to be `analyze/outputs/e2e/full/<agent name>.csv` and `output/e2e_task_output.csv` to be `analyze/outputs/e2e/full_tasks/<agent name>.csv`.
3. Run the `analyze.ipynb` notebook in `/analyze`

## License
This code is licensed under the [MIT License](https://www.tldrlegal.com/license/mit-license).

We include a modified version of natbot in our code, which is also [under the MIT license](https://github.com/nat/natbot/blob/main/LICENSE).