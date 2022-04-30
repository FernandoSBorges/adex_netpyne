"""
script to load sim and plot
"""

from netpyne import sim
from matplotlib import pyplot as plt
import os
import IPython as ipy
import pickle as pkl


###########################
######## MAIN CODE ########
###########################

if __name__ == '__main__':

    dataType = 'spont' #'speech' #'spont'

    if dataType == 'spont':
        filenames = ['../data/v0_batch1/v0_batch1_%d_data.pkl' % (iseed) for iseed in [0] ]
        timeRange = [8000, 9000]

    allData = []

    for filename in filenames:

        sim.load(filename, instantiate=True, instantiateConns = False, instantiateStims = False, instantiateRxD = False, createNEURONObj = False)

        # standardd plots
        # sim.analysis.plotRaster(**{'include': ['allCells'], 'saveFig': True, 'showFig': False, 'labels': None, 'popRates': False,'orderInverse': True, 'timeRange': timeRange, 'figSize': (48,24), 'fontSize':12, 'lw': 2, 'markerSize':2, 'marker': '.', 'dpi': 75})
        # sim.analysis.plotTraces(**{'oneFigPer': 'trace', 'overlay': False, 'timeRange': timeRange, 'ylim': [-70,-35], 'saveFig': True, 'showFig': False, 'figSize':(48,24)})
        
        sim.analysis.plotTraces(**{'oneFigPer': 'trace', 'overlay': False, 'timeRange': timeRange, 'ylim': [-60,-35], 'saveFig': filename[:-4]+'_traces_B.png', 'showFig': False, 'figSize':(24,12)})
                
        sim.analysis.plotRaster(**{'saveFig':True, 'showFig': False, 'popRates':True, 'spikeHist':True,  'spikeHistBin':5, 'syncLines':True, 'orderInverse': True, 'timeRange': timeRange, 'fontSize':8, 'figSize': (24,12), 'lw': 4.0, 'markerSize': 4, 'marker': 'o', 'dpi': 100})
# sim.analysis.plotSpikeStats(stats=['rate'],figSize = (6,12), timeRange=[1500, 31500], dpi=300, showFig=0, saveFig=filename[:-4]+'_stats_30sec')
        #sim.analysis.plotSpikeStats(stats=['rate'],figSize = (6,12), timeRange=[1500, 6500], dpi=300, showFig=0, saveFig=filename[:-4]+'_stats_5sec')
        #sim.analysis.plotLFP(**{'plots': ['spectrogram'], 'electrodes': ['avg', [0], [1], [2,3,4,5,6,7,8,9], [10, 11, 12], [13], [14, 15], [16,17,18,19]], 'timeRange': timeRange, 'maxFreq': 50, 'figSize': (8,24), 'saveData': False, 'saveFig': filename[:-4]+'_LFP_spec_7s_all_elecs', 'showFig': False})

        # sim.analysis.plotRaster(**{'include': S1cells, 'saveFig': True, 'showFig': False, 'labels': None, 'popRates': False,'orderInverse': True, 'timeRange': timeRange, 'figSize': (36,24), 'fontSize':4, 'lw': 5, 'markerSize':10, 'marker': '.', 'dpi': 300})
        
        # sim.analysis.plotLFP(**{'plots': ['locations'], 
        #         'figSize': (24,24), 
        #         'saveData': False, 
        #         'saveFig': True, 'showFig': False, 'dpi': 300})

        # sim.analysis.plotLFP(**{'plots': ['timeSeries'], 
        #         # 'electrodes': 
        #         # [[0,1,2,3]], #'avg', 
        #         'timeRange': timeRange, 
        #         'figSize': (24,12), 'saveFig': True, 'showFig': False})

        # sim.analysis.plotLFP(**{'plots': ['spectrogram'], 
        #         # 'electrodes': 
        #         # [[0,1,2,3]],
        #         'timeRange': timeRange, 
        #         'maxFreq': 400, 
        #         'figSize': (16,12), 
        #         'saveData': False, 
        #         'saveFig': True, 'showFig': False})

        # sim.analysis.plotLFP(**{'plots': ['PSD'], 
        #         # 'electrodes': 
        #         # [[0,1,2,3]],
        #         'timeRange': timeRange, 
        #         'maxFreq': 400, 
        #         'figSize': (8,12), 
        #         'saveData': False, 
        #         'saveFig': True, 'showFig': False})
