import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 16
c = 12
b = 16
m = 12
o = 12
n = 12
u = 45
v = 40
gflops = a*c*b*m*o*n*u*v*2/1e9
A = np.empty((a,v,b,u,c), order='f', dtype=np.float32)
B = np.empty((v,m,u,o,n), order='f', dtype=np.float32)
C = np.empty((b,c,n,a,o,m), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "a,v,b,u,c", B, "v,m,u,o,n", beta, C, "b,c,n,a,o,m" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("avbuc,vmuon->bcnaom", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC