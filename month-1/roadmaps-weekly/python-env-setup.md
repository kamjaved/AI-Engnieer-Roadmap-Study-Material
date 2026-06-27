# Python Environment Setup Guide for GenAI Engineering

> **For:** Month 1 — GenAI Engineer Roadmap
> **IDE:** Visual Studio Code
> **Toolchain:** Python 3.12 · UV · Ruff · Pylance · Pydantic v2 · Jupyter

This guide sets up a professional Python environment that mirrors what real AI engineering teams use in production. Every tool here has been chosen deliberately — each one is explained with the reasoning behind it so you understand *why*, not just *what*.

---

## Why This Toolchain

Most Python tutorials teach `pip`, `venv`, and `flake8`. Those tools work, but they have been largely superseded. Here is the modern equivalent:

| Old Approach | Modern Replacement | Why |
|---|---|---|
| `pip install` | `uv add` | 10–100× faster, automatic lockfiles |
| `python -m venv` | `uv venv` (built-in to UV) | One tool instead of two |
| `flake8` + `black` + `isort` | `ruff` | Single tool, 100× faster |
| `setup.py` / `requirements.txt` | `pyproject.toml` | Single source of truth |
| `python .env` manual loading | `pydantic-settings` | Type-safe config with validation |

---

## Step 1 — Install Python 3.12

### Why 3.12 (not 3.10 or 3.11)?
Python 3.12 offers significantly improved error messages (the error output is much more readable), better performance, and all the type system features we use throughout this course — `str | None` union syntax, `list[str]` generic syntax, `@override` decorator. The AI libraries we use all support it.

### Install
**macOS (recommended):** Use the official installer or Homebrew.
```bash
brew install python@3.12
```

**Windows:** Download from [python.org/downloads](https://python.org/downloads). During install, check **"Add Python to PATH"**.

**Linux (Ubuntu/Debian):**
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
```

### Verify
```bash
python3.12 --version
# Python 3.12.x
```

---

## Step 2 — Install UV (Package Manager)

### Why UV instead of pip?

`pip` was built in 2008. UV was built in 2024, written in Rust, and designed to replace `pip`, `pip-tools`, `poetry`, `virtualenv`, and `pyenv` with a single binary.

**Concrete advantages you will feel during this course:**
- `pip install` on a large project like sentence-transformers can take 3–5 minutes. `uv add` takes 10–20 seconds.
- UV automatically creates and manages a `uv.lock` file, so anyone cloning your project gets the exact same dependencies — no more "works on my machine."
- UV handles Python version management too — you never need `pyenv` separately.
- The command interface is close enough to pip that muscle memory transfers easily.

**The one trade-off:** UV is newer. If you Google an error and the Stack Overflow answer shows `pip install`, just substitute `uv add`. The package names are identical.

### Install UV
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart your terminal after installation.

### Verify
```bash
uv --version
# uv 0.x.x
```

### Core UV commands you will use

| Action | Command |
|---|---|
| Create a new project | `uv init my-project` |
| Add a dependency | `uv add package-name` |
| Add a dev-only dependency | `uv add --dev package-name` |
| Install all dependencies from lockfile | `uv sync` |
| Run a script in the project env | `uv run python script.py` |
| Run a module | `uv run python -m module_name` |
| Open a Python REPL in project env | `uv run python` |
| Remove a dependency | `uv remove package-name` |
| Update all dependencies | `uv sync --upgrade` |

**Key mental model:** After `uv init`, you never activate a venv manually. `uv run` handles it automatically. The `.venv` folder is created automatically the first time you run `uv sync` or `uv add`.

---

## Step 3 — Install VSCode

Download from [code.visualstudio.com](https://code.visualstudio.com). The default installation is fine.

---

## Step 4 — VSCode Extensions

Install these extensions. Each one is linked to its Marketplace ID so you can search by ID in the Extensions panel (`Ctrl+Shift+X` / `Cmd+Shift+X`).

### Essential (install all of these)

**1. Python** — `ms-python.python`
The base Python extension from Microsoft. Provides the Python interpreter selector, debugger, test runner, and terminal integration. Without this, nothing else works.

**2. Pylance** — `ms-python.vscode-pylance`
The language server that powers IntelliSense for Python. It understands your type hints and provides:
- Autocomplete that knows the shape of your Pydantic models
- Inline error detection before you run code
- "Go to definition" and "Find all references" for Python symbols
- Import organization

*Why Pylance over the default Python language server?* Pylance uses the Pyright type checker under the hood, which is the strictest and most accurate Python type inference engine available. When you write `def embed(self, texts: list[str]) -> np.ndarray`, Pylance enforces that contract.

**3. Ruff** — `charliermarsh.ruff`
Linting and formatting in one extension. Ruff is the modern replacement for `flake8` (linting), `black` (formatting), and `isort` (import sorting). It is written in Rust and runs on every save in under 50ms.

*Why Ruff instead of Black + flake8?* Three separate tools that sometimes conflict with each other, configured in three separate files, all replaced by one tool in one config section in `pyproject.toml`. If you have used Black before, Ruff's formatter is nearly identical.

**4. Jupyter** — `ms-toolsai.jupyter`
Runs `.ipynb` notebooks directly in VSCode. You will use this during Week 1 for the embedding visualization exercises — plotting cosine similarity heatmaps is much smoother in a notebook than a script.

**5. Even Better TOML** — `tamasfe.even-better-toml`
Syntax highlighting and validation for `pyproject.toml`. Small quality-of-life improvement, but you will be editing `pyproject.toml` frequently.

### Recommended

**6. GitLens** — `eamodio.gitlens`
Shows `git blame` inline, lets you visualize branch history, and makes code review much easier. Since this course emphasizes engineering maturity (DECISIONS.md, version-controlled prompts), having a great git workflow matters.

**7. Python Environments** — `ms-python.python-environments`
A UI panel for managing UV environments, switching Python versions, and viewing installed packages. Makes it easier to confirm your project is using the right interpreter.

**8. Error Lens** — `usernamehw.errorlens`
Shows linting errors and type errors inline on the same line as the problem, rather than requiring you to hover. Dramatically speeds up the debug loop.

**9. REST Client** — `humao.rest-client`
Lets you write `.http` files with HTTP requests (like Postman, but in VSCode). Useful for testing your FastAPI endpoints without leaving the editor.

---

## Step 5 — VSCode Settings

Open your User Settings JSON (`Ctrl+Shift+P` → "Open User Settings JSON") and add these settings. Each one is explained inline.

```jsonc
{
  // ── Python ────────────────────────────────────────────────────
  // Tell VSCode to find the Python interpreter from UV's .venv
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",

  // ── Pylance (type checking) ───────────────────────────────────
  "python.languageServer": "Pylance",
  // "basic" catches real errors. "strict" is great but overwhelming
  // when starting — upgrade to strict once your code is type-annotated.
  "python.analysis.typeCheckingMode": "basic",
  // Show inferred types as hints next to variable declarations
  "python.analysis.inlayHints.variableTypes": true,
  "python.analysis.inlayHints.functionReturnTypes": true,

  // ── Ruff (format on save) ────────────────────────────────────
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      // Auto-fix import sorting and simple lint issues on save
      "source.fixAll.ruff": "explicit",
      "source.organizeImports.ruff": "explicit"
    }
  },

  // ── Editor quality of life ────────────────────────────────────
  // Show a vertical ruler at 88 characters (Ruff's default line length)
  "editor.rulers": [88],
  // Trim trailing whitespace automatically
  "files.trimTrailingWhitespace": true,
  // Always insert a newline at end of file (required by Python style)
  "files.insertFinalNewline": true,

  // ── Terminal ──────────────────────────────────────────────────
  // Auto-activate the project venv when opening a terminal
  "python.terminal.activateEnvInCurrentTerminal": true,

  // ── Jupyter ───────────────────────────────────────────────────
  // Use the same Python interpreter as the project
  "jupyter.kernels.trusted": ["${workspaceFolder}/.venv/bin/python"]
}
```

---

## Step 6 — pyproject.toml Explained

Every project in this course uses `pyproject.toml` as its single configuration file. Here is an annotated example you can use as a template:

```toml
[project]
name = "my-ai-project"
version = "0.1.0"
# Always pin a minimum Python version. Helps others know what's required.
requires-python = ">=3.12"
dependencies = [
    # Pin major versions to avoid breaking changes silently
    "openai>=1.30.0",
    "anthropic>=0.28.0",
    "pydantic>=2.7.0",
    "fastapi>=0.111.0",
    "httpx>=0.27.0",
]

[dependency-groups]
# Dev dependencies are NOT installed when someone runs `uv sync` in production.
# They are only installed when you run `uv sync --dev` locally.
dev = [
    "ruff>=0.4.0",
    "mypy>=1.10.0",
    "pytest>=8.2.0",
    "pytest-asyncio>=0.23.0",
]

# ── Ruff configuration ─────────────────────────────────────────────────────
[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes (unused imports, undefined names)
    "I",   # isort (import ordering)
    "UP",  # pyupgrade (suggest modern Python syntax)
    "B",   # flake8-bugbear (common bugs and design problems)
    "SIM", # flake8-simplify (suggests simpler code)
]
# Ignore specific rules that conflict with AI/ML patterns
ignore = ["E501"]  # Line length handled by formatter, not linter

[tool.ruff.format]
# Match Black's quote style so diff noise is minimal if you ever migrate
quote-style = "double"
indent-style = "space"

# ── Mypy (strict type checking for CI) ────────────────────────────────────
[tool.mypy]
python_version = "3.12"
strict = false          # Set to true as your type coverage grows
ignore_missing_imports = true  # Many AI libs have incomplete stubs

# ── Pytest ────────────────────────────────────────────────────────────────
[tool.pytest.ini_options]
asyncio_mode = "auto"   # Required for testing async FastAPI endpoints
```

**Why not `requirements.txt`?**
`requirements.txt` is a flat list of packages. `pyproject.toml` is a structured project declaration that tools can parse — UV uses it to manage dependencies, Ruff uses it for its config, mypy uses it for its config. Everything in one file.

---

## Step 7 — Pydantic v2

### What is Pydantic?

Pydantic is a data validation library. You describe your data's shape using Python type hints, and Pydantic enforces that shape at runtime — with clear error messages when data doesn't match.

### Why does it matter for GenAI specifically?

LLMs return text. Your application needs structured data. The gap between "raw LLM string output" and "validated Python object your code can safely use" is exactly what Pydantic fills.

Without Pydantic:
```python
# Raw API response — what if "score" is missing? What if it's a string, not a float?
result = json.loads(llm_response)
score = result["score"]  # KeyError if missing, TypeError if wrong type
```

With Pydantic:
```python
class SentimentResult(BaseModel):
    label: Literal["positive", "negative", "neutral"]
    score: float = Field(ge=0.0, le=1.0)
    reasoning: str

# If the LLM gives you invalid data, you get a clear ValidationError, not a silent bug
result = SentimentResult.model_validate_json(llm_response)
```

### Why v2 and not v1?

Pydantic v2 (released 2023) rewrote the core in Rust — validation is 5–50× faster. It also changed several APIs (`validator` → `field_validator`, `parse_obj` → `model_validate`, etc.). **This course uses v2 throughout. Do not install `pydantic<2`.**

### Install
```bash
uv add "pydantic>=2.7.0"
```

### Key concepts at a glance

```python
from pydantic import BaseModel, Field, field_validator
from typing import Literal

class ChunkConfig(BaseModel):
    # Field() adds metadata: description for JSON schema, bounds validation
    chunk_size: int = Field(default=512, ge=64, le=4096,
                            description="Target chunk size in tokens")
    overlap: float = Field(default=0.15, ge=0.0, le=0.5,
                           description="Overlap fraction between consecutive chunks")
    strategy: Literal["fixed", "recursive", "semantic"] = "recursive"

    @field_validator("chunk_size")
    @classmethod
    def chunk_size_must_be_multiple_of_64(cls, v: int) -> int:
        if v % 64 != 0:
            raise ValueError(f"chunk_size must be a multiple of 64, got {v}")
        return v

# Use it:
config = ChunkConfig(chunk_size=512, overlap=0.1)
print(config.model_json_schema())  # Produces JSON Schema you can pass to an LLM
```

### pydantic-settings — for environment variables

Extend Pydantic to handle `.env` files and environment variables with the same validation:

```bash
uv add pydantic-settings
```

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    openai_api_key: str           # Required — will raise error if missing
    anthropic_api_key: str        # Required
    model: str = "gpt-4o"         # Optional with default
    max_tokens: int = 2048        # Optional with default
    debug: bool = False           # Optional with default

# Call once at startup — never use global os.environ.get() scattered through code
settings = Settings()
```

This replaces `python-dotenv` and `os.environ.get()`. Your configuration is now typed, validated, and documented.

---

## Step 8 — Jupyter for Exploration

Notebooks are not ideal for production code (hard to version control, no type checking, hidden state problems). But they are excellent for exploration — running small experiments, visualizing embeddings, trying out an API before you commit to the interface.

**Pattern for this course:** Use notebooks to explore, scripts/modules for production code. The Week 1 embedding visualization exercises work best in a notebook first, then refactored into a module.

### Install the Jupyter kernel in your project
```bash
uv add --dev ipykernel
# Register the kernel so VSCode's Jupyter extension can find it
uv run python -m ipykernel install --user --name="my-project"
```

Then in VSCode, open any `.ipynb` file and select the kernel matching your project name.

---

## Step 9 — `.env` File for API Keys

Never hardcode API keys. Create a `.env` file at the project root:

```bash
# .env — NEVER commit this file to git
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# Optional overrides
MODEL=gpt-4o
MAX_TOKENS=2048
DEBUG=false
```

And add `.env` to your `.gitignore` immediately:

```bash
echo ".env" >> .gitignore
```

Use `pydantic-settings` to load it (shown above). Do not use `python-dotenv` directly — `pydantic-settings` wraps it and adds validation.

---

## Quick-Start Template

Here is the exact sequence to start any new project in this course:

```bash
# 1. Create project with UV
uv init my-project
cd my-project

# 2. Add your production dependencies
uv add openai anthropic pydantic fastapi httpx structlog

# 3. Add dev dependencies
uv add --dev ruff mypy pytest pytest-asyncio ipykernel

# 4. Register Jupyter kernel
uv run python -m ipykernel install --user --name="my-project"

# 5. Create .env and add to .gitignore
touch .env
echo ".env" >> .gitignore
echo ".venv" >> .gitignore

# 6. Open in VSCode
code .
```

At this point:
- Your Python environment is isolated in `.venv/`
- `uv.lock` pins every dependency to an exact version
- Ruff formats and lints on every save
- Pylance gives you type-aware autocomplete
- `pydantic-settings` will load your `.env` when you import Settings

---

## Troubleshooting Common Issues

**VSCode is not finding the right Python interpreter**
Open the Command Palette (`Ctrl+Shift+P`) → "Python: Select Interpreter" → choose the one from `.venv/bin/python` in your project folder.

**`uv run python` gives `command not found`**
UV was not added to your PATH during installation. Run the install command again and follow the PATH instructions it prints.

**Ruff is not formatting on save**
Make sure `"editor.defaultFormatter": "charliermarsh.ruff"` is inside the `"[python]"` block in your settings, not at the top level.

**Pylance shows errors for libraries like numpy or torch**
These libraries have type stubs. Run `uv add --dev pandas-stubs types-requests` for libraries that have separate stub packages. For others, `"ignore_missing_imports": true` in `pyproject.toml` suppresses the noise.

**Jupyter kernel not found**
Run `uv run python -m ipykernel install --user --name="my-project"` and then reload VSCode. Make sure the Jupyter extension is installed.
