import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 24
b = 16
m = 15
o = 15
n = 15
p = 16
u = 15
v = 15
gflops = a*b*m*o*n*p*u*v*2/1e9
A = np.empty((a,u,b,v), order='f', dtype=np.float32)
B = np.empty((p,n,v,o,m,u), order='f', dtype=np.float32)
C = np.empty((b,a,m,n,p,o), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "a,u,b,v", B, "p,n,v,o,m,u", beta, C, "b,a,m,n,p,o" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("aubv,pnvomu->bamnpo", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC