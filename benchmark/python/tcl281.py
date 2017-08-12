import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 8
c = 12
b = 12
m = 40
n = 36
u = 12
w = 12
v = 8
gflops = a*c*b*m*n*u*w*v*2/1e9
A = np.empty((v,u,m,w,n), order='f', dtype=np.float32)
B = np.empty((a,u,w,v,c,b), order='f', dtype=np.float32)
C = np.empty((m,a,b,c,n), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "v,u,m,w,n", B, "a,u,w,v,c,b", beta, C, "m,a,b,c,n" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("vumwn,auwvcb->mabcn", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC