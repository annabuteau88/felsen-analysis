import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from pyopenephys import File
import pandas as pd

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

def runZetaTestForOpto(h5file, unitsToAnalyze, eventTimestamps, responseWindow):
    """
    ZETA test to check if neurons are responsive to the opto stim
    """
    session = AnalysisObject(h5file)
    population = session._population()
    tOffset = 0 - responseWindow[0]
    responseWindowAdjusted = np.array(responseWindow) + tOffset

    #
    result = np.full([len(unitsToAnalyze), 3], np.nan)
    for i, unit in enumerate(population):
        if unit.cluster not in unitsToAnalyze:
            continue
        # Skip if there are not enough spikes
        if len(unit.timestamps) < minimumSpikeCount:
            p, tLatency = np.nan, np.nan

        #
        else:
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
        
        #
        result = np.array([unit.index, p, tLatency])
        session.save(f'zeta/optostim/p', result[1])
        session.save(f'zeta/optostim/latency', result[2])
    return
