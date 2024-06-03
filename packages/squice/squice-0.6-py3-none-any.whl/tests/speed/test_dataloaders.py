"""
Test the speed of data loaders
"""

from os.path import dirname, abspath
import sys
import numpy as np

DIR = dirname(abspath(__file__))
sys.path.append((DIR))
print("Loading to path", (DIR))
import help_speed as hs  # noqa: E402
import squice.DataLoaders as dl  # noqa: E402


def make_3d():
    mtx = np.fromstring("1,2,3,4,5,6,7,8", dtype=int, sep=",").reshape([2, 2, 2])
    np.save(f"{DIR}/data/speed_data.npy", mtx)


def test_numpy():
    start = hs.get_start()
    for i in range(hs.get_iterations()):
        if i % 100000 == 0:
            print(f"{i}/{hs.get_iterations()}", "test_numpy")
        dl.NumpyFile(f"{DIR}/data/speed_data.npy")
    total_speed = hs.get_speed(start)
    assert hs.is_it_error("test_numpy", total_speed), f"test_numpy, {total_speed}"
    hs.update_speed("test_numpy", total_speed, start)


if __name__ == "__main__":
    test_numpy()
    # make_3d()
