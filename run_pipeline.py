from rlm_core.controller import RLMController

query = "Find abnormal lactate trends in ICU patients with sepsis."

controller = RLMController()
result = controller.run(query)

print("\nFINAL RESULT:\n", result)