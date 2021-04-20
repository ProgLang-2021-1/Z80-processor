	ORG AA10H
START:
	LD C, 1AH	; Dividend
	LD B, 03H	; Divisor
	CALL S_DIVISION
	HALT

S_DIVISION:
	; if B == 0 ---> DONE
	LD A, B
	NEG ; 0 - A
	JP Z, _ERROR
	JP P, B_NEGATIVE

	LD A, C
	NEG ; 0 - A
	JP P, C_NEGATIVE
	NEG

	CALL U_DIVISION

	RET


B_NEGATIVE:
	; TODO: Set b to -b and call S_DIVISION
	LD A, B
	NEG
	LD B, A ;B = -B
	CALL S_DIVISION

	LD E, A; tmp = R

	LD A, D
	NEG
	LD D, A; Q = -Q

	LD A, E ; R = tmp
	RET

C_NEGATIVE:
	LD A, C
	NEG
	LD C, A ;C = -C
	CALL S_DIVISION

	NEG
	JP Z, C_NEGATIVE_R_Z ; R == 0
	NEG

	LD E, A ; tmp = R

	LD A, D
	NEG
	SUB 01H
	LD D, A; Q = - (Q + 1)

	LD A, B
	SUB E; R = B - tmp (R)

	; TODO: This should return to
	RET

C_NEGATIVE_R_Z:
	LD A, D
	NEG
	LD D, A; Q = -Q

	LD A, 0; R = 0

	RET


U_DIVISION:
	LD A, C		; Remainder
	LD D, 00H	; Quotient
U_WHILE:
	CP B
	RET M ; while A >= B
	SUB B
	INC D
	JR U_WHILE

_ERROR:
	HALT
