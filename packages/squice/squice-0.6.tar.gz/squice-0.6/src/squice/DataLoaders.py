"""
Module to load different data fromats from file and convert into a numpy matrix
"""

from abc import ABC, abstractmethod
import numpy as np


####################################################################################
class DataLoader(ABC):
    """Abstract class to load data from file and convert to a numpy matrix"""

    def __init__(self, filedata):
        self.filedata = filedata
        self.mtx = None

    @abstractmethod
    def load(self):
        pass


####################################################################################
class NumpyNow(DataLoader):
    """
    Class to create a numpy matrix inline.
    The format of the uploaded data is
    (note the commas are the delim,sapce is for visuals)
    [[[1,2,3],
    [4, 5, 6]],

    [[7,  8,  9],
    [10, 11, 12]]]
    self.mtx = np.fromstring('1,2,3,4,5,6,7,8,9,10,11,12',
    dtype=int, sep=',').reshape([2,2,3])

    [[[1, 2],
    [3, 4],
    [5, 6]],

    [[7, 8],
    [9, 10],
    [11, 12]]]
    self.mtx = np.fromstring('1,2,3,4,5,6,7,8,9,10,11,12',
    dtype=int, sep=',').reshape([2,3,2])

    [[[1, 2],
    [3, 4]],

    [[5, 6],
    [7, 8]],

    [[9, 10],
    [11, 12]]]
    self.mtx = np.fromstring('1,2,3,4,5,6,7,8,9,10,11,12',
    dtype=int, sep=',').reshape([3,2,2])

    """

    def load(self):
        """
        Load the numpy data from a formatted string of 3d data that
        must pass the checks for [[[1,2],[3,4]],[[5,6],[7,8]]]"""

        # There must be the same number of [ as ]
        assert self.filedata.count("[") == self.filedata.count("]")
        self.filedata = self.filedata.strip().replace(" ", "")
        self.filedata = self.filedata.replace("\t", "")
        self.filedata = self.filedata.replace("\n", "")
        assert self.filedata[:3] == "[[["
        assert self.filedata[-3:] == "]]]"
        self.filedata = self.filedata.replace(" ", "")
        vec_slicea = self.filedata.split("]],[[")
        vec_slicesb = []
        for vs in vec_slicea:
            vss = vs.split("],[")
            v = []
            for vsss in vss:
                strv = vsss.replace("]", "").replace("[", "")
                v.append(strv)
            vec_slicesb.append(v)
        self.numa = len(vec_slicesb)
        self.numb = len(vec_slicesb[0])
        self.filedata = self.filedata.replace("]", "")
        self.filedata = self.filedata.replace("[", "")
        self.numc = int(len(self.filedata.split(",")) / (self.numa * self.numb))
        self.mtx = np.fromstring(self.filedata, dtype=float, sep=",").reshape(
            [self.numa, self.numb, self.numc]
        )


####################################################################################
class NumpyFile(DataLoader):
    """Class to load a file of numerical data from numpy serislisation format"""

    def load(self):
        """Load the numpy data"""
        self.mtx = np.load(self.filedata)


####################################################################################
class ElectronDensityCcp4(DataLoader):
    """Class to load electron density in the ccp4 format"""

    def load(self):
        """Load the numpy data"""
        self.mtx = None


####################################################################################

if __name__ == "__main__":
    # a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) #shape (3x3)
    # np.save('speed_data.npy', a)
    # npf = NumpyNow("[[[1,2], [3,4]], [[5,6], [7,8]]]")
    # npf = NumpyNow("[[[1,2,0], [3,4,0]], [[5,6,0], [7,8,0]]]")
    npf = NumpyNow("[[[1,2],[3,4],[3,4]], [[5,6],[7,8],[7,8]]]")
    npf = NumpyNow(
        "[[[1,2],[3,4],[3,4]], [[5,6],[7,8],[7,8]], [[5,6],[7,8],[7,8]], [[5,6],[7,8],[7,8]]]"
    )
    npf.load()
