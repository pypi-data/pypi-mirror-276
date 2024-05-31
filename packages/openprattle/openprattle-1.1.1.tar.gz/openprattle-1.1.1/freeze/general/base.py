# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files
import pathlib
import os

datas = []

# Add openbabel data.
datas.append((pathlib.Path(os.environ['CONDA_PREFIX'], "share/openbabel/3.1.0/"), "openbabel/data/3.1.0"))

# Now add extra binary libraries that we need.
binaries = [
    (pathlib.Path(os.environ['CONDA_PREFIX'], "lib/openbabel/3.1.0/"), "openbabel/lib/3.1.0"),
    # TODO: Do we still need this?
    (pathlib.Path(os.environ['CONDA_PREFIX'], "lib/libinchi.so.0"), ".")
]
