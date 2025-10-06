; SAP-1 Assembly Program: Addition with Loop
; Loads 51 and 25, adds them, stores 76, jumps back to add again, then halts

LDA 13    ; Load value 51 from address 13 into Register A
LDB 14    ; Load value 25 from address 14 into Register B
ADD       ; Add B to A, result in A
STA 15    ; Store result (76) into address 15
JMP 0     ; Jump back to address 0 to repeat
HLT       ; Halt execution (outside loop for demo)

ORG 13    ; Set data starting address to 13
DEC 19    ; Data value 51
DEC 47    ; Data value 25