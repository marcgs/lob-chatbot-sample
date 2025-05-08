# Support Ticket Chatbot User Guide

## Introduction

The Support Ticket Management Chatbot is designed to showcase how to implement a conversational AI assistant that helps users manage support tickets and their related action items. This guide explains the use case, how to interact with the system, and the various workflows available.

## Use Case Overview

The Support Ticket Chatbot simulates a help desk environment for an organization. It allows:

- **Creating and tracking support tickets**: Users can report issues that need to be addressed
- **Managing action items**: Tasks that need to be completed to resolve a ticket
- **Searching historical data**: Finding previous tickets for reference or reuse

This system demonstrates how a chatbot can facilitate these processes through natural language interactions, making it more efficient than traditional form-based interfaces.

## Key Concepts

### Support Ticket

A support ticket represents an issue that needs to be addressed. Each ticket includes:

- **Ticket ID**: A unique identifier
- **Title**: A brief description of the issue
- **Department**: The organizational unit responsible for addressing the ticket
- **Priority**: The urgency level (e.g., Low, Medium, High, Critical)
- **Workflow Type**: The process type to follow (e.g., Standard, Expedited)
- **Description**: Detailed explanation of the issue
- **Expected Outcome**: What should happen when the issue is resolved
- **Resolution**: How the issue was actually resolved
- **Customer Visible**: Whether the ticket details can be shared with customers

### Action Item

Action items are specific tasks that need to be completed within a support ticket. Each action item includes:

- **ID**: A unique identifier
- **Parent Ticket ID**: The ticket to which this action belongs
- **Title**: A brief description of the task
- **Assignee**: The person responsible for completing the task
- **Status**: Current state (e.g., Open, In Progress, Completed)
- **Due Date**: When the task should be completed

## Interacting with the Chatbot

The chatbot guides you through various workflows using natural language. Here are the main interactions:

### Initial Options

When you start a conversation, the chatbot presents four main options:

1. Create a new support ticket
2. Update information on an existing ticket
3. Create a new action item for an existing ticket
4. Update an existing action item

### Creating a Support Ticket

The chatbot offers three ways to create a ticket:

1. **Manual Entry**: Directly provide all required information
2. **Lookup by ID**: Reference an existing ticket by its ID to use as a template
3. **Search**: Use keywords to search for similar past tickets as references

The chatbot will guide you through collecting all necessary information and confirm before creating the ticket.

### Updating Ticket Information

Similar to creation, you can update a ticket by:

1. **Manual Entry**: Directly provide the information to update
2. **Lookup by ID**: Find the ticket to update
3. **Search**: Find a ticket using keywords

### Managing Action Items

Action items can be created or updated within the context of a support ticket. The chatbot will help you specify details like task description, assignee, and due date.

## Sample Conversations

### Creating a Support Ticket Sample

#### Manual Entry

