import sys
from pathlib import Path
from parser import Parser
from codewriter import CodeWriter

class Main:
	def __init__(self, path: str):
		self.path = Path(path)
		self.fpaths = [f for f in self.path.iterdir() if f.suffix == ".vm"] if self.path.is_dir() else [self.path]
		self.parser = Parser()
		self.codewriter = CodeWriter()

	def contains_sys(self):
		for fpath in self.fpaths:
			if fpath.name == "Sys.vm":
				return True
		return False

	def assemble(self):
		if self.contains_sys():
			self.codewriter.set_filename("")
			self.codewriter.write_init()
		for fpath in self.fpaths:
			print(fpath)
			self.parser.read(fpath)
			self.codewriter.set_filename(fpath.stem) # load filename
			while self.parser.has_more_commands():
				 command = self.parser.command_type()
				 segment = self.parser.arg1()
				 print(self.parser.current, self.parser._get_current_instruction(), command)
				 if command == "C_ARITHMETIC":
					 self.codewriter.write_arithmetic(segment)
				 elif command in ["C_PUSH", "C_POP"]:
					 index = self.parser.arg2()
					 self.codewriter.write_push_pop(command, segment, index)
				 elif command == "C_LABEL":
					 self.codewriter.write_label(segment)
				 elif command == "C_GOTO":
					 self.codewriter.write_goto(segment)
				 elif command == "C_IF":
					 self.codewriter.write_if(segment)
				 elif command == "C_FUNCTION":
					 index = self.parser.arg2()
					 self.codewriter.write_function(segment, index)
				 elif command == "C_CALL":
					 index = self.parser.arg2()
					 self.codewriter.write_call(segment, index)
				 elif command == "C_RETURN":
					 self.codewriter.write_return()
				 else:
					 raise NotImplementedError()
				 self.parser.advance()		

		fpath = self.path.with_suffix(".asm") if not self.path.is_dir() else self.path / Path(self.path.name + ".asm")
		print(f"[INFO] Generated Hack assembly code {fpath}")
		self.codewriter.close(fpath)


if __name__ == "__main__":
	if len(sys.argv) != 2:
		raise RuntimeError("[ERROR] please provide a VM file or a directory with VM files.")

	path = Path(sys.argv[1])
	if path.is_dir():
		# check if folder contains at least 1 .vm file
		is_valid = False
		for f in path.iterdir():
			if f.suffix == ".vm":
				is_valid = True

		if not is_valid:
			raise RuntimeError(f"[ERROR] the directory does not contain a VM file: {path}")
	else:
		if path.suffix != ".vm":
			raise RuntimeError(f"[ERROR] please provide a VM file")

	# now path is a valid path
	Main(path).assemble()
