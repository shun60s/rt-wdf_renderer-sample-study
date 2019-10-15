#coding:utf-8

#  compute S,E,F,M,and N Matrix of Triode Sadou (Differential), Push-Pull (mathematical addition in C source) Amplifier
#                                  between Sadou and Push-Pull connect by VCVS
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
#  Oct-2019, Shun
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
# Sadou
# Triode circuit 1
VIN1R = 1
E21=  200   # E terminated Vs
R11= 100000
C10= 4.700000e-08
R10= 470000
CGK1= 1.600000e-12
CGP1= 1.700000e-12
CPK1= 4.600000e-13
E11=175     # By transform current source(=Is) to voltage(=Rp * Is) source, pararell res become serial.
            # More bigger Rp,  constant accuracy may improve.   
R15= 100000 # seido 1% ( 470/100k) teido .....
   

# RA and RB is Triode Internal Port Resistances
RA = 1000 # set as same as rt-wdf_renderer/Circuits/wdfCCTAx1Tree.hpp
RB = 1000 # set as same as rt-wdf_renderer/Circuits/wdfCCTAx1Tree.hpp
RC= T0/(2 * CGP1)
RD= T0/(2 * CGK1)
RE= T0/(2 * CPK1)
subtree4= T0/(2 * C10) + VIN1R
tree4= ParallelRes( subtree4 , R10)
RF= tree4
RG= R11  # E terminated Vs
RH= R15
###R15=470
###RH= R15


# Triode circuit 2
E22= 200   # E terminated Vs
R12= 100000
C12= 1.0e-6
CGK2= 1.600000e-12
CGP2= 1.700000e-12
CPK2= 4.600000e-13


# RI and RJ is Triode Internal Port Resistances
RI = 1000 # set as same as rt-wdf_renderer/Circuits/wdfCCTAx1Tree.hpp
RJ = 1000 # set as same as rt-wdf_renderer/Circuits/wdfCCTAx1Tree.hpp
RK= T0/(2 * CGP2)
RL= T0/(2 * CGK2)
RM= T0/(2 * CPK2)
RN= T0/(2 * C12)
RO= R12  # E terminated Vs

# Connection between gates
R14= 1000000

RP= R14

# Push Pull
# Triode circuit 1
E31= -55   # E terminated Vs
E31R= 1
C23= 100.00e-6
R21= 470000

E41= 300   # E terminated Vs
E41R= 1 
CGK21= 7.500000e-12
CGP21= 16.50000e-12
CPK21= 5.50000e-12
R25 = 22

# Output transformaer equivalent
R1T1= 64.7
R2T1= 158400
R3T1= 74.22736
C1T1= 1126.0e-12
L1T1= 1.771e-3
L2T1= 61.84
RLT1= 2375.276


# RA and RB is Triode Internal Port Resistances
RA_ = 1000 # set as same as rt-wdf_renderer/Circuits/wdfCCTAx1Tree.hpp
RB_ = 1000 # set as same as rt-wdf_renderer/Circuits/wdfCCTAx1Tree.hpp
RC_= T0/(2 * CGP21)
RD_= T0/(2 * CGK21)
RE_= T0/(2 * CPK21)

subtree31a= ParallelRes( T0/(2 * C23) , E31R)
tree31= R21 + subtree31a
RF_= tree31

subtree41a= RLT1 +  R3T1
subtree41b= ParallelRes( R2T1, ( 2 * L2T1 / T0) )
subtree41c= ParallelRes( subtree41a, subtree41b)
subtree41d= R1T1 + ( 2 * L1T1 / T0)
subtree41e= subtree41c + subtree41d
subtree41f= ParallelRes( T0/(2 * C1T1), subtree41e)
tree41= subtree41f + E41R
RG_= tree41

RH_= R25


# Triode circuit 2
E32= -55   # E terminated Vs
E32R= 1
C24= 100.00e-6
R22= 470000

E42= 300   # E terminated Vs
E42R= 1 
CGK22= 7.500000e-12
CGP22= 16.50000e-12
CPK22= 5.50000e-12
R24 = 22

