import re

class SymbolTable:
	def __init__(self):
		self.data = dict()
		self.parsed_inst = None
	
	def load_parsed_inst(self, parsed_inst: list[str]):
		self.parsed_inst = parsed_inst

	def fetch(self):
		if self.parsed_inst is None:
			raise RuntimeError(f"Parsed instruction not supplied!")

		self._initialize_table()
		self._run_first_pass()
		self._run_second_pass()

	def _initialize_table(self):
		self.data.update({f"R{i}": i for i in range(16)})
		self.data.update({"SCREEN": 16384})
		self.data.update({"KBD": 24576})
		self.data.update({"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4})
	
	def _run_first_pass(self):
		counter = 0
		for i, line in enumerate(self.parsed_inst):
			if line.startswith("(") and line.endswith(")"):
				label = re.sub("[()]", "", line)
				self.data.update({label: i-counter}) # add the label symbol with corresponding line number
				counter += 1

	def _run_second_pass(self):
		var_counter = 0
		for line in self.parsed_inst:	
			label = line.lstrip("@")
			if line.startswith("@") and not label.isnumeric() and label not in self.data:
				self.data.update({label: 16+var_counter})
				var_counter += 1
