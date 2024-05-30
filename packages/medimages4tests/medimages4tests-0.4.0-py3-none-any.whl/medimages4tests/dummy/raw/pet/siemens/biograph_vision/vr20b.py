from pathlib import Path
from tempfile import mkdtemp


raw_data_files = [
    "{last_name}_{first_name}.PT.PET_U_FDG_SWB_LM_(Adult).602.PETCT_SPL.{date_time}.065000.2.0.52858823.ptd",
    "{last_name}_{first_name}.PT.PET_U_FDG_SWB_LM_(Adult).602.PET_CALIBRATION.{date_time}.080000.2.0.52858842.ptd",
    "{last_name}_{first_name}.PT.PET_U_FDG_SWB_LM_(Adult).602.PET_COUNTRATE.{date_time}.083000.2.0.52858872.ptd",
    "{last_name}_{first_name}.PT.PET_U_FDG_SWB_LM_(Adult).602.PET_LISTMODE.{date_time}.080000.2.0.52858858.ptd",
    "{last_name}_{first_name}.PT.PET_U_FDG_SWB_LM_(Adult).603.PET_CALIBRATION.{date_time}.30.115000.2.0.54764603.ptd",
    "{last_name}_{first_name}.PT.PET_U_FDG_SWB_LM_(Adult).603.PET_EM_SINO.{date_time}.30.118000.2.0.54764616.ptd",
    "{last_name}_{first_name}.PT.PET_U_FDG_SWB_LM_(Adult).603.PET_REPLAY_PARAM.{date_time}.30.118000.2.0.54764627.ptd",
]


def get_files(
    out_dir=None,
    first_name="TESTNAME",
    last_name="GePhantom",
    date_time="2023.08.25.15.50.51",
):
    if out_dir is None:
        out_dir = Path(mkdtemp())
    if not out_dir.exists():
        out_dir.mkdir(parents=True)
    fspaths = []
    for fname in raw_data_files:
        fspath = out_dir / fname.format(
            first_name=first_name, last_name=last_name, date_time=date_time
        )
        fspath.write_bytes(f"dummy data for {fname}".encode())
        fspaths.append(fspath)
    return fspaths
