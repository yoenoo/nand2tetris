// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen
// by writing 'black' in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen by writing
// 'white' in every pixel;
// the screen should remain fully clear as long as no key is pressed.

@pointer
M=0

(LOOP)
	@KBD
	D=M
	@WHITE
	D;JEQ // if key not pressed, goto WHITE
	@BLACK
	0;JMP // otherwise (i.e. key pressed), goto BLACK

(WHITE)
	@pointer
	D=M	
	@LOOP
	D;JLT // jump to LOOP if we are less than 0

	@pointer
	D=M
	@SCREEN
	A=A+D
	M=0

	@pointer
	M=M-1
	@LOOP
	0;JMP
	
(BLACK)
	@pointer
	D=M
	@8192
	D=D-A
	@LOOP
	D;JGE // if p > 8192, goto LOOP

	@pointer
	D=M
	@SCREEN
	A=A+D
	M=-1

	@pointer
	M=M+1 // increase pointer by 1
	@LOOP
	0;JMP

(END)
@END
0;JMP