# Output transformaer equivalent
R1T2= 73.5
R2T2= 158400
R3T2= 74.22736
C1T2= 1126.0e-12
L1T2= 1.771e-3
L2T2= 61.84
RLT2= 2375.276

# RI and RJ is Triode Internal Port Resistances
RI_ = 1000 # set as same as rt-wdf_renderer/Circuits/wdfCCTAx1Tree.hpp
RJ_ = 1000 # set as same as rt-wdf_renderer/Circuits/wdfCCTAx1Tree.hpp
RK_= T0/(2 * CGP22)
RL_= T0/(2 * CGK22)
RM_= T0/(2 * CPK22)

subtree32a= ParallelRes( T0/(2 * C24), E32R)
tree32= R22 + subtree32a
RN_= tree32

subtree42a= RLT2 +  R3T2
subtree42b= ParallelRes( R2T2, ( 2 * L2T2 / T0) )
subtree42c= ParallelRes( subtree42a, subtree42b)
subtree42d= R1T2 + ( 2 * L1T2 / T0)
subtree42e= subtree42c + subtree42d
subtree42f= ParallelRes( T0/(2 * C1T2), subtree42e)
tree42= subtree42f + E42R
RO_= tree42

RP_= R24

# VCVS by Sadou circuit outputs with DC-cut capacitor
VIN21=1
VIN22=1
C21= 4.700000e-08
C22= 4.700000e-08

RQ_= T0/(2 * C21) + VIN21
RR_= T0/(2 * C22) + VIN22


# symbols
#RA, RB, RC, RD, RE, RF, RG, RH, RI, RJ, RK, RL, RM, RN, RO, RP, RA_, RB_, RC_, RD_, RE_, RF_, RG_, RH_, RI_, RJ_, RK_, RL_, RM_, RN_, RO_, RP_, RQ_, RR_ = symbols('RA, RB, RC, RD, RE, RF, RG, RH, RI, RJ, RK, RL, RM, RN, RO, RP, RA_, RB_, RC_, RD_, RE_, RF_, RG_, RH_, RI_, RJ_, RK_, RL_, RM_, RN_, RO_, RP_, RQ_, RR_')
#
init_printing(use_unicode=True)

# Sadou
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
# GP= 1 / RP  # RH

# Connection between gates
GP = 1 / RP

# Push Pull
# Triode circuit 1
GA_= 1 / RA_
GB_= 1 / RB_
GC_= 1 / RC_
GD_= 1 / RD_
GE_= 1 / RE_
GF_= 1 / RF_
GG_= 1 / RG_
GH_= 1 / RH_

# Triode circuit 2
GI_= 1 / RI_  # RA
GJ_= 1 / RJ_  # RB
GK_= 1 / RK_  # RC
GL_= 1 / RL_  # RD
GM_= 1 / RM_  # RE
GN_= 1 / RN_  # RF
GO_= 1 / RO_  # RG
GP_= 1 / RP_  # RH

#  Connection from pre-amp, sadou to push-pull
GQ_ = 1 / RQ_
GR_ = 1 / RR_