```text
Bot: Hello! How can I assist you today with support ticket management? Here are the options you can choose from:

- Create a new support ticket.
- Update an existing support ticket.
- Create a new action item for an existing ticket.
- Update an existing action item.
- Search for historical tickets.
Please let me know which option you'd like to proceed with!

User: I need to create a new support ticket

Bot: I'd be happy to help you create a new support ticket. How would you like to provide the information?
     1. Enter ticket information manually
     2. Look up a ticket by ID to use as a template
     3. Search for similar past tickets

User: I'll enter the information manually

Bot: Great! Let's start creating your support ticket.
     What should be the title of this support ticket? (A brief description of the issue)

User: Email service outage in marketing department

Bot: Thanks. Which department is responsible for addressing this ticket?
     Available departments: [IT Support, HR, Finance, Marketing, Sales, Customer Service, Operations]

User: IT Support

Bot: What priority level would you assign to this ticket?
     Options: Low, Medium, High, Critical

User: High

Bot: What type of workflow should be used for this ticket?
     Options: Standard, Expedited

User: Standard

Bot: Please provide a detailed description of the issue:

User: The marketing department reports they cannot send or receive emails since 9 AM this morning. 
     All 15 team members are affected. They've already tried restarting their computers.

Bot: What is the expected outcome once this ticket is resolved?

User: All marketing team members should be able to send and receive emails normally.

Bot: Is this ticket information visible to customers? (Yes/No)

User: No

Bot: Here's a summary of the support ticket you're creating:
     Title: Email service outage in marketing department
     Department: IT Support
     Priority: High
     Workflow Type: Standard
     Description: The marketing department reports they cannot send or receive emails since 9 AM this morning. All 15 team members are affected. They've already tried restarting their computers.
     Expected Outcome: All marketing team members should be able to send and receive emails normally.
     Customer Visible: No
     
     Would you like to create this ticket? (Yes/No)

User: Yes

Bot: Successfully created ticket T-12345: "Email service outage in marketing department"
     What would you like to do next?
     1. Create an action item for this ticket
     2. Update this ticket
     3. Create another ticket
     4. Exit

User: Create an action item for this ticket

Bot: I'll help you create an action item for ticket T-12345. What should be the title of this action item?

User: Restart exchange server

Bot: Who should be assigned to this action item?

User: John Smith

Bot: What's the due date for this action item? (Format: YYYY-MM-DD)

User: 2025-05-07

Bot: Here's a summary of the action item:
     Title: Restart exchange server
     Assignee: John Smith
     Due Date: 2025-05-07
     Status: Open
     Parent Ticket: T-12345 (Email service outage in marketing department)
     
     Would you like to create this action item? (Yes/No)

User: Yes

Bot: Successfully created action item AI-5678 for ticket T-12345.
     What would you like to do next?
```

#### Using a Template

```text
Bot: Hello! How can I assist you today with support ticket management? Here are the options you can choose from:

- Create a new support ticket.
- Update an existing support ticket.
- Create a new action item for an existing ticket.
- Update an existing action item.
- Search for historical tickets.
Please let me know which option you'd like to proceed with!

User: I need to report a new issue

Bot: I'd be happy to help you create a new support ticket. How would you like to provide the information?
     1. Enter ticket information manually
     2. Look up a ticket by ID to use as a template
     3. Search for similar past tickets

User: I want to use a template. Can I look up ticket T-12240?

Bot: I found ticket T-12240: "Network connectivity issues in Finance department"
     Would you like to use this ticket as a template for your new ticket? (Yes/No)

User: Yes

Bot: I'll use T-12240 as a template. Let me know what information you'd like to change.
     Current title: "Network connectivity issues in Finance department"
     Would you like to change the title? (Yes/No)

User: Yes, change it to "Network connectivity issues in Sales department"

Bot: Updated title to: "Network connectivity issues in Sales department"
     Current department: IT Support
     Would you like to change the department? (Yes/No)

User: No

Bot: Current priority: High
     Would you like to change the priority? (Yes/No)

User: No

// ... conversation continues with the bot confirming each field ...
```

#### Using Search

```text
Bot: Hello! How can I assist you today with support ticket management? Here are the options you can choose from:

- Create a new support ticket.
- Update an existing support ticket.
- Create a new action item for an existing ticket.
- Update an existing action item.
- Search for historical tickets.
Please let me know which option you'd like to proceed with!

User: I need to create a ticket for printer issues

Bot: I'd be happy to help you create a new support ticket. How would you like to provide the information?
     1. Enter ticket information manually
     2. Look up a ticket by ID to use as a template
     3. Search for similar past tickets

User: Search for similar tickets

Bot: What keywords would you like to search for in past tickets?

User: printer not working

Bot: I found the following matching tickets:
     1. T-11892: "Printer in HR department not printing color documents"
     2. T-10576: "Marketing department printer offline"
     3. T-09234: "Sales team printer paper jam issues"
     
     Would you like to use any of these tickets as a template? If so, enter the number.

User: 2

// ... conversation continues with the bot using T-10576 as a template ...
```

### Updating a Support Ticket Sample

