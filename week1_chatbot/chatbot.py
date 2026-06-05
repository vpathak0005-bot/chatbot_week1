import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class ChatAgent:
    def __init__(
        self,
        model,  
        max_turns=10,
        system_prompt="You are a helpful assistant.",
        stream=False,
    ):
        self.model = model
        self.max_turns = max_turns
        self.stream = stream

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
        )

        self.messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]
    def trim_history(self):
        system_count = 0

        for msg in self.messages:
          if msg["role"] == "system":
            system_count += 1

        max_messages = system_count + (2 * self.max_turns)

        if len(self.messages) > max_messages:
            self.compact_history()



    def compact_history(self):
        """
        Summarize older conversation into a short context.
        """
        if len(self.messages) <= 3:
            print("Nothing to compact.")
            return

        summary_prompt = [
            {
                "role": "system",
                "content": (
                    "Summarize the conversation below in "
                    "5 concise bullet points."
                ),
            }
        ]

        summary_prompt.extend(self.messages[1:])

        response = self.client.chat.completions.create(
            model=self.model,
            messages=summary_prompt,
        )

        summary = response.choices[0].message.content

        system_message = self.messages[0]

        self.messages = [
            system_message,
            {
                "role": "system",
                "content": f"Conversation summary:\n{summary}",
            },
        ]

        print("\nConversation compacted.\n")

    def chat(self, user_input):
        self.trim_history()

        self.messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )


        if self.stream:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                stream=True,
            )

            print("\nAssistant: ", end="", flush=True)

            full_response = ""

            for chunk in stream:
                delta = chunk.choices[0].delta.content

                if delta:
                    print(delta, end="", flush=True)
                    full_response += delta

            print()

            self.messages.append(
                {
                    "role": "assistant",
                    "content": full_response,
                }
            )

            return full_response

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
        )

        reply = response.choices[0].message.content

        self.messages.append(
            {
                "role": "assistant",
                "content": reply,
            }
        )

        return reply


def choose_model():
    models = {
        "1": "nvidia/nemotron-3-nano-30b-a3b:free",
        
        "2": "google/gemma-4-26b-a4b-it:free",
    }

    print("\nAvailable Models:")
    print("1. nvidia/nemotron-3-nano-30b-a3b:free")
    print("2. google/gemma-4-26b-a4b-it:free")

    while True:
        choice = input("\nChoose a model (1-2): ")

        if choice in models:
            return models[choice]

        print("Invalid choice. Try again.")


def main():
    print("=" * 50)
    print("MULTI-TURN CHATBOT")
    print("=" * 50)

    model = choose_model()

    agent = ChatAgent(
        model=model,
        max_turns=10,
        system_prompt="You are a helpful assistant.",
        stream=False,
    )

    print("\nCommands:")
    print("exit      -> quit")
    print("/compact  -> summarize history")
    print()

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if user_input.lower() == "/compact":
            agent.compact_history()
            continue

        try:
            reply = agent.chat(user_input)

            if not agent.stream:
                print(f"\nAssistant: {reply}\n")

        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()