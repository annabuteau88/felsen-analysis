import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from pyopenephys import File
import pandas as pd
from toolkit.process import AnalysisObject
from zetapy import zetatest
import spikeinterface.extractors as se
import spikeinterface.preprocessing as spre
import spikeinterface.sorters as sorters
from spikeinterface.core import write_binary_recording


def removeArtifacts(h5file, basePath, output, mode, optoTimes):
    """
    Use spike interface's remove_artifacts function to remove artifacts and save out a .dat file that can be kilosorted
    Base path must contain in it the Record Node 101 directory!
    Hasn't been tested yet bc interfacing with anything processing related is annoying and out of the scope of this lol
    """
    session = AnalysisObject(h5file)
    recording = se.OpenEphysBinaryRecordingExtractor(basePath, stream_name=np.str_('Record Node 101#Neuropix-PXI-100.ProbeA-AP'))
    optoTimesTotal = list()
    optoListLabels = list()
    for onset in optoTimes:
        offset = onset + 0.01
        optoTimesTotal.append(onset)
        optoTimesTotal.append(offset)
        optoListLabels.append('onset')
        optoListLabels.append('offset')     
    optoTimesTotal = np.array(optoTimesTotal)
    recording = spre.remove_artifacts(recording, np.around(optoTimesTotal*30000).astype(int), ms_before = 0.5,ms_after = 3, list_labels=optoListLabels, mode=mode)
    write_binary_recording(recording, file_paths=[os.path.join(base, f'{output}{mode}artifact.dat')], dtype="int16")  # or "int16" depending on your analysis pipeline)
    return

def plotRawNeuropixelsData(t2plot, folderPath, datPath, vmin=None, vmax=None):
    """
    Takes .dat file (raw Neuropixels data) and plots a small section
    Probably not more than 10sec if you don't want to crash your computer :)
    Particularly useful for assessing opto artifacts
    """
    freq = 30_000  # sampling rate placeholder
    file = File(folderPath)
    exp = file.experiments[0]
    rec = exp.recordings[0]
    fs = rec.sample_rate
    file_size = os.path.getsize(datPath)  # in bytes
    channel_count = 384
    total_samples = file_size // (2 * channel_count)  # 2 bytes per int16
    # Memory-map full range
    sig_all = np.memmap(datPath, dtype='int16', mode='r', shape=(total_samples, channel_count))
    # Slice for your chosen window
    start_idx = int(t2plot[0] * fs)
    end_idx   = int(t2plot[1] * fs)
    sig_window = sig_all[start_idx:end_idx, :]  # shape: (window_duration × channel_count)
    sig = sig_window.T  # shape: (channels × window_duration)
    # Plot analog trace
    n_ch, n_samps = sig.shape
    fig, axs = plt.subplots(figsize=(10, 5))
    im = axs.imshow(sig, aspect='auto', origin='lower', extent=[t2plot[0], t2plot[1], 0, n_ch],cmap='inferno', vmin=vmin, vmax=vmax)
    fig.colorbar(im)
    return fig, axs

def runZetaTestForOpto(h5file, eventTimestamps, responseWindow, latencyMetric):
    """
    ZETA test to check if neurons are responsive to the opto stim
    """
    session = AnalysisObject(h5file)
    population = session._population()
    tOffset = 0 - responseWindow[0]
    responseWindowAdjusted = np.array(responseWindow) + tOffset
    #
    result = np.full([len(population), 3], np.nan)
    unitIndex = 0
    for i, unit in enumerate(population):
        p, dZeta, dRate = zetatest(
            unit.timestamps,
            eventTimestamps - tOffset,
            dblUseMaxDur=np.max(responseWindowAdjusted),
            tplRestrictRange=responseWindowAdjusted,
            boolReturnRate=True,
        )
        allLatencies = dZeta['vecLatencies']

        # NOTE: Sometimes this returns a list
        if type(allLatencies) == list:
            allLatencies = np.array(allLatencies)

        # NOTE: Sometimes this returns a 2D array (single column)
        if type(allLatencies) == np.ndarray and len(allLatencies.shape) == 2:
            allLatencies = np.ravel(allLatencies)

        #
        if latencyMetric == 'zenith':
            tLatency = round(allLatencies[0] - tOffset, 3)
        elif latencyMetric == 'peak':
            tLatency = round(allLatencies[2] - tOffset, 3)
        elif latencyMetric == 'onset':
            tLatency = round(allLatencies[3] - tOffset, 3)
        else:
            tLatency = np.nan
        result[unitIndex, :] = [unitIndex, tLatency, p]
        unitIndex = unitIndex + 1
        
        #
    session.save(f'zeta/optostim/p', result[:, 2])
    session.save(f'zeta/optostim/latency', result[:, 1])
    return

def defineOptoPopulation(h5file, clusterFile):
    """
    This function filters your population of neurons and pulls out premotor neurons based on ZETA test results
    """
    session = AnalysisObject(h5file)
    spikeClustersFile = clusterFile
    uniqueSpikeClusters = np.unique(np.load(spikeClustersFile))
    zetaOpto = session.load('zeta/optostim/p')
    ampCutoff = session.load('metrics/ac')
    presenceRatio = session.load('metrics/pr')
    firingRate = session.load('metrics/fr')
    isiViol = session.load('metrics/rpvr')
    qualityLabels = session.load('metrics/ql')
    optoUnitsZeta = list()
    for index, pVal in enumerate(zetaOpto):
        if pVal < 0.01:
            if qualityLabels is not None and qualityLabels[index] in (0, 1):
                    continue
            if ampCutoff[index] <= 0.1:
                if presenceRatio[index] >= 0.9:
                    if firingRate[index] >= 0.2:
                        if isiViol[index] <= 0.5:
                            unit = uniqueSpikeClusters[index]
                            optoUnitsZeta.append(unit)

    return optoUnitsZeta
