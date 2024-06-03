import tempfile
from pathlib import Path
import gemmi
import density_calculator
import pytest


@pytest.fixture(scope='session')
def data_base_path():
    return Path(__file__).parent / "test_data" / "5d5w"


def test_calculate(data_base_path):

    mtz = gemmi.read_mtz_file(str(data_base_path / "5D5W-sf.mtz"))
    st = gemmi.read_structure(str(data_base_path / "5D5W-NA-removed.pdb"))

    difference_mtz = density_calculator.calculate(st, mtz, ["FP", "SIGFP"])
    difference_map = difference_mtz.transform_f_phi_to_map("DELFWT", "PHDELWT")




