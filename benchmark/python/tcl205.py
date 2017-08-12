import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 8
c = 12
b = 12
m = 8
o = 12
n = 12
u = 1500
gflops = a*c*b*m*o*n*u*2/1e9
A = np.empty((m,n,o,u), order='f', dtype=np.float32)
B = np.empty((a,b,c,u), order='f', dtype=np.float32)
C = np.empty((m,c,n,b,o,a), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "m,n,o,u", B, "a,b,c,u", beta, C, "m,c,n,b,o,a" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("mnou,abcu->mcnboa", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC