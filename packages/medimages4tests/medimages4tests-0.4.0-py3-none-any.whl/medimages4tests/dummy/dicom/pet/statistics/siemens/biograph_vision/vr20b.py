from copy import copy
from medimages4tests.dummy.dicom.base import (
   generate_dicom, default_dicom_dir, evolve_header
)


def get_image(out_dir=default_dicom_dir(__file__), **kwargs):
    hdr = evolve_header(constant_hdr, **kwargs)
    return generate_dicom(out_dir, num_vols, hdr,
                          collated_data, varying_hdr)


num_vols = 3


constant_hdr = {
    "00080005": {
        "vr": "CS",
        "Value": [
            "ISO_IR 100"
        ]
    },
    "00080008": {
        "vr": "CS",
        "Value": [
            "DERIVED",
            "SECONDARY",
            "OTHER"
        ]
    },
    "00080016": {
        "vr": "UI",
        "Value": [
            "1.2.840.10008.5.1.4.1.1.7"
        ]
    },
    "00080020": {
        "vr": "DA",
        "Value": [
            "20230825"
        ]
    },
    "00080021": {
        "vr": "DA",
        "Value": [
            "20230825"
        ]
    },
    "00080023": {
        "vr": "DA",
        "Value": [
            "20230825"
        ]
    },
    "00080030": {
        "vr": "TM",
        "Value": [
            "144927.519000"
        ]
    },
    "00080031": {
        "vr": "TM",
        "Value": [
            "152520.212000"
        ]
    },
    "00080050": {
        "vr": "SH",
        "Value": [
            "987654321"
        ]
    },
    "00080060": {
        "vr": "CS",
        "Value": [
            "PT"
        ]
    },
    "00080064": {
        "vr": "CS",
        "Value": [
            "DRW"
        ]
    },
    "00080070": {
        "vr": "LO",
        "Value": [
            "SIEMENS"
        ]
    },
    "00080090": {
        "vr": "PN",
        "Value": [
            {
                "Alphabetic": "University"
            }
        ]
    },
    "00081030": {
        "vr": "LO",
        "Value": [
            "Researcher^Project"
        ]
    },
    "0008103E": {
        "vr": "LO",
        "Value": [
            "PET Statistics"
        ]
    },
    "00081080": {
        "vr": "LO",
        "Value": [
            "Physics"
        ]
    },
    "00100010": {
        "vr": "PN",
        "Value": [
            {
                "Alphabetic": "Session Identifier"
            }
        ]
    },
    "00100020": {
        "vr": "LO",
        "Value": [
            "Session Label"
        ]
    },
    "00100030": {
        "vr": "DA",
        "Value": [
            "19800228"
        ]
    },
    "00100040": {
        "vr": "CS",
        "Value": [
            "M"
        ]
    },
    "00101010": {
        "vr": "AS",
        "Value": [
            "043Y"
        ]
    },
    "00101020": {
        "vr": "DS",
        "Value": [
            1.8
        ]
    },
    "00101030": {
        "vr": "DS",
        "Value": [
            75.0
        ]
    },
    "00181012": {
        "vr": "DA",
        "Value": [
            "20230825"
        ]
    },
    "00181016": {
        "vr": "LO",
        "Value": [
            "SIEMENS"
        ]
    },
    "0020000D": {
        "vr": "UI",
        "Value": [
            "1.3.12.2.1107.5.1.4.10016.30000023082422093565300000019"
        ]
    },
    "0020000E": {
        "vr": "UI",
        "Value": [
            "1.3.12.2.1107.5.1.4.10016.30000023082422251027100000102"
        ]
    },
    "00200010": {
        "vr": "SH",
        "Value": [
            "PROJECT_ID"
        ]
    },
    "00200011": {
        "vr": "IS",
        "Value": [
            6
        ]
    },
    "00200020": {
        "vr": "CS"
    },
    "00280002": {
        "vr": "US",
        "Value": [
            1
        ]
    },
    "00280004": {
        "vr": "CS",
        "Value": [
            "MONOCHROME2"
        ]
    },
    "00280010": {
        "vr": "US",
        "Value": [
            512
        ]
    },
    "00280011": {
        "vr": "US",
        "Value": [
            512
        ]
    },
    "00280100": {
        "vr": "US",
        "Value": [
            16
        ]
    },
    "00280101": {
        "vr": "US",
        "Value": [
            12
        ]
    },
    "00280102": {
        "vr": "US",
        "Value": [
            11
        ]
    },
    "00280103": {
        "vr": "US",
        "Value": [
            0
        ]
    },
    "00281050": {
        "vr": "DS",
        "Value": [
            2048.0
        ]
    },
    "00281051": {
        "vr": "DS",
        "Value": [
            512.0
        ]
    },
    "00281052": {
        "vr": "DS",
        "Value": [
            0.0
        ]
    },
    "00281053": {
        "vr": "DS",
        "Value": [
            1.0
        ]
    },
    "00281054": {
        "vr": "LO",
        "Value": [
            "US"
        ]
    },
    "00290010": {
        "vr": "LO",
        "Value": [
            "SIEMENS MEDCOM OOG"
        ]
    },
    "00291008": {
        "vr": "CS",
        "Value": [
            "MEDCOM OOG 2"
        ]
    },
    "00291009": {
        "vr": "LO",
        "Value": [
            "0103 syngo VZ20A"
        ]
    },
    "60000010": {
        "vr": "US",
        "Value": [
            512
        ]
    },
    "60000011": {
        "vr": "US",
        "Value": [
            512
        ]
    },
    "60000015": {
        "vr": "IS",
        "Value": [
            1
        ]
    },
    "60000022": {
        "vr": "LO",
        "Value": [
            "Siemens MedCom Object Graphics"
        ]
    },
    "60000040": {
        "vr": "CS",
        "Value": [
            "G"
        ]
    },
    "60000050": {
        "vr": "SS",
        "Value": [
            1,
            1
        ]
    },
    "60000051": {
        "vr": "US",
        "Value": [
            1
        ]
    },
    "60000100": {
        "vr": "US",
        "Value": [
            1
        ]
    },
    "60000102": {
        "vr": "US",
        "Value": [
            0
        ]
    },
    "00104000": {
        "vr": "LT",
        "Value": [
            "Patient comments string"
        ]
    },
    "00081048": {
        "vr": "PN",
        "Value": [
            {
                "Alphabetic": "Some Phenotype"
            }
        ]
    },
    "00080081": {
        "vr": "ST",
        "Value": [
            "Address of said institute"
        ]
    },
    "00080080": {
        "vr": "LO",
        "Value": [
            "An institute"
        ]
    }
}


