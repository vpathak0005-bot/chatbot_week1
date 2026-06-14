

## Setup Instructions

### 1. Install Dependencies

Create and activate a virtual environment (recommended), then install the required packages:


pip install -r requirements.txt

### 2. Configure Environment Variables

Create a .env file in the project root directory with the following variables:


OPENROUTER_API_KEY=your_openrouter_api_key
SERPER_API_KEY=your_serper_api_key


The project uses:

OpenRouter for LLM access
Serper for web search functionality

### 3. AlphaXiv MCP Setup

The agent connects to the public AlphaXiv MCP server to search and retrieve academic papers. No local MCP server needs to be run. Internet access is required for MCP functionality.

### 4. Run the Application

Launch the Textual interface using:

```bash
python tui.py
```

### 5. Controls

* **Enter** → Submit a question
* **Ctrl + L** → Clear displayed chat
* **Ctrl + K** → Clear chat history and display
* **Ctrl + Q** → Quit the application

---

## What I Built

For this project, I built a terminal-based research assistant inspired by Perplexity. The application allows a user to ask a research question through a Textual TUI (Terminal User Interface). The agent can search the web, fetch and read webpages, retrieve relevant academic papers from AlphaXiv through MCP, and then generate a synthesized answer based on the gathered information.

The project follows an agent loop pattern. When a user submits a question, the model first decides whether it needs additional information. If it does, it calls one or more tools such as web search, webpage fetching, or paper retrieval. The tool results are then added back into the conversation history and sent back to the model. This process continues until the model has enough information to generate a final answer.

## Design Decision

One design decision I made was to limit the amount of webpage content returned by the `web_fetch` tool. Many webpages contain advertisements, navigation elements, and large amounts of text that are not useful for answering the user's question. Passing the full webpage to the model would increase token usage and slow down responses.

To address this, I used Trafilatura to extract the main article content and truncated very large pages before sending them to the model. This keeps the context focused while reducing unnecessary token consumption.

## Something That Surprised Me

One thing that surprised me was how much the quality of the results depended on the tool descriptions and system prompt. Small changes in wording affected whether the model decided to perform a web search, fetch a webpage, or retrieve academic papers.

I also found MCP integration more challenging than expected. Understanding how to connect to an external MCP server and correctly structure tool calls required careful debugging and reading of the documentation.

## Future Improvements

Given more time, I would add streaming responses so answers appear token-by-token instead of all at once. I would also add a separate panel in the TUI showing tool calls and their outputs in real time, making it easier to understand the agent's reasoning process.

Another improvement would be a note-saving feature that allows research summaries to be stored as markdown files for future reference. This would make the assistant more useful for longer research sessions and repeated investigations.

Overall, this project provided hands-on experience with agent loops, tool calling, MCP integration, web retrieval, and building an interactive research assistant that combines information from multiple sources.
