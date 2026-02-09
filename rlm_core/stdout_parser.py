"""
stdout_parser.py

Parses and compresses REPL execution output so the root model
gets useful feedback without large data dumps.
"""

class StdoutParser:
    def __init__(self, max_chars=500):
        self.max_chars = max_chars

    def parse(self, execution_result):
        """
        Takes the REPL execution result and returns a short summary.
        """
        if not execution_result["success"]:
            return f"ERROR:\n{execution_result['error'][:self.max_chars]}"

        stdout = execution_result["stdout"].strip()

        if not stdout:
            return "Execution successful. No printed output."

        if len(stdout) > self.max_chars:
            stdout = stdout[:self.max_chars] + "... [truncated]"

        return f"Execution output:\n{stdout}"
