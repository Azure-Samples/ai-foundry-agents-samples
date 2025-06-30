# pylint: disable=line-too-long,useless-suppression
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

"""
DESCRIPTION:
    This sample demonstrates how to use agent operations with code interpreter from
    the Azure Agents service using a synchronous client.

USAGE:
    Before running the sample:

    Set these environment variables with your own values:
    1) PROJECT_ENDPOINT - The Azure AI Project endpoint, as found in the Overview
                          page of your Azure AI Foundry portal.
    2) MODEL_DEPLOYMENT_NAME - The deployment name of the AI model, as found under the "Name" column in
       the "Models + endpoints" tab in your Azure AI Foundry project.
"""

import os
import time
import json

from azure.ai.agents.models import MessageTextContent, ListSortOrder
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
    api_version="2025-05-15-preview"
)

with project_client:
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-mcp-agent", 
        instructions="You are a helpful assistant. Use the tools provided to answer the user's questions. Be sure to cite your sources.",
        tools=[
            {
                "type": "mcp",
		        "server_label": "weather",
                "server_url": os.environ["WEATHER_MCP_SERVER_URL"],
                "require_approval": "never"
            }
        ],
        tool_resources=None
    )
    # [END upload_file_and_create_agent_with_code_interpreter]
    print(f"Created agent, agent ID: {agent.id}")

    thread = project_client.agents.threads.create()
    print(f"Created thread, thread ID: {thread.id}")

    message = project_client.agents.messages.create(
        thread_id=thread.id, role="user", content="weather alerts in CA",
    )
    print(f"Created message, message ID: {message.id}")

    run = project_client.agents.runs.create(thread_id=thread.id, agent_id=agent.id)

    
    # Poll the run as long as run status is queued or in progress
    while run.status in ["queued", "in_progress", "requires_action"]:
        # Wait for a second
        time.sleep(1)
        run = project_client.agents.runs.get(thread_id=thread.id, run_id=run.id)
        print(f"Run status: {run.status}")

    if run.status == "failed":
        print(f"Run error: {run.last_error}")

    run_steps = project_client.agents.run_steps.list(thread_id=thread.id, run_id=run.id)
    for step in run_steps:
        print(f"Run step: {step.id}, status: {step.status}, type: {step.type}")
        if step.type == "tool_calls":
            print(f"Tool call details:")
            for tool_call in step.step_details.tool_calls:
                print(json.dumps(tool_call.as_dict(), indent=2))

    messages = project_client.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    for data_point in messages:
        last_message_content = data_point.content[-1]
        if isinstance(last_message_content, MessageTextContent):
            print(f"{data_point.role}: {last_message_content.text.value}")

    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")
