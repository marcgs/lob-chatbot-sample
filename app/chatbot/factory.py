import os
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import (
    FunctionChoiceBehavior,
)
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)
from semantic_kernel.functions.kernel_arguments import KernelArguments
from app.chatbot.root_path import chatbot_root_path


def create_support_ticket_agent(
    name: str, kernel: Kernel | None = None
) -> ChatCompletionAgent:
    """
    Create a support ticket management agent with the specified name and instructions.
    Args:
        name (str): The name of the agent.
        kernel (Kernel|None): The kernel instance to use. If None, a new kernel will be created.
    Returns:
        ChatCompletionAgent: The created support ticket management agent.
    """

    if kernel is None:
        kernel = create_kernel_with_chat_completion(service_id=name)

    _load_support_ticket_plugins(kernel)

    # Enable planning
    execution_settings = AzureChatPromptExecutionSettings()
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    execution_settings.temperature = 0.3
    execution_settings.top_p = 0.9

    # Create the agent
    agent = ChatCompletionAgent(
        kernel=kernel,
        id=name,
        name=name,
        instructions=_load_support_ticket_instructions(),
        arguments=KernelArguments(settings=execution_settings),
    )

    return agent


def create_kernel_with_chat_completion(service_id: str | None = None) -> Kernel:
    """
    Create a kernel with Azure OpenAI chat completion service.
    Args:
        service_id (str|None): The service ID for the Azure OpenAI service. If None, a default ID will be used.
    Returns:
        Kernel: The created kernel instance.
    """
    kernel = Kernel()

    # Add Azure OpenAI chat completion
    kernel.add_service(
        AzureChatCompletion(
            service_id=service_id,
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        )
    )
    return kernel

def _load_support_ticket_instructions() -> str:
    """
    Load the support ticket management instructions from a file.
    Returns:
        str: The loaded instructions.
    """
    with open(
        f"{chatbot_root_path()}/workflow-definitions/support-ticket-workflow.txt",
        "r",
    ) as file:
        support_ticket_process_definition = file.read()
        instructions = f"""
            You are a Support Ticket Management assistant. You must only answer requests related to Support Tickets.

            Below is the exact policy that you must follow to help users create and manage support tickets.

            POLICY:
            {support_ticket_process_definition}
            """
        return instructions


def _load_support_ticket_plugins(kernel: Kernel):
    """
    Load the support ticket management plugins based on the specified plugin type.
    Args:
        kernel (Kernel): The kernel instance to load the plugins into.
    """
    from app.chatbot.plugins.common_plugin import CommonPlugin
    from app.chatbot.plugins.support_ticket_system.ticket_management_plugin import (
        TicketManagementPlugin,
    )
    from app.chatbot.plugins.support_ticket_system.action_item_plugin import (
        ActionItemPlugin,
    )
    from app.chatbot.plugins.support_ticket_system.reference_data_plugin import (
        ReferenceDataPlugin,
    )

    kernel.add_plugin(CommonPlugin(), plugin_name="CommonPlugin")
    kernel.add_plugin(TicketManagementPlugin(), plugin_name="TicketManagementPlugin")
    kernel.add_plugin(ActionItemPlugin(), plugin_name="ActionItemPlugin")
    kernel.add_plugin(ReferenceDataPlugin(), plugin_name="ReferenceDataPlugin")
