# Evaluating LLM-Powered Chatbots in Enterprise Workflows

## Introduction

The landscape of conversational AI has undergone a seismic shift with the emergence of large language models (LLMs). These sophisticated systems have transformed chatbots from rigid, rule-based interactions to dynamic, seemingly intelligent conversations. But with this transformation comes a fundamental challenge: how do we effectively measure the performance of these systems, especially in business-critical environments?

Traditional chatbot evaluation frameworks fall short when applied to modern LLM-based agents. The metrics that worked for deterministic, rule-based systems—like binary success/failure rates or strict accuracy measures—cannot capture the nuanced performance of systems capable of handling ambiguity, context, and complex reasoning.

## The Open-Ended vs. Closed-Domain Evaluation Challenge

Evaluating conversational AI presents a spectrum of challenges that vary dramatically based on the task domain:

*Open-ended task agents* (like those generating images, answering general knowledge questions, or providing creative content) operate in unbounded spaces where success criteria are often subjective. For these systems, evaluation typically focuses on user satisfaction, appropriateness, and creative quality.

*Closed-domain, business-specific agents* — the Line of Business (LOB) chatbots that manage inventory, process orders, or handle employee requests—face a different reality. These systems interact with structured business processes and must deliver precise, reliable outcomes with minimal tolerance for error. Here, evaluation must balance the flexibility of natural language interaction with the rigor of business process execution.

