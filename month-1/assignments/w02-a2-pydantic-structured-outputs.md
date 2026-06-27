# Assignment 2.2: Pydantic for Structured LLM Outputs

> **Week 2** | [Back to Week 2 Plan](../week-2.md)

## Title
**Pydantic for Structured LLM Outputs** -- Turning Messy AI Text into Clean Data

## Objective
Master Pydantic v2 by building real-world models for parsing LLM outputs: meeting notes extraction, resume parsing, and API error handling. Learn to generate JSON Schema from your models and integrate them with OpenAI's structured output feature. This is the bridge between "AI returns text" and "AI returns typed data my app can use."

## Difficulty
Beginner-Intermediate

## Estimated Time
2-3 hours

## Prerequisites
- Python 3.10+ installed
- Basic understanding of Python dataclasses or TypeScript interfaces (you know this from React/TypeScript)
- Install dependencies:
```bash
pip install "pydantic>=2.0" openai rich
```
- **Optional**: OpenAI API key (for the structured outputs integration in Step 6)

## Why This Matters
Think of Pydantic as TypeScript's type system for Python, but enforced at runtime. In GenAI engineering:
- LLMs return unstructured text. Your app needs structured data.
- Pydantic validates that the LLM output matches the shape you expect.
- OpenAI and other providers now support "structured outputs" -- you send a JSON Schema, they guarantee the response matches. Pydantic generates that schema.
- Every FastAPI endpoint (your next assignment) uses Pydantic models for request/response validation.

Coming from TypeScript, you already think in interfaces and types. Pydantic will feel natural.

---

## Detailed Instructions

### Step 1: Project Setup (5 min)

```
pydantic-structured-outputs/
  models/
    __init__.py
    meeting.py
    resume.py
    errors.py
  parsers/
    __init__.py
    meeting_parser.py
    resume_parser.py
  schemas/          # Generated JSON schemas go here
  examples/         # Sample input data
  main.py
  pyproject.toml
```

### Step 2: Meeting Notes Extraction Models (30 min)

In `models/meeting.py`, define models that can parse raw meeting transcripts into structured data:

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime, date, time
from enum import Enum


class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Attendee(BaseModel):
    """A meeting participant."""
    name: str = Field(..., min_length=1, description="Full name of the attendee")
    email: str | None = Field(None, description="Email address if mentioned")
    role: str | None = Field(None, description="Job title or role if mentioned")
    was_present: bool = Field(True, description="Whether the person actually attended")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str | None) -> str | None:
        if v is not None and "@" not in v:
            raise ValueError("Invalid email format")
        return v


class ActionItem(BaseModel):
    """A task assigned during the meeting."""
    description: str = Field(..., min_length=5, description="What needs to be done")
    assignee: str = Field(..., description="Person responsible")
    due_date: date | None = Field(None, description="Deadline if mentioned")
    priority: Priority = Field(Priority.MEDIUM, description="Urgency level")
    status: str = Field("pending", description="Current status")

    @field_validator("description")
    @classmethod
    def description_must_be_actionable(cls, v: str) -> str:
        """Ensure the description starts with a verb or is clearly actionable."""
        # Simple heuristic: just ensure it's not too vague
        vague_terms = ["stuff", "things", "etc", "misc"]
        if v.lower().strip() in vague_terms:
            raise ValueError(
                "Action item description is too vague. Be specific."
            )
        return v


class Decision(BaseModel):
    """A decision made during the meeting."""
    description: str = Field(..., description="What was decided")
    made_by: str | None = Field(None, description="Who made or proposed the decision")
    context: str | None = Field(None, description="Why this decision was made")
    dissenting_opinions: list[str] = Field(
        default_factory=list,
        description="Any disagreements or alternative views"
    )


class MeetingNotes(BaseModel):
    """Complete structured meeting notes."""
    title: str = Field(..., description="Meeting title or topic")
    date: date = Field(..., description="When the meeting occurred")
    start_time: time | None = Field(None, description="Meeting start time")
    end_time: time | None = Field(None, description="Meeting end time")
    attendees: list[Attendee] = Field(..., min_length=1)
    summary: str = Field(
        ..., min_length=20, max_length=500,
        description="Brief summary of the meeting"
    )
    action_items: list[ActionItem] = Field(default_factory=list)
    decisions: list[Decision] = Field(default_factory=list)
    key_discussion_points: list[str] = Field(default_factory=list)
    follow_up_meeting_needed: bool = Field(False)
    raw_transcript: str | None = Field(
        None, exclude=True,
        description="Original transcript (excluded from serialization)"
    )

    @model_validator(mode="after")
    def validate_assignees_are_attendees(self) -> "MeetingNotes":
        """Ensure all action item assignees were in the meeting."""
        attendee_names = {a.name.lower() for a in self.attendees}
        for item in self.action_items:
            if item.assignee.lower() not in attendee_names:
                raise ValueError(
                    f"Action item assignee '{item.assignee}' "
                    f"is not in the attendee list"
                )
        return self
```

Now test it with sample data. Create `examples/meeting_raw.json`:
```json
{
  "title": "Q4 Product Roadmap Review",
  "date": "2024-10-15",
  "start_time": "10:00",
  "end_time": "11:30",
  "attendees": [
    {"name": "Sarah Chen", "role": "Product Manager", "was_present": true},
    {"name": "Mike Johnson", "email": "mike@company.com", "role": "Tech Lead"},
    {"name": "Lisa Park", "role": "Designer", "was_present": false}
  ],
  "summary": "Reviewed Q4 roadmap priorities, decided to defer the analytics dashboard to Q1, and agreed to ship the new onboarding flow by November 15th.",
  "action_items": [
    {
      "description": "Create technical spec for new onboarding flow",
      "assignee": "Mike Johnson",
      "due_date": "2024-10-22",
      "priority": "high"
    },
    {
      "description": "Design mockups for simplified settings page",
      "assignee": "Lisa Park",
      "due_date": "2024-10-25",
      "priority": "medium"
    }
  ],
  "decisions": [
    {
      "description": "Defer analytics dashboard to Q1 2025",
      "made_by": "Sarah Chen",
      "context": "Team bandwidth is fully allocated to onboarding improvements"
    }
  ],
  "key_discussion_points": [
    "Current onboarding has 40% drop-off at step 3",
    "Analytics dashboard needs backend changes that conflict with Q4 timeline"
  ]
}
```

Write code that loads this JSON and validates it:
```python
import json
from models.meeting import MeetingNotes

with open("examples/meeting_raw.json") as f:
    data = json.load(f)

# This will validate everything
notes = MeetingNotes.model_validate(data)
print(notes.model_dump_json(indent=2))
```

### Step 3: Resume Parsing Models (30 min)

In `models/resume.py`, build models for extracting structured data from resumes:

```python
from pydantic import BaseModel, Field, field_validator, HttpUrl
from datetime import date
from enum import Enum


class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class Skill(BaseModel):
    name: str
    level: SkillLevel | None = None
    years_of_experience: float | None = Field(None, ge=0, le=50)


class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    gpa: float | None = Field(None, ge=0.0, le=4.0)

    @model_validator(mode="after")
    def end_after_start(self) -> "Education":
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValueError("end_date must be after start_date")
        return self


class Experience(BaseModel):
    company: str
    title: str
    start_date: date | None = None
    end_date: date | None = Field(
        None, description="None means current position"
    )
    description: str | None = None
    achievements: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)

    @property
    def is_current(self) -> bool:
        return self.end_date is None

    @field_validator("achievements")
    @classmethod
    def achievements_should_be_specific(cls, v: list[str]) -> list[str]:
        for achievement in v:
            if len(achievement) < 10:
                raise ValueError(
                    f"Achievement too brief: '{achievement}'. "
                    "Use specific, measurable descriptions."
                )
        return v


class Resume(BaseModel):
    """Complete structured resume."""
    name: str
    email: str | None = None
    phone: str | None = None
    location: str | None = None
    website: str | None = None
    linkedin: str | None = None
    github: str | None = None
    summary: str | None = Field(
        None, max_length=1000,
        description="Professional summary or objective"
    )
    experience: list[Experience] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    skills: list[Skill] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)

    @property
    def total_years_experience(self) -> float | None:
        """Calculate total years of professional experience."""
        if not self.experience:
            return None
        total_days = 0
        for exp in self.experience:
            start = exp.start_date
            end = exp.end_date or date.today()
            if start:
                total_days += (end - start).days
        return round(total_days / 365.25, 1)

    @property
    def current_position(self) -> Experience | None:
        """Get the current job."""
        for exp in self.experience:
            if exp.is_current:
                return exp
        return None
```

Create `examples/resume_raw.json` with sample data and validate it.

### Step 4: API Error Response Models (20 min)

In `models/errors.py`, build models for standardized API error responses (you will use these in your FastAPI assignment):

```python
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Any


class ErrorCategory(str, Enum):
    VALIDATION = "validation_error"
    AUTHENTICATION = "authentication_error"
    RATE_LIMIT = "rate_limit_error"
    PROVIDER = "provider_error"
    INTERNAL = "internal_error"
    NOT_FOUND = "not_found"


class ErrorDetail(BaseModel):
    """Detailed information about a specific error."""
    field: str | None = Field(None, description="Which field caused the error")
    message: str = Field(..., description="Human-readable error message")
    code: str = Field(..., description="Machine-readable error code")
    context: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context about the error"
    )


class APIError(BaseModel):
    """Standardized API error response."""
    error: ErrorCategory
    message: str = Field(..., description="Summary error message")
    details: list[ErrorDetail] = Field(default_factory=list)
    request_id: str | None = Field(None, description="For tracing/debugging")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    retry_after: float | None = Field(
        None, description="Seconds to wait before retrying (for rate limits)"
    )
    documentation_url: str | None = Field(
        None, description="Link to relevant documentation"
    )

    @property
    def is_retryable(self) -> bool:
        return self.error in {
            ErrorCategory.RATE_LIMIT,
            ErrorCategory.PROVIDER,
            ErrorCategory.INTERNAL,
        }

    def to_http_status(self) -> int:
        status_map = {
            ErrorCategory.VALIDATION: 422,
            ErrorCategory.AUTHENTICATION: 401,
            ErrorCategory.RATE_LIMIT: 429,
            ErrorCategory.PROVIDER: 502,
            ErrorCategory.INTERNAL: 500,
            ErrorCategory.NOT_FOUND: 404,
        }
        return status_map.get(self.error, 500)
```

### Step 5: JSON Schema Generation and Validation Demos (30 min)

In `main.py`, demonstrate the full power of Pydantic:

```python
import json
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from models.meeting import MeetingNotes, ActionItem, Priority
from models.resume import Resume
from models.errors import APIError, ErrorCategory, ErrorDetail

console = Console()


def demo_schema_generation():
    """Generate JSON Schema from Pydantic models."""
    console.rule("[bold]JSON Schema Generation[/bold]")

    schema = MeetingNotes.model_json_schema()
    schema_json = json.dumps(schema, indent=2)

    console.print(Panel(
        Syntax(schema_json, "json", theme="monokai"),
        title="MeetingNotes JSON Schema",
        subtitle="This is what you send to OpenAI's structured outputs"
    ))

    # Save schemas to files
    for model_class in [MeetingNotes, Resume, APIError]:
        schema = model_class.model_json_schema()
        path = f"schemas/{model_class.__name__}.json"
        with open(path, "w") as f:
            json.dump(schema, f, indent=2)
        console.print(f"Saved schema: {path}")


