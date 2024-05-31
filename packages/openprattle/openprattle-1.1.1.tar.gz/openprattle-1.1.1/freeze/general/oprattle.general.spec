# -*- mode: python ; coding: utf-8 -*-

import sys
import itertools
from pathlib import Path
sys.path.insert(0,str(Path("../").resolve()))
from collect_licenses import find_licenses

datas = []

# Add openbabel data.
datas.append((Path(os.environ['CONDA_PREFIX'], "share/openbabel/3.1.0/"), "openbabel/data/3.1.0"))

# Now add extra binary libraries that we need.
binaries = [
    (Path(os.environ['CONDA_PREFIX'], "lib/openbabel/3.1.0/"), "openbabel/lib/3.1.0"),
    # TODO: Do we still need this?
    (Path(os.environ['CONDA_PREFIX'], "lib/libinchi.so.0"), ".")
]

script = "../../bin/oprattle"
prog_name = "oprattle"
package_name = os.environ['BUILD_TARGET']
# Modules to include in source form:
src_modules = []

a = Analysis([script],
     pathex=["../../"],
     binaries=binaries,
     datas=datas,
     hiddenimports=[],
     hookspath=[],
     module_collection_mode = {mod: 'py' for mod in src_modules},
     runtime_hooks=[],
     excludes=['tkinter', '_tkinter'],
     win_no_prefer_redirects=False,
     win_private_assemblies=False,
     cipher=None,
     noarchive=False
)

# Collect licenses.
new_datas = []
for module, module_path, module_type in itertools.chain(a.pure, a.binaries, a.datas):
    license_files = find_licenses(module, module_path)
    for license_file in license_files:
        file_name = license_file.name
        dest_module = module
        new_datas.append((f'LICENSES/{dest_module}/{file_name}', license_file, 'DATA'))

a.datas.extend(new_datas)

pyz = PYZ(a.pure, a.zipped_data,
     cipher=None
)

exe = EXE(pyz,
     a.scripts,
     [],
     exclude_binaries=True,
     name=prog_name,
     debug=False,
     bootloader_ignore_signals=False,
     strip=False,
     upx=True,
     console=True
)

import openprattle
coll = COLLECT(exe,
     a.binaries,
     a.zipfiles,
     a.datas,
     strip=False,
     upx=True,
     upx_exclude=[],
     name="{}.{}.{}".format("openprattle", openprattle.__version__, package_name)
)
