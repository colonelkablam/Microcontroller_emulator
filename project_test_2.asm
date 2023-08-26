main:

ADDLW	0xA0
MOVWF	0x20
CALL	subroutine

CLRW

GOTO	main


subroutine:
loop:
DECFSZ	0x20	1
GOTO	loop
RETURN
