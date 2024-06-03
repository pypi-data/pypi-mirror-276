import sys
import os
import inspect
from pathlib import Path
from os.path import dirname, abspath

sys.path.append(os.path.join(os.path.dirname(Path(__file__).parent), ""))
sys.path.append(os.path.join(os.path.dirname(Path(__file__).parent.parent), ""))
sys.path.append(os.path.join(os.path.dirname(Path(__file__).parent.parent), "squice"))
sys.path.append(os.path.join(os.path.dirname(Path(__file__).parent.parent.parent), ""))
from squice import DataLoaders as dl  # noqa: E402
from squice import MtxInterpolator as mi  # noqa: E402
from squice import GridMaker as gm  # noqa: E402
from squice import SpaceTransform as sp  # noqa: E402


DIR = dirname(abspath(__file__))
print(DIR)


# ---------------------------------------------------------------------------
def test_slice_screen():
    mtx_txt = """[[[0,0,0],[0,3,0],[0,0,0]],
        [[0,0,0],[3,5,0],[0,0,0]],
        [[0,0,0],[0,0,1],[0,0,0]]]
        """
    MY_MTX = dl.NumpyNow(mtx_txt)
    MY_MTX.load()

    interp_methods = []
    interp_methods.append("nearest")
    # interp_methods.append("linear")

    clp = []
    clp.append(("(1.0, 1.0, 1.0)", "(2.0, 1.0, 1.0)", "(1.0, 2.0, 1.0)"))
    # clp.append(("(1.0, 1.0, 1.0)", "(1.8091,0.4122,1.0)", "(1.5878,1.8091,1.0)"))
    width_samples = []
    width_samples.append((2, 3))
    # width_samples.append((5,4))

    for interp_method in interp_methods:
        if interp_method == "linear":
            interp_none = mi.Linear(MY_MTX.mtx, wrap="none")
            interp_periodic = mi.Linear(MY_MTX.mtx, wrap="periodic")
        else:
            interp_none = mi.Nearest(MY_MTX.mtx, wrap="none")
            interp_periodic = mi.Nearest(MY_MTX.mtx, wrap="periodic")
        for central, linear, planar in clp:
            for width, samples in width_samples:
                spc = sp.SpaceTransform(central, linear, planar)
                grid = gm.GridMaker()
                print("The unit slice is")
                slice_grid = grid.get_unit_grid(width, samples)
                print(f"{slice_grid}")

                print("Which converts to")
                xyz_coords = spc.convert_coords(slice_grid)
                print(f"{xyz_coords}")

                print("With vals")
                vals = interp_none.get_val_slice(xyz_coords)[:, :, 0]
                print(f"{vals}")

                print("With vals periodic")
                vals_p = interp_periodic.get_val_slice(xyz_coords)[:, :, 0]
                print(f"{vals_p}")

                # test vals
                _000 = xyz_coords.matrix[2][2][0]
                print(_000)
                x, y, z = _000.A, _000.B, _000.C
                v = interp_none.get_value(x, y, z)
                print(x, y, z, v)

                # test vals
                _000 = xyz_coords.matrix[2][2][0]
                print(_000)
                x, y, z = _000.A, _000.B, _000.C
                vp = interp_periodic.get_value(x, y, z)
                print(x, y, z, vp)

                # assert v == vp, "Vals and periodic vals should be the same"


def test_slice():
    print(f"Testing utility: {inspect.stack()[0][3]}")
    # matrix data
    npf = dl.NumpyNow("[[[1,2], [3,4]], [[5,6], [7,8]]]")
    npf.load()

    # interpolator
    interp = mi.Nearest(npf.mtx)

    # unit grid
    grid = gm.GridMaker()
    slice_grid = grid.get_unit_grid(1, 2)
    print(slice_grid.matrix)
    print(slice_grid.shape())

    # space transformer
    spc = sp.SpaceTransform("(0.5,0.5,0.5)", (0, 0.5, 0), (0.5, 0, 0))
    xyz_coords = spc.convert_coords(slice_grid)

    # get all vals from interpolator
    vals = interp.get_val_slice(xyz_coords)
    print(vals)
    print(vals[:, :, 0])


def test_slice_periodic():
    print(f"Testing utility: {inspect.stack()[0][3]}")
    # matrix data
    npf = dl.NumpyNow("[[[1,2], [3,4]], [[5,6], [7,8]]]")
    npf.load()

    # interpolator
    interp = mi.Linear(npf.mtx, wrap="periodic")

    # unit grid
    grid = gm.GridMaker()
    slice_grid = grid.get_unit_grid(2, 2)
    print(slice_grid)
    print(slice_grid.shape())

    # space transformer
    spc = sp.SpaceTransform("(0.5,0.5,0.5)", (0, 0.5, 0), (0.5, 0, 0))
    xyz_coords = spc.convert_coords(slice_grid)

    # get all vals from interpolator
    vals = interp.get_val_slice(xyz_coords)
    print(vals)


###########################################################################
if __name__ == "__main__":
    test_slice_screen()
    # test_slice()
    # test_slice_periodic()
