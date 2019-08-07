#coding:utf-8

#  compute R-type adaptor S-Matrix of Fender Bassman tone stack using symbols
#
#  REFERENCES:
#    WAVE DIGITAL FILTER ADAPTORS FOR ARBITRARY TOPOLOGIES AND MULTIPORT LINEAR ELEMENTS (DAFx-15)  
#    Eq. (6) and Figure-4 
#
#    rt-wdf_renderer/Circuits/wdfTonestackTree.hpp
#
#  Aug-2019
#  GPL v3


from sympy import *
import pickle
import codecs

# Check version  
# python 3.6.4 win32 (64bit)  
# windows 10 (64bit)  
# sympy (1.4)
# mpmath (1.1.0)


init_printing(use_unicode=True)

# Fender Bassman tone stack R-type adaptor is  6 PORTS
RA, RB, RC, RD, RE, RF = symbols('RA, RB, RC, RD, RE, RF')

GA= 1 / RA
GB= 1 / RB
GC= 1 / RC
GD= 1 / RD
GE= 1 / RE
GF= 1 / RF


Y= Matrix( [
[ GA, -GA,   0,   0,   0,   0,   0,   0,   0 ],
[-GA, GA+GB, 0, -GB,   0,   0,   0,   0,   0 ],
[ 0,   0,   GC+GD, 0, -GC,  0, -GD,   0,   0 ],
[ 0, -GB,   0,   GB,   0,   0,   0,   0,   0 ],
[ 0,   0, -GC,   0,   GC,   0,   0,   0,   0 ],
[ 0,   0,   0,   0,    0,  GF,   0,   0, -GF ],
[ 0,   0, -GD,   0,    0,  0,   GD,   0,   0 ],
[ 0,   0,   0,   0,    0,  0,    0,  GE,   0 ],
[ 0,   0,   0,   0,    0, -GF,   0,   0,  GF ],
])

# There are 9 NODES
A= Matrix( [
[  1, 0, 0, 0, 0, 0 ],
[  0, 0, 0, 0, 0,-1 ],
[  0,-1, 0, 0, 0, 0 ],
[  0, 1, 0, 0, 0, 0 ],
[  0, 0, 1, 0, 0, 0 ],
[  0, 0, 0,-1,-1, 0 ],
[  0, 0, 0, 1, 0, 0 ],
[  0, 0, 0, 0, 1, 0 ],
[  0, 0, 0, 0, 0, 1 ],
])
AT= A.T

# R-type adaptor is 6 PORTS
Rp= Matrix( [
[ RA,   0,   0,   0,   0,   0],
[ 0,   RB,   0,   0,   0,   0],
[ 0,    0,  RC,   0,   0,   0],
[ 0,    0,   0,  RD,   0,   0],
[ 0,    0,   0,   0,  RE,   0],
[ 0,    0,   0,   0,   0,  RF]
])

# make [0 Rp]
mz6x9= zeros(6,9)
m0Rp=mz6x9.col_insert(9, Rp)

# make X from Y and A
YA= Y.col_insert(9, A)
ATz= AT.col_insert(9, zeros(6,6))
X2= YA.row_insert(9, ATz)
XINV= X2**-1

# simplify inverse Matrix
XINVS= simplify( XINV)   # This takes long time !


# make [0 I]
mz6x9= zeros(6,9)
m0I=mz6x9.col_insert(9, eye(6))
m0IT= m0I.T

# make I
I6= eye(6)


# compute S matrix
z=m0Rp * XINVS * m0IT
S= I6 + 2 * z

# write S matrix as txt
print(S, file=codecs.open('s_matrix1.txt', 'w', 'utf-8'))

# write S matrix as pickle
with open('s_matrix1.pickle', 'wb') as outf:
    outf.write(pickle.dumps(S))

