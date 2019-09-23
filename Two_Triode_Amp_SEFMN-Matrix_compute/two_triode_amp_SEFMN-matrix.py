#coding:utf-8

#  compute S,E,F,M,and N Matrix of Two Triode Amplifier
#
#  REFERENCES:
#    WAVE DIGITAL FILTER ADAPTORS FOR ARBITRARY TOPOLOGIES AND MULTIPORT LINEAR ELEMENTS (DAFx-15)  
#    Eq. (6)
#
#    RT-WDF-A MODULAR DIGITAL FILTER LIBRARY WITH SUPPORT FOR ARBITRARY TOPOLOGIES AND MULTIPLATE NONLINEARITIES (DAFx-16)
#    Figure 4 Common Cathode Triode Amplifier
#
#    RESOLVING GROUPED NONLINEARITIES IN WAVE DIGITAL FILTERS USING ITERATIVE TECHNIQUES (DAFx-16)
#    Eq. (1), (3), and (4)
#
#    rt-wdf_renderer/Circuits/wdfCCTAx1Tree.hpp
#
#  Sept-2019, Shun
#  GPL v3


from sympy import *
import pickle
import codecs
import numpy as np

# Check version  
# python 3.6.4 win32 (64bit)  
# windows 10 (64bit)  
# sympy (1.4)
# mpmath (1.1.0)
# numpy (1.16.3)

def ParallelRes(R1, R2 ):
    return ( R1 * R2 ) / ( R1 + R2 )

def get_S11(S, internal_ports_number=2):
    Sx=S.copy()
    for i in range (S.shape[0] - internal_ports_number):
        Sx.col_del(-1)
        Sx.row_del(-1)
    return Sx

def get_S22(S, internal_ports_number=2):
    Sx=S.copy()
    for i in range (internal_ports_number):
        Sx.col_del(0)
        Sx.row_del(0)
    return Sx

def get_S12(S, internal_ports_number=2):
    Sx=S.copy()
    for i in range (internal_ports_number):
        Sx.col_del(0)
    for i in range (S.shape[0] - internal_ports_number):
        Sx.row_del(-1)
    return Sx

def get_S21(S, internal_ports_number=2):
    Sx=S.copy()
    for i in range (internal_ports_number):
        Sx.row_del(0)
    for i in range (S.shape[0] - internal_ports_number):
        Sx.col_del(-1)
    return Sx

def get_max(diff):
    ndiff= matrix2numpy(diff)
    return np.amax(np.abs(ndiff))
    
def get_min(diff):
    ndiff= matrix2numpy(diff)
    return np.amin(np.abs(ndiff))

def write_matrx(f, M, name0):
    # name0 is S, E, F, M, N
    f.write('//---- ' + name0 + ' Matrix\n')
    c0='rootMats->' + name0 + 'mat.at'
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            c1= '(%d,%d) = ' % (i, j) 
            if M[i , j] == 0. :
                c2= '0.0'
            elif M[i , j] == 1.0 :
                c2= '1.0'
            else:
                M0= M[i,j] * 1.0
                c2='{:.14e}'.format( M0 )  # M[i,j])
            f.write( c0+c1+c2+';\n')
    f.write('\n')


# set value
FS= 44100 #176400
T0= 1 / FS

# Triode circuit 1
VIN1R = 1
E1=  200   # E terminated Vs
E1R= 100000
CI1= 2.000000e-08
RI1= 470000
CGK1= 1.600000e-12
CGP1= 1.700000e-12
CPK1= 4.600000e-13
RK1= 2000
CK1= 1.000000e-04

# RA and RB is Triode Internal Port Resistances
RA = 1000 # set as same as rt-wdf_renderer/Circuits/wdfCCTAx1Tree.hpp
RB = 1000 # set as same as rt-wdf_renderer/Circuits/wdfCCTAx1Tree.hpp
RC= T0/(2 * CGP1)
RD= T0/(2 * CGK1)
RE= T0/(2 * CPK1)
RF= ParallelRes((T0/(2 * CI1) + VIN1R) , RI1)
RG= E1R
RH= ParallelRes( (T0/(2 * CK1)), RK1)


# Triode circuit 2
E2= 200   # E terminated Vs
E2R= 1 
RI2= 470000
CGK2= 5.500000e-12
CGP2= 5.00000e-13
CPK2= 6.00000e-12
RK2 = 470
CK2 = 1.000000e-04

