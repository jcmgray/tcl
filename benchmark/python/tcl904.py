import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 5000
m = 72
v = 72
u = 72
n = 72
gflops = a*m*v*u*n*2/1e9
A = np.empty((n,v,u,m), order='f', dtype=np.float32)
B = np.empty((u,v,a), order='f', dtype=np.float32)
C = np.empty((n,m,a), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "n,v,u,m", B, "u,v,a", beta, C, "n,m,a" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("nvum,uva->nma", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC