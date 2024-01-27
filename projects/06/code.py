COMP = {
	  "0": "0_101010",
	  "1": "0_111111",
	 "-1": "0_111010",
	  "D": "0_001100",
	  "A": "0_110000",
	 "!D": "0_001101",
	 "!A": "0_110001",
	 "-D": "0_001111",
	 "-A": "0_110011",
	"D+1": "0_011111",
	"A+1": "0_110111",
	"D-1": "0_001110",
	"A-1": "0_110010",
	"D+A": "0_000010",
	"D-A": "0_010011",
	"A-D": "0_000111",
	"D&A": "0_000000",
	"D|A": "0_010101",
	  "M": "1_110000",
	 "!M": "1_110001",
	 "-M": "1_110011",
	"M+1": "1_110111",
	"M-1": "1_110010",
	"D+M": "1_000010",
	"D-M": "1_010011",
	"M-D": "1_000111",
	"D&M": "1_000000",
	"D|M": "1_010101",
}

DEST = {
	 None: "000",
	  "M": "001",
	  "D": "010",
	 "MD": "011",
	  "A": "100",
	 "AM": "101",
	 "AD": "110",
	"AMD": "111",
}

JUMP = {
	 None: "000",
	"JGT": "001",
	"JEQ": "010",
	"JGE": "011",
	"JLT": "100",
	"JNE": "101",
	"JLE": "110",
	"JMP": "111",
}

class Code:
	def __init__(self):
		self.symbol_table = None  

	def load_symbol_table(self, symbol_table: dict):
		self.symbol_table = symbol_table

	def _int2binary(self, x: int):
		return '{0:016b}'.format(x)

	def _translate_A_inst(self, inst):
		addr = inst[1].lstrip("@")
		if addr in self.symbol_table:
			addr = self.symbol_table[addr]
		addr = int(addr)
		out = self._int2binary(addr)
		return out

	def _translate_C_inst(self, inst):
		_, (dest, comp, jump) = inst
		out =	"111"
		a, cccccc = COMP[comp].split("_")
		out += a
		out += cccccc
		out += DEST[dest]
		out += JUMP[jump]
		return out

	def translate(self, inst):
		if inst[0] == "A": 
			return self._translate_A_inst(inst)
		else:
			return self._translate_C_inst(inst)
