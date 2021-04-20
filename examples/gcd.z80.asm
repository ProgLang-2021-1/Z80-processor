; Inputs: a, b
; Outputs: a = gcd(a, b)
; Assumes: a and b are positive one-byte integers
    org AFFAh
start: ;05
	ld a, 0Ah
	ld b, 0Fh
    ld e, b                 ; Stores the initial value of b in e
	call gcd ;7
	halt
gcd: ; 0D
	cp b
	ret z                   ; while a != b

	jr c, else              ; if a > b

	sub b                   ; a = a - b

	jr gcd

else: ;14
	ld c, a                 ; Save a
	ld a, b                 ; Swap b into a so we can do the subtraction
	sub c                   ; b = b - a
	ld b, a                 ; Put a and b back where they belong
	ld a, c

	jr gcd
