def get_versions():
    return versions[0]["number"]

versions = [
    {
        "number": "0.0.4",
        "features": [
            "1. move from toolbiox to yxtools",
        ],
    },
    {
        "number": "0.0.3",
        "features": [
            "1. There seems to be a lot of errors in GeneSys with the label of whether Accession is Landraces or not, removed that part of the information from genesys.py.",
        ],
    },
    {
        "number": "0.0.2",
        "features": [
            "1. added merge function.",
        ],
    },
    {
        "number": "0.0.1",
        "features": [
            "1. initial version.",
        ],
    },
]