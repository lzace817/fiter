from resistors import *
from prefixed import Float

def design_amp():
    ignore =['vcc', 'vref', 'A', 'ins' , '_ins']
    #----------------------------------------------------------
    vcc = 10
    rd, ru = design_div(0, vcc, 1.9, 2000)

    rd = preferred_closest(rd)
    ru = preferred_closest(ru)

    vth = vcc*rd/(rd+ru)
    rth = rd*ru/(rd+ru)

    ib = (vth-0.7)/(rth + 100*39)
    #----------------------------------------------------------
    print('\nResults:')
    vars = locals()
    for n in vars:
        if n not in ignore and n != 'ignore':
            if n[0] == 'r':
                print(f'{n:5} = {Float(vars[n]):.1h}')    
            else:
                print(f'{n:5} = {vars[n]}')    

if __name__ == '__main__':
    design_amp()

'''
.model BC547C NPN(IS=4.679E-14 NF=1.01  ISE=2.642E-15 NE=1.581 BF=458.7 IKF=0.1371 VAF=52.64 NR=1.019 ISC=2.337E-14 NC=1.164 BR=11.57 IKR=0.1144 VAR=364.5 RB=1 IRB=1.00E-06 RBM=1 RE=0.2598 RC=1    XTB=0 EG=1.11 XTI=3 CJE=1.229E-11 VJE=0.5591 MJE=0.3385 TF=4.689E-10 XTF=160 VTF=2.828 ITF=0.8842 PTF=0 CJC=4.42E-12  VJC=0.1994 MJC=0.2782 XCJC=0.6193 TR=1.00E-32 CJS=0 VJS=0.75 MJS=0.333 FC=0.7936 Vceo=45 Icrating=100m mfg=NXP)
.model BC547B NPN(IS=2.39E-14  NF=1.008 ISE=3.545E-15 NE=1.541 BF=294.3 IKF=0.1357 VAF=63.2  NR=1.004 ISC=6.272E-14 NC=1.243 BR=7.946 IKR=0.1144 VAR=25.9  RB=1 IRB=1.00E-06 RBM=1 RE=0.4683 RC=0.85 XTB=0 EG=1.11 XTI=3 CJE=1.358E-11 VJE=0.65   MJE=0.3279 TF=4.391E-10 XTF=120 VTF=2.643 ITF=0.7495 PTF=0 CJC=3.728E-12 VJC=0.3997 MJC=0.2955 XCJC=0.6193 TR=1.00E-32 CJS=0 VJS=0.75 MJS=0.333 FC=0.9579 Vceo=45 Icrating=100m mfg=NXP)
'''