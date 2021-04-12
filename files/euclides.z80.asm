; Inputs: a, b
; Outputs: a = gcd(a, b)
; Destroys: c
; Assumes: a and b are positive one-byte integers

	ORG 0005h
	ld a 0fh
	ld b 0ah
gcd:
	cp b
	ret z                   ; while a != b

	jr c, else              ; if a > b

	sub b                   ; a = a - b

	jr gcd

else:
	ld c, a                 ; Save a
	ld a, b                 ; Swap b into a so we can do the subtraction
	sub c                   ; b = b - a
	ld b, a                 ; Put a and b back where they belong
	ld a, c

	jr gcd