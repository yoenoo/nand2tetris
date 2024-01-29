REGISTER = {
	"local": "LCL",
	"argument": "ARG",
	"this": "THIS",
	"that": "THAT",
	"temp": "R5",
}

class CodeWriter:
	def __init__(self, fname: str):
		self.asm = ""
		self.fname = fname
		self.symbol_counter = 0

	def write(self, command):
		self.asm += command + "\n"

	def close(self, fpath: str):
		with open(fpath, "w") as f:
			f.write(self.asm.strip())

	def get_register_name(self, segment: str):
		if segment in REGISTER: return REGISTER[segment]
		else: raise RuntimeError(f"Invalid segment: {segment}")

	def write_arithmetic(self, command: str):
		if   command == "add": self._write_add()
		elif command == "sub": self._write_sub()
		elif command == "neg": self._write_neg()
		elif command == "eq" : self._write_eq()
		elif command == "gt" : self._write_gt()
		elif command == "lt" : self._write_lt()
		elif command == "and": self._write_and()
		elif command == "or" : self._write_or()
		elif command == "not": self._write_not()

	def _write_add(self):
		self.write("// add")
		self.write("@SP")
		self.write("M=M-1")
		self.write("A=M")
		self.write("D=M")
		self.write("@SP")
		self.write("M=M-1")
		self.write("A=M")
		self.write("M=D+M")
		self.write("@SP")
		self.write("M=M+1")

	def _write_sub(self):
		self.write("// sub")
		self.write("@SP")
		self.write("M=M-1")
		self.write("A=M")
		self.write("D=M") 
		self.write("@SP")
		self.write("M=M-1")
		self.write("A=M")
		self.write("M=M-D")
		self.write("@SP")
		self.write("M=M+1")

	def _write_neg(self): 
		self.write("// neg")
		self.write("@SP")
		self.write("M=M-1")
		self.write("A=M")
		self.write("D=-M")
		self.write("M=D")
		self.write("@SP")
		self.write("M=M+1")

	def _write_eq(self): 
		self.write("// eq")
		self.write("@SP")
		self.write("M=M-1")
		self.write("A=M")
		self.write("D=M")
		self.write("@SP")
		self.write("M=M-1")
		self.write("A=M")
		self.write("D=D-M")
		self.write(f"@EQ_{self.symbol_counter}")
		self.write("D;JEQ")
		self.write("D=0") # false
		self.write(f"@END_{self.symbol_counter}")
		self.write("0;JMP")
		self.write(f"(EQ_{self.symbol_counter})")
		self.write("D=-1") # true
		self.write(f"(END_{self.symbol_counter})")
		self.write("@SP")
		self.write("A=M")
		self.write("M=D")
		self.write("@SP")
		self.write("M=M+1")

		self.symbol_counter += 1

	def _write_gt(self):
		self.write("// gt")
		self.write("@SP")
		self.write("M=M-1")
		self.write("A=M")
		self.write("D=M")
		self.write("@SP")
		self.write("M=M-1")
		self.write("A=M")
		self.write("D=M-D")
		self.write(f"@GT_{self.symbol_counter}")
		self.write("D;JGT")
		self.write("D=0")
		self.write(f"@END_{self.symbol_counter}")
		self.write("0;JMP")
		self.write(f"(GT_{self.symbol_counter})")
		self.write("D=-1")
		self.write(f"(END_{self.symbol_counter})")
		self.write("@SP")
		self.write("A=M")
		self.write("M=D")
		self.write("@SP")
		self.write("M=M+1")

		self.symbol_counter += 1

	def _write_lt(self): 
		self.write("// lt")
		self.write("@SP")
		self.write("M=M-1")
		self.write("A=M")
		self.write("D=M")
		self.write("@SP")
		self.write("M=M-1")
		self.write("A=M")
		self.write("D=M-D")
		self.write(f"@LT_{self.symbol_counter}")
		self.write("D;JLT")
		self.write("D=0")
		self.write(f"@END_{self.symbol_counter}")
		self.write("0;JMP")
		self.write(f"(LT_{self.symbol_counter})")
		self.write("D=-1")
		self.write(f"(END_{self.symbol_counter})")
		self.write("@SP")
		self.write("A=M")
		self.write("M=D")
		self.write("@SP")
		self.write("M=M+1")

		self.symbol_counter += 1

	def _write_and(self): 
		self.write("// and")
		self.write("@SP")
		self.write("M=M-1")
		self.write("A=M")
		self.write("D=M")
		self.write("@SP")
		self.write("M=M-1")
		self.write("A=M")
		self.write("M=D&M")
		self.write("@SP")
		self.write("M=M+1")

	def _write_or(self): 
		self.write("// or")
		self.write("@SP")
		self.write("M=M-1")
		self.write("A=M")
		self.write("D=M")
		self.write("@SP")
		self.write("M=M-1")
		self.write("A=M")
		self.write("M=D|M")
		self.write("@SP")
		self.write("M=M+1")

	def _write_not(self): 
		self.write("// not")
		self.write("@SP")
		self.write("M=M-1")
		self.write("A=M")
		self.write("D=!M")
		self.write("M=D")
		self.write("@SP")
		self.write("M=M+1")

	def write_push_pop(self, command: str, segment: str, index: int):
		if   command == "C_PUSH" and segment == "local": self._write_push_local(index)	
		elif command == "C_PUSH" and segment == "argument": self._write_push_argument(index)	
		elif command == "C_PUSH" and segment == "this": self._write_push_this(index)	
		elif command == "C_PUSH" and segment == "that": self._write_push_that(index)	
		elif command == "C_PUSH" and segment == "constant": self._write_push_constant(index)	
		elif command == "C_PUSH" and segment == "static": self._write_push_static(index) # TODO
		elif command == "C_PUSH" and segment == "temp": self._write_push_temp(index)	
		elif command == "C_PUSH" and segment == "pointer": self._write_push_pointer(index)	
		elif command == "C_POP"  and segment == "local": self._write_pop_local(index)	
		elif command == "C_POP"  and segment == "argument": self._write_pop_argument(index)	
		elif command == "C_POP"  and segment == "this": self._write_pop_this(index)	
		elif command == "C_POP"  and segment == "that": self._write_pop_that(index)	
		elif command == "C_POP"  and segment == "constant": self._write_pop_constant(index)	
		elif command == "C_POP"  and segment == "static": self._write_pop_static(index) # TODO
		elif command == "C_POP"  and segment == "temp": self._write_pop_temp(index)	
		elif command == "C_POP"  and segment == "pointer": self._write_pop_pointer(index)	
		else: 
			if command not in ["C_PUSH", "C_POP"]:
				raise RuntimeError(f"Invalid VM command: '{command}'")
			else:
				raise RuntimeError(f"Invalid segment: '{segment}'")

	# =====================================
	# TEMPLATES
	# =====================================
	def _write_push_constant(self, index: int):
		# *SP = i; SP++
		self.write(f"// push constant {index}")
		self.write(f"@{index}")
		self.write("D=A")
		self.write("@SP")
		self.write("A=M")
		self.write("M=D") # *SP = i
		self.write("@SP")
		self.write("M=M+1") # SP++

	def _write_push_pointer(self, index: int):
		assert index in [0, 1], f"Invalid index for pointer: {index}"
		register = "THIS" if index == 0 else "THAT"
		# *SP = THIS/THAT; SP++
		self.write(f"// push pointer {index}")
		self.write(f"@{register}")
		self.write("D=M")
		self.write("@SP")
		self.write("A=M")
		self.write("M=D") # TODO: create a function for *SP = D
		self.write("@SP")
		self.write("M=M+1") # TODO: create a function for SP++

	def _write_push_static(self, index: int):
		self.write(f"// push static {index}")
		self.write(f"@{self.fname}.{index}") # TODO: replace fname with memory addr?
		self.write("D=M")
		self.write("@SP")
		self.write("A=M")
		self.write("M=D") # TODO: create a function for *SP = D
		self.write("@SP")
		self.write("M=M+1") # TODO: create a function for SP++

	def _write_push(self, segment: str, index: int): 
		register = self.get_register_name(segment)

		# addr = segmentPointer + i; *SP = *addr; SP++
		self.write(f"// push {segment} {index}")
		self.write(f"@{index}")
		self.write("D=A")
		self.write(f"@{register}")
		self.write("A=D+A") if segment == "temp" else self.write("A=D+M") # addr = segmentPointer + i
		self.write("D=M")
		self.write("@SP")
		self.write("A=M")
		self.write("M=D") # *SP = *addr
		self.write("@SP")
		self.write("M=M+1") # SP++

	def _write_push_local(self, index: int): return self._write_push(segment="local", index=index)
	def _write_push_argument(self, index: int): return self._write_push(segment="argument", index=index)
	def _write_push_this(self, index: int): return self._write_push(segment="this", index=index)
	def _write_push_that(self, index: int): return self._write_push(segment="that", index=index)
	def _write_push_temp(self, index: int): return self._write_push(segment="temp", index=index)

	def _write_pop_constant(self, index: int): raise NotImplementedError()

	def _write_pop_pointer(self, index: int):
		assert index in [0, 1], f"Invalid index for pointer: {index}"
		register = "THIS" if index == 0 else "THAT"

		# SP--; THIS/THAT = *SP
		self.write(f"// pop pointer {index}")
		self.write("@SP")
		self.write("M=M-1") 
		self.write("A=M")
		self.write("D=M")
		self.write(f"@{register}")
		self.write("M=D")

	# TODO: same skeleton as pointer op?
	def _write_pop_static(self, index: int):
		self.write(f"// pop static {index}")
		self.write("@SP")
		self.write("M=M-1")
		self.write("A=M")
		self.write("D=M")
		self.write(f"@{self.fname}.{index}")
		self.write("M=D")

	def _write_pop(self, segment: str, index: int):
		register = self.get_register_name(segment)
		out = f"// pop {segment} {index}\n"

		# addr = segmentPointer + i; SP--; *addr = *SP
		self.write(f"// pop {segment} {index}")
		self.write(f"@{index}")
		self.write("D=A")
		self.write(f"@{register}")
		self.write("D=D+A") if segment == "temp" else self.write("D=D+M") # addr = segmentPointer + i
		self.write("@frame")
		self.write("M=D")
		self.write("@SP")
		self.write("M=M-1") # SP--
		self.write("A=M")
		self.write("D=M")	
		self.write("@frame")
		self.write("A=M")
		self.write("M=D") # *addr = *SP

	def _write_pop_local(self, index: int): return self._write_pop(segment="local", index=index)
	def _write_pop_argument(self, index: int): return self._write_pop(segment="argument", index=index)
	def _write_pop_this(self, index: int): return self._write_pop(segment="this", index=index)
	def _write_pop_that(self, index: int): return self._write_pop(segment="that", index=index)
	def _write_pop_temp(self, index: int): return self._write_pop(segment="temp", index=index)
