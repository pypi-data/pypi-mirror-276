from pathlib import Path
from medimages4tests import base_cache_dir
from medimages4tests.utils import retrieve_from_openneuro, OpenneuroSpec


cache_dir = base_cache_dir / "mri" / "neuro" / "t1w"


SAMPLES = {
    "ds004024-CON031": OpenneuroSpec(
        dataset="ds004024",
        tag="1.0.1",
        path="sub-CON031/ses-mri/dwi/sub-CON031_ses-mri_dwi",
    )
}


def get_image(out_dir: Path = None, sample: str = "ds004024-CON031"):
    if out_dir is None:
        out_dir = cache_dir / sample
    return retrieve_from_openneuro(
        SAMPLES[sample], out_dir, suffixes=(".nii.gz", ".json", ".bvec", ".bval")
    )
