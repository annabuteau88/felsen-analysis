from toolkit.process import AnalysisObject
from interface.ephys import Population
import unit_localizer as ul
import numpy as np

def definePremotorPopulation(h5file, clusterFile):
    """
    This function filters your population of neurons and pulls out premotor neurons based on ZETA test results
    """
    session = AnalysisObject(h5file)
    population = Population(session)
    labels = session.load('nptracer/labels')
    transformed = session.load('nptracer/transformed')
    brainAreas = ul.translateBrainAreaIdentities(labels) 
    #spikeClustersFile = session.home.joinpath('ephys/sorting/manual/spike_clusters.npy') #fix
    spikeClustersFile = clusterFile
    uniqueSpikeClusters = np.unique(np.load(spikeClustersFile))
    zetaNasal = session.load('zeta/saccade/nasal/p')
    zetaTemporal = session.load('zeta/saccade/temporal/p')
    ampCutoff = session.load('metrics/ac')
    presenceRatio = session.load('metrics/pr')
    firingRate = session.load('metrics/fr')
    isiViol = session.load('metrics/rpvr')
    qualityLabels = session.load('metrics/ql')
    premotorUnitsZeta = list()
    for index, pVal in enumerate(zetaNasal):
        if brainAreas[index] in ['SCsg','SCop', 'SCig', 'SCiw', 'SCdg']:
            pNasal = pVal
            pTemporal = zetaTemporal[index]
            if pNasal < pTemporal:
                p = pNasal
            elif pTemporal < pNasal:
                p = pTemporal
            if p < 0.05:
                if qualityLabels is not None and qualityLabels[index] in (0, 1):
                        continue
                if ampCutoff[index] <= 0.1:
                    if presenceRatio[index] >= 0.9:
                        if firingRate[index] >= 0.2:
                            if isiViol[index] <= 0.5:
                                unit = uniqueSpikeClusters[index]
                                premotorUnitsZeta.append(unit)

    return premotorUnitsZeta
    
def defineVisualPopulation(h5file, clusterFile):
    """
    This function filters your population of neurons and pulls out visual neurons based on ZETA test results
    """
    session = AnalysisObject(h5file)
    population = Population(session)
    labels = session.load('nptracer/labels')
    transformed = session.load('nptracer/transformed')
    #spikeClustersFile = session.home.joinpath('ephys/sorting/manual/spike_clusters.npy')
    spikeClustersFile = clusterFile
    uniqueSpikeClusters = np.unique(np.load(spikeClustersFile))
    brainAreas = ul.translateBrainAreaIdentities(labels) 
    zetaLeft = session.load('zeta/probe/left/p')
    zetaRight = session.load('zeta/probe/right/p')
    ampCutoff = session.load('metrics/ac')
    presenceRatio = session.load('metrics/pr')
    firingRate = session.load('metrics/fr')
    isiViol = session.load('metrics/rpvr')
    qualityLabels = session.load('metrics/ql')
    visualUnitsZeta = list()
    for index, pVal in enumerate(zetaLeft):
        if brainAreas[index] in ['SCsg','SCop', 'SCig', 'SCiw', 'SCdg']:
            pLeft = pVal
            pRight = zetaRight[index]
            if pLeft < pRight:
                p = pLeft
            elif pRight < pLeft:
                p = pRight
            if p < 0.05:
                if qualityLabels is not None and qualityLabels[index] in (0, 1):
                        continue
                if ampCutoff[index] <= 0.1:
                    if presenceRatio[index] >= 0.9:
                        if firingRate[index] >= 0.2:
                            if isiViol[index] <= 0.5:
                                unit = uniqueSpikeClusters[index]
                                visualUnitsZeta.append(unit)
    return visualUnitsZeta
