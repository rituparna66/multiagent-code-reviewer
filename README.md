# 🤖 Multi-Agent Code Review System

A fintech-grade, AI-powered code review pipeline that automatically analyzes Python code for **security vulnerabilities**, **performance issues**, and **code quality** using a multi-agent LangGraph workflow.

---

## 🏗️ Architecture

```
Input (File / GitHub PR)
        │
        ▼
┌─────────────────────────────────────┐
│           LangGraph Workflow         │
│                                     │
│  load_code → code_agent             │
│                  ↓                  │
│           security_agent            │
│                  ↓                  │
│          performance_agent          │
│                  ↓                  │
│             aggregate               │
└─────────────────────────────────────┘
        │
        ▼
  Structured Report (JSON + UI)
```

---

## 🧠 Agents

| Agent | Role | Checks |
|-------|------|--------|
| `CodeAnalyzer` | Code quality | Smells, naming, docstrings, structure |
| `SecurityAgent` | Security audit | Hardcoded secrets, PCI-DSS, PAN/IBAN, injection, encryption |
| `PerformanceAgent` | Performance | Loops, complexity, memory, redundant ops |

---

## ⚙️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-0.1+-orange)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-purple)

- **LangGraph** — stateful multi-agent orchestration
- **OpenAI GPT-4o-mini** — LLM backbone for all agents
- **Streamlit** — interactive web UI
- **Pydantic v2** — structured output validation
- **GitHub API** — PR-level code review via `github_bot.py`

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/multiagent-code-reviewer.git
cd multiagent-code-reviewer
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Fill in your API keys in .env
```

### 5. Run the Streamlit UI
```bash
streamlit run app.py
```

### 6. Or run via CLI
```bash
python main.py
```

### 7. Review a GitHub PR
```bash
python github_bot.py <owner> <repo> <pr_number>
```

---

## 📊 Sample Output

```
Summary:
{'total_issues': 7, 'critical': 0, 'serious': 2, 'moderate': 2, 'low': 3}

Issues:
  [4] structural_problem  — Hard-coded severity map makes code inflexible
  [4] performance         — Long string construction may lead to high token usage
  [3] code_smell          — Stateful variables increase cognitive complexity
  [3] performance         — Nested loop introduces O(n*m) complexity
  [2] bad_naming          — Function name too generic
  [2] performance         — Redundant string splitting
  [1] missing_docstrings  — Vague docstring on analyze_security
```

---

## 🏦 Fintech-Specific Security Checks

The `SecurityAgent` is tuned for fintech compliance:

- 🔴 Hardcoded API keys, tokens, passwords
- 🔴 PAN / card number patterns
- 🔴 SWIFT / IBAN code exposure
- 🟠 PCI-DSS violations
- 🟠 Unencrypted financial data storage
- 🟡 Missing audit logs for transactions
- 🟡 Unsafe environment variable usage
- 🟢 Overly permissive file operations

---

## 📁 Project Structure

```
multiagent/
├── app.py                  # Streamlit UI
├── main.py                 # CLI entry point
├── github_bot.py           # GitHub PR reviewer
├── agents/
│   ├── code_analyzer.py    # Code quality agent
│   ├── security_agent.py   # Security audit agent
│   └── performance_agent.py# Performance agent
├── graph/
│   └── workflow.py         # LangGraph orchestration
├── schemas/
│   └── issue_schema.py     # Pydantic models
├── tools/
│   ├── aggregator.py       # Issue deduplication
│   ├── file_reader.py      # File I/O
│   └── patch_parser.py     # Git diff parser
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🔒 Security

- API keys are loaded via `.env` — never hardcoded
- `.env` is excluded via `.gitignore`
- All secrets managed through `python-dotenv`

---

## 📄 License

MIT