varying_hdr = {"00080018": {"0": {"vr": "UI", "Value": ["1.3.12.2.1107.5.1.4.10016.30000023082422251027100000103"]}, "1": {"vr": "UI", "Value": ["1.3.12.2.1107.5.1.4.10016.30000023082422251027100000104"]}, "2": {"vr": "UI", "Value": ["1.3.12.2.1107.5.1.4.10016.30000023082422251027100000105"]}}, "00080033": {"0": {"vr": "TM", "Value": ["152520.395000"]}, "1": {"vr": "TM", "Value": ["153123.225000"]}, "2": {"vr": "TM", "Value": ["153236.963000"]}}, "00181014": {"0": {"vr": "TM", "Value": ["152520.395000"]}, "1": {"vr": "TM", "Value": ["153123.225000"]}, "2": {"vr": "TM", "Value": ["153236.963000"]}}, "00200013": {"0": {"vr": "IS", "Value": [2000]}, "1": {"vr": "IS", "Value": [2002]}, "2": {"vr": "IS", "Value": [2002]}}, "00204000": {"0": {"vr": "LT", "Value": ["PET Count Rate Statistics"]}, "1": {"vr": "LT", "Value": ["PET PET SWB Uncorrected Reconstruction Parameters"]}, "2": {"vr": "LT", "Value": ["PET PET SWB 8MIN Reconstruction Parameters"]}}}


collated_data = {"00291010": {"0": {"vr": "OB", "BinaryLength": 25132}, "1": {"vr": "OB", "BinaryLength": 31944}, "2": {"vr": "OB", "BinaryLength": 33636}}, "60003000": {"0": {"vr": "OW", "BinaryLength": 43692}, "1": {"vr": "OW", "BinaryLength": 43692}, "2": {"vr": "OW", "BinaryLength": 43692}}, "7FE00010": {"0": {"vr": "OW", "BinaryLength": 699052}, "1": {"vr": "OW", "BinaryLength": 699052}, "2": {"vr": "OW", "BinaryLength": 699052}}}


