"""
Class to load and handle binary data.
This could be electron density data or numpy data.
They feature header info followed by the boinary data.
"""

from abc import ABC, abstractmethod


####################################################################################
class BinaryFile(ABC):
    """Abstract class to various formats of binary data"""

    def __init__(self, filedata, header):
        self.filedata = filedata
        self.header = header

    @abstractmethod
    def load(self):
        pass


####################################################################################
class NumpyBinary(BinaryFile):
    """
    Features binray data in the format:
    https://numpy.org/doc/1.13/neps/npy-format.html
    """

    def load(self):
        """Load the numpy data"""
        # for i in range
        # val = int.from_bytes(ccp4_binary[i:i+inc], byteorder='little', signed=True)
