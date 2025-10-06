; SAP-1 Assembly Program: Simple Addition
; Loads 51 and 25, adds them, stores 76, and halts

LDA 13    ; Load value 51 from address 13 into Register A
LDB 14    ; Load value 25 from address 14 into Register B
ADD       ; Add B to A, result in A
STA 15    ; Store result (76) into address 15
HLT       ; Halt execution

ORG 13    ; Set data starting address to 13
DEC 19    ; Data value 51
DEC 47    ; Data value 25