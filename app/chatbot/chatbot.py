from semantic_kernel.contents import (
    ChatHistory,
    ChatMessageContent,
)
from semantic_kernel.agents import (
    ChatCompletionAgent,
    ChatHistoryAgentThread,
    AgentResponseItem,
)

from app.chatbot.agent_factory import create_support_ticket_agent


class Chatbot:
    """Chatbot is a wrapper around the ChatCompletionAgent to manage the conversation history and handle special function calls not managed by Semantic Kernel."""

    # The agent that will be used to generate responses
    agent: ChatCompletionAgent

    def __init__(self, agent: ChatCompletionAgent):
        # Create a thread of the conversation
        self.chat_thread = ChatHistoryAgentThread()

        # Create the agent
        self.agent = agent

    @staticmethod
    def create_support_ticket_chatbot() -> "Chatbot":
        return Chatbot(create_support_ticket_agent(name="SupportTicketAgent"))

    async def chat(self, message: str, history: ChatHistory | None = None):
        # Get the response from the AI
        response: AgentResponseItem[ChatMessageContent] = await self.agent.get_response(
            messages=message, thread=self.chat_thread
        )

        # Handle function calls if any
        await self.__handle_function_calls(response)

        return str(response)

    async def __handle_function_calls(self, response):
        """Handle function calls from the response and check if the user wants to start over."""
        history = await self.chat_thread.get_messages()

        if len(history) >= 2:
            last_message = history[-2].to_dict()
            tool_calls = last_message.get("tool_calls", [])
            for tool_call in tool_calls:
                function_call = tool_call.get("function")
                if function_call:
                    # Check if the tool call is a function call
                    function_name = function_call["name"]
                    arguments = function_call["arguments"]
                    if "start_over" in function_name:
                        self.__start_over()

    def __start_over(self):
        # Clear the history
        self.chat_thread = ChatHistoryAgentThread()
