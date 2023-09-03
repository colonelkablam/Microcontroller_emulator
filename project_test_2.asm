; testing CALL and RETURN

main:	PSECT	0x0000	; main location at 0x0000
	
	CLRF	TRISB
	CLRF	PORTB
	CLRF	PORTA

	ADDLW	0x0B
	MOVWF	PORTB

loop:
	BTFSS	0x05	0	; test pin 0, port A
	GOTO	loop

	DECF	PORTB
	MOVF	PORTB	1	; test PORTB reached 0 
	BTFSS	STATUS	2	; STATUS Z will be 1
	GOTO	loop

	CALL a			; go into stack test

	CLRF	0x21

end_loop:
	INCF	0x21	1

	GOTO	end_loop		; stay in end loop when done


; subroutines
a:
	CALL b
	RETURN

b:
	CALL c
	RETURN

c:
	RETURN
