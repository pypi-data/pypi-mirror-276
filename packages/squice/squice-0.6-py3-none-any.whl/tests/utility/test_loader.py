import sys
import os
import inspect
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(Path(__file__).parent.parent), ""))
from squice import DataLoaders as cc

from os.path import dirname, abspath
import sys

DIR = dirname(abspath(__file__))
print(DIR)


# ---------------------------------------------------------------------------
def test_numpyfile():
    print(f"Testing utility: {inspect.stack()[0][3]}")
    npf = cc.NumpyFile(f"{DIR}/data/data1.npy")
    npf.load()
    print(npf.mtx)
    assert npf.mtx[0][0] == 1, npf.mtx[0][0]
    assert npf.mtx[0][2] == 3, npf.mtx[0][2]
    assert npf.mtx[2][0] == 7, npf.mtx[2][0]
    assert npf.mtx[1][1] == 5, npf.mtx[1][1]
    assert npf.mtx[2][2] == 9, npf.mtx[2][2]


def test_numpyfile3d():
    print(f"Testing utility: {inspect.stack()[0][3]}")
    npf = cc.NumpyFile(f"{DIR}/data/data3d.npy")
    npf.load()
    print(npf.mtx)
    assert npf.mtx[0][0][0] == 1, npf.mtx[0][0][0]


def test_numpynow():
    print(f"Testing utility: {inspect.stack()[0][3]}")
    datas = []
    datas.append("[[[1,2], [3,4]], [[5,6], [7,8]]]")
    datas.append("[[[1,2,0], [3,4,0]], [[5,6,0], [7,8,0]]]")
    datas.append("[[[1,2],[3,4],[3,4]], [[5,6],[7,8],[7,8]]]")
    datas.append(
        "[[[1,2],[3,4],[3,4]], [[5,6],[7,8],[7,8]], [[5,6],[7,8],[7,8]], [[5,6],[7,8],[7,8]]]"
    )

    for dt in datas:
        print(dt)
        npf = cc.NumpyNow(dt)
        npf.load()
        assert npf.mtx[0][0][0] == 1, npf.mtx[0][0][0]


def test_numpynow_tabs_and_lines():
    print(f"Testing utility: {inspect.stack()[0][3]}")
    datas = []
    datas.append(
        "[[[1.0,2],[3,4],[3,4]], \t[[5,6],[7,8],[7,8]], \n[[5,6],[7,8],[7,8]],\t [[5,6],[7,8],[7,8]\n]]"
    )

    for dt in datas:
        print(dt)
        npf = cc.NumpyNow(dt)
        npf.load()
        assert npf.mtx[0][0][0] == 1, npf.mtx[0][0][0]


###########################################################################
if __name__ == "__main__":
    # test_numpyfile()
    # test_numpynow()
    test_numpynow_tabs_and_lines()
