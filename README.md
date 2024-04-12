# benchmark for web agents

## setup

1. Make sure `.env` and `frontend/.env.local` have the same `FLASK_RUN_PORT`
2. Install python requirements with `pip install -r requirements.txt`
3. Install Next requirements with `cd frontend && npm i`
4. Run with `./start.sh`

## evaluation

1. Run `python -m evaluation.agents.natbot.natbot`