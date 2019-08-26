#coding:utf-8

#  compute S,E,F,M,and N Matrix of Common Cathode Triode Amplifier
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
#  Aug-2019, Shun
#  GPL v3


from sympy import *
import pickle
import codecs


# Check version  
# python 3.6.4 win32 (64bit)  
# windows 10 (64bit)  
# sympy (1.4)
# mpmath (1.1.0)


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

def write_matrx(f, M, name0):
    # name0 is S, E, F, M, N
    f.write('//---- ' + name0 + ' Matrix\n')
    c0='rootMats->' + name0 + 'mat.at'
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            c1= '(%d,%d) = ' % (i, j) 
            c2='{:.14e}'.format( M[i,j])
            f.write( c0+c1+c2+';\n')
    f.write('\n')

# set value
FS=44100
T0= 1 / FS

VINR_= 1
E= 250   # E terminated Vs
RA_= 100000
CI= 1.000000e-07
RI_= 1000000
RG_= 20000
CGK= 1.600000e-12
CGP= 1.700000e-12
CPK= 4.600000e-13
RK_= 1500
CK= 1.000000e-05
CO= 1.000000e-08
RO_= 1000000

# 
RC= T0/(2 * CGP)
RD= T0/(2 * CGK)
RE= T0/(2 * CPK)
RF= ParallelRes((T0/(2 * CI) + VINR_) , RI_) + RG_
RG= ParallelRes( (T0/(2 * CO) + RO_) , RA_)
RH= ParallelRes( T0/(2 * CK), RK_)


# RA and RB is Triode Internal Port Resistances
RA = 1000 # set as same as rt-wdf_renderer/Circuits/wdfCCTAx1Tree.hpp
RB = 1000 # set as same as rt-wdf_renderer/Circuits/wdfCCTAx1Tree.hpp

# symbols
#RA, RB, RC, RD, RE, RF, RG, RH = symbols('RA, RB, RC, RD, RE, RF, RG, RH')

init_printing(use_unicode=True)

GA= 1 / RA
GB= 1 / RB
GC= 1 / RC
GD= 1 / RD
GE= 1 / RE
GF= 1 / RF
GG= 1 / RG
GH= 1 / RH

#
# Regarding to Thevenin port equivalent, see Common_Cathhode_Triode_Amp_Thevenin_port.png
#
# There are 11 NODES
Y= Matrix( [
# 2    3    4          5    6    7    8    9    10    11   12
[ GA, -GA,   0,        0,   0,   0,   0,   0,   0,    0,    0 ],  # 2 V2
[ -GA, GA+GC+GE+GG, 0, 0,   0, -GC,   0,  -GE,   0,  -GG,   0 ],  # 3 V3
[ 0,   0,  GH,         0,   0,   0,   0,   0,   0,    0,  -GH ],  # 4 V4
[ 0,   0,   0,        GB, -GB,   0,   0,   0,   0,    0,    0 ],  # 5 V5
[ 0,   0,   0,   -GB, GB+GD+GF,  0, -GD,   0, -GF,    0,    0 ],  # 6 V6
[ 0,  -GC,  0,         0,   0,   GC,  0,   0,   0,    0,    0 ],  # 7 V7
[ 0,   0,   0,         0, -GD,   0,  GD,   0,   0,    0,    0 ],  # 8 V8
[ 0,  -GE,  0,         0,   0,   0,   0,  GE,   0,    0,    0 ],  # 9 V9
[ 0,   0,   0,         0, -GF,   0,   0,   0,  GF,    0,    0 ],  # 10 V10
[ 0, -GG,   0,         0,   0,   0,   0,   0,   0,   GG,    0 ],  # 11 V11
[ 0,   0, -GH,         0,   0,   0,   0,   0,   0,    0,   GH ]   # 12 V12
])

A= Matrix( [
#  A  B  C  D  E  F  G  H
# JA JB JC JD JE JF JG JH
[  1, 0, 0, 0, 0, 0, 0, 0 ],   # 2
[  0, 0, 0, 0, 0, 0, 0, 0 ],   # 3
[ -1,-1, 0,-1,-1, 0, 0, 0 ],   # 4
[  0, 1, 0, 0, 0, 0, 0, 0 ],   # 5
[  0, 0,-1, 0, 0, 0, 0, 0 ],   # 6 
[  0, 0, 1, 0, 0, 0, 0, 0 ],   # 7
[  0, 0, 0, 1, 0, 0, 0, 0 ],   # 8
[  0, 0, 0, 0, 1, 0, 0, 0 ],   # 9 
[  0, 0, 0, 0, 0, 1, 0, 0 ],   # 10 
[  0, 0, 0, 0, 0, 0, 1, 0 ],   # 11 
[  0, 0, 0, 0, 0, 0, 0, 1 ]    # 12
])

AT= A.T

# R-type adaptor is 8 PORTS
Rp= Matrix( [
[ RA,   0,   0,   0,   0,   0,   0,   0],
[ 0,   RB,   0,   0,   0,   0,   0,   0],
[ 0,    0,  RC,   0,   0,   0,   0,   0],
[ 0,    0,   0,  RD,   0,   0,   0,   0],
[ 0,    0,   0,   0,  RE,   0,   0,   0],
[ 0,    0,   0,   0,   0,  RF,   0,   0],
[ 0,    0,   0,   0,   0,   0,  RG,   0],
[ 0,    0,   0,   0,   0,   0,   0,  RH]
])

# make [0 Rp]
mz8x11= zeros(8,11)
m0Rp=mz8x11.col_insert(11, Rp)

# make X from Y and A
YA= Y.col_insert(11, A)
ATz= AT.col_insert(11, zeros(8,8))
X2= YA.row_insert(11, ATz)
XINV= X2**-1

# make [0 I]
mz8x11= zeros(8,11)
m0I=mz8x11.col_insert(11, eye(8))
m0IT= m0I.T

# make I
I8= eye(8)

# compute S matrix
z=m0Rp * XINV * m0IT
S2_eval= I8 + 2 * z


S11O=get_S11(S2_eval)
S12O=get_S12(S2_eval)
S21O=get_S21(S2_eval)
S22O=get_S22(S2_eval)


# C-matrix : convert A_interal and B_interal into V_c and I_c
RI = Matrix([ [RA,0], [0, RB] ])
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
print(S2_eval, file=codecs.open('s_matrix.txt', 'w', 'utf-8'))
# write S matrix as pickle
with open('s_matrix.pickle', 'wb') as outf:
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

