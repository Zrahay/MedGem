"""
recursion_manager.py

Handles recursive sub-model calls inside the R-MedLM system.
Allows the REPL environment to invoke MedGemma on focused subtasks.
"""

from models.medgemma_subcall import MedGemmaSubcall


class RecursionManager:
    def __init__(self):
        self.sub_model = MedGemmaSubcall()

    def call_submodel(self, instruction: str, data: str):
        """
        Performs a recursive reasoning call using the sub-model.

        Parameters:
        - instruction: What the model should do (e.g., analyze trends)
        - data: The chunk of patient or cohort data

        Returns:
        - Model-generated reasoning output
        """
        prompt = f"""
You are a clinical reasoning assistant.

TASK:
{instruction}

DATA:
{data}

Provide a structured clinical analysis.
"""

        return self.sub_model.generate(prompt)
