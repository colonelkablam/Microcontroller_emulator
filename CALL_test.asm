; testing CALL and RETURN

main:	PSECT	0x0000
	
	ADDLW	0xCC
	MOVWF	0x20

	CALL a

end_loop:
	GOTO	end_loop

; subroutines
a:
	CALL b
	RETURN

b:
	CALL c
	RETURN

c:
	CALL d
	RETURN

d:
	RETURN
