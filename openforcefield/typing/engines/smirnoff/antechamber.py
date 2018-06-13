import os
from distutils.spawn import find_executable
import tempfile
import shutil
import contextlib


ANTECHAMBER_PATH = find_executable("antechamber")
@contextlib.contextmanager
def temporary_directory():
    """Context for safe creation of temporary directories."""
    tmp_dir = tempfile.mkdtemp()
    try:
        yield tmp_dir
    finally:
        shutil.rmtree(tmp_dir)

def charge_mol(sdf_filename, output_filename, charge_model = "bcc"):
    """
    currently only sdf file supported as input and mol2 as output

    https://github.com/choderalab/openmoltools/blob/master/openmoltools/packmol.py
    """
    if ANTECHAMBER_PATH is None:
        raise(IOError("Antechamber not found, cannot run charge_mol()"))

    with temporary_directory() as tmp_dir: #FIXME remove sqm files
        # output_filename = tempfile.mktemp(suffix = ".mol2", dir = tmp_dir)
        os.system("antechamber -i {} -fi sdf -o {} -fo mol2 -pf y -c {}".format(sdf_filename, output_filename, charge_model))
        os.system("rm sqm.*")
    return
