from semantic_kernel import Kernel
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

from app.chatbot.factory import create_kernel_with_chat_completion


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
        kernel = create_kernel_with_chat_completion(service_id=name)

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
    kernel = create_kernel_with_chat_completion(service_id=service_id)

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
