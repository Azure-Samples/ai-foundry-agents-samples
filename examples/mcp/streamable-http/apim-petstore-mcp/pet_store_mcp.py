# This sample demonstrates how to use the Azure API Management (APIM) service
# to expose Pet Store APIs as a MCP server, to create a chatbot using the Semantic Kernel.
# 
# NOTE: when running this sample code, you'll get `HTTP/1.1 401 Unauthorized` error, when connecting to the Pet Store MCP Server on APIM. 
# This demonstrates that the MCP Server is secure and can be reachable only by providing the Bearer token.
# To fix this, uncomment the line setting the headers in the `MCPStreamableHttpPlugin` definition (around line 115). 


import asyncio
import logging
import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.mcp import MCPStreamableHttpPlugin
from semantic_kernel.contents import ChatHistory
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from azure.identity import DefaultAzureCredential


"""
This sample demonstrates how to build a conversational chatbot
using Semantic Kernel,
it creates a Plugin from a MCP server config and adds it to the kernel.
The chatbot is designed to interact with the user, call MCP tools
as needed, and return responses.
"""

# Configure the logging module
logging.basicConfig(
    level=logging.INFO,  # Set the desired logging level (DEBUG, INFO, WARNING, etc.)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Step 2: Create a logger
logger = logging.getLogger("mcp.streamable-http.mcp-client")

load_dotenv()
petstore_mcp_server_url = os.getenv("PETSTORE_MCP_SERVER_URL")
api_key=os.getenv("AZURE_OPENAI_API_KEY")
endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
api_version=os.getenv("AZURE_OPENAI_API_VERSION")
logger.info(f"Using MCP server URL: {petstore_mcp_server_url}")
logger.info(f"Using Azure OpenAI endpoint: {endpoint}")
logger.info(f"Using Azure OpenAI deployment name: {deployment_name}")
logger.info(f"Using Azure OpenAI API version: {api_version}")

# System message defining the behavior and persona of the chat bot.
system_message = """
You are a chat bot. And you help users interact with pet store services.
You can call functions to get the information you need.
"""

# Create and configure the kernel.
kernel = Kernel()

chat_service = AzureChatCompletion(
    api_key=api_key,
    endpoint=endpoint,
    deployment_name=deployment_name,
    api_version=api_version
)
settings = AzureChatPromptExecutionSettings()


# Configure the function choice behavior. Here, we set it to Auto, where auto_invoke=True by default.
# With `auto_invoke=True`, the model will automatically choose and call functions as needed.
settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

kernel.add_service(chat_service)

# Create a chat history to store the system message, initial messages, and the conversation.
history = ChatHistory()
history.add_system_message(system_message)


async def chat() -> bool:
    """
    Continuously prompt the user for input and show the assistant's response.
    Type 'exit' to exit.
    """
    try:
        user_input = input("User:> ")
    except (KeyboardInterrupt, EOFError):
        print("\n\nExiting chat...")
        return False
    if user_input.lower().strip() == "exit":
        print("\n\nExiting chat...")
        return False

    history.add_user_message(user_input)
    result = await chat_service.get_chat_message_content(history, settings, kernel=kernel)
    if result:
        print(f"Bot:> {result}")
        history.add_message(result)

    return True


async def main() -> None:

    # Get an access token for the Azure API
    credential = DefaultAzureCredential()
    access_token = credential.get_token("https://azure-api.net/authorization-manager")

    # Create a plugin from the MCP server config and add it to the kernel.
    # The MCP server plugin is defined using the MCPStreamableHttpPlugin, which take a URL.
    async with MCPStreamableHttpPlugin(
        name="Petstore",
        description="Petstore Plugin",
        url=petstore_mcp_server_url,
        load_prompts=False,
        # UNCOMMENT THE BELOW LINE TO MAKE THIS SAMPLE CODE WORK
        # headers={"Authorization": f"Bearer {access_token.token}"}
    ) as petstore_plugin:
    
        # Add the plugin to the kernel.
        kernel.add_plugin(petstore_plugin)

        # Start the chat loop.
        print("Welcome to the chat bot!\n  Type 'exit' to exit.\n")
        chatting = True
        while chatting:
            chatting = await chat()


if __name__ == "__main__":
    asyncio.run(main())
