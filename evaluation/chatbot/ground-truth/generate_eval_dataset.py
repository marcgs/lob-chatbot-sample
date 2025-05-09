"""
Script to generate chatbot evaluation dataset from scenario templates and dummy business data.
"""
import argparse
import json
import csv
import random
from pathlib import Path
from typing import Any

# System prompt template (matches support_ticket_eval_dataset.json style)
SYSTEM_PROMPT_TEMPLATE = """
You are simulating a human user interacting with a chatbot assistant.

Your goal is to complete a specific task by conversing naturally with the assistant.
Behave like a non-technical user who understands the task, but not the internal workings of the system.
You have access to some business data relevant to your task. Use it when appropriate during the conversation.

Follow these rules:
- Never correct the assistant or point out mistakes.
- You are not allowed to change the inputs proposed by the assistant.
- Stay focused on the task but allow for slight variability in how you express yourself.
- Use the business data as needed, but do not mention that it was \"given\" to you.
- Do not modify the business data you are given.
- Speak naturally, as if you are recalling or referencing information you know.
- Once your task is completed, you must end the conversation by saying \"the session is finished\".
- Your goal is achieved when the assistant has completed the task and you have confirmed it.

Here is the business data you can use during the conversation:
{business_data}

Here is your task:
{user_instructions}

Begin the conversation. Respond as the user.
"""

def load_templates(path: Path) -> list[dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_business_data(path: Path) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def format_business_data(data: dict[str, str]) -> str:
    # Group fields for display (support ticket, action item, etc.)
    ticket_fields = [
        "title", "department_code", "priority", "workflow_type", "description", "expected_outcome"
    ]
    action_fields = ["parent_ticket_id", "assignee", "due_date"]
    ticket = "\n".join(f"- {k}: \"{data[k]}\"" for k in ticket_fields if data.get(k))
    action = "\n".join(f"- {k}: \"{data[k]}\"" for k in action_fields if data.get(k))
    out = []
    if ticket:
        out.append("Support Ticket data:\n" + ticket)
    if action:
        out.append("Action Item data:\n" + action)
    return "\n\n".join(out)

def fill_placeholders(obj: Any, data: dict[str, str]) -> Any:
    if isinstance(obj, dict):
        return {k: fill_placeholders(v, data) for k, v in obj.items()}
    if isinstance(obj, list):
        return [fill_placeholders(v, data) for v in obj]
    if isinstance(obj, str):
        for key, value in data.items():
            obj = obj.replace(f"{{{key}}}", value)
        return obj
    return obj

def generate_dataset(
    templates: list[dict[str, Any]],
    business_data: list[dict[str, str]],
    num_cases_per_scenario: int,
) -> list[dict[str, Any]]:
    dataset = []
    for template in templates:
        for _ in range(num_cases_per_scenario):
            data = random.choice(business_data)
            filled_calls = fill_placeholders(template["expected_function_calls"], data)
            business_data_str = format_business_data(data)
            instructions = SYSTEM_PROMPT_TEMPLATE.format(
                business_data=business_data_str,
                user_instructions=template["user_instructions"]
            )
            dataset.append({
                "scenarioType": template["scenario_name"],
                "instructions": instructions,
                "task_completion_condition": template["task_completion"],
                "expected_function_calls": filled_calls
            })
    return dataset

def main():
    parser = argparse.ArgumentParser(description="Generate chatbot evaluation dataset.")
    parser.add_argument("--templates", type=Path, default=Path("evaluation/chatbot/ground-truth/test_scenarios_templates.json"))
    parser.add_argument("--business-data", type=Path, default=Path("evaluation/chatbot/ground-truth/dummy_support_ticket_data.csv"))
    parser.add_argument("--output", type=Path, default=Path("evaluation/chatbot/ground-truth/support_ticket_eval_dataset.json"))
    parser.add_argument("--cases-per-scenario", type=int, default=3)
    args = parser.parse_args()

    templates = load_templates(args.templates)
    business_data = load_business_data(args.business_data)
    dataset = generate_dataset(templates, business_data, args.cases_per_scenario)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)
    print(f"Generated {len(dataset)} test cases in {args.output}")

if __name__ == "__main__":
    main()
