import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 25
b = 24
m = 25
o = 24
n = 25
u = 600
gflops = a*b*m*o*n*u*2/1e9
A = np.empty((u,o,n,m), order='f', dtype=np.float32)
B = np.empty((b,u,a), order='f', dtype=np.float32)
C = np.empty((o,a,m,b,n), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "u,o,n,m", B, "b,u,a", beta, C, "o,a,m,b,n" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("uonm,bua->oambn", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC