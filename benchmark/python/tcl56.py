import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 32
u = 32
b = 32
m = 1152
v = 32
gflops = a*u*b*m*v*2/1e9
A = np.empty((m,u,v), order='f', dtype=np.float32)
B = np.empty((a,b,v,u), order='f', dtype=np.float32)
C = np.empty((m,b,a), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "m,u,v", B, "a,b,v,u", beta, C, "m,b,a" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("muv,abvu->mba", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC