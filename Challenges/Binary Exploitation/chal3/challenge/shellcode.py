from pwn import * 

context.arch='x86-64'
shellcode='''
    xorps xmm0,xmm0 
    xorps xmm1,xmm1
    xorps xmm2,xmm2
    xorps xmm3,xmm3
    xorps xmm4,xmm4
    vxorps ymm0,ymm0,ymm0
    vxorps ymm1,ymm1,ymm1
    vxorps ymm2,ymm2,ymm2
    vxorps ymm3,ymm3,ymm3
    vxorps ymm4,ymm4,ymm4

'''
'''
    

'''
print(asm(shellcode))
p.interactive()