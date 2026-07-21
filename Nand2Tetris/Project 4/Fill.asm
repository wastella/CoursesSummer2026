// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

(START)
    @KBD
    D=M
    @BLACK
    D;JNE     
    @WHITE
    0;JMP     

(BLACK)
    @color
    M=-1      
    @FILL
    0;JMP

(WHITE)
    @color
    M=0       
    @FILL
    0;JMP

(FILL)
    @8192
    D=A
    @n
    M=D      

    @SCREEN
    D=A
    @addr
    M=D 

(FILLLOOP)
    @n
    D=M
    @START
    D;JEQ     

    @color
    D=M
    @addr
    A=M
    M=D       

    @addr
    M=M+1     

    @n
    M=M-1    

    @FILLLOOP
    0;JMP
