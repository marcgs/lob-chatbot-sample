# Support Ticket Chatbot Architecture

## Overview

The Support Ticket Chatbot demonstrates a structured approach to building line-of-business conversational interfaces using Semantic Kernel and large language models. This document provides an in-depth look at the system's architecture and key components.

## Core Components

### Agent Class

The `SupportTicketAgent` class serves as the main orchestrator for the chatbot system:

- Manages the conversation with users via the `chat()` method
- Maintains conversation history using Semantic Kernel's `ChatHistory`
- Handles function calls from the LLM responses
- Provides utilities for conversation management (e.g., starting over)

### Agent Factory

The `agent_factory.py` module is responsible for creating and configuring the agent:

- Creates a Semantic Kernel instance with Azure OpenAI integration
- Loads and registers all necessary plugins
- Configures the agent with appropriate settings:
  - Temperature for controlled response generation
  - Top-p sampling for diverse responses
  - Auto function choice behavior for optimal function calling
- Loads workflow definitions from text files to guide the conversation flow

### Workflow Definition

The `SupportTicketAgent` uses text-based definitions to guide the chatbot's conversational flow:

- **Text-Based Definition**: Uses a numbered step format with branching logic
- **Step-Based Approach**: Each step represents a distinct part of the conversation
- **Decision Points**: Contains conditional logic for conversation paths
- **Function Calls**: Specifies when to call which functions with what parameters

The workflow definition (in `support-ticket-workflow.txt`) outlines a complete process for:

1. Initial options presentation
2. Support ticket creation (manual or template-based)
3. Support ticket updating
4. Action item creation and management
5. Historical ticket searching

For more details on the conversation workflow, refer to the [workflow diagrams](/docs/architecture/support-ticket-workflow.md).

### Plugins System

The chatbot uses a modular plugin architecture for business logic:

> **Note:** In this sample, all plugins use mocked services with in-memory data storage for demonstration purposes. A production implementation would replace these with connectors to your actual enterprise systems.

#### Ticket Management Plugin

- Core functions: `create_support_ticket`, `get_support_ticket`, `update_support_ticket`, `search_tickets`
- Manages the lifecycle of support tickets with validation and storage
- Each function is annotated with detailed parameter descriptions for the LLM

#### Action Item Plugin

- Core functions: `create_action_item`, `get_action_item`, `update_action_item`, `list_action_items`
- Handles tasks associated with support tickets
- Maintains relationships between action items and their parent tickets

#### Reference Data Plugin

- Provides validation and lookup data for departments, priorities, and status values
- Ensures data consistency across the system

#### Common Plugin

- Contains utility functions like `start_over` and `explain_workflow`
- Supports the conversational flow with helper functions

### Data Models

The system uses strongly-typed data models for business objects:

- **SupportTicket**: Represents a support request with fields like:
  - `ticket_id`, `title`, `department_code`, `priority`
  - `workflow_type`, `description`, `expected_outcome`
  - `resolution`, `customer_visible`, timestamps

- **ActionItem**: Represents a task within a ticket:
  - `item_id`, `ticket_id`, `title`, `assignee`
  - `status`, `due_date`, timestamps

- **Enum Types**: Structured types for consistent values:
  - `TicketPriority`: Low, Medium, High, Critical
  - `TicketWorkflowType`: Standard, Expedited
  - `Department`: HR, IT, Finance, etc.

## Component Interactions

1. The user provides input to the `SupportTicketAgent` via the `chat()` method
2. The agent forwards the input to the Semantic Kernel agent
3. The LLM processes the input using the workflow definition as guidance
4. The LLM generates a response that may include function calls
5. The agent processes any function calls by invoking the appropriate plugins
6. The plugins interact with the data models and return results
7. The agent forwards the final response back to the user

## Integration with Azure OpenAI

The system integrates with Azure OpenAI through Semantic Kernel's `AzureChatCompletion` service:

- Uses the deployment specified in the environment configuration
- Leverages function calling capabilities of advanced models
- Configures appropriate temperature and sampling parameters

## Extending the Architecture

The system is designed for extensibility:

1. **Add New Plugins**: Create new Python classes with `@kernel_function` decorators
2. **Extend Data Models**: Add fields or create new model classes
3. **Modify Workflow**: Update the text-based workflow definition
4. **Add New Agent Types**: Use the agent factory pattern to create specialized agents
