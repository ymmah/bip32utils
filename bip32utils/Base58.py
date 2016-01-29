#!/usr/bin/env python
#
# Copyright 2014 Corgan Labs
# See LICENSE.txt for distribution terms
#

from hashlib import sha256

__base58_alphabet = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__base58_radix = len(__base58_alphabet)


def __string_to_int(data):
    "Convert string of bytes Python integer, MSB"
    val = 0
   
    # Python 2.x compatibility
    if type(data) == str:
        data = bytearray(data)

    for (i, c) in enumerate(data[::-1]):
        val += (256**i)*c
    return val


def encode(data):
    "Encode string into Bitcoin base58"
    enc = bytearray()
    val = __string_to_int(data)
    while val >= __base58_radix:
        val, mod = divmod(val, __base58_radix)
        enc.append(__base58_alphabet[mod]) 
    if val:
        enc.append(__base58_alphabet[val]) 

    # Pad for leading zeroes
    n = len(data)-len(data.lstrip(b'\0'))
    # TODO python2 xrange
    for i in range(n):
        enc.append(__base58_alphabet[0])

    return bytes(enc[::-1])


def check_encode(raw):
    "Encode raw string into Bitcoin base58 with checksum"
    chk = sha256(sha256(raw).digest()).digest()[:4]
    return encode(raw+chk)


def decode(data):
    "Decode Bitcoin base58 format to string"
    val = 0
    for (i, c) in enumerate(data[::-1]):
        val += __base58_alphabet.find(c) * (__base58_radix**i)
    dec = bytearray()
    while val >= 256:
        val, mod = divmod(val, 256)
        dec.append(mod)
    if val:
        dec.append(val)
    return bytes(dec[::-1])


def check_decode(enc):
    "Decode string from Bitcoin base58 and test checksum"
    dec = decode(enc)
    raw, chk = dec[:-4], dec[-4:]
    if chk != sha256(sha256(raw).digest()).digest()[:4]:
        raise ValueError("base58 decoding checksum error")
    else:
        return raw


if __name__ == '__main__':
    assert(__base58_radix == 58)
    data = 'now is the time for all good men to come to the aid of their country'
    enc = check_encode(data)
    assert(check_decode(enc) == data)
