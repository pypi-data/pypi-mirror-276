from pathlib import Path
from medimages4tests import base_cache_dir
from medimages4tests.utils import retrieve_from_openneuro, OpenneuroSpec


cache_dir = base_cache_dir / "mri" / "neuro" / "bold"


SAMPLES = {
    "ds002014-01": OpenneuroSpec(
        dataset="ds002014",
        tag="1.0.1",
        path="sub-01/func/sub-01_task-languageproduction_run-01_bold",
    )
}


def get_image(out_dir: Path = None, sample: str = "ds002014-01"):
    if out_dir is None:
        out_dir = cache_dir / sample
    return retrieve_from_openneuro(SAMPLES[sample], out_dir)
