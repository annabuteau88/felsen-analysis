class AnalysisObject():
    """
    This class is used in the background of the toolkit modules. 
    It has helper properties to make the code more readable & writeable.
    """
    def load(self, h5file, path):
        """
        This is a helper function for easily loading h5 files
        """
        obj = None
        with h5py.File(str(h5file), 'r') as file:
            try:
                obj = file[path]
                if type(obj) == h5py.Dataset:
                    if returnMetadata:
                        return np.array(obj), dict(obj.attrs)
                    else:
                        return np.array(obj)
                elif type(obj) == h5py.Group:
                    return obj
            except KeyError:
                pass
        
