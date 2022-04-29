COMMENT
    Point process implementation of the AdEx neuron.
    Equations and parameter values are taken from
    Brette, R., & Gerstner, W. (2005). Adaptive exponential integrate-and-fire model 
    as an effective description of neuronal activity. 
    Journal of neurophysiology, 94(5), 3637-3642.

    TODO: define this example usage
    Example usage (in Python):
    from neuron import h
    sec = h.Section(name=sec) # section will be used to calculate v
    adex = h.Adex2021b(0.5)
    def initiz () : sec.v=-60
    fih=h.FInitializeHandler(initz)
    adex.I_ext = 70  # current clamp

    Cell types available are based on Naud et al.,Biol Cybern(2008):
        1.
        2.
        3.
        4.
        5.
        6.
        7.
        8.
        9.
        10.
        11.

    This model is an adaptation from the work done by Cliff Kerr (http://thekerrlab.com), June 2019.
    Enhancement done by Javier Palma-Espinosa (https://github.com/jpalma-espinosa), April 2022,
    based on the work of Fernando Borges.
ENDCOMMENT

: Declare name of object and variables
NEURON {
    POINT_PROCESS adex
    RANGE gl, deltaT, tauk, a, b, E_l, I_ext, C, V_reset, V_T, fflag
    NONSPECIFIC_CURRENT i
}

UNITS {
	(mV) = (millivolt)
	(pA) = (picoamp)
    (pF) = (picofarads)
    (nS) = (nanosiemens)

}

:initializion and activation of the process
INITIAL { 
    k = 0.0            
    v = -65.0          
    net_send(0,1)
}

: Parameters for delayed cell. See cell types in the comments above
PARAMETER {
	V_reset = -68.0	(mV)		:reset potential after spike
	V_T = -50.0	    (mV)		:threshold for spike detection
	V_spike = 40.0  (mV)	    :value of spike

	a = 2.0		    (nS)		:coupling with adaptive variable
	b = 60.0   		(pA)		:adaptive increment
	tauk = 300.0	(ms)		:adaptive time costant
	E_l = -70.0		(mV)		:resting potential for leak term
	gl  = 12.0		(nS)	    :leak conductance
	deltaT = 2.0	(mV)	    :speed of exp
    C = 200.0       (pF)        :cell Capacitance
    
    I_ext = 509.7     (pA)        :Current Clamp
    fflag = 1
    
}

ASSIGNED {
    v (mV)
    i (nA)
}

STATE {
    k (mV/ms)
}

BREAKPOINT{ 
    SOLVE states METHOD cnexp
    i =-0.001*(1.0/C)*(-gl*(v-E_l)+gl*deltaT*exp((v-V_T)/deltaT)- k + I_ext)
}

:solve the system
DERIVATIVE states { 
    k' = (1.0/tauk)*(a*(v-E_l)-k)
}

: Input received
NET_RECEIVE (w) {
  : Check if spike occurred
  if (flag == 1){ 
      WATCH (v > -35) 2
  }  
  else if (flag == 2){
    : Send spike event 
      net_event(t)
      v = V_reset
      k = k + b
  }
}