# Output transformaer equivalent
RPT1= 146.8
RST1= 184.35
RIT1= 291000
CPT1= 393.3e-12
CST1= 10.168e-12
LLT1= 9.965e-3
LPT1= 12.12
RLT1= 2234

# RI and RJ is Triode Internal Port Resistances
RI = 1000 # set as same as rt-wdf_renderer/Circuits/wdfCCTAx1Tree.hpp
RJ = 1000 # set as same as rt-wdf_renderer/Circuits/wdfCCTAx1Tree.hpp
RK= T0/(2 * CGP2)
RL= T0/(2 * CGK2)
RM= T0/(2 * CPK2)
RN= RI2

subtree10a= ParallelRes( RLT1, (T0/(2 * CST1)))
subtree10b= RST1 + subtree10a
subtree10c= ParallelRes( RIT1, ( 2 * LPT1 / T0) )
subtree10d= ParallelRes( subtree10c, subtree10b)
subtree10e= RPT1 + ( 2 * LLT1 / T0)
subtree10f= subtree10e + subtree10d
subtree10g= ParallelRes( T0/(2 * CPT1), subtree10f)
RO= subtree10g + E2R

RP= ParallelRes( (T0/(2 * CK2)), RK2)

# Connection between triode circuit 1 and triode circuit 2
CI2= 2.000000e-08

RQ= T0/(2 * CI2)


# symbols
#RA, RB, RC, RD, RE, RF, RG, RH, RI, RJ, RK, RL, RM, RN, RO, RP, RQ = symbols('RA, RB, RC, RD, RE, RF, RG, RH, RI, RJ, RK, RL, RM, RN, RO, RP, RQ')
#
init_printing(use_unicode=True)

# Triode circuit 1
GA= 1 / RA
GB= 1 / RB
GC= 1 / RC
GD= 1 / RD
GE= 1 / RE
GF= 1 / RF
GG= 1 / RG
GH= 1 / RH

# Triode circuit 2
GI= 1 / RI  # RA
GJ= 1 / RJ  # RB
GK= 1 / RK  # RC
GL= 1 / RL  # RD
GM= 1 / RM  # RE
GN= 1 / RN  # RF
GO= 1 / RO  # RG
GP= 1 / RP  # RH

# Connection between triode circuit1 and triode circuit 2
GQ = 1 / RQ


