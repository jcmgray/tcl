import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 192
u = 192
b = 192
m = 192
gflops = a*u*b*m*2/1e9
A = np.empty((m,u), order='f', dtype=np.float32)
B = np.empty((u,a,b), order='f', dtype=np.float32)
C = np.empty((m,b,a), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "m,u", B, "u,a,b", beta, C, "m,b,a" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("mu,uab->mba", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC