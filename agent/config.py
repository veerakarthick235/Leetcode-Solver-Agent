"""Configuration constants for LeetCode Auto-Solver"""

# DOM Selectors for LeetCode UI
SELECTORS = {
    "problem_description": ".elfjS, .content__u3I1, [data-track-load='description_content']",
    "monaco_editor": ".monaco-editor .view-lines",
    "code_area": "textarea.inputarea, .monaco-editor",
    "run_button": "[data-e2e-locator='console-run-button'], button[data-cy='run-code-btn']",
    "submit_button": "[data-e2e-locator='console-submit-button'], button[data-cy='submit-code-btn']",
    "result_container": "[data-e2e-locator='submission-result'], .result-container, #result",
    "status_text": ".result-status, [data-e2e-locator='console-result']",
    "accepted_status": ".success, [class*='accepted'], [class*='Success']",
    "wrong_answer": ".error, [class*='wrong'], [class*='Error']"
}

# Timeout values (seconds)
TIMEOUTS = {
    "page_load": 10,
    "editor_ready": 5,
    "test_execution": 30,
    "result_appear": 30,
    "submit_confirm": 10
}

# Retry configuration
RETRY_CONFIG = {
    "max_retries": 2,
    "backoff_factor": 2,  # 2s, 4s, 8s, ...
    "initial_delay": 1
}

# Polling intervals (seconds)
POLLING_INTERVALS = {
    "result_check": 0.5
}