As noted by Anthropic in their engineering blog on [building effective agents](https://www.anthropic.com/engineering/building-effective-agents), "Agents should be designed not to replace humans but to augment them, handling routine tasks while escalating complex scenarios." This principle becomes even more critical in LOB applications where business outcomes and process integrity are non-negotiable.

## The Non-Deterministic Evaluation Problem

LLM-based chatbots introduce a fundamental challenge to evaluation: non-determinism. Unlike rule-based systems that produce identical outputs for identical inputs, LLMs incorporate elements of randomness and contextual interpretation that can result in varied—yet equally valid—responses to the same query.

This non-determinism creates several evaluation hurdles:

- Reproducibility issues: Test cases may pass or fail inconsistently
- Ground truth ambiguity: Multiple response paths may be equally correct
- Function calling reliability: The same user intent might be mapped to different function calls on different runs
- Hallucination risk: Models may confidently present incorrect information or take inappropriate actions

## The Evolution of Chatbot Architectures

To understand evaluation challenges, we must recognize how chatbot architectures have evolved:
Classic Rule-Based Chatbots

- Deterministic response mapping
- Limited domain coverage
- Explicit state management
- High precision but narrow scope
LLM-as-State-Machine Chatbots
- LLM manages conversation state
- Expanded domain coverage
- Natural language understanding
- Trade-off between flexibility and predictability
Fully Agentic Systems
- Goal-directed behavior
- Tool and function integration
- Planning and self-correction
- Complex evaluation across multiple dimensions
Bommasani et al. discuss in their paper "On the Opportunities and Risks of Foundation Models" (2021) how foundation models present unique evaluation challenges, particularly as these models become more capable and integrated with tools. Their work suggests that as AI systems gain more agency and functionality, our evaluation approaches must evolve beyond traditional metrics.

## Why LOB Applications Demand Rigorous Evaluation

For general-purpose assistants, occasional errors might be acceptable. For business systems managing inventory, processing payments, or handling sensitive customer data, they are not. Several factors make evaluation especially critical for LOB applications:

1. Business process integrity: Errors can disrupt critical workflows
2. Compliance requirements: Many industries face strict regulatory oversight
3. System integrations: Chatbots must reliably interact with multiple backend systems
4. Financial implications: Mistakes can directly impact revenue and costs
5. Employee and customer trust: Consistent performance builds essential confidence
Research consistently shows that enterprises implementing comprehensive evaluation frameworks before wide deployment of AI assistants tend to achieve better ROI and adoption rates compared to organizations using limited evaluation approaches.

## Toward a Comprehensive Evaluation Framework

The gap between traditional metrics and the needs of modern LLM-based LOB applications demands a new evaluation paradigm. We need frameworks that can:

- Assess both deterministic (did it correctly call the right function?) and non-deterministic aspects (did it understand user intent?)
- Evaluate across multiple dimensions: task completion, conversation quality, and business impact
- Account for the complexity of multi-turn conversations and complex business processes
- Scale to enterprise needs while providing actionable insights for improvement
In the following sections, I'll share our journey building an end-to-end evaluation framework for LLM-powered LOB chatbots, the technical challenges we overcame, and the methodology we developed to ensure these powerful but complex systems deliver reliable business value.

## Proposed Solution Details

The diagram below illustrates the architecture of our evaluation framework, highlighting its key components and their interactions. This framework is designed to address the unique challenges of evaluating LOB chatbots, ensuring scalability, reproducibility, and actionable insights.

![lob_chatbot_evaluation_diagram](./docs/evaluation/lob_chatbot_eval_diagram.png)

### Chat Simulation

A key pillar of our evaluation framework is the ability to simulate realistic, multi-turn conversations between a user and the chatbot. To achieve this, we developed an LLM-powered User Agent that acts as a stand-in for real users, following scenario-specific instructions and interacting with the chatbot just as a human would.

In each evaluation run, the User Agent is provided with a set of instructions that define the user's intent and business context (for example, creating a high-priority support ticket for an IT issue). The User Agent then engages in a natural conversation with the chatbot, responding to prompts, clarifying details, and navigating the workflow as a real user would. This back-and-forth continues until a predefined completion condition is met, such as the successful creation of a ticket or resolution of a request.

Throughout the simulated conversation, the framework automatically captures every function call made by the chatbot, including the function name and all arguments provided. This structured record of function calls is essential for evaluation: it allows us to directly compare the chatbot's actions against the ground truth for each scenario, measuring not just whether the right functions were called, but also whether the correct parameters were supplied and the business process was followed as intended.

```python
    # Create Support Ticket Agent (evaluation target)
    support_ticket_agent: ChatCompletionAgent = create_support_ticket_agent(name="SupportTicketAgent")

    # Create User Agent
    user_agent: ChatCompletionAgent = create_user_agent(name="UserAgent", instructions=instructions)

    # Termination Strategy to detect conversation end
    termination_strategy: KernelFunctionTerminationStrategy = (
        create_termination_strategy(
            task_completion_condition=task_completion_condition
        )
    )

    # Create agent conversation thread
    agent_thread: ChatHistoryAgentThread = ChatHistoryAgentThread(
        thread_id="ChatSimulatorAgentThread"
    )

    # Create separate user thread for the user agent to keep track of conversation separately
    user_thread: ChatHistoryAgentThread = ChatHistoryAgentThread(
        thread_id="ChatSimulatorUserThread"
    )

    while True:
        agent_message: AgentResponseItem[ChatMessageContent] = await support_ticket_agent.get_response(messages=user_message, thread=agent_thread)

        user_response = await user_agent.get_response(messages=agent_message.content, thread=user_thread)

        # ...
        
        history = await agent_thread.get_messages()

        # Check if conversation is finished according to the specified termination condition
        should_agent_terminate = await termination_strategy.should_agent_terminate(
            agent=support_ticket_agent,
            history=history,
        )

        if should_agent_terminate:
            # Conversation is finished => exit loop
            break

    # Extract history including function calls
    return history
```

 The simulation logic is implemented within the project’s evaluation framework in the [chat_simulator.py](https://github.com/marcgs/lob-chatbot-sample/blob/main/evaluation/chatbot/simulation/chat_simulator.py) module.

To ensure realistic interactions, the User Agent is configured to simulate non-technical users who understand the task but not the internal workings of the system. This approach helps identify potential usability issues and ensures the chatbot can handle diverse user expressions effectively. See sample [User Agent instructions](https://github.com/marcgs/lob-chatbot-sample/blob/main/evaluation/chatbot/ground-truth/support_ticket_eval_dataset.json#L4) in the evaluation dataset.

### Chat History with Function Calling



### Metrics, Evaluation, and Error Analysis

With the conversation and function call data in hand, the framework automatically computes a suite of evaluation metrics. These include:

- **Function Call Name Precision and Recall**: Measures the accuracy and completeness of function calls, in terms of function names.
- **Function Call Argument Precision and Recall**: Measures the accuracy and completeness of function parameters.
- **Reliability**: Measures overall success in completing business processes.

The evaluation framework integrates with the [Azure AI Evaluation SDK](https://learn.microsoft.com/python/api/overview/azure/ai-evaluation-readme) and optionally with [Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/) to calculate metrics and track evaluation runs. This integration enables advanced analysis, including performance tracking across chatbot versions and actionable summaries for error patterns.

### Ground Truth Generation at Scale

To generate evaluation datasets at scale, we leverage a script [generate_eval_dataset.py](https://github.com/marcgs/lob-chatbot-sample/blob/main/evaluation/chatbot/ground-truth/generate_eval_dataset.py) that combines scenario templates with real or representative business data. This script automates the creation of test cases by filling placeholders in templates with data from support tickets and action items. Below is a simplified example of how the dataset is generated:

```python
from pathlib import Path
from generate_eval_dataset import load_templates, load_and_process_data, generate_dataset

# Load templates and business data
templates = load_templates(Path("test_scenarios_templates.json"))
business_data = load_and_process_data(
    tickets_path=Path("dummy_support_tickets.csv"),
    actions_path=Path("dummy_action_items.csv")
)

# Generate dataset
dataset = generate_dataset(
    templates=templates,
    business_data=business_data,
    num_cases_per_scenario=3
)

# Save dataset to file
with open("support_ticket_eval_dataset.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=4)
```

This approach ensures that the dataset reflects real-world scenarios while maintaining scalability and consistency.

### Conclusion

By combining realistic simulation, comprehensive data capture, and automated evaluation, this solution provides a scalable and repeatable methodology for assessing LOB chatbots in enterprise environments. The result is a robust foundation for continuous improvement and confident deployment of conversational AI in business-critical workflows.
