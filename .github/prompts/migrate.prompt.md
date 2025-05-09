# Line-of-Business Chatbot Migration

This repository showcases the implementation of a Line-of-business (LOB) chatbot including an evaluation framework as described in the [README](../../README.md). Your task is to help the user migrate the Support Ticket Management System sample code to another business use case that the user will specify.

## Analyze Current Implementation

First, thoroughly analyze the existing Support Ticket Management System implementation to understand:

1. **Core Architecture**:
   - Review the architecture documentation in `docs/architecture/support-ticket-chatbot-architecture.md`
   - Understand the workflow pattern in `docs/architecture/support-ticket-workflow.md`
   - Analyze plugin structures in `app/chatbot/plugins/support_ticket_system/`

2. **Data Models**:
   - Examine ticket data models in `app/chatbot/data_models/ticket_models.py`
   - Identify key entities and their relationships

3. **Workflows**:
   - Study workflow definition in `app/chatbot/workflow-definitions/support-ticket-workflow.txt`
   - Understand conversational flow patterns

4. **Evaluation Framework**:
   - Review the evaluation approach in `docs/evaluation/evaluation-framework.md`
   - Understand ground-truth data formats in `evaluation/chatbot/ground-truth/`

## Ask for Target Use Case

Second, ask the user to provide details about their target use case

## Create Migration Plan

Finally, based on the user's requirements, create a detailed migration plan organized into phases. After presenting the plan, wait for the user's confirmation before proceeding with any implementation.

## Important Guidelines

1. Maintain the same architectural pattern but adapt it to the new domain
2. Preserve the evaluation methodology while adapting it to new requirements
3. Follow best practices for Python coding as per user's instructions
4. Ensure backward compatibility with the evaluation framework where possible
