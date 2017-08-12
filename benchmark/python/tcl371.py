import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 8
b = 12
m = 12
o = 12
n = 12
p = 16
u = 16
v = 12
gflops = a*b*m*o*n*p*u*v*2/1e9
A = np.empty((u,b,v,a), order='f', dtype=np.float32)
B = np.empty((p,u,n,v,o,m), order='f', dtype=np.float32)
C = np.empty((a,p,m,n,b,o), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "u,b,v,a", B, "p,u,n,v,o,m", beta, C, "a,p,m,n,b,o" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("ubva,punvom->apmnbo", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC