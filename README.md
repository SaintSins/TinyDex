# TinyDex

A lightweight, autonomous coding agent harness built in Python. TinyDex implements a deterministic ReAct (Reason + Act) loop using OpenRouter-compatible models to inspect, edit, and execute Python code inside an isolated workspace sandbox.

---

## Architecture Overview

TinyDex functions as an **Agent Harness** that bridges raw LLM reasoning with sandboxed local execution"

* **State & Turn Management:** Maintains multi-turn conversation context across system, user, assistant, and tool execution roles.
* **Execution Dispatcher:** Maps structured tool calls (`tool_calls`) directly to native Python functions and injects safe workspace paths.
* **Security & Containment:** Enforces strict filesystem boundaries to intercept directory climbing (`../`) or absolute path traversal attempts.
* **Deterministic Tool Routing:** Operates with zero temperature and directive system instructions to prevent hallucinated calls or premature termination.

---

## Tool Capabilities

| Tool | Purpose | Security Controls |
|---|---|---|
| `get_files_info` | Lists files, directories, and byte sizes in a given folder. | Blocked from scanning outside the sandbox root using `os.path.commonpath`. |
| `get_file_content` | Reads UTF-8 file contents into memory. | Enforces bounds checking and configurable character truncation limits (`MAX_CHARS`). |
| `write_file` | Writes or overwrites code files in the workspace. | Constrained strictly to valid relative workspace paths. |
| `run_python_file` | Runs scripts and returns `stdout`/`stderr` output. | Executes within the isolated target environment with argument passing. |

---

## Project Structure

```text
.
├── config.py              # Central environment and agent limits (MAX_ITERS, MAX_CHARS)
├── prompts.py             # Agent system prompts and operational rules
├── tools.py               # OpenAI JSON schemas and execution dispatch table
├── main.py                # CLI runner, argument parser, and iterative ReAct loop
├── functions/             # Core sandboxed tool implementations
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
├── tests/                 # Integration test suite for boundary verification
│   ├── test_get_files_info.py
│   ├── test_get_file_content.py
│   ├── test_write_file.py
│   └── test_run_python_file.py
└── calculator/            # Target application sandbox workspace
```

---

## Getting Started

### Prerequisites

* Python 3.10+
* [uv](https://github.com/astral-sh/uv) package manager
* An API key from [OpenRouter](https://openrouter.ai/)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SaintSins/TinyDex.git
   cd tinydex
   ```

2. **Install dependencies:**
    ```bash
    uv sync
    ```

3. **Create environment variables:**
    Create `.env` file in project root:
    ```
    OPENROUTER_API_KEY = your_openrouter_api_key_here
    ```

---

## Usage

Run the agent from the command line by supplying a task prompt:

* **Basic task execution:** Displays the function calls and final response.
```bash
uv run main.py "Inspect the calculator application and run its tests"
```
* **Verbose mode:** Displays token metrics and user prompt along side function calls and final response.
```bash
uv run main.py "Check what files are in the repository" --verbose
```

---

## Verification Tests

Run the integration and sandboxing test suite using module execution:

```bash
uv run python -m tests.test_get_files_info
uv run python -m tests.test_get_file_content
uv run python -m tests.test_write_file
uv run python -m tests.test_run_python_file
```
