# Support Ticket Management System Workflow

This document provides a visual representation of the workflows implemented in the Support Ticket Management System, showing how users interact with the system and how data flows between components.

## Main Workflow Overview

The diagram below illustrates the primary workflow paths in the Support Ticket Management System:

```mermaid
flowchart TD
    Start([Start Conversation]) --> InitialOptions{Choose Option}
    
    %% Create Ticket Flow
    InitialOptions -->|Create Ticket| ChooseTicketMethod{Choose Method}
    ChooseTicketMethod -->|Manual Entry| CollectTicketInfo[Collect Ticket Information]
    ChooseTicketMethod -->|Lookup by ID| EnterTicketID[Enter Ticket ID]
    ChooseTicketMethod -->|Search| EnterSearchTerms[Enter Search Terms]
    
    EnterTicketID --> RetrieveTicket[Retrieve Ticket]
    EnterSearchTerms --> SearchResults{Review Results}
    SearchResults -->|Select Ticket| RetrieveTicket
    SearchResults -->|Create New| CollectTicketInfo
    
    RetrieveTicket --> EditTicketInfo[Edit Ticket Information]
    CollectTicketInfo --> ConfirmTicket{Confirm Creation}
    EditTicketInfo --> ConfirmTicket
    
    ConfirmTicket -->|Confirm| CreateTicket[Create Ticket]
    ConfirmTicket -->|Revise| CollectTicketInfo
    
    CreateTicket --> Success([Success])
    
    %% Update Ticket Flow
    InitialOptions -->|Update Ticket| IdentifyTicket{Identify Ticket}
    IdentifyTicket -->|Enter ID| EnterTicketIDUpdate[Enter Ticket ID]
    IdentifyTicket -->|Search| EnterSearchTermsUpdate[Enter Search Terms]
    
    EnterTicketIDUpdate --> RetrieveTicketUpdate[Retrieve Ticket]
    EnterSearchTermsUpdate --> SearchResultsUpdate{Review Results}
    SearchResultsUpdate -->|Select Ticket| RetrieveTicketUpdate
    
    RetrieveTicketUpdate --> SelectFieldsToUpdate[Select Fields to Update]
    SelectFieldsToUpdate --> UpdateTicketInfo[Update Ticket Information]
    UpdateTicketInfo --> ConfirmUpdate{Confirm Update}
    
    ConfirmUpdate -->|Confirm| SaveUpdate[Save Update]
    ConfirmUpdate -->|Revise| UpdateTicketInfo
    
    SaveUpdate --> SuccessUpdate([Success])
    
    %% Create Action Item Flow
    InitialOptions -->|Create Action Item| IdentifyTicketForAction{Identify Parent Ticket}
    IdentifyTicketForAction -->|Enter ID| EnterTicketIDAction[Enter Ticket ID]
    IdentifyTicketForAction -->|Search| EnterSearchTermsAction[Enter Search Terms]
    
    EnterTicketIDAction --> RetrieveTicketAction[Retrieve Ticket]
    EnterSearchTermsAction --> SearchResultsAction{Review Results}
    SearchResultsAction -->|Select Ticket| RetrieveTicketAction
    
    RetrieveTicketAction --> CollectActionInfo[Collect Action Item Information]
    CollectActionInfo --> ConfirmAction{Confirm Creation}
    
    ConfirmAction -->|Confirm| CreateAction[Create Action Item]
    ConfirmAction -->|Revise| CollectActionInfo
    
    CreateAction --> SuccessAction([Success])
    
    %% Update Action Item Flow
    InitialOptions -->|Update Action Item| IdentifyAction{Identify Action Item}
    IdentifyAction -->|Enter ID| EnterActionID[Enter Action ID]
    IdentifyAction -->|Find via Ticket| SelectTicketForAction[Select Parent Ticket]
    
    EnterActionID --> RetrieveAction[Retrieve Action Item]
    SelectTicketForAction --> ListActions[List Action Items]
    ListActions --> SelectAction[Select Action Item]
    SelectAction --> RetrieveAction
    
    RetrieveAction --> SelectFieldsToUpdateAction[Select Fields to Update]
    SelectFieldsToUpdateAction --> UpdateActionInfo[Update Action Information]
    UpdateActionInfo --> ConfirmActionUpdate{Confirm Update}
    
    ConfirmActionUpdate -->|Confirm| SaveActionUpdate[Save Update]
    ConfirmActionUpdate -->|Revise| UpdateActionInfo
    
    SaveActionUpdate --> SuccessActionUpdate([Success])
```

