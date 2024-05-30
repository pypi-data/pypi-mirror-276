from pathlib import Path
from medimages4tests import base_cache_dir
from medimages4tests.utils import retrieve_from_openneuro, OpenneuroSpec


cache_dir = base_cache_dir / "mri" / "neuro" / "t1w"


SAMPLES = {
    "ds004130-ON01016": OpenneuroSpec(
        dataset="ds004130",
        tag="1.0.0",
        path="sub-ON01016/anat/sub-ON01016_acq-fspgr_run-01_T1w",
    ),
    "ds002014-01": OpenneuroSpec(
        dataset="ds002014",
        tag="1.0.1",
        path="sub-01/anat/sub-01_T1w",
    ),
    "ds001743-01": OpenneuroSpec(
        dataset="ds001743",
        tag="1.0.1",
        path="sub-01/anat/sub-01_T1w",
    ),
    "ds004024-CON031": OpenneuroSpec(
        dataset="ds004024",
        tag="1.0.1",
        path="sub-CON031/ses-mri/dwi/sub-CON031_ses-mri_T1w",
    ),
}


def get_image(out_dir: Path = None, sample: str = "ds004130-ON01016"):
    if out_dir is None:
        out_dir = cache_dir / sample
    return retrieve_from_openneuro(SAMPLES[sample], out_dir)
