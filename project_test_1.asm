; nick's test code - comments preceded with a ';'

; decalring variable locations
count1	EQU	0x22
count2	EQU	0x23

main:	CODE	0x00 ; create main program section

; initialise registers

	MOVLW	0x0A
	MOVWF 	count1
	MOVLW	0x03
	MOVWF	count2

	CLRF	PORTA ; clear PORTA
	CLRF	0x85 ; set PORTA to output via TRISA
	BSF	0x05	0
	GOTO	main_loop

main_loop:	CODE 0x0020

	DECFSZ	count1
	GOTO	main_loop	; skip if above inst. 0
	
	BCF	0x05	0 ; turns on PORTA bit 0
	
	MOVLW	0x0A
	MOVWF	count1	; reset count1

	BSF 	0x05	0 ; turn off PORTA bit 0

	DECFSZ	count2	
	GOTO main_loop

end:	
	GOTO end		; stay in end_loop
