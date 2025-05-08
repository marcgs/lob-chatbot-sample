# Constants for function call objects to reduce clutter in tests
FC_TICKET_CREATE = {
    "functionName": "TicketManagementPlugin-create_support_ticket",
    "arguments": {
        "title": "Email client crashes on startup",
        "description": "When launching the email client, it crashes immediately with an error message",
        "department": "IT",
        "priority": "High",
        "workflow_type": "Standard",
    },
}

FC_TICKET_CREATE_2 = {
    "functionName": "TicketManagementPlugin-create_support_ticket-2",
    "arguments": {
        "title": "Network connectivity issues",
        "description": "Unable to connect to the network in meeting room 4",
        "department": "IT",
        "priority": "Medium",
        "workflow_type": "Standard",
    },
}

FC_TICKET_CREATE_3 = {
    "functionName": "TicketManagementPlugin-create_support_ticket-3",
    "arguments": {
        "title": "Printer not working",
        "description": "The printer on 3rd floor is not responding to print jobs",
        "department": "Facilities",
        "priority": "Low",
        "workflow_type": "Standard",
    },
}

FC_TICKET_CREATE_DIFF_ARGS = {
    "functionName": "TicketManagementPlugin-create_support_ticket",
    "arguments": {
        "title": "some-other-title",
        "description": "some-other-description",
        "department": "some-other-department",
        "priority": "some-other-priority",
        "workflow_type": "some-other-workflow",
    },
}

FC_TICKET_CREATE_NO_ARGS = {
    "functionName": "TicketManagementPlugin-create_support_ticket",
    "arguments": {},
}

FC_TICKET_CREATE_MISSING_ARG = {
    "functionName": "TicketManagementPlugin-create_support_ticket",
    "arguments": {
        "title": "Email client crashes on startup",
        "description": "When launching the email client, it crashes immediately with an error message",
        "department": "IT",
        "priority": "High",
    },
}

FC_TICKET_CREATE_DIFF_NAME = {
    "functionName": "some-other-function",
    "arguments": {
        "title": "Email client crashes on startup",
        "description": "When launching the email client, it crashes immediately with an error message",
        "department": "IT",
        "priority": "High",
        "workflow_type": "Standard",
    },
}

FC_TICKET_CREATE_2_DIFF_ARGS = {
    "functionName": "TicketManagementPlugin-create_support_ticket-2",
    "arguments": {
        "title": "some-other-title",
        "description": "some-other-description",
        "department": "some-other-department",
        "priority": "some-other-priority",
        "workflow_type": "some-other-workflow",
    },
}

FC_COMMON_ASK_CLARIFICATION = {
    "functionName": "CommonPlugin-ask_clarification",
    "arguments": {"question": "What are you looking for?"},
}

FC_REFERENCE_DATA_GET_DEPARTMENTS = {
    "functionName": "ReferenceDataPlugin-get_departments",
    "arguments": {},
}
