from mem0 import Memory
from dotenv import load_dotenv
from openai import AzureOpenAI
import os

load_dotenv()

llm_azure_openai_api_key = os.environ["LLM_AZURE_OPENAI_API_KEY"]
llm_azure_chat_completion_deployment = os.environ["LLM_AZURE_CHAT_COMPLETION_DEPLOYMENT"]
llm_azure_endpoint = os.environ["LLM_AZURE_ENDPOINT"]
llm_azure_api_version = os.environ["LLM_AZURE_API_VERSION"]
llm_azure_embedding_deployment = os.environ["LLM_AZURE_EMBEDDING_DEPLOYMENT"]
search_service_name = os.environ["SEARCH_SERVICE_NAME"]
search_service_api_key = os.environ["SEARCH_SERVICE_API_KEY"]
print("Using Azure OpenAI deployment:", llm_azure_chat_completion_deployment)
print("Using Azure AI Search service:", search_service_name)


# Create Azure OpenAI client
azure_openai_client = AzureOpenAI(
    azure_endpoint=llm_azure_endpoint,
    api_key=llm_azure_openai_api_key,
    api_version=llm_azure_api_version
)

config = {
    "llm": {
        "provider": "azure_openai",
        "config": {
            "model": llm_azure_chat_completion_deployment,
            "temperature": 0.1,
            "max_tokens": 2000,
            "azure_kwargs": {
                  "azure_deployment": llm_azure_chat_completion_deployment,
                  "api_version": llm_azure_api_version,
                  "azure_endpoint": llm_azure_endpoint,
                  "api_key": llm_azure_openai_api_key,
              }
        }
    },
    "embedder": {
        "provider": "azure_openai",
        "config": {
            "model": llm_azure_embedding_deployment,
            "embedding_dims": 1536,
            "azure_kwargs": {
                "api_version": "2024-10-21",
                "azure_deployment": llm_azure_embedding_deployment,
                "azure_endpoint": llm_azure_endpoint,
                "api_key": llm_azure_openai_api_key,
            },
        },
    },
    "vector_store": {
                "provider": "azure_ai_search",
                "config": {
                    "service_name": search_service_name,
                    "api_key": search_service_api_key,
                    "collection_name": "my-demo-mem0-agent-memories",
                    "embedding_model_dims": 1536,
                    "compression_type": "binary",
                },
            },
}

memory = Memory.from_config(config)


def chat_with_memories(message: str, user_id: str = "default_user") -> str:
    # Retrieve relevant memories
    relevant_memories = memory.search(query=message, user_id=user_id, limit=3)
    memories_string = "\n".join(
        f"- {entry['memory']}" for entry in relevant_memories["results"]
    )

    # Generate Assistant response
    system_prompt = f"You are a helpful AI. Answer the question based on query and memories.\nUser Memories:\n{memories_string}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message},
    ]
    response = azure_openai_client.chat.completions.create(
        model=llm_azure_chat_completion_deployment, messages=messages
    )
    assistant_response = response.choices[0].message.content

    # Create new memories from the conversation
    messages.append({"role": "assistant", "content": assistant_response})
    # This is where the magic happens
    memory.add(messages, user_id=user_id, metadata={"source": "my-demo-mem0-agent"})

    return assistant_response


def main():

    # This is a demo user ID. In a real application, use actual user IDs.
    demo_user_id = "user_123" 

    print("Chat with AI (type 'exit' to quit)")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        print(f"AI: {chat_with_memories(user_input, demo_user_id)}")


if __name__ == "__main__":
    main()
