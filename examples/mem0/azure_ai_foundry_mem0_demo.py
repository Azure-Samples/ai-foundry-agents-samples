from mem0 import Memory
from openai import AzureOpenAI

# Load reusable Azure configuration and Mem0 wiring.
from mem0_config import (
    CONFIG,
    LLM_AZURE_CHAT_COMPLETION_API_VERSION,
    LLM_AZURE_CHAT_COMPLETION_DEPLOYMENT,
    LLM_AZURE_OPENAI_ENDPOINT,
    LLM_AZURE_OPENAI_API_KEY,
    SEARCH_SERVICE_NAME,
)

print("Using Azure OpenAI deployment:", LLM_AZURE_CHAT_COMPLETION_DEPLOYMENT)
print("Using Azure AI Search service:", SEARCH_SERVICE_NAME)


# Create Azure OpenAI client that powers chat completions.
azure_openai_client = AzureOpenAI(
    azure_endpoint=LLM_AZURE_OPENAI_ENDPOINT,
    api_key=LLM_AZURE_OPENAI_API_KEY,
    api_version=LLM_AZURE_CHAT_COMPLETION_API_VERSION,
)

# Build the Mem0 memory interface using the shared config block.
memory = Memory.from_config(CONFIG)


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
        model=LLM_AZURE_CHAT_COMPLETION_DEPLOYMENT, messages=messages
    )
    assistant_response = response.choices[0].message.content

    # Create new memories from the conversation
    messages.append({"role": "assistant", "content": assistant_response})
    # This is where the magic happens
    memory.add(messages, user_id=user_id, metadata={"source": "my-demo-mem0-agent"})

    return assistant_response


def main():

    # This is a demo user ID. In a real application, use actual user IDs
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
