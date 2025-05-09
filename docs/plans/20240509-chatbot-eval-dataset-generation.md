# Plan: 20240509-chatbot-eval-dataset-generation.md

## Phase 1: Prepare Scenario Templates
- [x] Task 1.1: Designed the structure for `test_scenarios_templates.json` to include:
  - `scenario_name`
  - `user_instructions`
  - `task_completion`
  - `expected_function_calls` (with placeholders for business data fields)
- [x] Task 1.2: Created initial scenario templates (at least 3) in `test_scenarios_templates.json` following the new structure, based on the actual capabilities and supported workflows of the chatbot implemented in `app/chatbot` (e.g., ticket creation, ticket search, action item management, ticket updates, etc.).

## Phase 2: Prepare Dummy Business Data
- [x] Task 2.1: Designed the schema for the dummy business data CSV. Field names exactly match the argument names used by the chatbot's functions (see app/chatbot/plugins/support_ticket_system/ticket_management_plugin.py and action_item_plugin.py). Example fields: title, department_code, priority, workflow_type, description, expected_outcome, parent_ticket_id, assignee, due_date, search_query, action_id.
- [x] Task 2.2: Generated a CSV file (`dummy_support_ticket_data.csv`) with 50 rows of realistic, varied dummy data.

## Phase 3: Implement Dataset Generation Script
- [ ] Task 3.1: Design and implement a Python script (`generate_eval_dataset.py`) that:
  - Reads `test_scenarios_templates.json`
  - Reads `dummy_support_ticket_data.csv`
  - For each scenario template, generates multiple test cases by injecting business data into placeholders
  - Outputs the final dataset in the same structure as `support_ticket_eval_dataset.json`
- [ ] Task 3.2: Add a system prompt template (with placeholders for business data and user instructions) to be used for each generated scenario. The script should inject the appropriate business data and user instructions into this template, following the style and structure of the `instructions` field in `support_ticket_eval_dataset.json`.
- [ ] Task 3.3: Add CLI arguments to the script for input/output file paths and number of test cases per scenario with default values (3 cases per scenarios)

## Phase 4: Validation and Documentation
- [ ] Task 4.1: Validate that the generated dataset matches the required structure and is suitable for evaluation.
- [ ] Task 4.2: Document the process and file formats in a new markdown file in `docs/evaluation/`.

## Success Criteria
- [ ] `test_scenarios_templates.json` exists and contains at least 3 scenario templates with placeholders.
- [ ] `dummy_support_ticket_data.csv` exists with 50 rows of realistic dummy data.
- [ ] `generate_eval_dataset.py` can generate a valid evaluation dataset from the templates and dummy data.
- [ ] Documentation is available describing the process, file formats, and usage instructions.
