r = r'[A-EHL]'
n = r'[A-F0-9]{2}'
dd = r'(BC)|(DE)|(HL)|(SP)'
cc = r'(NZ)|(Z)|(NC)|(C)|(PO)|(PE)|(P)|(M)'
space = r'(\s*)'
comment = r'(;.*)'
line_ending = rf'({space}?{comment}?\r?\n?)'

TAG = fr'^(\w+):{line_ending}$'

ORG = fr'^{space}?ORG +(?P<n1>{n})(?P<n2>{n})H{line_ending}$'

LD_R_N = fr'^{space}LD +(?P<r>{r}), *(?P<n>{n})H{line_ending}$'
LD_R_R = fr'^{space}LD +(?P<r1>{r}), *(?P<r2>{r}){line_ending}$'
LD_DD_NN = fr'^{space}LD +(?P<dd>{dd}), *(?P<n1>{n})(?P<n2>{n})H{line_ending}$'
LD__NN__A = fr'^{space}LD +\((?P<n1>{n})(?P<n2>{n})H\), *A{line_ending}$'


CPL = fr'^{space}CPL{line_ending}$'
CP_R = fr'^{space}CP +(?P<r>{r}){line_ending}$'

SUB_R = fr'^{space}SUB +(?P<r>{r}){line_ending}$'

ADD_A_R = fr'^{space}ADD +A, *(?P<r>{r}){line_ending}$'
ADD_A__HL_ = fr'^{space}ADD +A, *\(HL\){line_ending}$'

INC = fr'^{space}INC +(?P<r>{r}){line_ending}$'
HALT = fr'^{space}HALT{line_ending}$'

JP_CC_TAG = fr'{space}JP +(?P<cc>{cc}), *(?P<tag>(\w+)){line_ending}$'

JR_C_TAG = fr'^{space}JR +C, *(?P<tag>\w+){line_ending}$'

# FIXME: Ambiguity when cc is used as a tag
JR_TAG = fr'^{space}JR +(?P<tag>(\w+)){line_ending}$'

RET = fr'^{space}RET{line_ending}$'

NEG = fr'^{space}NEG{line_ending}$'

RET_CC = fr'^{space}RET +(?P<cc>{cc}){line_ending}$'

CALL = fr'^{space}CALL +(?P<tag>(\w+)){line_ending}$'
