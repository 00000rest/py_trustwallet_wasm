import cppyy
import pathlib
import hashlib

cppyy.cppdef(f"""#include "{pathlib.Path(__file__).parent.resolve()}/mnemonic.cpp\"""")

def mnemonic_wordlist() -> list:
    with open(f"{pathlib.Path(__file__).parent.resolve()}/mnemonic.txt", "r") as f:
        mnemonic_wordlist = f.read().splitlines()
        return mnemonic_wordlist

def mnemonic_rng(seed: int) -> bytearray:
    return bytearray(list(cppyy.gbl.mnemnonic_rng(seed)))
    

def mnemonic_generate(seed: int) -> str:
    bip39_max_words = 12
    bip39_max_length = 10
    bip39_word_list = mnemonic_wordlist()
    bip39_buf = bytearray(bip39_max_words * (bip39_max_length + 1))

    rng_length = 128 // 8
    rng_data = mnemonic_rng(seed)
    rng_bits = bytearray(32 + 1)
    rng_bits[:rng_length] = rng_data[:rng_length]
    
    rng_sha256 = hashlib.sha256()
    rng_sha256.update(rng_data[:rng_length])
    rng_checksum = rng_sha256.digest()
    rng_bits[rng_length] = rng_checksum[0]
    
    l = rng_length * 3 // 4
    p = 0
    for i in range(l):
        idx = 0
        for j in range(11):
            idx <<= 1
            idx += (rng_bits[(i * 11 + j) // 8] & (1 << (7 - ((i * 11 + j) % 8)))) > 0
        word_bytes = bip39_word_list[idx].encode('utf-8') 
        bip39_buf[p:p+len(word_bytes)] = word_bytes
        p += len(word_bytes)
        bip39_buf[p] = ord(' ') if i < l - 1 else 0
        p += 1

    return bip39_buf.decode().rstrip('\x00')