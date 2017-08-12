import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 64
m = 3240
b = 54
u = 54
v = 64
gflops = a*m*b*u*v*2/1e9
A = np.empty((a,u,v,b), order='f', dtype=np.float32)
B = np.empty((v,u,m), order='f', dtype=np.float32)
C = np.empty((a,m,b), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "a,u,v,b", B, "v,u,m", beta, C, "a,m,b" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("auvb,vum->amb", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC