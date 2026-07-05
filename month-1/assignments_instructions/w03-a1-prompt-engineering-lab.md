# Assignment 3.1: Prompt Engineering Lab

> **Week 3** | [Back to Week 3 Plan](../week-3.md)

## Title
**Prompt Engineering Lab** -- Systematic Prompt Testing Framework

## Objective
Build a Python framework that systematically tests and compares different prompt strategies against a suite of test cases. You will define evaluation criteria, run multiple prompt variants, score outputs using multiple methods (exact match, keyword presence, LLM-as-judge), and generate comparison reports. Move prompt engineering from "vibes-based" to "data-driven."

## Difficulty
Intermediate

## Estimated Time
4-5 hours

## Prerequisites
- Python 3.10+ installed
- Completed Assignments 2.1 and 2.2 (toolkit + Pydantic)
- At least one LLM API key (OpenAI or Anthropic)
- Install dependencies:
```bash
pip install openai anthropic pydantic rich tabulate pandas jinja2
```

## Why This Matters
Prompt engineering is not guesswork. Professional GenAI engineers:
- Test prompts against standardized datasets
- Measure performance quantitatively
- Track prompt versions like code versions
- Know when few-shot beats zero-shot and by how much

This framework is something you will use on every project going forward. Companies like Anthropic and OpenAI use internal versions of exactly this tool.

---

## Detailed Instructions

### Step 1: Project Setup (10 min)

```
prompt-engineering-lab/
  prompt_lab/
    __init__.py
    models.py          # Pydantic models for test cases, results
    runner.py           # Executes prompts against test cases
    scorers.py          # Scoring functions
    reporters.py        # Generate comparison reports
    providers.py        # LLM provider abstraction
  test_suites/
    classification.json
    extraction.json
    summarization.json
    code_generation.json
  prompts/
    classification/
      zero_shot.txt
      few_shot.txt
      cot.txt
    extraction/
      zero_shot.txt
      few_shot.txt
      structured.txt
  reports/              # Generated reports go here
  main.py
  pyproject.toml
```

### Step 2: Define the Data Models (20 min)

In `prompt_lab/models.py`:

```python
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class ScoringMethod(str, Enum):
    EXACT_MATCH = "exact_match"
    CONTAINS = "contains"
    KEYWORD = "keyword"
    LLM_JUDGE = "llm_judge"
    REGEX = "regex"
    CUSTOM = "custom"


class TestCase(BaseModel):
    """A single test case: input + expected output."""
    id: str = Field(..., description="Unique test case identifier")
    input: str = Field(..., description="Input text to send to the LLM")
    expected_output: str = Field(..., description="Expected/ideal output")
    category: str = Field("general", description="Test category for grouping")
    tags: list[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)


class TestSuite(BaseModel):
    """A collection of test cases for a specific task."""
    name: str
    description: str
    task_type: str  # classification, extraction, summarization, code_generation
    scoring_methods: list[ScoringMethod]
    test_cases: list[TestCase]


class PromptVariant(BaseModel):
    """A specific prompt template to test."""
    name: str = Field(..., description="e.g., 'zero_shot_v1', 'few_shot_cot'")
    system_prompt: str | None = None
    user_prompt_template: str = Field(
        ..., description="Template with {input} placeholder"
    )
    description: str = ""
    tags: list[str] = Field(default_factory=list)


class TestResult(BaseModel):
    """Result of running one test case with one prompt variant."""
    test_case_id: str
    prompt_variant: str
    model: str
    input: str
    expected_output: str
    actual_output: str
    scores: dict[str, float] = Field(
        default_factory=dict,
        description="Scoring method -> score (0.0 to 1.0)"
    )
    latency_ms: float
    token_count: int | None = None
    cost_estimate: float | None = None


class RunReport(BaseModel):
    """Complete report of a prompt testing run."""
    run_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    test_suite: str
    model: str
    results: list[TestResult]

    @property
    def variant_names(self) -> list[str]:
        return list({r.prompt_variant for r in self.results})

    def average_score(
        self, variant: str, method: str
    ) -> float:
        scores = [
            r.scores.get(method, 0.0)
            for r in self.results
            if r.prompt_variant == variant
        ]
        return sum(scores) / len(scores) if scores else 0.0

    def variant_summary(self) -> dict[str, dict[str, float]]:
        """Average scores per variant per scoring method."""
        summary = {}
        methods = set()
        for r in self.results:
            methods.update(r.scores.keys())

        for variant in self.variant_names:
            summary[variant] = {}
            for method in methods:
                summary[variant][method] = self.average_score(
                    variant, method
                )
        return summary
```

### Step 3: Create Test Suites (30 min)

Create `test_suites/classification.json`:
```json
{
  "name": "Sentiment Classification",
  "description": "Classify text sentiment as positive, negative, or neutral",
  "task_type": "classification",
  "scoring_methods": ["exact_match", "contains"],
  "test_cases": [
    {
      "id": "cls-001",
      "input": "This product is absolutely amazing! Best purchase I've ever made.",
      "expected_output": "positive",
      "category": "obvious",
      "tags": ["easy"]
    },
    {
      "id": "cls-002",
      "input": "Terrible experience. The item broke after one day.",
      "expected_output": "negative",
      "category": "obvious"
    },
    {
      "id": "cls-003",
      "input": "The package arrived on time.",
      "expected_output": "neutral",
      "category": "subtle"
    },
    {
      "id": "cls-004",
      "input": "I expected better quality for this price, but it works fine I guess.",
      "expected_output": "negative",
      "category": "subtle",
      "tags": ["ambiguous"]
    },
    {
      "id": "cls-005",
      "input": "Not bad, not great. It does what it says.",
      "expected_output": "neutral",
      "category": "subtle",
      "tags": ["ambiguous"]
    },
    {
      "id": "cls-006",
      "input": "I can't believe how terrible this isn't! Surprisingly decent.",
      "expected_output": "positive",
      "category": "tricky",
      "tags": ["negation", "hard"]
    },
    {
      "id": "cls-007",
      "input": "The restaurant was so bad it was almost funny. Would not recommend.",
      "expected_output": "negative",
      "category": "sarcasm",
      "tags": ["sarcasm"]
    },
    {
      "id": "cls-008",
      "input": "Oh great, another software update that breaks everything. Just what I needed.",
      "expected_output": "negative",
      "category": "sarcasm",
      "tags": ["sarcasm"]
    }
  ]
}
```

Create `test_suites/extraction.json`:
```json
{
  "name": "Entity Extraction",
  "description": "Extract structured entities from unstructured text",
  "task_type": "extraction",
  "scoring_methods": ["keyword", "llm_judge"],
  "test_cases": [
    {
      "id": "ext-001",
      "input": "Meeting scheduled with John Smith from Acme Corp on March 15, 2024 at 2:30 PM to discuss the Q2 budget proposal.",
      "expected_output": "{\"person\": \"John Smith\", \"company\": \"Acme Corp\", \"date\": \"March 15, 2024\", \"time\": \"2:30 PM\", \"topic\": \"Q2 budget proposal\"}",
      "category": "meeting"
    },
    {
      "id": "ext-002",
      "input": "Please ship 500 units of SKU-A1234 to 742 Evergreen Terrace, Springfield, IL 62704 by next Friday. Contact: Homer Simpson, homer@springfield.gov",
      "expected_output": "{\"quantity\": 500, \"sku\": \"SKU-A1234\", \"address\": \"742 Evergreen Terrace, Springfield, IL 62704\", \"deadline\": \"next Friday\", \"contact_name\": \"Homer Simpson\", \"contact_email\": \"homer@springfield.gov\"}",
      "category": "shipping"
    },
    {
      "id": "ext-003",
      "input": "Bug report: App crashes on iPhone 15 Pro running iOS 17.2 when opening the camera feature. Error code: ERR_CAMERA_INIT_FAIL. Reported by 23 users since v3.4.1 release.",
      "expected_output": "{\"device\": \"iPhone 15 Pro\", \"os_version\": \"iOS 17.2\", \"feature\": \"camera\", \"error_code\": \"ERR_CAMERA_INIT_FAIL\", \"affected_users\": 23, \"since_version\": \"3.4.1\"}",
      "category": "bug_report"
    }
  ]
}
```

Create similar files for `summarization.json` and `code_generation.json` with at least 5 test cases each.

### Step 4: Create Prompt Variants (25 min)

Create `prompts/classification/zero_shot.txt`:
```
Classify the sentiment of the following text as exactly one of: positive, negative, or neutral.

Text: {input}

Sentiment:
```

Create `prompts/classification/few_shot.txt`:
```
Classify the sentiment of the following text as exactly one of: positive, negative, or neutral.

Examples:
Text: "I love this new phone, it's incredible!"
Sentiment: positive

Text: "The service was awful and the food was cold."
Sentiment: negative

Text: "The meeting was at 3pm in the conference room."
Sentiment: neutral

Now classify this text:
Text: {input}

Sentiment:
```

Create `prompts/classification/cot.txt`:
```
Classify the sentiment of the following text as exactly one of: positive, negative, or neutral.

Think step by step:
1. Identify the key emotional words or phrases
2. Consider if there is sarcasm or irony
3. Weigh the overall tone
4. Give your final classification

Text: {input}

Analysis:
```

Create corresponding prompt files for extraction (zero_shot, few_shot, structured output format).

### Step 5: Build the Scoring Engine (40 min)

In `prompt_lab/scorers.py`:

```python
import re
import json
from typing import Callable


def exact_match_score(expected: str, actual: str) -> float:
    """1.0 if outputs match exactly (case-insensitive, stripped)."""
    return 1.0 if expected.strip().lower() == actual.strip().lower() else 0.0


def contains_score(expected: str, actual: str) -> float:
    """1.0 if expected output appears anywhere in actual output."""
    return 1.0 if expected.strip().lower() in actual.strip().lower() else 0.0


def keyword_score(expected: str, actual: str) -> float:
    """
    Score based on keyword overlap.
    Parses expected as JSON and checks if key values appear in actual.
    Falls back to word overlap if not JSON.
    """
    try:
        expected_data = json.loads(expected)
        if isinstance(expected_data, dict):
            found = 0
            total = len(expected_data)
            for key, value in expected_data.items():
                str_value = str(value).lower()
                if str_value in actual.lower():
                    found += 1
            return found / total if total > 0 else 0.0
    except json.JSONDecodeError:
        pass

    # Fallback: word overlap
    expected_words = set(expected.lower().split())
    actual_words = set(actual.lower().split())
    if not expected_words:
        return 0.0
    overlap = expected_words & actual_words
    return len(overlap) / len(expected_words)


def regex_score(expected_pattern: str, actual: str) -> float:
    """1.0 if the actual output matches the expected regex pattern."""
    try:
        return 1.0 if re.search(expected_pattern, actual, re.IGNORECASE) else 0.0
    except re.error:
        return 0.0


async def llm_judge_score(
    input_text: str,
    expected: str,
    actual: str,
    judge_client,
    judge_model: str = "gpt-4o-mini",
) -> float:
    """
    Use an LLM to judge the quality of the output.
    Returns a score from 0.0 to 1.0.

    This is the most powerful scoring method but costs money per evaluation.
    """
    judge_prompt = f"""You are an expert evaluator. Score the following AI output on a scale of 0 to 10.

INPUT: {input_text}

EXPECTED OUTPUT: {expected}

ACTUAL OUTPUT: {actual}

Score based on:
- Correctness: Does it contain the right information?
- Completeness: Is anything missing?
- Format: Is it in the expected format?

Respond with ONLY a JSON object: {{"score": <0-10>, "reasoning": "<brief explanation>"}}"""

    response = await judge_client.chat.completions.create(
        model=judge_model,
        messages=[{"role": "user", "content": judge_prompt}],
        temperature=0.0,
    )

    try:
        result = json.loads(response.choices[0].message.content)
        return result["score"] / 10.0
    except (json.JSONDecodeError, KeyError):
        return 0.0


# Registry of scoring functions
SCORERS: dict[str, Callable] = {
    "exact_match": exact_match_score,
    "contains": contains_score,
    "keyword": keyword_score,
    "regex": regex_score,
    # llm_judge is async and handled separately
}
```

