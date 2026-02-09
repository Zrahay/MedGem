import os
from utils.prompt_loader import load_prompt

from models.medgemma_root import MedGemmaRoot
from rlm_core.repl_env import REPLEnvironment
from rlm_core.recursion_manager import RecursionManager
from rlm_core.memory_manager import MemoryManager
from rlm_core.stdout_parser import StdoutParser


class RLMController:
    def __init__(self, max_iterations=8):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prompt_path = os.path.join(base_dir, "prompts", "root_system_prompt.txt")
        self.root_system_prompt = load_prompt(prompt_path)

        self.root_model = MedGemmaRoot()
        self.repl = REPLEnvironment()
        self.recursion_manager = RecursionManager()
        self.memory_manager = MemoryManager(self.repl)
        self.stdout_parser = StdoutParser()
        self.max_iterations = max_iterations

        self.repl.set_variable("recursion_manager", self.recursion_manager)

    def run(self, user_query: str):
        history = self.root_system_prompt + f"\nUSER QUERY:\n{user_query}\n"

        for step in range(self.max_iterations):
            print(f"\n🔁 Iteration {step + 1}")

            model_output = self.root_model.generate(history)

            # Clean up model output to extract Python code
            import re
            
            # Remove markdown bold markers but keep content inside
            model_output = re.sub(r'\*\*([^*]+)\*\*', r'\1', model_output)
            
            # Remove markdown code fence markers
            model_output = model_output.replace("```python", "").replace("```", "")
            
            # Remove numbered list prefixes (1. , 2. , etc.)
            model_output = re.sub(r'^\d+\.\s*', '', model_output, flags=re.MULTILINE)
            
            # Filter out lines that are purely explanatory (don't contain Python syntax)
            lines = model_output.strip().split('\n')
            code_lines = []
            for line in lines:
                stripped = line.strip()
                # Skip empty lines or lines that look like explanatory text
                if not stripped:
                    continue
                # Skip "Step N:" lines that are explanatory
                if re.match(r'^Step\s*\d+[:\.]', stripped, re.IGNORECASE):
                    continue
                # Skip lines that start with dashes or bullets (explanation lists)
                if stripped.startswith('-') and '=' not in stripped:
                    continue
                # Skip lines that start with common explanation patterns
                if any(stripped.lower().startswith(p) for p in [
                    'this code', 'the code', 'this function', 'we ', 'you ', 
                    'here', 'note:', 'explanation:', 'output:', 'this snippet',
                    'identifying', 'extracting', 'summarizing', 'filtering',
                    'storing', 'finalizing', 'outputting', 'retrieves', 'queries'
                ]):
                    continue
                # Skip lines that are just punctuation or markdown
                if stripped in ['---', '***', '===', '"""', "'''"]:
                    continue
                code_lines.append(line)
            
            model_output = '\n'.join(code_lines).strip()

            print("🧠 Model generated code:\n", model_output)

            # Skip if no code was extracted
            if not model_output:
                history += f"\nMODEL CODE:\n<empty>\n"
                history += f"\nEXECUTION FEEDBACK:\nNo code provided. Please output Python code.\n"
                continue

            result = self.repl.execute(model_output)
            feedback = self.stdout_parser.parse(result)
            memory_state = self.memory_manager.memory_snapshot()

            history += f"\nMODEL CODE:\n{model_output}\n"
            history += f"\nEXECUTION FEEDBACK:\n{feedback}\n"
            history += f"\nMEMORY STATE:\n{memory_state}\n"

            final_answer = self.repl.get_variable("Final")
            if final_answer is not None:
                print("\n✅ Final answer produced.")
                return final_answer

        return "⚠️ Max iterations reached without producing Final answer."