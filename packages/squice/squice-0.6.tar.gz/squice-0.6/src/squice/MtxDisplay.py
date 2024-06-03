"""
Module to interpolate inside a numpy matrix with some bespoke methods
"""


####################################################################################
class MtxDisplay:
    """Class to display a numpy matrix in the simplest way as 3d data"""

    def __init__(self, mtx):
        self.mtx = mtx
