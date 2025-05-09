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
    """Chatbot is a wrapper around the ChatCompletionAgent to manage the conversation history."""

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

        return str(response)