### Step 6: Build the Test Runner (45 min)

In `prompt_lab/runner.py`:

```python
import asyncio
import json
import time
import uuid
from pathlib import Path
from typing import AsyncIterator

from prompt_lab.models import (
    TestSuite, PromptVariant, TestResult, RunReport, ScoringMethod
)
from prompt_lab.scorers import SCORERS, llm_judge_score


class PromptRunner:
    """Runs prompt variants against test suites and collects results."""

    def __init__(
        self,
        provider_client,
        model: str = "gpt-4o-mini",
        judge_client=None,
        judge_model: str = "gpt-4o-mini",
    ):
        self.client = provider_client
        self.model = model
        self.judge_client = judge_client or provider_client
        self.judge_model = judge_model

    async def run_single(
        self,
        test_case_input: str,
        prompt_variant: PromptVariant,
    ) -> tuple[str, float]:
        """Run a single test case with a prompt variant. Returns (output, latency_ms)."""
        # Build the messages
        messages = []
        if prompt_variant.system_prompt:
            messages.append({
                "role": "system",
                "content": prompt_variant.system_prompt,
            })

        user_content = prompt_variant.user_prompt_template.replace(
            "{input}", test_case_input
        )
        messages.append({"role": "user", "content": user_content})

        # Call the LLM
        start = time.time()
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.0,  # deterministic for evaluation
            max_tokens=512,
        )
        latency = (time.time() - start) * 1000

        output = response.choices[0].message.content or ""
        return output, latency

    async def score_result(
        self,
        test_input: str,
        expected: str,
        actual: str,
        methods: list[ScoringMethod],
    ) -> dict[str, float]:
        """Score a result using multiple methods."""
        scores = {}
        for method in methods:
            if method == ScoringMethod.LLM_JUDGE:
                scores[method.value] = await llm_judge_score(
                    test_input, expected, actual,
                    self.judge_client, self.judge_model,
                )
            elif method.value in SCORERS:
                scores[method.value] = SCORERS[method.value](
                    expected, actual
                )
        return scores

    async def run_suite(
        self,
        suite: TestSuite,
        variants: list[PromptVariant],
        on_progress: callable | None = None,
    ) -> RunReport:
        """Run all variants against all test cases in a suite."""
        results: list[TestResult] = []
        total = len(suite.test_cases) * len(variants)
        completed = 0

        for variant in variants:
            for test_case in suite.test_cases:
                try:
                    output, latency = await self.run_single(
                        test_case.input, variant
                    )
                    scores = await self.score_result(
                        test_case.input,
                        test_case.expected_output,
                        output,
                        suite.scoring_methods,
                    )
                    results.append(TestResult(
                        test_case_id=test_case.id,
                        prompt_variant=variant.name,
                        model=self.model,
                        input=test_case.input,
                        expected_output=test_case.expected_output,
                        actual_output=output,
                        scores=scores,
                        latency_ms=latency,
                    ))
                except Exception as e:
                    results.append(TestResult(
                        test_case_id=test_case.id,
                        prompt_variant=variant.name,
                        model=self.model,
                        input=test_case.input,
                        expected_output=test_case.expected_output,
                        actual_output=f"ERROR: {str(e)}",
                        scores={m.value: 0.0 for m in suite.scoring_methods},
                        latency_ms=0,
                    ))

                completed += 1
                if on_progress:
                    on_progress(completed, total)

        return RunReport(
            run_id=uuid.uuid4().hex[:12],
            test_suite=suite.name,
            model=self.model,
            results=results,
        )


def load_test_suite(path: str) -> TestSuite:
    """Load a test suite from a JSON file."""
    with open(path) as f:
        data = json.load(f)
    return TestSuite.model_validate(data)


def load_prompt_variant(path: str, name: str | None = None) -> PromptVariant:
    """Load a prompt variant from a text file."""
    with open(path) as f:
        template = f.read()
    return PromptVariant(
        name=name or Path(path).stem,
        user_prompt_template=template,
    )
```