# Regarding to Thevenin port equivalent, see Two_Triode_Amp_Thevenin_port.png
# There are 23=(11+11+1) NODES
Y= Matrix( [
# Triode circuit 1                                                 Triode circuit 2                                                   Connection
# 2    3    4          5    6    7    8    9    10    11   12      13    14   15       16   17   18   19   20   21    22    23        24
[ GA, -GA, 0,          0,   0,   0,   0,   0,   0,    0,    0,     0,    0,   0,        0,   0,   0,   0,   0,   0,    0,    0,        0  ],  # 2 V2
[ -GA, GA+GC+GE+GG+GQ, 0, 0,0, -GC,   0,  -GE,   0,  -GG,   0,     0,    0,   0,        0,   0,   0,   0,   0,   0,    0,    0,      -GQ  ],  # 3 V3
[ 0,   0,  GH,         0,   0,   0,   0,   0,   0,    0,  -GH,     0,    0,   0,        0,   0,   0,   0,   0,   0,    0,    0,        0  ],  # 4 V4
[ 0,   0,   0,        GB, -GB,   0,   0,   0,   0,    0,    0,     0,    0,   0,        0,   0,   0,   0,   0,   0,    0,    0,        0  ],  # 5 V5
[ 0,   0,   0,   -GB, GB+GD+GF,  0, -GD,   0, -GF,    0,    0,     0,    0,   0,        0,   0,   0,   0,   0,   0,    0,    0,        0  ],  # 6 V6
[ 0,  -GC,  0,         0,   0,   GC,  0,   0,   0,    0,    0,     0,    0,   0,        0,   0,   0,   0,   0,   0,    0,    0,        0  ],  # 7 V7
[ 0,   0,   0,         0, -GD,   0,  GD,   0,   0,    0,    0,     0,    0,   0,        0,   0,   0,   0,   0,   0,    0,    0,        0  ],  # 8 V8
[ 0,  -GE,  0,         0,   0,   0,   0,  GE,   0,    0,    0,     0,    0,   0,        0,   0,   0,   0,   0,   0,    0,    0,        0  ],  # 9 V9
[ 0,   0,   0,         0, -GF,   0,   0,   0,  GF,    0,    0,     0,    0,   0,        0,   0,   0,   0,   0,   0,    0,    0,        0  ],  # 10 V10
[ 0, -GG,   0,         0,   0,   0,   0,   0,   0,   GG,    0,     0,    0,   0,        0,   0,   0,   0,   0,   0,    0,    0,        0  ],  # 11 V11
[ 0,   0, -GH,         0,   0,   0,   0,   0,   0,    0,   GH,     0,    0,   0,        0,   0,   0,   0,   0,   0,    0,    0,        0  ],  # 12 V12

[ 0,   0,   0,         0,   0,   0,   0,   0,   0,    0,    0,     GI, -GI,   0,        0,   0,   0,   0,   0,   0,    0,    0,        0  ],  # 13 V13
[ 0,   0,   0,         0,   0,   0,   0,   0,   0,    0,    0,     -GI, GI+GK+GM+GO, 0, 0,   0, -GK,   0, -GM,   0,  -GO,    0,        0  ],  # 14 V14
[ 0,   0,   0,         0,   0,   0,   0,   0,   0,    0,    0,     0,   0,  GP,         0,   0,   0,   0,   0,   0,    0,  -GP,        0  ],  # 15 V15
[ 0,   0,   0,         0,   0,   0,   0,   0,   0,    0,    0,     0,   0,   0,        GJ, -GJ,   0,   0,   0,   0,    0,    0,        0  ],  # 16 V16
[ 0,   0,   0,         0,   0,   0,   0,   0,   0,    0,    0,     0,   0,   0,   -GJ, GJ+GL+GN,  0, -GL,   0, -GN,    0,    0,        0  ],  # 17 V17
[ 0,   0,   0,         0,   0,   0,   0,   0,   0,    0,    0,     0,  -GK,  0,         0,   0,   GK,  0,   0,   0,    0,    0,        0  ],  # 18 V18
[ 0,   0,   0,         0,   0,   0,   0,   0,   0,    0,    0,     0,   0,   0,         0, -GL,   0,  GL,   0,   0,    0,    0,        0  ],  # 19 V19
[ 0,   0,   0,         0,   0,   0,   0,   0,   0,    0,    0,     0,  -GM,  0,         0,   0,   0,   0,  GM,   0,    0,    0,        0  ],  # 20 V20
[ 0,   0,   0,         0,   0,   0,   0,   0,   0,    0,    0,     0,   0,   0,         0, -GN,   0,   0,   0,  GN,    0,    0,        0  ],  # 21 V21
[ 0,   0,   0,         0,   0,   0,   0,   0,   0,    0,    0,     0, -GO,   0,         0,   0,   0,   0,   0,   0,   GO,    0,        0  ],  # 22 V22
[ 0,   0,   0,         0,   0,   0,   0,   0,   0,    0,    0,     0,   0, -GP,         0,   0,   0,   0,   0,   0,    0,   GP,        0  ],  # 23 V23

[ 0, -GQ,   0,         0,   0,   0,   0,   0,   0,    0,    0,     0,   0,   0,         0,   0,   0,   0,   0,   0,    0,    0,       GQ   ]   # 24 V24

])

NUM_NODES=Y.shape[0]
print ( 'NUM_NODES', NUM_NODES)

"""
A= Matrix( [
#  Triode circuit 1          Triode circuit 2            Connection between triode circuit 1 and triode circuit 2
#  A  B  C  D  E  F  G  H    I  J  K  L  M  N  O  P      Q 
# JA JB JC JD JE JF JG JH   JI JJ JK JL JM JN JO JP     JQ
[  1, 0, 0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0,     0 ],   # 2
[  0, 0, 0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0,     0 ] ,  # 3
[ -1,-1, 0,-1,-1, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0,     0 ],   # 4
[  0, 1, 0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0,     0 ],   # 5
[  0, 0,-1, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0,     0 ],   # 6 
[  0, 0, 1, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0,     0 ],   # 7
[  0, 0, 0, 1, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0,     0 ],   # 8
[  0, 0, 0, 0, 1, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0,     0 ],   # 9 
[  0, 0, 0, 0, 0, 1, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0,     0 ],   # 10 
[  0, 0, 0, 0, 0, 0, 1, 0,   0, 0, 0, 0, 0, 0, 0, 0,     0 ],   # 11 
[  0, 0, 0, 0, 0, 0, 0, 1,   0, 0, 0, 0, 0, 0, 0, 0,     0 ],   # 12

[  0, 0, 0, 0, 0, 0, 0, 0,   1, 0, 0, 0, 0, 0, 0, 0,     0 ],   # 13
[  0, 0, 0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0,     0 ],   # 14
[  0, 0, 0, 0, 0, 0, 0, 0,  -1,-1, 0,-1,-1, 0, 0, 0,     0 ],   # 15
[  0, 0, 0, 0, 0, 0, 0, 0,   0, 1, 0, 0, 0, 0, 0, 0,     0 ],   # 16
[  0, 0, 0, 0, 0, 0, 0, 0,   0, 0,-1, 0, 0, 0, 0, 0,    -1 ],   # 17
[  0, 0, 0, 0, 0, 0, 0, 0,   0, 0, 1, 0, 0, 0, 0, 0,     0 ],   # 18
[  0, 0, 0, 0, 0, 0, 0, 0,   0, 0, 0, 1, 0, 0, 0, 0,     0 ],   # 19
[  0, 0, 0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 1, 0, 0, 0,     0 ],   # 20
[  0, 0, 0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 1, 0, 0,     0 ],   # 21 
[  0, 0, 0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0, 1, 0,     0 ],   # 22 
[  0, 0, 0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0, 1,     0 ],   # 23

[  0, 0, 0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0,     1 ]    # 24

])
"""

