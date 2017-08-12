import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 10
c = 10
b = 10
m = 32
n = 30
u = 8
w = 10
v = 8
gflops = a*c*b*m*n*u*w*v*2/1e9
A = np.empty((v,m,w,u,n), order='f', dtype=np.float32)
B = np.empty((u,v,a,w,c,b), order='f', dtype=np.float32)
C = np.empty((m,b,n,c,a), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "v,m,w,u,n", B, "u,v,a,w,c,b", beta, C, "m,b,n,c,a" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("vmwun,uvawcb->mbnca", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC