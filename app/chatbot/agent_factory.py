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
from semantic_kernel.agents.strategies import (
    KernelFunctionTerminationStrategy,
)
from semantic_kernel.functions import KernelFunctionFromPrompt
from semantic_kernel.functions.kernel_arguments import KernelArguments

from app.chatbot.root_path import chatbot_root_path


def create_user_agent(
    name: str, instructions: str, kernel: Kernel | None = None
) -> ChatCompletionAgent:
    """
    Create a user agent with the given name and instructions.
    Args:
        name (str): The name of the agent.
        instructions (str): The instructions for the agent.
        kernel (Kernel|None): The kernel instance to use. If None, a new kernel will be created.
    Returns:
        ChatCompletionAgent: The created user agent.
    """
    if kernel is None:
        kernel = _create_kernel_with_chat_completion(service_id=name)

    # Enable planning
    execution_settings = AzureChatPromptExecutionSettings()
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    execution_settings.temperature = 0.3
    execution_settings.top_p = 0.8

    # Create the agent
    agent = ChatCompletionAgent(
        kernel=kernel,
        id=name,
        name=name,
        instructions=instructions,
        arguments=KernelArguments(settings=execution_settings),
    )

    return agent


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
        kernel = _create_kernel_with_chat_completion(service_id=name)

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


def create_termination_strategy(
    task_completion_condition: str,
    service_id: str = "termination_service",
    maximum_iterations: int = 50,
) -> KernelFunctionTerminationStrategy:
    """
    Create a termination strategy for the task completion process.
    Args:
        task_completion_condition (str): The condition to determine if the task is complete.
        service_id (str): The ID of the service.
        maximum_iterations (int): The maximum number of iterations for the termination strategy.
    Returns:
        KernelFunctionTerminationStrategy: The created termination strategy.
    """
    kernel = _create_kernel_with_chat_completion(service_id=service_id)

    termination_function = KernelFunctionFromPrompt(
        function_name="termination",
        prompt=f"""
        Determine if {task_completion_condition}. If so, respond with a single word: yes

        History:
        {{{{$history}}}}
        """,
    )

    termination_strategy = KernelFunctionTerminationStrategy(
        function=termination_function,
        kernel=kernel,
        result_parser=lambda result: str(result.value[0]).lower() == "yes",
        history_variable_name="history",
        maximum_iterations=maximum_iterations,
    )

    return termination_strategy


# Private functions


def _load_support_ticket_instructions() -> str:
    # Load the workflow from a file
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


def _create_kernel_with_chat_completion(service_id: str | None = None) -> Kernel:
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
