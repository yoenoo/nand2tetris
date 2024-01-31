from collections import defaultdict

REGISTER = {
	"local": "LCL",
	"argument": "ARG",
	"this": "THIS",
	"that": "THAT",
	"temp": "R5",
}

class CodeWriter:
	def __init__(self):
		self.asm = ""
		self.fname = None
		self.scope = None # defines the function scope
		self.symbol_counter = 0
		self.function_counter = defaultdict(lambda: 0)

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
		self.write("0;JEQ")
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
		self.write("0;JEQ")
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
		assert self.fname is not None, "Please call 'set_filename' to set filename"
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
		self.write(f"// pop {segment} {index}\n")

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

	# ===============================
	# additional files for project 08
	# ===============================
	def set_filename(self, fname: str):
		self.fname = fname

	def write_init(self):
		# SP=256
		self.write("// SP=256")
		self.write("@256")
		self.write("D=A")
		self.write("@SP")
		self.write("M=D")
		# Call Sys.init
		self.write_call("Sys.init", num_args=0)

	def write_label(self, label: str):
		self.write(f"// label {label}")
		self.write(f"({self.fname}.{self.scope}${label})") if self.scope is not None else self.write(f"({label})")

	def write_goto(self, label: str): 
		self.write(f"// goto {label}")
		self.write(f"@{self.fname}.{self.scope}${label}") if self.scope is not None else self.write(f"@{label}")
		self.write("0;JMP") # unconditional jump

	def write_if(self, label: str): 
		self.write(f"// if-goto {label}")
		self.write("@SP")
		self.write("M=M-1")
		self.write("A=M")
		self.write("D=M")
		self.write(f"@{self.fname}.{self.scope}${label}") if self.scope is not None else self.write(f"@{label}")
		self.write("D;JNE")

	def write_function(self, function_name: str, num_vars: int): 
		self.write(f"// function {function_name} {num_vars}")
		# (functionName)				// declares a label for the function entry
		self.write(f"({function_name})")
		# repeat nVars times:		// nVars = number of local variables
		#   push 0							// initializes the local variables to 0
		for _ in range(num_vars):
			self.write("@0")
			self.write("D=A")
			self.write("@SP")
			self.write("A=M")
			self.write("M=D")
			self.write("@SP")
			self.write("M=M+1")

	def write_call(self, function_name: str, num_args: int): 
		self.write(f"// call {function_name} {num_args}")	
		# push returnAddress  // (using the label declared below)
		counter = self.function_counter[function_name]
		self.write("@"+f"{self.fname}.{function_name}$ret.{counter}".strip(".")) # xxx.foo$ret.i 
		self.write("D=A")
		self.write("@SP")
		self.write("A=M")
		self.write("M=D")
		self.write("@SP")
		self.write("M=M+1")
		# push LCL						// saves LCL of the caller
		self.write("@LCL")
		self.write("D=M")
		self.write("@SP")
		self.write("A=M")
		self.write("M=D")
		self.write("@SP")
		self.write("M=M+1")
		# push ARG						// saves ARG of the caller
		self.write("@ARG")
		self.write("D=M")
		self.write("@SP")
		self.write("A=M")
		self.write("M=D")
		self.write("@SP")
		self.write("M=M+1")
		# push THIS						// saves THIS of the caller
		self.write("@THIS")
		self.write("D=M")
		self.write("@SP")
		self.write("A=M")
		self.write("M=D")
		self.write("@SP")
		self.write("M=M+1")
		# push THAT						// saves THAT of the caller
		self.write("@THAT")
		self.write("D=M")
		self.write("@SP")
		self.write("A=M")
		self.write("M=D")
		self.write("@SP")
		self.write("M=M+1")
		# ARG = SP-5-nArgs		// repositions ARG
		self.write("@SP")
		self.write("D=M")
		self.write(f"@{5+num_args}")
		self.write("D=D-A")
		self.write("@ARG")
		self.write("M=D")
		# LCL = SP						// repositions LCL
		self.write("@SP")
		self.write("D=M")
		self.write("@LCL")
		self.write("M=D")
		# goto functionName		// transfers control to the called function
		self.write(f"@{function_name}")
		self.write("0;JMP")
		# (returnAddress)			// declares a label for the return-address
		self.write("("+f"{self.fname}.{function_name}$ret.{counter})".strip("."))

		self.function_counter[function_name] += 1

	def write_return(self): 
		self.write("// return")
		# endFrame = LCL						// endFrame is a temporary variable
		self.write("@LCL")
		self.write("D=M")
		self.write("@endFrame")
		self.write("M=D")
		# retAddr = *(endFrame - 5) // gets the return address
		self.write("@5")
		self.write("D=D-A")
		self.write("A=D")
		self.write("D=M")
		self.write("@retAddr")
		self.write("M=D")
		# *ARG = pop()							// repositions the return value for the caller
		self.write("@SP")
		self.write("M=M-1")
		self.write("A=M")
		self.write("D=M")
		self.write("@ARG")
		self.write("A=M")
		self.write("M=D")
		# SP = ARG + 1							// repositions SP of the caller
		self.write("@ARG")
		self.write("D=M+1")
		self.write("@SP")
		self.write("M=D")
		# THAT = *(endFrame - 1)		// restores THAT of the caller
		self.write("@endFrame")
		self.write("D=M-1")
		self.write("A=D")
		self.write("D=M")
		self.write("@THAT")
		self.write("M=D")
		# THIS = *(endFrame - 2)		// restores THIS of the caller
		self.write("@endFrame")
		self.write("D=M")
		self.write("@2")
		self.write("D=D-A")
		self.write("A=D")
		self.write("D=M")
		self.write("@THIS")
		self.write("M=D")
		# ARG = *(endFrame - 3)			// restores ARG of the caller
		self.write("@endFrame")
		self.write("D=M")
		self.write("@3")
		self.write("D=D-A")
		self.write("A=D")
		self.write("D=M")
		self.write("@ARG")
		self.write("M=D")
		# LCL = *(endFrame - 4)			// restores LCL of the caller
		self.write("@endFrame")
		self.write("D=M")
		self.write("@4")
		self.write("D=D-A")
		self.write("A=D")
		self.write("D=M")
		self.write("@LCL")
		self.write("M=D")
		# goto retAddr							// goes to return address in the caller's code
		self.write("@retAddr")
		self.write("A=M")
		self.write("0;JMP")
