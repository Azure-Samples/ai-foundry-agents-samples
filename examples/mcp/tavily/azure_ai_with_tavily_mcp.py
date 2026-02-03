# Copyright (c) Microsoft. All rights reserved.

import asyncio

from agent_framework import ChatAgent, MCPStreamableHTTPTool
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

import os
from dotenv import load_dotenv

load_dotenv()

"""
Azure AI Agent with Tavily MCP Tool Example

This sample demonstrates integration of Azure AI Agents with Tavily MCP Server.

USAGE:
    Before running the sample:

    Set these environment variables with your own values:
    1) AZURE_AI_PROJECT_ENDPOINT - The Azure AI Project endpoint, as found in the Overview
       page of your Azure AI Foundry portal.
    2) AZURE_AI_MODEL_DEPLOYMENT_NAME - The deployment name of the AI model, as found under the "Name" column in
       the "Models + endpoints" tab in your Azure AI Foundry project.
    3) TAVILY_MCP_SERVER_URL - The URL of your Tavily MCP server instance.
       
"""

async def main() -> None:
    print("=== Azure AI Chat Client Agent with Tavily MCP Tool Example ===\n")

    # Tools are provided when creating the agent
    # The agent can use these tools for any query during its lifetime
    # The agent will connect to the MCP server through its context manager.
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            chat_client=AzureAIAgentClient(
                project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
                model_deployment_name=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
                credential=credential,
                agent_name="MyTavilyWebSearchAgent",
                should_cleanup_agent=False,  # Set to False if you want to disable automatic agent cleanup
            ),
            instructions="You are a helpful assistant that can help answering questions related to web search using Taviliy MCP Server.",
            tools=MCPStreamableHTTPTool(  # Tools defined at agent creation
                name="Taviliy",
                url=os.environ["TAVILY_MCP_SERVER_URL"],
            ),
        ) as agent,
    ):
        query = "Search for articles about AI startups"
        print(f"User: {query}")
        result = await agent.run(query)
        print(f"{agent.name}: {result}\n")
        print("\n=======================================\n")


if __name__ == "__main__":
    asyncio.run(main())