# Regarding to Thevenin port equivalent, see Triode_Sadou_AMP_Thevenin_port.png and triode_PushPull_AMP_VCVS_connection_Thevenin_port.png
Y= Matrix( [
# Triode circuit 1                                                 Triode circuit 2                                 Connection   Triode circuit 1                                                Triode circuit 2                                                  Connection

# 2,3,4,5,6,7,8,9,10,11,12,13,14,16,17,18,19,20,21,22,23, 2_,    3_,    4_,       5_,   6_,   7_,   8_,  9_,   10_,   11_,  12_,    13_,   14_,  15_,      16_,  17_,  18_,  19_,   20_,  21_,   22_,   23_,     24_,   25_,
[ GA, -GA,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 2 V2
[ -GA, GA+GC+GE+GG ,0,0,0, -GC,0,  -GE,0,  -GG,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0 ,0],  # 3 V3
[0,0,  GH,0,0,0,0,0,0,0,  -GH,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 4 V4
[0,0,0,        GB, -GB,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 5 V5
[0,0,0,   -GB, GB+GD+GF+GP,0, -GD,0, -GF,0,0,0,0,0,0,0,0,0,0,0,  -GP,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 6 V6
[0,  -GC,0,0,0,   GC,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 7 V7
[0,0,0,0, -GD,0,  GD,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 8 V8
[0,  -GE,0,0,0,0,0,  GE,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 9 V9
[0,0,0,0, -GF,0,0,0,  GF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 10 V10
[0, -GG,0,0,0,0,0,0,0,   GG,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 11 V11
[0,0, -GH,0,0,0,0,0,0,0,   GH,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 12 V12
[0,0,0,0,0,0,0,0,0,0,0,     GI, -GI,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 13 V13
[0,0,0,0,0,0,0,0,0,0,0, -GI, GI+GK+GM+GO ,0,0,   -GK,0, -GM,0,    -GO,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0 ],  # 14 V14
[0,0,0,0,0,0,0,0,0,0,0,0,0,    GJ, -GJ,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 16 V16
[0,0,0,0,0,0,0,0,0,0,0,0,0, -GJ, GJ+GL+GN,0, -GL,0, -GN,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 17 V17
[0,0,0,0,0,0,0,0,0,0,0,0,  -GK,0,0,   GK,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 18 V18
[0,0,0,0,0,0,0,0,0,0,0,0,0,0, -GL,0,  GL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 19 V19
[0,0,0,0,0,0,0,0,0,0,0,0,  -GM,0,0,0,0,  GM,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 20 V20
[0,0,0,0,0,0,0,0,0,0,0,0,0,0, -GN,0,0,0,  GN,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 21 V21
[0,0,0,0,0,0,0,0,0,0,0,0, -GO,0,0,0,0,0,0,   GO,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 22 V22
[0,0,0,0, -GP,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,   GP,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 23 V23
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, GA_, -GA_,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 2 V2_
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, -GA_,GA_+GC_+GE_+GG_    ,0,0,0, -GC_,0, -GE_,0,  -GG_,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 3 V3_
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  GH_,0,0,0,0,0,0,0,  -GH_,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 4 V4_
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,     GB_, -GB_,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 5 V5_
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, -GB_,GB_+GD_+GF_+GQ_,0, -GD_,0, -GF_,0,0,0,0,0,0,0,0,0,0,0,0,0,-GQ_,0],  # 6 V6_
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  -GC_,0,0,0,   GC_,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 7 V7_
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, -GD_,0,  GD_,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 8 V8_
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  -GE_,0,0,0,0,0,  GE_,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 9 V9_
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, -GF_,0,0,0,   GF_,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 10 V10_
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, -GG_,0,0,0,0,0,0,0,    GG_,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 11 V11_
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, -GH_,0,0,0,0,0,0,0, GH_,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 12 V12_
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,     GI_, -GI_,0,0,0,0,0,0,0,0,0,0,0],  # 13 V13_
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, -GI_, GI_+GK_+GM_+GO_,0,0,0,  -GK_,0, -GM_,0,  -GO_,0,0,0],  # 14 V14_
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  GP_,0,0,0,0,0,0,0, -GP_,0,0],  # 15 V15_
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,     GJ_, -GJ_,0,0,0,0,0,0,0,0],  # 16 V16_
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, -GJ_, GJ_+GL_+GN_ + GR_,0, -GL_,0, -GN_,0,0,0,-GR_],  # 17 V17_
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  -GK_,0,0,0,   GK_,0,0,0,0,0,0,0],  # 18 V18_
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, -GL_,0,  GL_,0,0,0,0,0,0],  # 19 V19_
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  -GM_,0,0,0,0,0,   GM_,0,0,0,0,0],  # 20 V20_
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, -GN_,0,0,0,  GN_,0,0,0,0],  # 21 V21_
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, -GO_,0,0,0,0,0,0,0,   GO_,0,0,0],  # 22 V22_
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, -GP_,0,0,0,0,0,0,0,   GP_,0,0],  # 23 V23_
[0, 0 ,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, -GQ_,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,    GQ_ ,0],   # 24 V24_
[0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,    -GR_,0,0,0,0,0,0,0,  GR_ ]     # 25 V25_


])

print ('Y.shape', Y.shape)
NUM_NODES=Y.shape[0]
print ( 'NUM_NODES', NUM_NODES)



A= Matrix( [
#  A,  B,   I,   J,  A_, B_,  I_,  J_,     C,  D,  E,  F,  G,  H,   K,  L,  M,  N,  O,       P ,    C_, D_, E_, F_, G_, H_,  K_, L_, M_, N_, O_, P_,     Q_, R_ ,
# JA, JB,  JI,  JJ, JA_,JB_, JI_, JJ_,    JC, JD, JE, JF, JG, JH,   JK, JL, JM, JN, JO,      JP,   JC_,JD_J,E_,JF_,JG_,JH_,  JK_,JL_,JM_,JN_,JO_,JP_,    JQ_,JR_,
[ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 2
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 3
[ -1,-1,-1,-1,0,0,0,0,0,-1,-1,0,0,0,0,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 4
[ 0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 5
[ 0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 6 
[ 0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 7
[ 0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 8
[ 0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 9 
[ 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 10 
[ 0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 11 
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 12
[ 0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 13
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 14
[ 0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 16
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 17
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 18
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 19
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 20
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 21 
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 22
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],     # 23
[ 0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 2_
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 3_
[ 0,0,0,0,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,0,0,0,0,0,0,0,0,0,0,0],   # 4_
[ 0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 5_
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 6_ 
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 7_
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],   # 8_
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],   # 9_
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],   # 10_ 
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],   # 11_ 
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],   # 12_
[ 0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 13_
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 14_
[ 0,0,0,0,0,0,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,0,0,0,0,0],   # 15_
[ 0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # 16_
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0],   # 17_
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],   # 18_
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],   # 19_
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],   # 20_
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],   # 21_
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],   # 22_ 
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],   # 23_
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],   # 24_
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]    # 25_


])

print ('A.shape', A.shape)

AT= A.T

# R-type adaptor
Rp= Matrix( [
# trode portion
[ RA,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,   RB,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,  RI,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,  RJ,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   RA_,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,   RB_,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,    0,  RI_,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,    0,   0,  RJ_,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
# other portion
[ 0,    0,   0,   0,   0,    0,   0,   0,  RC,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,  RD,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,  RE,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,  RF,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,  RG,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,  RH,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
#  skip...
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,  RK,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RL,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RM,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RN,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RO,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RP,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
# other portion
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RC_,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RD_,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RE_,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RF_,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0, RG_,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0, RH_,   0,   0,   0,   0,   0,   0,   0,   0],
#  skip...
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, RK_,   0,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, RL_,   0,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, RM_,   0,   0,   0,   0,   0],
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RN_,  0,   0,   0,   0],
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RO_,  0,   0,   0],
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RP_,  0,   0],
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  RQ_,  0],
[ 0,    0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, RR_]
])

print ('Rp.shape', Rp.shape)
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


# two triode internal port number is 8(=2port x 2 x 2)
NUM_internal_ports=8
S11O=get_S11(S2_eval, internal_ports_number=NUM_internal_ports)
S12O=get_S12(S2_eval, internal_ports_number=NUM_internal_ports)
S21O=get_S21(S2_eval, internal_ports_number=NUM_internal_ports)
S22O=get_S22(S2_eval, internal_ports_number=NUM_internal_ports)


# C-matrix : convert A_interal and B_interal into V_c and I_c
RI = Matrix([
[RA, 0, 0, 0,  0, 0, 0,  0],
[0, RB, 0, 0,  0, 0, 0,  0],
[0, 0, RI, 0,  0, 0, 0,  0],
[0, 0, 0, RJ,  0, 0, 0,  0],
[0, 0, 0,  0, RA_, 0, 0, 0],
[0, 0, 0,  0, 0, RB_, 0, 0],
[0, 0, 0,  0, 0, 0, RI_, 0],
[0, 0, 0,  0, 0, 0, 0, RJ_] 
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


"""
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
    
"""

# write S,E,F,M,N matrix as c form
with open('matrix_c_form_sadou_pushpull_VCVS_connection.txt','wt') as outf:
    write_matrx(outf, S2_eval, 'S')
    write_matrx(outf, E, 'E')
    write_matrx(outf, F, 'F')
    write_matrx(outf, M, 'M')
    write_matrx(outf, N, 'N')


