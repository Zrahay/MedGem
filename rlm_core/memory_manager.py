"""
memory_manager.py

Tracks and summarizes variables created during REPL execution.
Prevents flooding the root model with large medical data objects.
"""

class MemoryManager:
    def __init__(self, repl_env):
        self.repl_env = repl_env

    def list_variables(self):
        """
        Returns a list of variable names currently in memory,
        excluding internal/system entries.
        """
        return [
            name for name in self.repl_env.globals.keys()
            if not name.startswith("__")
        ]

    def summarize_variable(self, name):
        """
        Provides a short summary of a variable without exposing full data.
        """
        value = self.repl_env.get_variable(name)

        if value is None:
            return f"{name}: Not found"

        try:
            length = len(value)
            return f"{name}: type={type(value).__name__}, length={length}"
        except:
            return f"{name}: type={type(value).__name__}"

    def memory_snapshot(self):
        """
        Returns summaries of all variables for feeding back to root model.
        """
        summaries = [self.summarize_variable(v) for v in self.list_variables()]
        return "\n".join(summaries)
