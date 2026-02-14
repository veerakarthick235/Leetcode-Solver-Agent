
# 🧠 Autonomous LeetCode AI Agent
### Browser-Native LLM System for End-to-End Problem Solving

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Selenium](https://img.shields.io/badge/Selenium-WebDriver-green?logo=selenium)
![LLM](https://img.shields.io/badge/AI-Llama%203.1%208B-purple)
![Status](https://img.shields.io/badge/Status-Production%20Grade-success)

**An autonomous AI agent that reads LeetCode problems directly from the browser, generates optimized solutions using LLMs, injects code into the Monaco editor, submits responses, and navigates to the next problem — fully hands-free.**

This project demonstrates **AI systems engineering**, **agent orchestration**, and **browser-level automation**, going beyond simple prompt engineering to build a resilient, acting agent.

---

## 🚀 Key Capabilities

### 🔗 Browser–AI Synchronization
* **Live Session Attachment:** Attaches to an existing Chrome session via Chrome DevTools Protocol (CDP) on port `9222`.
* **Real-Time DOM Extraction:** Scrapes problem descriptions, constraints, and examples directly from the DOM.
* **Authenticated Context:** Operates on an already logged-in instance, bypassing complex login automation and CAPTCHAs.

### 🧠 Autonomous Reason–Act Loop
The agent performs a continuous state-machine loop without human intervention:
1.  **PERCEIVE:** Reads the problem statement and starter code.
2.  **THINK:** Generates a Python solution using **Llama-3.1-8B** (via Bytez API).
3.  **ACT:** Injects code into the Monaco editor using a JavaScript bridge.
4.  **VERIFY:** Runs test cases first to ensure syntax correctness.
5.  **SUBMIT:** Submits the solution and evaluates the result (Accepted/Error).
6.  **NAVIGATE:** Moves to the next problem in the list.

### 🛡️ Advanced Anti-Detection Engineering
* **Exponential Backoff:** Automatically detects `429 Too Many Requests` errors and triggers a "Cooldown Mode" (20-60 mins).
* **Batch Processing:** Solves problems in batches (e.g., 5 problems) followed by a mandatory "Coffee Break" to mimic human pacing.
* **Human-Like Interaction:** Implements a "Write → Run → Wait (10s) → Submit" workflow to avoid bot detection flags.

---

## 🏗️ System Architecture

```mermaid
graph TD
    A[Chrome Browser (LeetCode Tab)] <-->|DevTools Protocol :9222| B(Browser Controller)
    B -->|Extract Context| C{Agent Core}
    C -->|Prompt Engineering| D[LLM Router]
    D -->|API Call| E[Bytez API / Llama 3.1]
    E -->|Generated Code| C
    C -->|JS Injection| B
    B -->|Click 'Run' & 'Submit'| A
    C -->|Log Result| F[Memory / Logs]
```

---

## 🧪 Tech Stack

| Layer | Technology | Description |
| --- | --- | --- |
| **Agent Core** | Python 3.x | Main logic loop and state management. |
| **Browser Control** | Selenium WebDriver | DOM manipulation and JavaScript execution. |
| **LLM Integration** | Bytez API | Access to open-source models (Meta-Llama-3.1-8B-Instruct). |
| **Editor Automation** | JavaScript Injection | Direct manipulation of the Monaco Editor model. |
| **Resilience** | `retry` / `backoff` | Custom logic to handle network instability and rate limits. |

---

## 📊 Engineering Challenges Solved

| Challenge | Solution |
| --- | --- |
| **Live Browser Attachment** | Utilized `--remote-debugging-port=9222` to attach Selenium to a manual Chrome session. |
| **Rate Limiting (429)** | Implemented a "Batch & Cool-down" strategy: Solve 5 -> Sleep 3 mins -> Refresh Session. |
| **Editor Injection** | Bypassed standard `send_keys` (which is slow/flaky) by injecting directly into the `monaco.editor` instance via JS. |
| **Dynamic UI Changes** | Created a "Multi-Selector" strategy that tries 5+ different CSS/XPath selectors for buttons to handle LeetCode's A/B testing. |
| **Bot Detection** | Added random variance to wait times (e.g., `random.uniform(30, 60)`) and forced "Run Code" before "Submit". |

---

## 🧭 How to Run

### 1️⃣ Start Chrome in Debug Mode

Close all Chrome instances. Open your terminal (CMD/PowerShell) and run:

```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenium\ChromeProfile"
```

*Log in to LeetCode in this new window.*

### 2️⃣ Install Dependencies

```bash
pip install selenium requests python-dotenv
```

### 3️⃣ Configure Environment

Create a `.env` file in the root directory:

```env
BYTEZ_API_KEY=your_key_here
```

### 4️⃣ Start the Agent

```bash
python main.py
```

*The agent will attach to your open Chrome window and begin solving.*

---

## 🧠 Agent Design Pattern

This system follows a strict **State Machine** architecture:

* **🟢 READ:** Extract `description`, `constraints`, and `starter_code`.
* **🟡 THINK:** Query LLM with strict output formatting rules.
* **🟠 ACT:** Inject code -> Click 'Run' -> Wait for 'Accepted' text.
* **🔴 EVALUATE:** If success, Click 'Submit'. If fail, log error.
* **🔵 NAVIGATE:** Click 'Next Problem', refreshing if the DOM freezes.

---

## 🛣️ Roadmap

* [ ] **Reinforcement Learning:** Use submission feedback (Runtime/Memory) to optimize code.
* [ ] **Vector Memory:** Store solved problems in a vector DB to reuse patterns for similar questions.
* [ ] **Multi-Tab Solving:** Parallelize solving across multiple browser tabs.
* [ ] **Local Fallback:** Switch to Ollama/vLLM if the API quota is exhausted.

---

## ⚠️ Ethical & Platform Compliance Note

*This project is for educational and research purposes only.*
Users must ensure compliance with LeetCode’s terms of service and API usage policies before running autonomous automation. The "Safe Mode" delays are implemented to be respectful of the platform's resources.

---

## 👤 Author

**Veera Karthick**
*AI & Data Science Engineer*
Applied AI Systems • Autonomous Agents • LLM Orchestration

🌐 **Portfolio:** https://veerakarthick.in
💻 **GitHub:** https://github.com/veerakarthick235

---

### 🏁 Recruiter Summary

An end-to-end autonomous AI agent that:

1. **Grounds LLMs** in a live browser environment.
2. Performs **multi-step reasoning** and tool use.
3. **Recovers from failures** and manages strict API quotas.
4. Executes **continuous task loops** with production-grade reliability.

*This project showcases architecture suitable for Applied AI, AI Infrastructure, and LLM Systems Engineering roles.*
