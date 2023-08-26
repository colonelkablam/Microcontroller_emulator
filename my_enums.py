from enum import Enum
# locally used enums for pin direction/values
class PinDir(Enum):
    INPUT = 1
    OUTPUT = 0

class PinVal(Enum):
    ON = 1
    OFF = 0

class Side(Enum):
    LEFT = 0
    RIGHT = 1

class Instruction(Enum):
    ADDWF   = 0
    ANDWF   = 1
    CLRF    = 2
    CLRW    = 3
    COMF    = 4
    DECF    = 5
    DECFSZ  = 6
    INCF    = 7
    INCFSZ  = 8
    IORWF   = 9
    MOVF    = 10
    MOVWF   = 11
    NOP     = 12
    RLF     = 13
    RRF     = 14
    SUBWF   = 15
    SWAPF   = 16
    XORWF   = 17
    #BIT ORIENTATED
    BCF     = 18
    BSF     = 19
    BTFSC   = 20
    BTFSS   = 21
    # LITERAL AND CONTROL
    ADDLW   = 22
    ANDLW   = 23
    CALL    = 24
    CLRWDT  = 25
    GOTO    = 26
    IORLW   = 27
    MOVLW   = 28
    RETFIE  = 29
    RETLW   = 30
    RETURN  = 31
    SLEEP   = 32
    SUBLW   = 33
    XORLW   = 34

