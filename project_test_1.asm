; nick's test code - comments preceded with a ';'

; declaring variable locations with 'EQU'
count1	EQU	0x22
count2	EQU	0x23

main:	PSECT	0x00    ;'PSECT' labels a section of code
			; create main program section

; initialise registers

	MOVLW	0x0A
	MOVWF 	count1
	MOVLW	0x03
	MOVWF	count2

	CLRF	PORTA ; clear PORTA
	CLRF	0x85 ; set PORTA to output via TRISA
	BSF	0x05	0
	GOTO	main_loop

main_loop:	PSECT 0x0020

	DECFSZ	count1
	GOTO	main_loop	; skip if above inst. 0
	
	BCF	0x05	0 ; turns on PORTA bit 0
	
	MOVLW	0x0A
	MOVWF	count1	; reset count1

	BSF 	0x05	0 ; turn off PORTA bit 0

	DECFSZ	count2	
	GOTO main_loop

end:	
	NOP
	GOTO end		; stay in end_loop
