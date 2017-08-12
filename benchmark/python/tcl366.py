import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 432
m = 24
n = 20
u = 20
w = 24
v = 20
gflops = a*m*n*u*w*v*2/1e9
A = np.empty((w,m,v,u,n), order='f', dtype=np.float32)
B = np.empty((w,v,a,u), order='f', dtype=np.float32)
C = np.empty((m,n,a), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "w,m,v,u,n", B, "w,v,a,u", beta, C, "m,n,a" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("wmvun,wvau->mna", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC