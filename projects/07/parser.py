from pathlib import Path
from utils import remove_comment

ARITHMETIC_CMD = ["add", "sub", "neg", "eq", "gt", "lt"]
LOGICAL_CMD = ["and", "or", "not"]
MEMORY_ACCESS_CMD = ["push", "pop"]
BRANCHING_CMD = [] # TODO
FUNCTION_CMD = [] # TODO

class Parser:
	def __init__(self):
		self._instructions = []
		self.current = 0

	def __len__(self):
		return len(self._instructions)

	def read(self, fpath: str) -> None:
		fpath = Path(fpath)
		assert fpath.suffix == ".vm", f"Invalid file extension: {fpath}"
		with open(fpath) as f:
			insts = f.readlines() # each instruction per line
			insts = [remove_comment(inst).strip() for inst in insts] # remove comments
			insts = [inst for inst in insts if inst != ""] # drop empty lines
			self._instructions = insts 

	def has_more_commands(self) -> bool:	
		return True if self.current < self.__len__() else False

	def advance(self):
		if self.has_more_commands():
			self.current += 1

	def command_type(self):
		cmd = self._get_current_instruction().split(" ")[0]
		if cmd in ARITHMETIC_CMD + LOGICAL_CMD:
			return "C_ARITHMETIC"
		elif cmd == "push":
			return "C_PUSH"
		elif cmd == "pop":
			return "C_POP"
		elif cmd == "label":
			return "C_LABEL"
		elif cmd == "goto":
			return "C_GOTO"
		elif cmd == "if-goto":
			return "C_IF"
		elif cmd == "function":
			return "C_FUNCTION"
		elif cmd == "call":
			return "C_CALL"
		elif cmd == "return":
			return "C_RETURN"
		else:
			raise RuntimeError(f"Invalid VM command: {cmd}")

	def _get_current_instruction(self) -> str:
		return self._instructions[self.current]

	def arg1(self) -> str: # segment
		cinst = self._get_current_instruction()
		if self.command_type() == "C_ARITHMETIC":
			return cinst
		else:
			return cinst.split(" ")[1]

	def arg2(self) -> int: # index
		ctype = self.command_type()
		assert ctype in ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"], f"Invalid VM command type: {ctype}"

		cinst = self._get_current_instruction()
		return int(cinst.split(" ")[2])
			

if __name__ == "__main__":
	parser = Parser()
	#parser.read("./MemoryAccess/BasicTest/BasicTest.asm")
	parser.read("./MemoryAccess/BasicTest/BasicTest.vm")
	while parser.has_more_commands():
		try:
			print(parser.current, parser._get_current_instruction(), "||", parser.command_type(), parser.arg1(), parser.arg2())
		except AssertionError:
			print(parser.current, parser._get_current_instruction(), "||", parser.command_type(), parser.arg1(), None)
		parser.advance()