```text
Bot: Hello! How can I assist you today with support ticket management? Here are the options you can choose from:

- Create a new support ticket.
- Update an existing support ticket.
- Create a new action item for an existing ticket.
- Update an existing action item.
- Search for historical tickets.
Please let me know which option you'd like to proceed with!

User: I need to update a ticket status

Bot: I can help you update an existing support ticket. Do you know the ticket ID?

User: Yes, T-12345

Bot: I found ticket T-12345: "Email service outage in marketing department"
     What information would you like to update?
     1. Title
     2. Department
     3. Priority
     4. Workflow Type
     5. Description
     6. Expected Outcome
     7. Resolution
     8. Customer Visible Status
     9. Ticket Status

User: Ticket Status

Bot: The current status of this ticket is: Open
     What would you like to change the status to?
     Options: Open, In Progress, Resolved, Closed

User: In Progress

Bot: I'll update the status to "In Progress". Would you like to add any notes about this update?

User: John is currently working on the exchange server issue

Bot: Here's a summary of the update:
     Ticket: T-12345 (Email service outage in marketing department)
     Change: Status updated from "Open" to "In Progress"
     Notes: John is currently working on the exchange server issue
     
     Would you like to apply this update? (Yes/No)

User: Yes

Bot: Successfully updated ticket T-12345. The status is now "In Progress".
```

### Creating an Action Item Sample

```text
Bot: Hello! How can I assist you today with support ticket management? Here are the options you can choose from:

- Create a new support ticket.
- Update an existing support ticket.
- Create a new action item for an existing ticket.
- Update an existing action item.
- Search for historical tickets.
Please let me know which option you'd like to proceed with!

User: I need to add a new task to ticket T-12345

Bot: I'll help you create an action item for ticket T-12345: "Email service outage in marketing department".
     What should be the title of this action item?

User: Check network firewall settings

Bot: Who should be assigned to this action item?

User: Sarah Johnson

Bot: What's the due date for this action item? (Format: YYYY-MM-DD)

User: 2025-05-08

Bot: Here's a summary of the action item:
     Title: Check network firewall settings
     Assignee: Sarah Johnson
     Due Date: 2025-05-08
     Status: Open
     Parent Ticket: T-12345 (Email service outage in marketing department)
     
     Would you like to create this action item? (Yes/No)

User: Yes

Bot: Successfully created action item AI-5679 for ticket T-12345.
```

### Updating an Action Item Sample

```text
Bot: Hello! How can I assist you today with support ticket management? Here are the options you can choose from:

- Create a new support ticket.
- Update an existing support ticket.
- Create a new action item for an existing ticket.
- Update an existing action item.
- Search for historical tickets.
Please let me know which option you'd like to proceed with!

User: I need to update action item AI-5678

Bot: I found action item AI-5678: "Restart exchange server" (for ticket T-12345)
     What would you like to update?
     1. Title
     2. Assignee
     3. Due Date
     4. Status

User: Status

Bot: The current status is: Open
     What would you like to change the status to?
     Options: Open, In Progress, Completed, Cancelled

User: Completed

Bot: I'll update the status to "Completed". Would you like to add any notes about this update?

User: Server restarted successfully at 10:30 AM

Bot: Here's a summary of the update:
     Action Item: AI-5678 (Restart exchange server)
     Change: Status updated from "Open" to "Completed"
     Notes: Server restarted successfully at 10:30 AM
     
     Would you like to apply this update? (Yes/No)

User: Yes

Bot: Successfully updated action item AI-5678. The status is now "Completed".
```

## Best Practices

1. **Be specific**: Provide clear, detailed information to get the most accurate help
2. **Use references**: When possible, reference existing tickets to maintain consistency
3. **Confirm details**: Always review information before final submission
4. **Use natural language**: The chatbot understands conversational requests

## Conclusion

The Support Ticket Management System demonstrates how conversational AI can streamline support processes. Through natural language interactions, users can efficiently create and manage tickets without navigating complex forms or interfaces.