def demo_validation_errors():
    """Show how Pydantic catches bad data."""
    console.rule("[bold]Validation Errors[/bold]")

    # 1. Missing required fields
    try:
        MeetingNotes(title="Test")  # Missing date, attendees, summary
    except Exception as e:
        console.print("[red]Missing required fields:[/red]")
        console.print(str(e)[:500])

    # 2. Invalid types
    try:
        ActionItem(
            description="Do stuff",  # too vague - custom validator
            assignee="Alice",
            priority="urgent"  # not a valid Priority enum value
        )
    except Exception as e:
        console.print("\n[red]Invalid field values:[/red]")
        console.print(str(e)[:500])

    # 3. Custom validator failure
    try:
        ActionItem(
            description="stuff",  # our custom validator flags this
            assignee="Alice",
            priority="high"
        )
    except Exception as e:
        console.print("\n[red]Custom validator caught vague description:[/red]")
        console.print(str(e)[:500])


def demo_model_validate():
    """Show model_validate with raw dicts and JSON strings."""
    console.rule("[bold]model_validate Demo[/bold]")

    # From dict (like you'd get from json.loads)
    raw_dict = {
        "error": "rate_limit_error",
        "message": "Too many requests",
        "retry_after": 30.0,
        "details": [
            {
                "field": None,
                "message": "Rate limit exceeded: 60 requests per minute",
                "code": "RATE_LIMIT_EXCEEDED",
                "context": {"limit": 60, "current": 61}
            }
        ]
    }

    error = APIError.model_validate(raw_dict)
    console.print(f"Error category: {error.error.value}")
    console.print(f"Is retryable: {error.is_retryable}")
    console.print(f"HTTP status: {error.to_http_status()}")
    console.print(f"Retry after: {error.retry_after}s")

    # From JSON string
    json_str = '{"error": "not_found", "message": "Model not found"}'
    error2 = APIError.model_validate_json(json_str)
    console.print(f"\nFrom JSON string: {error2.error.value} -> {error2.to_http_status()}")


def demo_serialization():
    """Show model_dump and model_dump_json options."""
    console.rule("[bold]Serialization Options[/bold]")

    error = APIError(
        error=ErrorCategory.VALIDATION,
        message="Invalid request",
        details=[
            ErrorDetail(field="prompt", message="Too long", code="MAX_LENGTH"),
        ]
    )

    # Full dump
    console.print("[bold]Full dump:[/bold]")
    console.print(error.model_dump_json(indent=2))

    # Exclude None values
    console.print("\n[bold]Exclude None:[/bold]")
    console.print(json.dumps(error.model_dump(exclude_none=True), indent=2, default=str))

    # Include only specific fields
    console.print("\n[bold]Only error + message:[/bold]")
    console.print(json.dumps(
        error.model_dump(include={"error", "message"}),
        indent=2
    ))


if __name__ == "__main__":
    demo_schema_generation()
    print()
    demo_validation_errors()
    print()
    demo_model_validate()
    print()
    demo_serialization()
```

### Step 6: OpenAI Structured Outputs Integration (30 min)

**This step requires an OpenAI API key. If you do not have one, read through the code to understand the pattern -- you will use it later.**

Create `parsers/meeting_parser.py`:

```python
"""
Parse raw meeting transcripts into structured MeetingNotes
using OpenAI's structured output feature.
"""
from openai import OpenAI
from models.meeting import MeetingNotes
import json


def parse_meeting_transcript(transcript: str) -> MeetingNotes:
    """
    Use an LLM with structured outputs to extract meeting notes.

    The key insight: we send our Pydantic model's JSON Schema to OpenAI,
    and it guarantees the response matches that schema.
    """
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a meeting notes extractor. Given a raw meeting "
                    "transcript, extract structured meeting notes. Be thorough "
                    "with action items and decisions. Use the exact names "
                    "mentioned in the transcript."
                ),
            },
            {
                "role": "user",
                "content": f"Extract structured meeting notes from this transcript:\n\n{transcript}",
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "meeting_notes",
                "schema": MeetingNotes.model_json_schema(),
                "strict": True,
            },
        },
    )

    raw_json = response.choices[0].message.content
    return MeetingNotes.model_validate_json(raw_json)


