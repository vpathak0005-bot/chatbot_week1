Submission Report
Overview

For this assignment, I built a multi-turn chatbot using the OpenRouter API. The chatbot supports maintaining conversation history, selecting between different models, streaming using LLM-generated summaries.

The main challenge was handling long conversations. Since LLMs are stateless , I needed a way to preserve important information without continuously sending the entire conversation history. To solve this, I implemented a compaction mechanism that summarizes older conversations and uses the summary as memory for future interactions.

Storing Conversation History

I stored the conversation as a list of messages using the standard chat format:
[
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
]
I chose this format because it is directly compatible with chat-completion APIs and makes it easy to send the entire conversation context back to the model on every turn.
I learned that LLMs do not actually remember previous conversations. The only reason a chatbot appears to have memory is because previous messages are repeatedly included in the prompt.
Instead of deleting older messages when the conversation becomes too long, I ask the same LLM to generate a concise summary of the conversation.


Challenges and Learnings

One issue I encountered was deciding when to trigger compaction.
Initially, compaction happened after adding the latest user message. After testing, I realized that this could potentially remove the current user query during summarization.
To avoid this, I changed the flow so that compaction is checked before adding the latest user message.This helped me better

Another challenge is that repeated summarization can gradually lose details over time.

Through this project, I implemented a functional multi-turn chatbot with support for conversation compaction using LLM-generated summaries.