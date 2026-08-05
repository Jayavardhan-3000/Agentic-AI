import asyncio
import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
load_dotenv()

async def main():

    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "stdio",
                "command": "python",
                "args": ["math_server.py"],
            },
            "weather": {
                "transport": "streamable-http",
                "url": "http://127.0.0.1:8000/mcp",
            },
        }
    )
    tools = await client.get_tools()
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=os.getenv("GROQ_API_KEY"),
    )
    agent = create_agent(
        model=llm,
        tools=tools,
    )
    response = await agent.ainvoke(
        {
            "messages": [
                (
                    "user",
                    "Multiply 15 and 7. Then tell me the weather in Vizianagaram."
                )
            ]
        }
    )
    print(response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())