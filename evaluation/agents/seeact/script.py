from seeact.agent import SeeActAgent
import asyncio
import os


async def run_agent(agent: SeeActAgent):
    await agent.start()

    while True:
        prediction_dict = await agent.predict()
        if prediction_dict["action"] == "TERMINATE":
            agent.stop()
            break
        await agent.execute(prediction_dict)


def run_seeact(goal: str, url: str):
    agent = SeeActAgent(
        openai_key=os.getenv("OPENAI_API_KEY"),
        default_task=goal,
        default_website=url,
    )

    asyncio.run(run_agent(agent))
