; text preceded with a ';' is ignored - useful for comments and clarification
; whitespace is ignored, other than separating words but useful for clarity
; text can be in either upper or lower case.

loop:	; a word at beginning of the line is treated as a label (semicolon needed after)
		; and can be used in the code to simplify commands (whithout the ':')

; directives

subroutine_1:	PSECT	0x001A	; a label follwed by 'PSECT' followed by a valid program address will 
								; force the label to be located at that address

variable	EQU		0x20	; a word (not beginning with a number and without ':') followed by 'EQU'
							; will treat the word as the following register address within the code
							; essentially creating a variable

; example

var1	EQU		0x20		; locate var1 variable at register address 0x20
var2	EQU		0x21

main:	PSECT	0x0000		; place main at the beginning of program

	MOVLW	0x0A	
	MOVWF	var1	1		; will move w to var1 register (could have typled '0x20)
	MOVLW	0x01
	MOVWF	var2

loop:						; label a program address
	ADDWF	var1
	GOTO	loop			; will jump back to 'loop' label 

; this will continue
