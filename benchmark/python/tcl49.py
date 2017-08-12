import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 30
m = 32
c = 32
b = 32
u = 32
gflops = a*m*c*b*u*2/1e9
A = np.empty((b,a,c,u), order='f', dtype=np.float32)
B = np.empty((u,m), order='f', dtype=np.float32)
C = np.empty((b,c,a,m), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "b,a,c,u", B, "u,m", beta, C, "b,c,a,m" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("bacu,um->bcam", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC