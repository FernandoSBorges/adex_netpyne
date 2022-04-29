"""
adex - adaptive exponential integrate-and-fire model

Python wrappers for the different celltypes of adex neuron.
Equations and parameter values taken from
  Borges, FS (2017). "Synchronised firing patterns in a random network of adaptive
  exponential integrate-and-fire neuron model" Neural Networks 90 (2017) 1–7
  http://dx.doi.org/10.1016/j.neunet.2017.03.005
  Corresponding author.
	fernandodasilvaborges@gmail.com
    
    updated on 420 2022 by Javier Palma-Espinosa
    javier.palma@cinv.cl
  

Cell types from 1 to 5 are based on Borges, FS (2017) Fig. 1:
    a. Adaptation
    b. Tonic spiking
    c. Initial burst
    d. Regular bursting
    e. Irregular
"""
import json
from neuron import h
#%%
fname = './cells/AdExPars.json'

with open(fname) as f:
    var = json.load(f)

dummy = h.Section()


# class of basic AdEx neuron based on parameters 
class AdExCell ():
  '''
  Create an adex cell based on izhi2003b.mod (https://senselab.med.yale.edu/ModelDB/ShowModel?model=39948)
  Note: Capacitance 'C' differs from sec.cm which will be 1
'''
  def getVars(self,var):
      for key,val in zip(var.keys(),var.values()):
            exec(f"self.adx.{key} = {val}")

  def __init__ (self, type='Adaptation', cellid=-1):
      self.sec = h.Section(name='adex'+type+str(cellid))
      self.sec.L, self.sec.diam = 6.3, 5 # empirically tuned 
      self.adx = h.adex(0.5, sec=self.sec)
    
      self.type = type
      self.getVars(var[type])
    

  def init (self): self.sec(0.5).v = self.vinit

  def reparam (self, type='Adaptation', cellid=-1):
      self.type=type
      self.getVars(var[type])
    
