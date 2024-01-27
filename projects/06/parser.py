import re

class Parser:
	def __init__(self, verbose=1):
		self.inst = None
		self.verbose = verbose
		if self.verbose: print(f"[DEBUG={verbose}]")

	def is_loaded(self):
		return False if self.inst is None else True

	def load_instruction(self, inst):
		self.inst = inst
		if self.verbose: print("="*25)

	def get_instruction_type(self):
		return "A" if self.inst.startswith("@") else "C"

	def parse_c_instruction(self):
		assert self.get_instruction_type() == "C", f"A-instruction was supplied: {self.inst}"
		dest, comp, jump = re.match("(?:(.*)=)?([\w|&!+-]+)(?:;(.*))?", self.inst).groups()
		return dest, comp, jump

	def run(self):
		if self.verbose: print(f"Instruction: {self.inst}")
		if not self.is_loaded:
			raise RuntimeError(f"Please load instruction first!")

		if not self.inst.strip():
			if self.verbose: print("Empty instruction")
			return 

		inst_type = self.get_instruction_type()
		if inst_type == "A":
			out = ("A", self.inst)
		else:
			out = ("C", self.parse_c_instruction())

		if self.verbose: print(out)
		return out

if __name__ == "__main__":
	parser = Parser(verbose=2)

	# example 1
	inst = "D=M+1;JEQ"
	parser.load_instruction(inst)
	parser.run()

	# example 2
	inst = "D;JMP"
	parser.load_instruction(inst)
	parser.run()

	# example 3
	inst = "@8149"
	parser.load_instruction(inst)
	parser.run()

	"""
	# example 4
	inst = "// this is a comment"
	parser.load_instruction(inst)
	parser.run()

	# example 5
	inst = "@a // this is a"
	parser.load_instruction(inst)
	parser.run()
	"""
