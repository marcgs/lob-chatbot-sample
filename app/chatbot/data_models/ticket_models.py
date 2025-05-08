from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class TicketPriority(str, Enum):
    """Priority levels for support tickets"""

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class TicketWorkflowType(str, Enum):
    """Workflow types for support tickets"""

    STANDARD = "Standard"
    EXPEDITED = "Expedited"


class ActionItemStatus(str, Enum):
    """Status options for action items"""

    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    BLOCKED = "Blocked"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


@dataclass
class Department:
    """Department reference data model"""

    code: str
    name: str
    description: str | None = None


@dataclass
class SupportTicket:
    """
    Support Ticket data model

    Represents an issue that needs to be addressed by the support team.
    """

    ticket_id: str
    title: str
    department_code: str
    priority: TicketPriority
    workflow_type: TicketWorkflowType
    description: str
    expected_outcome: str
    resolution: str | None = None
    customer_visible: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self):
        """Set default values for timestamps if not provided"""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = self.created_at


@dataclass
class ActionItem:
    """
    Action Item data model

    Represents a specific task that needs to be completed to resolve a ticket.
    """

    action_id: str
    parent_ticket_id: str
    title: str
    assignee: str
    status: ActionItemStatus = ActionItemStatus.OPEN
    due_date: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self):
        """Set default values for timestamps if not provided"""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = self.created_at
