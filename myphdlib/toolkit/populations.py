population = Population()
#for unit in population:
    #spikeTimes = unit.timestamps
    #spikeCluster = unit.cluster

def definePremotorPopulation(self, h5file):
    """
    This function filters your population of neurons and pulls out premotor neurons based on ZETA test results
    """
    session = AnalysisObject()
    population = Population(session)
    labels = session.load(h5file, 'nptracer/labels')
    transformed = session.load(h5file, 'nptracer/transformed')
    brainAreas = ul.translateBrainAreaIdentities(labels) 
    spikeClustersFile = session.home.joinpath('ephys/sorting/manual/spike_clusters.npy') #fix
    uniqueSpikeClusters = np.unique(np.load(spikeClustersFile))
    zetaNasal = session.load(h5file, 'zeta/saccade/nasal/p')
    zetaTemporal = session.load(h5file, 'zeta/saccade/temporal/p')
    ampCutoff = session.load(h5file, 'metrics/ac')
    presenceRatio = session.load(h5file, 'metrics/pr')
    firingRate = session.load(h5file, 'metrics/fr')
    isiViol = session.load(h5file, 'metrics/rpvr')
    qualityLabels = session.load('h5file, metrics/ql')
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
    