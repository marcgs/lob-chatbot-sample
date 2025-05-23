import asyncio

from semantic_kernel.contents import ChatHistory, ChatMessageContent
from semantic_kernel.agents import (
    ChatCompletionAgent,
    ChatHistoryAgentThread,
    AgentResponseItem,
)
from semantic_kernel.agents.strategies import KernelFunctionTerminationStrategy
from semantic_kernel.contents.function_call_content import FunctionCallContent
from semantic_kernel.contents.utils.author_role import AuthorRole

from app.chatbot.factory import create_support_ticket_agent
from evaluation.chatbot.models import FunctionCall
from evaluation.chatbot.simulation.factory import create_termination_strategy, create_user_agent


class SupportTicketChatSimulator:
    """
    This class is used to simulate a conversation between a user agent and a support ticket agent.
    It implements agent collaboration manually because AgentGroupChat history is not returning
    the function calls made by the chatbot.
    """

    async def run(
        self,
        instructions: str,
        task_completion_condition: str,
    ) -> ChatHistory:
        """
        This method simulates a conversation between a user and a support ticket agent.

        Args:
            instructions (str): Instructions for the user agent to follow.
            task_completion_condition (str): Condition to determine if the task is complete.
        """
        
        support_ticket_agent: ChatCompletionAgent = create_support_ticket_agent(
            name="SupportTicketAgent"
        )
        user_agent: ChatCompletionAgent = create_user_agent(
            name="UserAgent", instructions=instructions
        )
        termination_strategy: KernelFunctionTerminationStrategy = (
            create_termination_strategy(
                task_completion_condition=task_completion_condition
            )
        )

        # The agent thread is used to make sure the support ticket agent retains the full context of the conversation
        # it also contains the function calls made by the chatbot and is then returned for evaluation purposes
        agent_thread: ChatHistoryAgentThread = ChatHistoryAgentThread(
            thread_id="ChatSimulatorAgentThread"
        )
        # The user thread is used to make sure user agent retains the full context of the conversation
        # it's separated from the agent thread to avoid exposing tool calls and other messages to the user agent
        user_thread: ChatHistoryAgentThread = ChatHistoryAgentThread(
            thread_id="ChatSimulatorUserThread"
        )

        # Initial system message coming to have the Support Ticket Agent start the conversation
        user_message: ChatMessageContent = ChatMessageContent(
            content="Starting the simulation", role=AuthorRole.SYSTEM, name="system"
        )

        while True:
            agent_message: AgentResponseItem[ChatMessageContent] = await support_ticket_agent.get_response(
                messages=user_message, thread=agent_thread
            )

            print(f"Support Ticket Agent: {agent_message.to_dict()}")

            user_response = await user_agent.get_response(
                messages=agent_message.content, thread=user_thread
            )

            # Set the role to user for the support ticket agent to think it is a user message
            user_message = user_response.content
            user_message = ChatMessageContent(
                content=user_message.content,
                role=AuthorRole.USER,
                name=user_message.name
            )
            
            print(f"User: {user_message.to_dict()}")

            # Convert to list of messages to satisfy the type checker
            messages_list = await agent_thread.get_messages()
            # # Convert ChatHistory to list[ChatMessageContent] to solve type compatibility issue
            should_agent_terminate = await termination_strategy.should_agent_terminate(
                agent=support_ticket_agent,
                history=[msg for msg in messages_list], # list comprehension required for resolving type compatibility
            )

            if should_agent_terminate:
                print("Task completed")
                break

        history = await agent_thread.get_messages()

        return history

    def get_function_calls(self, chatHistory: ChatHistory) -> list[FunctionCall]:
        """
        This method retrieves the function calls made by the chatbot.
        It is used for evaluation purposes only.
        """

        function_calls: list[FunctionCall] = [
            FunctionCall.from_FunctionCallContent(item)
                for chatMessageContent in chatHistory 
                for item in chatMessageContent.items 
                if isinstance(item, FunctionCallContent)
        ]

        return function_calls


if __name__ == "__main__":
    # Create the support ticket simulator
    simulator = SupportTicketChatSimulator()

    # Start the simulation for ticket creation
    instructions = "You are a user who wants to create a new support ticket for a software issue. You need a ticket with title 'Email client crashes on startup', assigned to the IT department, with High priority and Expedited workflow. Provide a detailed description of the issue when asked."

    history = asyncio.run(
        simulator.run(
            instructions=instructions,
            task_completion_condition="the SupportTicketAgent has confirmed the creation of a Support Ticket",
        )
    )
    print(f"Function Calls: {simulator.get_function_calls(history)}")