### Step 7: Build the Report Generator (30 min)

In `prompt_lab/reporters.py`:

```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from prompt_lab.models import RunReport
import json


def print_summary_report(report: RunReport) -> None:
    """Print a rich terminal report comparing prompt variants."""
    console = Console()

    console.rule(f"[bold blue]Prompt Testing Report: {report.test_suite}")
    console.print(f"Run ID: {report.run_id}")
    console.print(f"Model: {report.model}")
    console.print(f"Timestamp: {report.timestamp}")
    console.print(f"Total test cases: {len(report.results)}")
    console.print()

    # Summary table
    summary = report.variant_summary()
    if not summary:
        console.print("[red]No results to display.[/red]")
        return

    # Get all scoring methods
    all_methods = set()
    for scores in summary.values():
        all_methods.update(scores.keys())

    table = Table(title="Average Scores by Prompt Variant")
    table.add_column("Variant", style="bold cyan")
    for method in sorted(all_methods):
        table.add_column(method, justify="right")
    table.add_column("Avg Latency (ms)", justify="right")

    for variant, scores in summary.items():
        # Calculate average latency for this variant
        latencies = [
            r.latency_ms for r in report.results
            if r.prompt_variant == variant
        ]
        avg_latency = sum(latencies) / len(latencies) if latencies else 0

        row = [variant]
        for method in sorted(all_methods):
            score = scores.get(method, 0.0)
            # Color code: green > 0.8, yellow > 0.5, red <= 0.5
            if score >= 0.8:
                row.append(f"[green]{score:.2%}[/green]")
            elif score >= 0.5:
                row.append(f"[yellow]{score:.2%}[/yellow]")
            else:
                row.append(f"[red]{score:.2%}[/red]")
        row.append(f"{avg_latency:.0f}")
        table.add_row(*row)

    console.print(table)

    # Per-test-case breakdown
    console.print()
    console.rule("[bold]Detailed Results[/bold]")

    for variant in report.variant_names:
        console.print(f"\n[bold cyan]{variant}[/bold cyan]")
        detail_table = Table(show_header=True)
        detail_table.add_column("ID", width=10)
        detail_table.add_column("Input", width=40, no_wrap=True)
        detail_table.add_column("Expected", width=15)
        detail_table.add_column("Actual", width=30)
        detail_table.add_column("Score", width=10, justify="right")

        for r in report.results:
            if r.prompt_variant != variant:
                continue
            avg_score = (
                sum(r.scores.values()) / len(r.scores)
                if r.scores else 0.0
            )
            score_str = (
                f"[green]{avg_score:.0%}[/green]" if avg_score >= 0.8
                else f"[yellow]{avg_score:.0%}[/yellow]" if avg_score >= 0.5
                else f"[red]{avg_score:.0%}[/red]"
            )
            detail_table.add_row(
                r.test_case_id,
                r.input[:40] + "..." if len(r.input) > 40 else r.input,
                r.expected_output[:15],
                r.actual_output[:30],
                score_str,
            )
        console.print(detail_table)

    # Winner announcement
    console.print()
    if summary:
        best_variant = max(
            summary.items(),
            key=lambda x: sum(x[1].values()) / len(x[1]) if x[1] else 0
        )
        console.print(Panel(
            f"[bold green]Best performing variant: {best_variant[0]}[/bold green]",
            title="Winner",
        ))


def save_report_json(report: RunReport, path: str) -> None:
    """Save the full report as JSON for later analysis."""
    with open(path, "w") as f:
        f.write(report.model_dump_json(indent=2))
```

