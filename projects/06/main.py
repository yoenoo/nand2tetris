from parser import Parser
from code import Code
from symbol_table import SymbolTable
from utils import remove_comment, remove_whitespace

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, required=True)
parser.add_argument('-v', type=int, default=0)
FLAGS,_ = parser.parse_known_args()


class Main:
	def __init__(self, fpath, verbose=0):
		self.fpath = fpath
		self.insts = []
		self.parser = Parser(verbose=verbose)
		self.code = Code()
		self.symbol_table = SymbolTable()

	def read(self, fpath):
		with open(fpath) as f:
			return f.read()

	def save(self, bytecodes: list[str], fpath: str):
		with open(fpath, "w") as f:
			f.write("\n".join(bytecodes))

	def generate_insts(self, asm: str) -> list[str]:
		insts = []
		for line in asm.split("\n"):
			line = remove_comment(line)
			line = remove_whitespace(line)
			if line != "":
				insts.append(line)
		return insts

	def assemble(self):
		asm = self.read(self.fpath)

		bytecodes = []
		self.insts = self.generate_insts(asm)
		self.symbol_table.load_parsed_inst(self.insts)
		self.symbol_table.fetch()
		print(self.symbol_table.data)
		self.code.load_symbol_table(self.symbol_table.data)

		self.insts = [inst for inst in self.insts if not (inst.startswith("(") and inst.endswith(")"))]
		for inst in self.insts:
			self.parser.load_instruction(inst)
			inst = self.parser.run()
			bytecode = self.code.translate(inst)
			bytecodes.append(bytecode)
	
		save_path = self.fpath.replace(".asm", ".hack")
		self.save(bytecodes, save_path)
		print(f"[INFO] Generated {save_path}")
		return bytecodes


if __name__ == "__main__":
	Main(FLAGS.f, verbose=FLAGS.v).assemble()