A= Matrix( [
#  A  B   I   J     C  D  E  F  G  H   K  L  M  N  O  P      Q 
# JA JB  JI  JJ    JC JD JE JF JG JH   JK JL JM JN JO JP     JQ
[  1, 0,  0,  0,   0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0,     0 ],   # 2
[  0, 0,  0,  0,   0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0,     0 ] ,  # 3
[ -1,-1,  0,  0,   0,-1,-1, 0, 0, 0,   0, 0, 0, 0, 0, 0,     0 ],   # 4
[  0, 1,  0,  0,   0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0,     0 ],   # 5
[  0, 0,  0,  0,  -1, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0,     0 ],   # 6 
[  0, 0,  0,  0,   1, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0,     0 ],   # 7
[  0, 0,  0,  0,   0, 1, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0,     0 ],   # 8
[  0, 0,  0,  0,   0, 0, 1, 0, 0, 0,   0, 0, 0, 0, 0, 0,     0 ],   # 9 
[  0, 0,  0,  0,   0, 0, 0, 1, 0, 0,   0, 0, 0, 0, 0, 0,     0 ],   # 10 
[  0, 0,  0,  0,   0, 0, 0, 0, 1, 0,   0, 0, 0, 0, 0, 0,     0 ],   # 11 
[  0, 0,  0,  0,   0, 0, 0, 0, 0, 1,   0, 0, 0, 0, 0, 0,     0 ],   # 12

[  0, 0,  1,  0,   0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0,     0 ],   # 13
[  0, 0,  0,  0,   0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0,     0 ],   # 14
[  0, 0, -1, -1,   0, 0, 0, 0, 0, 0,   0,-1,-1, 0, 0, 0,     0 ],   # 15
[  0, 0,  0,  1,   0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0,     0 ],   # 16
[  0, 0,  0,  0,   0, 0, 0, 0, 0, 0,  -1, 0, 0, 0, 0, 0,    -1 ],   # 17
[  0, 0,  0,  0,   0, 0, 0, 0, 0, 0,   1, 0, 0, 0, 0, 0,     0 ],   # 18
[  0, 0,  0,  0,   0, 0, 0, 0, 0, 0,   0, 1, 0, 0, 0, 0,     0 ],   # 19
[  0, 0,  0,  0,   0, 0, 0, 0, 0, 0,   0, 0, 1, 0, 0, 0,     0 ],   # 20
[  0, 0,  0,  0,   0, 0, 0, 0, 0, 0,   0, 0, 0, 1, 0, 0,     0 ],   # 21 
[  0, 0,  0,  0,   0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 1, 0,     0 ],   # 22 
[  0, 0,  0,  0,   0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 1,     0 ],   # 23

[  0, 0,  0,  0,   0, 0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0,     1 ]    # 24

])

AT= A.T

# R-type adaptor is 17=(8+8+1) PORTS
"""
Rp= Matrix( [
# trode portion
[ RA,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,   RB,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,  RC,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,  RD,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,  RE,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,  RF,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,   0,  RG,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,   0,   0,  RH,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,   0,   0,   0,  RI,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,   0,   0,   0,   0,  RJ,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,   0,   0,   0,   0,   0,  RK,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RL,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RM,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RN,   0,   0,   0],
[ 0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RO,   0,   0],
[ 0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RP,   0],
[ 0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RQ]
])
"""

