
# 🧠 Autonomous LeetCode AI Agent
### Browser-Native LLM System with Verified Run → Submit Pipeline

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Selenium](https://img.shields.io/badge/Selenium-WebDriver-green?logo=selenium)
![LLM](https://img.shields.io/badge/AI-Llama%203.1%208B-purple)
![Status](https://img.shields.io/badge/Status-Production%20Grade-success)

An autonomous AI agent that reads LeetCode problems from the browser, generates solutions with LLMs, **runs test cases for verification**, then submits only when valid — and navigates to the next problem fully hands-free.

This project focuses on **AI systems engineering, agent orchestration, and resilient browser automation**.

---

# 🚀 Core Capabilities

## 🔗 Browser–AI Synchronization
- Attaches to an authenticated Chrome session via **CDP (port 9222)**
- Real-time DOM extraction of problem, constraints, and starter code
- No login automation required

## 🧠 Autonomous Reason–Act Loop

The agent follows a strict **verified execution pipeline**:

1. **READ** → Extract problem + starter code from DOM  
2. **THINK** → Generate Python solution using Llama‑3.1‑8B (Bytez API)  
3. **ACT** → Inject code into Monaco editor via JavaScript bridge  
4. **RUN** → Click **Run Code** and wait for test output  
5. **VERIFY** → Parse console for:
   - Compile Error  
   - Runtime Error  
   - Wrong Answer  
   - Accepted (sample tests)  
6. **SUBMIT** → Only if RUN stage passes  
7. **EVALUATE** → Parse final submission result  
8. **NAVIGATE** → Move to next problem  

This ensures **human-like behavior**, higher acceptance rate, and safer platform interaction.

---

## 🛡️ Resilience & Anti-Detection Engineering

- **Exponential Backoff** for `429 Too Many Requests`
- **Batch Processing** (e.g., 5 problems → cooldown)
- **Human-like pacing** (Run → wait → Submit)
- Randomized delays to avoid deterministic timing patterns

---

# 🧪 Tech Stack

| Layer | Technology | Description |
|-------|------------|-------------|
Agent Core | Python 3.x | State machine loop and orchestration |
Browser Control | Selenium WebDriver | DOM control + JS execution |
LLM Integration | Bytez API | Llama‑3.1‑8B‑Instruct inference |
Editor Control | Monaco JS Injection | Direct editor model update |
Resilience | retry / backoff | Rate-limit and failure recovery |

---

# 📊 Engineering Challenges Solved

| Challenge | Solution |
|-----------|----------|
Live browser attachment | CDP remote debugging session |
Rate limits (429) | Exponential backoff + cooldown mode |
Editor instability | Direct Monaco model injection (no send_keys) |
UI A/B changes | Multi-selector fallback strategy |
Bot detection risk | Mandatory Run → Verify → Submit workflow |

---

# 🧠 Agent State Machine

```
READ → THINK → ACT → RUN → VERIFY → SUBMIT → EVALUATE → NAVIGATE
```

Submission is **blocked** if:
- Compile Error  
- Runtime Error  
- Failed sample tests  

---

# ▶️ How to Run

## 1️⃣ Start Chrome in Debug Mode

```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenium\ChromeProfile"
```

Log into LeetCode and open any problem.

## 2️⃣ Install Dependencies

```bash
pip install selenium requests python-dotenv
```

## 3️⃣ Configure Environment

Create `.env`:

```
OPENAI_API_KEY=your_key_here
```

## 4️⃣ Start the Agent

```bash
python main.py
```

The agent will:
- Attach to the active LeetCode tab  
- Inject code  
- **Run tests → Verify → Submit**  
- Navigate automatically  

---

# 📈 Performance Goals (Add Your Metrics)

```
Problems solved: XX
Acceptance rate: XX%
Avg solve time: XX seconds
Failover recovery: <2 seconds
```

---

# 🛣️ Roadmap

- Reinforcement learning from runtime/memory feedback  
- Vector memory for pattern reuse  
- Multi-tab parallel solving  
- Local fallback via Ollama/vLLM  

---

# ⚠️ Ethical Note

For educational and research purposes only.  
Ensure compliance with LeetCode Terms of Service before running automation.

---

# 👤 Author

**Veera Karthick**  
AI & Data Science Engineer  
Applied AI Systems • Autonomous Agents • LLM Orchestration  

🌐 https://veerakarthick.in  
💻 https://github.com/veerakarthick235  

---

# 🏁 Recruiter Summary

A production-style autonomous LLM agent that:

- Grounds reasoning in a live browser environment  
- Verifies outputs via test execution before submission  
- Handles rate limits and failures gracefully  
- Executes continuous tool-using decision loops  

Demonstrates real-world **AI agent architecture and orchestration**.
