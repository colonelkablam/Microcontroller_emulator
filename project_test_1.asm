; nick's test code - comment precedes with a ';'

; decalring variable locations
var1	EQU	0x20
var2	EQU	0x21

; create main program section

main:

ADDLW 0xFF
ADDLW 255

; comment

loop_head:

ADDLW 0x01
GOTO loop_head
