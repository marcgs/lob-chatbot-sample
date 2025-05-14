# Dummy Data for Support Ticket Chatbot

This directory contains the dummy data files used for generating evaluation scenarios for the support ticket chatbot.

## Files

- `dummy_support_tickets.csv`: Contains the support ticket data
- `dummy_action_items.csv`: Contains the action item data associated with support tickets
- `generate_eval_dataset.py`: Original script (for reference)
- `test_scenarios_templates.json`: Templates for test scenarios with function call expectations

## Data Schema

### Support Tickets

Each support ticket has the following fields:

- Support Ticket ID: A unique identifier (format: TKT-2XXXX)
- Title: A brief description of the issue
- Department Code: The code for the department responsible (IT, HR, DEV, etc.)
- Priority: The urgency level (Low, Medium, High, Critical)
- Workflow Type: The process type (Standard, Expedited)
- Description: Detailed explanation of the issue
- Expected Outcome: What should happen when the issue is resolved
- Resolution: How the issue was resolved (may be empty)
- Customer Visible: Whether the ticket is visible to customers (True/False)

### Action Items

Each action item has the following fields:

- Action Item ID: A unique identifier (format: ACT-XXX)
- Parent Ticket ID: The ID of the ticket this action item belongs to
- Title: A brief description of the action
- Assignee: The person assigned to the action
- Status: The current status (Open, In Progress, Closed, etc.)
- Due Date: When the action should be completed

## Data Relationships

- A support ticket can have zero, one, or multiple action items
- Each action item is associated with exactly one support ticket

## Field References in Templates

In the test scenario templates, fields are referenced using the following pattern:

- Ticket fields: `{ticket.field_name}`
  Example: `{ticket.title}`, `{ticket.priority}`, etc.

- Action item fields: `{action.field_name}`
  Example: `{action.title}`, `{action.assignee}`, etc.

This pattern allows the templates to clearly reference which object a field belongs to, especially in scenarios where both tickets and actions are present.

Each action item has the following fields:

- Action Item ID: A unique identifier (format: ACT-XXX)
- Parent Ticket ID: The ID of the support ticket this action item belongs to
- Title: A brief description of the task
- Assignee: The person responsible for the task
- Status: Current state (Open, In Progress, Completed, etc.)
- Due Date: When the task should be completed (format: YYYY-MM-DD)

## Data Generation

The script `generate_eval_dataset.py` combines these two data files to create evaluation scenarios. It matches action items with their parent tickets to create comprehensive test cases.

### Field Naming Pattern

To clearly indicate which object a field belongs to, the script uses a nested object approach with placeholders in this format:

- Ticket fields: `{ticket.field_name}` (e.g., `{ticket.title}`, `{ticket.priority}`)
- Action item fields: `{action.field_name}` (e.g., `{action.title}`, `{action.assignee}`)

These placeholders can be used in test scenario templates to create dynamic test cases.