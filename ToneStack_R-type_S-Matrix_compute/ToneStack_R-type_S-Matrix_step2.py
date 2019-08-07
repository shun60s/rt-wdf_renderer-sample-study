#coding:utf-8

#  compute S-Matrix of Fender Bassman tone stack, substitute value for symbol
#
#  REFERENCES:
#    WAVE DIGITAL FILTER ADAPTORS FOR ARBITRARY TOPOLOGIES AND MULTIPORT LINEAR ELEMENTS (DAFx-15)  
#    Eq. (6) and Figure-4 
#
#    rt-wdf_renderer/Circuits/wdfTonestackTree.hpp
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


# set value
FS=44100
T0= 1 / FS
pBASS=0.5
pMID=0.5
pTREBLE=0.5

R1 = 250E3
R1M = pTREBLE * R1 
R1P = R1 - R1M
R2 = 1E6 * pBASS
R3 = 25E3
R3P= pMID * R3
R3M= R3 - R3P
R4 = 56E3
C1 = 250E-12
C2 = 20E-9
C3 = 20E-9


# RA and RB is variable, due to it depends on R3M(pMID), R3P(pMID), and R2(pBass)
#vRA= R3M
#vRB= R3P + R2
vRC= R1 + T0/(2 * C1)
vRD= T0/(2 * C2)
vRE= R4
vRF= T0/(2 * C3)


#
init_printing(use_unicode=True)

# symbols
RA, RB, RC, RD, RE, RF = symbols('RA, RB, RC, RD, RE, RF')

# load the Matrix computed by step 1
with open('s_matrix1.pickle', 'rb') as inf:    
   S2 = pickle.loads(inf.read())

# create new matrix to substitute 
S2_eval= S2.subs( {RC : vRC,  RD : vRD, RE : vRE, RF : vRF} )
S2_eval

# simplify
S2_evals= simplify( S2_eval )

# write S matrix as txt
print(S2_evals, file=codecs.open('s_matrix2.txt', 'w', 'utf-8'))

# write S matrix as pickle
with open('s_matrix2.pickle', 'wb') as outf:
    outf.write(pickle.dumps(S2_evals))

