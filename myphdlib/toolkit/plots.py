import matplotlib.pyplot as plt

def plotPCA3D(pcs, trial_types, dimensions, stimIndex):
    """
    Takes PCA output & plots it in 3D
    """
    ax = plt.figure().add_subplot(projection='3d')
    ax.plot(pcs[dimensions[0],:, 0], pcs[dimensions[1],:, 0], pcs[dimensions[2],:, 0], color='deepskyblue', label=trial_types[0])
    ax.plot(pcs[dimensions[0],:, 1], pcs[dimensions[1],:, 1], pcs[dimensions[2],:, 1], color='magenta', label=trial_types[1])
    ax.plot(pcs[dimensions[0],stimIndex, 1], pcs[dimensions[1],stimIndex, 1], pcs[dimensions[2],stimIndex, 1], color='magenta', marker='o')
    ax.plot(pcs[dimensions[0],stimIndex, 0], pcs[dimensions[1],stimIndex, 0], pcs[dimensions[2],stimIndex, 0], color='deepskyblue', marker='o')
    ax.plot(pcs[dimensions[0],0, 0], pcs[dimensions[1],0, 0], pcs[dimensions[2],0, 0], color='k', marker='o')
    ax.plot(pcs[dimensions[0],0, 1], pcs[dimensions[1],0, 1], pcs[dimensions[2],0, 1], color='k', marker='o')

    ax.set_xlabel('PC' + str(dimensions[0]))
    ax.set_ylabel('PC' + str(dimensions[1]))
    ax.set_zlabel('PC' + str(dimensions[2]))
    ax.legend()
    return ax