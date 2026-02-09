"""
controller.py

Core Recursive Language Model (RLM) loop for the Recursive Medical Language Model system.

This orchestrates:
- Root model planning
- Code execution in REPL
- Recursive sub-calls
- Memory tracking
- Iterative reasoning until Final answer is produced
"""

from models.medgemma_root import MedGemmaRoot
from rlm_core.repl_env import REPLEnvironment
from rlm_core.recursion_manager import RecursionManager
from rlm_core.memory_manager import MemoryManager
from rlm_core.stdout_parser import StdoutParser

from utils.prompt_loader import load_prompt
ROOT_SYSTEM_PROMPT = load_prompt("prompts/root_system_prompt.txt")


class RLMController:
    def __init__(self, max_iterations=8):
        self.root_model = MedGemmaRoot()
        self.repl = REPLEnvironment()
        self.recursion_manager = RecursionManager()
        self.memory_manager = MemoryManager(self.repl)
        self.stdout_parser = StdoutParser()
        self.max_iterations = max_iterations

        # Expose recursion tool inside REPL
        self.repl.set_variable("recursion_manager", self.recursion_manager)

    def run(self, user_query: str):
        """
        Main recursive reasoning loop.
        """
        history = ROOT_SYSTEM_PROMPT + f"\nUSER QUERY:\n{user_query}\n"

        for step in range(self.max_iterations):
            print(f"\n🔁 Iteration {step + 1}")

            # Ask root model to generate code
            model_output = self.root_model.generate(history)

            # Remove markdown code fences if present
            import re

            model_output = self.root_model.generate(history)

            # Remove markdown/code formatting
            model_output = re.sub(r"\*\*.*?\*\*", "", model_output)  # remove bold sections
            model_output = model_output.replace("```python", "").replace("```", "")
            model_output = model_output.strip()

            print("🧠 Model generated code:\n", model_output)

            # Execute code in REPL
            result = self.repl.execute(model_output)

            # Parse stdout and errors
            feedback = self.stdout_parser.parse(result)

            # Snapshot memory state
            memory_state = self.memory_manager.memory_snapshot()

            # Update history
            history += f"\nMODEL CODE:\n{model_output}\n"
            history += f"\nEXECUTION FEEDBACK:\n{feedback}\n"
            history += f"\nMEMORY STATE:\n{memory_state}\n"

            # Check if model created Final variable
            final_answer = self.repl.get_variable("Final")
            if final_answer is not None:
                print("\n✅ Final answer produced.")
                return final_answer

        return "⚠️ Max iterations reached without producing Final answer."