Rp= Matrix( [
# trode portion
[ RA,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,   RB,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,  RI,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,  RJ,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
# other portion
[ 0,    0,   0,   0,  RC,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,  RD,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,   0,  RE,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,   0,   0,  RF,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,   0,   0,   0,  RG,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,   0,   0,   0,   0,  RH,   0,   0,   0,   0,   0,   0,   0],
#  skip...
[ 0,    0,   0,   0,   0,   0,   0,   0,   0,   0,  RK,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RL,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RM,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RN,   0,   0,   0],
[ 0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RO,   0,   0],
[ 0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RP,   0],
[ 0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RQ]
])


NUM_PORTS= Rp.shape[0]
print ('NUM_PORTS', NUM_PORTS)

# make [0 Rp]
mz8x11= zeros(NUM_PORTS,NUM_NODES)
m0Rp=mz8x11.col_insert(NUM_NODES, Rp)

# make X from Y and A
YA= Y.col_insert(NUM_NODES, A)
ATz= AT.col_insert(NUM_NODES, zeros(NUM_PORTS,NUM_PORTS))
X2= YA.row_insert(NUM_NODES, ATz)

XINV= X2**-1

# make [0 I]
mz8x11= zeros(NUM_PORTS,NUM_NODES)
m0I=mz8x11.col_insert(NUM_NODES, eye(NUM_PORTS))
m0IT= m0I.T

# make I
I8= eye(NUM_PORTS)

# compute S matrix
z=m0Rp * XINV * m0IT
S2_eval= I8 + 2 * z


# two triode internal port number is 4(=2port x 2)
NUM_internal_ports=4
S11O=get_S11(S2_eval, internal_ports_number=NUM_internal_ports)
S12O=get_S12(S2_eval, internal_ports_number=NUM_internal_ports)
S21O=get_S21(S2_eval, internal_ports_number=NUM_internal_ports)
S22O=get_S22(S2_eval, internal_ports_number=NUM_internal_ports)


# C-matrix : convert A_interal and B_interal into V_c and I_c
RI = Matrix([
[RA, 0, 0, 0], 
[0, RB, 0, 0],
[0, 0, RI, 0],
[0, 0, 0, RJ] 
])
C11 = -1 * RI
C21 = -2 * RI
C12 = eye( RI.shape[0] )
C22 = eye( RI.shape[0] )

C11C12= C11.col_insert( RI.shape[0], C12)
C21C22= C21.col_insert( RI.shape[0], C22)
C= C11C12.row_insert( RI.shape[0], C21C22)

# H matrix
z= C22 * S11O
Iz= eye( z.shape[0])
z2= Iz - z
H= z2**-1

# N matrix
N= S21O * H * C21

# M matrix
M= S21O * H * C22 * S12O + S22O

# F matrix
F= C12 * S11O * H * C21 + C11

# E matrix
z3= S11O * H * C22
z4= eye(z3.shape[0]) + z3
E= C12 * z4 * S12O 


# write S matrix as txt
print(S2_eval, file=codecs.open('s_matrix2.txt', 'w', 'utf-8'))
# write S matrix as pickle
with open('s_matrix2.pickle', 'wb') as outf:
    outf.write(pickle.dumps(S2_eval))

# write N matrix as txt
print(N, file=codecs.open('N_matrix.txt', 'w', 'utf-8'))
# write N matrix as pickle
with open('N_matrix.pickle', 'wb') as outf:
    outf.write(pickle.dumps(N))

# write M matrix as txt
print(M, file=codecs.open('M_matrix.txt', 'w', 'utf-8'))
# write M matrix as pickle
with open('M_matrix.pickle', 'wb') as outf:
    outf.write(pickle.dumps(M))

# write F matrix as txt
print(F, file=codecs.open('F_matrix.txt', 'w', 'utf-8'))
# write F matrix as pickle
with open('F_matrix.pickle', 'wb') as outf:
    outf.write(pickle.dumps(F))

# write E matrix as txt
print(E, file=codecs.open('E_matrix.txt', 'w', 'utf-8'))
# write E matrix as pickle
with open('E_matrix.pickle', 'wb') as outf:
    outf.write(pickle.dumps(E))
    


# write S,E,F,M,N matrix as c form
with open('matrix_c_form.txt','wt') as outf:
    write_matrx(outf, S2_eval, 'S')
    write_matrx(outf, E, 'E')
    write_matrx(outf, F, 'F')
    write_matrx(outf, M, 'M')
    write_matrx(outf, N, 'N')


