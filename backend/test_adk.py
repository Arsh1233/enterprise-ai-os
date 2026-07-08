import asyncio

from google.adk import Agent, __version__

agent = Agent(name="test_agent", model="gemini-2.5-flash", instruction="Say 'pong'.")


async def main() -> None:
    try:
        print("ADK version:", __version__)
        if hasattr(agent, "__call__"):
            print("Agent is callable!")

        from google.adk.engine.context import Context

        ctx = Context()
        async for event in agent.run(ctx=ctx, node_input="ping"):
            print("Event:", type(event), event)
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    asyncio.run(main())