## Component Interaction During Ticket Creation

The sequence diagram below shows how system components interact during ticket creation:

```mermaid
sequenceDiagram
    actor User
    participant Chat as Chat Interface
    participant Agent as SupportTicketAgent
    participant LLM as LLM (Azure OpenAI)
    participant TicketPlugin as Ticket Management Plugin
    participant RefPlugin as Reference Data Plugin
    
    User->>Chat: Request to create ticket
    Chat->>Agent: Forward request
    Agent->>LLM: Send user request + workflow definition
    
    Note over Agent,LLM: LLM has the workflow definition as part of its instructions
    
    LLM->>Agent: Present ticket creation options
    Agent->>Chat: Display options
    Chat->>User: Show options
    
    User->>Chat: Select manual creation
    Chat->>Agent: Forward selection
    Agent->>LLM: Send user selection
    
    LLM->>Agent: Request ticket info
    Agent->>Chat: Ask for ticket title
    Chat->>User: Prompt for title
    
    User->>Chat: Provide title
    Chat->>Agent: Forward input
    
    Note over Agent,LLM: This sequence repeats for all required fields
    
    Agent->>LLM: Send collected data
    LLM->>Agent: Request department options
    Agent->>RefPlugin: Get department list
    RefPlugin->>Agent: Return departments (mocked data)
    Agent->>Chat: Request department selection
    Chat->>User: Show department options
    
    User->>Chat: Select department
    Chat->>Agent: Forward selection
    
    Agent->>LLM: Send updated data
    LLM->>Agent: Request confirmation
    Agent->>Chat: Ask for confirmation
    Chat->>User: Show summary and confirm
    
    User->>Chat: Confirm creation
    Chat->>Agent: Forward confirmation
    
    Agent->>LLM: Send confirmation
    LLM->>Agent: Call createSupportTicket()
    Agent->>TicketPlugin: createSupportTicket()
    TicketPlugin->>Agent: Return success + ID
    
    Agent->>LLM: Send function result
    LLM->>Agent: Generate success message
    Agent->>Chat: Send success message
    Chat->>User: Display success message
```

## Data Flow Between Components

The diagram below illustrates how data flows between system components. Note that this sample implementation uses in-memory data stores with mocked services for demonstration purposes. In a production environment, you would replace these with connections to actual enterprise systems:

```mermaid
flowchart TD
    subgraph UI["User Interface"]
        ChatInterface["Chat Interface"]
    end
    
    subgraph Core["Core Components"]
        Agent["SupportTicketAgent"]
        LLM["LLM (Azure OpenAI)"]
        WorkflowDef["Workflow Definition File"]
    end
    
    subgraph Plugins["Plugin System"]
        TicketPlugin["Ticket Management Plugin"]
        ReferencePlugin["Reference Data Plugin"]
        ActionPlugin["Action Item Plugin"]
        CommonPlugin["Common Plugin"]
    end
    
    subgraph Data["In-Memory Data"]
        TicketData["Mocked Ticket Data"]
        ActionData["Mocked Action Item Data"]
        ReferenceData["Mocked Reference Data"]
    end
    
    %% UI to Core flow
    ChatInterface -- "User Input" --> Agent
    Agent -- "Responses" --> ChatInterface
    
    %% Core interactions
    Agent -- "Send requests" --> LLM
    LLM -- "Generate responses" --> Agent
    WorkflowDef -- "Loaded as instructions" --> LLM
    
    %% Core to Plugin flow
    Agent -- "Function Calls" --> TicketPlugin
    Agent -- "Function Calls" --> ReferencePlugin
    Agent -- "Function Calls" --> ActionPlugin
    Agent -- "Function Calls" --> CommonPlugin
    
    %% Plugin to Data flow
    TicketPlugin <-- "In-Memory Operations" --> TicketData
    ActionPlugin <-- "In-Memory Operations" --> ActionData
    ReferencePlugin <-- "Read Operations" --> ReferenceData
    ReferencePlugin <-- "Search Operations" --> TicketData
```

These diagrams provide a visual representation of how the Support Ticket Management System works, showing both the user interaction flows and the internal component interactions.