### Step 8: Main Runner Script (20 min)

In `main.py`:

```python
import asyncio
from openai import AsyncOpenAI
from prompt_lab.runner import PromptRunner, load_test_suite, load_prompt_variant
from prompt_lab.reporters import print_summary_report, save_report_json


async def main():
    client = AsyncOpenAI()

    # Load test suite
    suite = load_test_suite("test_suites/classification.json")

    # Load prompt variants
    variants = [
        load_prompt_variant("prompts/classification/zero_shot.txt", "zero_shot"),
        load_prompt_variant("prompts/classification/few_shot.txt", "few_shot"),
        load_prompt_variant("prompts/classification/cot.txt", "chain_of_thought"),
    ]

    # Run
    runner = PromptRunner(client, model="gpt-4o-mini")

    def progress(done, total):
        print(f"  Progress: {done}/{total}", end="\r")

    print("Running classification tests...")
    report = await runner.run_suite(suite, variants, on_progress=progress)
    print()

    # Display report
    print_summary_report(report)

    # Save report
    save_report_json(report, f"reports/{report.run_id}.json")
    print(f"\nReport saved to reports/{report.run_id}.json")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Expected Output

Running `python main.py` should produce a table like:

```
         Average Scores by Prompt Variant
┌──────────────────┬──────────────┬──────────┬──────────────────┐
│ Variant          │ contains     │ exact    │ Avg Latency (ms) │
├──────────────────┼──────────────┼──────────┼──────────────────┤
│ zero_shot        │ 75.00%       │ 62.50%   │ 450              │
│ few_shot         │ 87.50%       │ 87.50%   │ 520              │
│ chain_of_thought │ 87.50%       │ 50.00%   │ 890              │
└──────────────────┴──────────────┴──────────┴──────────────────┘

Best performing variant: few_shot
```

Note: Chain-of-thought may have high `contains` scores but lower `exact_match` because it produces longer explanations before the final answer. This is a real finding you should discuss.

---

## Evaluation Criteria

| Criteria | Weight | Description |
|---|---|---|
| **Test Suite Quality** | 20% | At least 2 complete test suites with 5+ diverse test cases each |
| **Prompt Variants** | 20% | At least 3 variants per task type, demonstrating zero-shot, few-shot, and CoT |
| **Scoring Implementation** | 20% | At least 3 scoring methods implemented correctly |
| **Report Quality** | 20% | Clear, readable reports that make it easy to pick the best prompt |
| **Code Structure** | 10% | Clean separation of concerns, Pydantic models throughout |
| **Analysis** | 10% | Written observations about what worked and why |

---

## Bonus Challenges

1. **A/B Test Calculator**: Add statistical significance testing. Given N runs of each variant, calculate confidence intervals and p-values. Tell the user when they have enough data to declare a winner.
2. **Prompt Version Control**: Add git-like versioning for prompts. Track which version was used in each run. Show performance trends over versions.
3. **Cost Optimizer**: For each test suite, calculate the total API cost per variant. Produce a cost-per-quality-point metric. Sometimes the cheaper model with a better prompt beats the expensive model.
4. **Automated Prompt Optimization**: Implement DSPy-style prompt optimization: run the test suite, identify the worst-performing cases, and use an LLM to suggest prompt improvements. Test the improved prompt and iterate.
5. **HTML Report**: Use Jinja2 to generate a beautiful HTML report with charts (using Chart.js). Include per-category breakdowns, failure analysis, and prompt text side-by-side.

---

## Key Concepts You Will Learn

- **Systematic evaluation**: Why intuition is unreliable for prompt quality
- **Zero-shot vs few-shot**: Quantified comparison with your own data
- **Chain-of-thought (CoT)**: When thinking step-by-step helps (and when it hurts)
- **LLM-as-judge**: Using one model to evaluate another model's output
- **Scoring trade-offs**: Exact match is strict; contains is lenient; LLM judge is expensive but nuanced
- **Prompt engineering as engineering**: Versioning, testing, measurement, iteration
