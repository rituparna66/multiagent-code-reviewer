# 🤖 Multi-Agent Code Review System

> An AI-driven multi-agent code review pipeline engineered for fintech applications, enabling automated detection of security vulnerabilities, performance bottlenecks, and code quality issues while supporting compliance, auditability, and high-stakes transactional systems.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Workflow-FF6B35?style=for-the-badge)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=for-the-badge&logo=openai&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)

---

## 🏗️ Architecture

```
╔══════════════════════════════════════════════════════════════╗
║                      INPUT LAYER                             ║
║                                                              ║
║     📄 Python File            🐙 GitHub Pull Request         ║
║      (Streamlit UI)             (github_bot.py)              ║
╚═══════════════════════╦══════════════════════════════════════╝
                        ║
                        ▼
╔══════════════════════════════════════════════════════════════╗
║                  LANGGRAPH WORKFLOW                          ║
║                                                              ║
║        ┌─────────────────┐                                  ║
║        │   load_code     │  ← reads file into state         ║
║        └────────┬────────┘                                  ║
║                 │                                            ║
║                 ▼                                            ║
║        ┌─────────────────┐                                  ║
║        │ 🔍  CodeAgent   │  ← smells, naming, structure     ║
║        └────────┬────────┘                                  ║
║                 │                                            ║
║                 ▼                                            ║
║        ┌─────────────────┐                                  ║
║        │ 🔐  SecAgent    │  ← secrets, injections, exposure ║
║        └────────┬────────┘                                  ║
║                 │                                            ║
║                 ▼                                            ║
║        ┌─────────────────┐                                  ║
║        │ ⚡  PerfAgent   │  ← loops, complexity, memory     ║
║        └────────┬────────┘                                  ║
║                 │                                            ║
║                 ▼                                            ║
║        ┌─────────────────┐                                  ║
║        │  📊  Aggregate  │  ← dedup, rank, summarise        ║
║        └────────┬────────┘                                  ║
╚═════════════════╬════════════════════════════════════════════╝
                  ║
                  ▼
╔══════════════════════════════════════════════════════════════╗
║                     OUTPUT LAYER                             ║
║                                                              ║
║    🖥️  Streamlit Dashboard       📄 review_report.json       ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🧠 Agent Breakdown

```
┌──────────────────────┬──────────────────┬─────────────────────────────────────┐
│ Agent                │ Role             │ What It Catches                     │
├──────────────────────┼──────────────────┼─────────────────────────────────────┤
│ 🔍 CodeAnalyzer      │ Code Quality     │ Smells, naming, docstrings, struct  │
│ 🔐 SecurityAgent     │ Security Audit   │ Secrets, injections, unsafe storage │
│ ⚡ PerformanceAgent  │ Performance      │ Loops, complexity, memory, redund.  │
└──────────────────────┴──────────────────┴─────────────────────────────────────┘
```

---

## ⚙️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| 🧠 Orchestration | LangGraph | Stateful multi-agent workflow |
| 🤖 LLM | OpenAI GPT-4o-mini | Agent reasoning backbone |
| 🖥️ UI | Streamlit | Interactive web dashboard |
| ✅ Validation | Pydantic v2 | Structured output enforcement |
| 🐙 Integration | GitHub API | PR-level automated review |

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/rituparna66/multiagent-code-reviewer.git
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
╔══════════════════════════════════════════════╗
║             REVIEW SUMMARY                  ║
╠══════════════════════════════════════════════╣
║  Total Issues : 7                           ║
║  🔴 Critical  : 0                           ║
║  🟠 Serious   : 2                           ║
║  🟡 Moderate  : 2                           ║
║  🟢 Low       : 3                           ║
╚══════════════════════════════════════════════╝

Issues Found:
  [5] 🔴 security          — Hardcoded API key detected
  [4] 🟠 structural        — Hard-coded severity map, inflexible design
  [4] 🟠 performance       — String construction causes high token usage
  [3] 🟡 code_smell        — Stateful variables increase complexity
  [3] 🟡 performance       — Nested loop → O(n×m) complexity
  [2] 🟢 bad_naming        — Function name too generic
  [1] 🟢 missing_docstring — Vague docstring on analyze_security
```

---

## 🔐 Security Checks

```
╔══════════════════════════════════════════════════════════════╗
║                  SECURITY RULESET                            ║
╠══════════════════════════════════════════════════════════════╣
║  🔴 CRITICAL   Hardcoded API keys, tokens, passwords         ║
║  🔴 CRITICAL   Credentials or secrets in source code         ║
║  🔴 CRITICAL   Injection vulnerabilities (SQL, shell, prompt)║
║  🟠 HIGH       Insecure or unencrypted data storage          ║
║  🟠 HIGH       Exposed file paths or world-readable files    ║
║  🟡 MEDIUM     Missing access controls or unsafe defaults    ║
║  🟡 MEDIUM     Unsafe environment variable usage             ║
║  🟢 LOW        Potential info leakage or risky patterns      ║
╚══════════════════════════════════════════════════════════════╝
```

> 💡 **Domain Extensible** — Security rules can be extended for specific domains:
> fintech (PCI-DSS, PAN/IBAN), healthtech (HIPAA, PHI), SaaS (OAuth, rate limits), and more.

---

## 📁 Project Structure

```
multiagent-code-reviewer/
│
├── 📄 app.py                    ← Streamlit web UI
├── 📄 main.py                   ← CLI entry point
├── 📄 github_bot.py             ← GitHub PR reviewer
│
├── 🤖 agents/
│   ├── code_analyzer.py         ← Code quality agent
│   ├── security_agent.py        ← Security audit agent
│   └── performance_agent.py     ← Performance agent
│
├── 🔀 graph/
│   └── workflow.py              ← LangGraph orchestration
│
├── 📐 schemas/
│   └── issue_schema.py          ← Pydantic models
│
├── 🛠️  tools/
│   ├── aggregator.py            ← Issue deduplication & ranking
│   ├── file_reader.py           ← File I/O
│   └── patch_parser.py          ← Git diff parser
│
├── 📄 .env.example
├── 📄 requirements.txt
├── 📄 LICENSE
└── 📄 README.md
```

---

## 🔒 Security Best Practices

- API keys loaded via `.env` — never hardcoded
- `.env` excluded via `.gitignore`
- All secrets managed through `python-dotenv`

---

## 📄 License

MIT © 2026 Soumadeep
