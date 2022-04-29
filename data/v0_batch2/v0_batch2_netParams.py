
"""
netParams.py

High-level specifications for S1 network model using NetPyNE

Contributors: salvadordura@gmail.com, fernandodasilvaborges@gmail.com
"""

from netpyne import specs
import os

netParams = specs.NetParams()   # object of class NetParams to store the network parameters


try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    from cfg import cfg

#------------------------------------------------------------------------------
#
# NETWORK PARAMETERS
#
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# General network parameters
#------------------------------------------------------------------------------
netParams.scale = cfg.scale # Scale factor for number of cells
netParams.sizeX = cfg.sizeX # x-dimension (horizontal length) size in um
netParams.sizeY = cfg.sizeY # y-dimension (vertical height or cortical depth) size in um
netParams.sizeZ = cfg.sizeZ # z-dimension (horizontal depth) size in um
netParams.shape = 'cylinder' # cylindrical (column-like) volume
   
#------------------------------------------------------------------------------
# General connectivity parameters
#------------------------------------------------------------------------------
netParams.defaultThreshold = -35.0 # spike threshold, 10 mV is NetCon default, lower it for all cells
netParams.defaultDelay = 0.1 # default conn delay (ms)
netParams.propVelocity = 300.0 #  300 μm/ms (Stuart et al., 1997)
netParams.scaleConnWeightNetStims = 0.001  # weight conversion factor (from nS to uS)

#------------------------------------------------------------------------------
# Population parameters
#------------------------------------------------------------------------------
netParams.popParams['E'] = {'cellType': 'PYR', 'numCells': 800, 'cellModel': 'Adex'}
netParams.popParams['I'] = {'cellType': 'PYR', 'numCells': 200, 'cellModel': 'Adex'}

#------------------------------------------------------------------------------
# Cell parameters
#------------------------------------------------------------------------------
### AdEx2007 (section voltage)
firing = 'adaptation2'
netParams.importCellParams(
    label='PYR_Adex_rule', 
    conds={'cellType': 'PYR', 'cellModel':'Adex'},
    fileName='cells/adexWrapper.py', 
    cellName='AdExCell',  
    cellArgs={'type':firing},
    )
netParams.renameCellParamsSec('PYR_Adex_rule', 'sec', 'soma')  # rename imported section 'sec' to 'soma'

#------------------------------------------------------------------------------
# Synaptic mechanism parameters
#------------------------------------------------------------------------------
netParams.synMechParams['exc'] = {
    'mod': 'Exp2Syn', 
    'tau1': 0.01, 
    'tau2': 2.728, 
    'e': 0}  # excitatory synaptic mechanism
netParams.synMechParams['inh'] = {
    'mod': 'Exp2Syn', 
    'tau1': 0.01, 
    'tau2': 2.728, 
    'e': -80}  # inhibitory synaptic mechanism

#------------------------------------------------------------------------------
# Cell connectivity rules
#------------------------------------------------------------------------------
netParams.connParams['exc->all'] = {    #  S -> M label
    'preConds': {'pop': 'E'},       # conditions of presyn cells
    'postConds': {'pop': ['E','I']},      # conditions of postsyn cells
    'probability': 0.1,               # probability of connection
    'weight': cfg.gsyn,                 # synaptic weight
    'delay': 0.01,                     # transmission delay (ms)
    'synMech': 'exc'}    

netParams.connParams['inh->all'] = {    #  S -> M label
    'preConds': {'pop': 'I'},       # conditions of presyn cells
    'postConds': {'pop': ['E','I']},      # conditions of postsyn cells
    'probability': 0.1,               # probability of connection
    'weight': 4*cfg.gsyn,                 # synaptic weight
    'delay': 0.01,                     # transmission delay (ms)
    'synMech': 'inh'}    

#------------------------------------------------------------------------------    
# Current inputs (IClamp)
#------------------------------------------------------------------------------
if cfg.addIClamp:
     for j in range(cfg.IClampnumber):
        key ='IClamp'
        params = getattr(cfg, key, None)
        key ='IClamp'+str(j+1)
        params = params[j]
        [pop,sec,loc,start,dur,amp] = [params[s] for s in ['pop','sec','loc','start','dur','amp']]

        # add stim source
        netParams.stimSourceParams[key] = {'type': 'IClamp', 'delay': start, 'dur': dur, 'amp': amp}
        
        # connect stim source to target
        netParams.stimTargetParams[key+'_'+pop] =  {
            'source': key, 
            'conds': {'pop': pop},
            'sec': sec, 
            'loc': loc}