# Example transcript for testing
SAMPLE_TRANSCRIPT = """
Meeting: Sprint 23 Planning
October 15, 2024, 10am to 11:30am

Present: Sarah Chen (PM), Mike Johnson (Tech Lead), Alex Rivera (Backend Dev)
Absent: Lisa Park (Designer) - on PTO

Sarah opened the meeting by reviewing last sprint's velocity. We completed 34
story points out of 40 planned. The auth migration task took longer than expected.

Mike raised concerns about the database migration timeline. He estimates 3 more
days of work. Sarah agreed to push the deadline to October 25th.

Key decisions:
- We will use PostgreSQL instead of MongoDB for the new analytics service.
  Mike proposed this based on query complexity requirements. Alex initially
  preferred MongoDB but agreed after seeing the query patterns.
- The API rate limiting feature will be deprioritized to next sprint.

Action items:
- Mike: Complete database migration by October 25th (high priority)
- Alex: Write API docs for the new endpoints by October 20th
- Sarah: Schedule design review with Lisa for next week
- Mike: Review Alex's PR for the caching layer by October 17th
"""

if __name__ == "__main__":
    # If you have an OpenAI API key:
    # notes = parse_meeting_transcript(SAMPLE_TRANSCRIPT)
    # print(notes.model_dump_json(indent=2))

    # Without API key, demonstrate schema generation:
    schema = MeetingNotes.model_json_schema()
    print("Schema that would be sent to OpenAI:")
    print(json.dumps(schema, indent=2))
```

---

## Expected Output

Running `python main.py` should produce:

1. Generated JSON Schema files in the `schemas/` directory
2. A clear demonstration of validation errors being caught
3. Successful parsing from raw dicts and JSON strings
4. Serialization examples showing different output formats

The schema files are particularly important -- inspect them and understand how Pydantic's Python types map to JSON Schema types.

---

## Evaluation Criteria

| Criteria | Weight | Description |
|---|---|---|
| **Model Design** | 30% | Models are well-structured with appropriate field types, constraints, and descriptions |
| **Validators** | 25% | Custom validators catch real-world edge cases (not toy examples) |
| **Schema Quality** | 20% | Generated JSON schemas are correct and could be used with OpenAI structured outputs |
| **Code Organization** | 15% | Clean separation of models, parsers, and demo code |
| **Edge Cases** | 10% | Handles missing fields, invalid types, boundary values gracefully |

---

## Bonus Challenges

1. **Recursive Models**: Create a model for a threaded conversation (messages that can have replies, which can have replies, etc.). Generate its schema and verify it handles 5 levels of nesting.
2. **Dynamic Models**: Use `pydantic.create_model()` to generate models at runtime from a user-provided schema definition. This is how some AI frameworks work internally.
3. **Discriminated Unions**: Model a system where different event types have different payloads (like TypeScript discriminated unions). For example: `ChatEvent | ToolCallEvent | ErrorEvent`, discriminated by a `type` field.
4. **Streaming Validation**: Build a system that validates partial JSON as it streams in from an LLM. Handle the case where the stream is cut off mid-JSON.
5. **Model Comparison Tool**: Build a CLI that takes two Pydantic model versions (v1 and v2 of the same schema) and reports what fields were added, removed, or changed -- useful for API versioning.

---

## Key Concepts You Will Learn

- **Pydantic v2**: The standard for data validation in Python AI applications
- **JSON Schema**: The bridge between Python types and LLM structured outputs
- **Field validators**: Runtime enforcement of business rules
- **Model validators**: Cross-field validation (like TypeScript refinement types)
- **Serialization control**: `model_dump`, `exclude`, `include`, `by_alias`
- **Structured outputs**: How OpenAI guarantees JSON response format using your schema
