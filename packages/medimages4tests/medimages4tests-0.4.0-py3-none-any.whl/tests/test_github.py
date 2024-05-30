import pytest
import nibabel as nb
import numpy as np
from medimages4tests.utils import retrieve_from_github


@pytest.mark.xfail
def test_github_retrieve():

    nifti_fpath = retrieve_from_github(
        org="nipype", repo="pydra-fsl-testdata", path="melodic_ica"
    )
    nifti = nifti = nb.load(nifti_fpath)

    assert np.array_equal(nifti.header["dim"][:4], [3, 204, 256, 256])
