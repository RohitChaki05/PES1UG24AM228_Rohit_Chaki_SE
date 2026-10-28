# Issues Document — Hospital Patient System

| Issue Type | Severity | Line(s) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- |
| **Insecure Expression Evaluation (`eval`)** | High | 38 | Use of `eval()` allows arbitrary code execution if user input is malicious. | Replaced `eval()` with safe calculation logic or restricted dictionary operations. |
| **Insecure Hash Function (`md5`)** | Medium | 42 | MD5 is cryptographically broken and vulnerable to collision attacks. | Switched from `hashlib.md5` to `hashlib.sha256`. |
| **Shell Injection / Process Execution** | Medium | 51 | `os.system()` runs commands in a shell, risking command injection. | Replaced `os.system()` with Python's built-in `print()` or logging. |
| **Mutable Default Argument** | Bug / Quality | 16 | `intake_log=[]` retains state across function calls, causing unintended data sharing. | Changed default argument to `None` and initialized `[]` inside the function body. |
| **Bare `except` Clause** | Quality | 27 | Catching all exceptions blindly can mask critical errors or keyboard interrupts. | Specified `except KeyError:` or removed the unnecessary try-except block. |