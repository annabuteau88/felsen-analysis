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

def createTrialArray(h5file, timeBins, units):
    """
    This function creates a list of len(trials) where each line is a units x 11 time bins array of spiking activity 
    This is the first step to running a PCA analysis that looks at population activity over time
    """
    trials = list()
    session = AnalysisObject(h5file)
    #population = Population(session)
    population = session._population()
    saccades = session.load('saccades/predicted/left/timestamps')[:, 0]
    for trial in saccades:
        unitArray = np.zeros((len(units), 10))
        ind = 0
        for unit in population:
            if unit.cluster in units:
                spikeTimes = unit.timestamps
                t1 = trial + timeBins[0]
                t2 = trial + timeBins[1]
                t3 = trial + timeBins[2]
                t4 = trial + timeBins[3]
                t5 = trial + timeBins[4]
                t6 = trial + timeBins[5]
                t7 = trial + timeBins[6]
                t8 = trial + timeBins[7]
                t9 = trial + timeBins[8]
                t10 = trial + timeBins[9]
                t11 = trial + timeBins[10]
                mask1 = np.logical_and(spikeTimes >= t1, spikeTimes < t2)
                a = len(spikeTimes[mask1])/0.3
                mask2 = np.logical_and(spikeTimes >= t2, spikeTimes < t3)
                b = len(spikeTimes[mask2])/0.3
                mask3 = np.logical_and(spikeTimes >= t3, spikeTimes < t4)
                c = len(spikeTimes[mask3])/0.3
                mask4 = np.logical_and(spikeTimes >= t4, spikeTimes < t5)
                d = len(spikeTimes[mask4])/0.3
                mask5 = np.logical_and(spikeTimes >= t5, spikeTimes < t6)
                e = len(spikeTimes[mask5])/0.3
                mask6 = np.logical_and(spikeTimes >= t6, spikeTimes < t7)
                f = len(spikeTimes[mask6])/0.3
                mask7 = np.logical_and(spikeTimes >= t7, spikeTimes < t8)
                g = len(spikeTimes[mask7])/0.3
                mask8 = np.logical_and(spikeTimes >= t8, spikeTimes < t9)
                h = len(spikeTimes[mask8])/0.3
                mask9 = np.logical_and(spikeTimes >= t9, spikeTimes < t10)
                i = len(spikeTimes[mask9])/0.3
                mask10 = np.logical_and(spikeTimes >= t10, spikeTimes < t11)
                j = len(spikeTimes[mask10])/0.3
                fr = [a, b, c, d, e, f, g, h, i, j]
                unitArray[ind, :] = fr
                ind = ind + 1
        trials.append(unitArray)
    return trials
