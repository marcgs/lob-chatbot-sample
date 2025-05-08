from semantic_kernel import Kernel

from semantic_kernel.connectors.ai.chat_completion_client_base import (
    ChatCompletionClientBase,
)
from semantic_kernel.contents import (
    ChatHistory,
    ChatMessageContent,
)
from semantic_kernel.agents import (
    ChatCompletionAgent,
    ChatHistoryAgentThread,
    AgentResponseItem,
)

from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)
from app.chatbot.agent_factory import create_support_ticket_agent


class SupportTicketAgent:
    history: ChatHistory
    kernel: Kernel
    chat_completion: ChatCompletionClientBase
    execution_settings: AzureChatPromptExecutionSettings
    agent: ChatCompletionAgent
    service_id: str = "chat-completion"

    def __init__(self):
        # Create a history of the conversation
        self.history = ChatHistory()
        self.chat_thread = ChatHistoryAgentThread(chat_history=self.history)

        # Create the agent
        self.agent = create_support_ticket_agent(name="SupportTicketAgent")

    async def chat(self, message: str, history: ChatHistory | None = None):
        # Add user input to the history
        self.history.add_user_message(message)

        # Get the response from the AI
        response: AgentResponseItem[ChatMessageContent] = await self.agent.get_response(
            messages=message, thread=self.chat_thread
        )

        # Handle function calls if any
        await self.__handle_function_calls(response)

        # Add the message from the agent to the chat history
        self.history.add_message(message=response.message)

        return str(response)

    def get_history(self) -> ChatHistory:
        """Get the chat history as a string."""
        return self.history

    async def __handle_function_calls(self, response):
        """Handle function calls from the response.
        This method checks if the last message in the history contains a function call.
        Extension to add more logic to handle special uses cases like clear history objects
        Args:
            response (_type_): _ChatMessageContent_: The response from the agent.
        """
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
        self.history.clear()
