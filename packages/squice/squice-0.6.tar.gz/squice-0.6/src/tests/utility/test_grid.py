import sys
import os
import inspect
from pathlib import Path
from os.path import dirname, abspath

sys.path.append(os.path.join(os.path.dirname(Path(__file__).parent), ""))
sys.path.append(os.path.join(os.path.dirname(Path(__file__).parent.parent), ""))
sys.path.append(os.path.join(os.path.dirname(Path(__file__).parent.parent), "squice"))
sys.path.append(os.path.join(os.path.dirname(Path(__file__).parent.parent.parent), ""))
from squice import GridMaker as gm  # noqa: E402


DIR = dirname(abspath(__file__))
print(DIR)


# ---------------------------------------------------------------------------
def test_grid_unit():
    print(f"Testing utility: {inspect.stack()[0][3]}")

    # unit grid
    grid = gm.GridMaker()
    # 2x2 0 samples
    slice_grid = grid.get_unit_grid(2, 2)
    print(slice_grid.matrix)
    print(slice_grid.shape())

    # 2x2 grid points
    slice_grid = grid.get_unit_grid(2, 3)
    print(slice_grid.matrix)
    print(slice_grid.shape())

    # 2x2 lose a point
    try:
        slice_grid = grid.get_unit_grid(1, 2)
        print(slice_grid.matrix)
        print(slice_grid.shape())
        assert True, "Should have failed"
    except Exception as e:
        print("Correctly fails < 2)", e)

    # 3x3 lose a point
    slice_grid = grid.get_unit_grid(3, 6)
    print(slice_grid.matrix)
    print(slice_grid.shape())


###########################################################################
if __name__ == "__main__":
    # test_slice()
    test_grid_unit()
