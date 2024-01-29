import sys
from pathlib import Path
from parser import Parser
from codewriter import CodeWriter

class Main:
	def __init__(self, fpath: str):
		self.fpath = Path(fpath)
		self.parser = Parser()
		self.codewriter = CodeWriter(self.fpath.stem)

	def assemble(self):
		self.parser.read(self.fpath)
		while self.parser.has_more_commands():
			 command = self.parser.command_type()
			 segment = self.parser.arg1()
			 print(self.parser.current, self.parser._get_current_instruction(), command)
			 if command == "C_ARITHMETIC":
				 self.codewriter.write_arithmetic(segment)
			 elif command in ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]:
				 index = self.parser.arg2()
				 self.codewriter.write_push_pop(command, segment, index)
			 else:
				 raise NotImplementedError()
			 self.parser.advance()		

		fpath = Path(self.fpath).with_suffix(".asm")
		print(f"[INFO] Generated Hack assembly code {fpath}")
		self.codewriter.close(fpath)

if __name__ == "__main__":
	if len(sys.argv) == 1:
		raise RuntimeError("[ERROR] please provide the VM file")
	elif len(sys.argv) > 2:
		print(f"[WARNING] arguments ignored: {' '.join(sys.argv[2:])}")

	Main(sys.argv[1]).assemble()
