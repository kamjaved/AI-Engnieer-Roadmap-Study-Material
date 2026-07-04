from enum import Enum

from pydantic import BaseModel, Field


class IssuePriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class IssueState(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"


class IssueCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=5, max_length=1000)
    priority: IssuePriority = IssuePriority.LOW
    state: IssueState = IssueState.OPEN


class IssueUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=1000)
    priority: IssuePriority | None = None
    state: IssueState | None = None


class IssueResponse(BaseModel):
    id: str
    title: str
    description: str
    priority: IssuePriority
    state: IssueState
