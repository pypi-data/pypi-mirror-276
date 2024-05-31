import os
from pathlib import Path
import json

def get_conda_licenses():
    """Find which licenses conda know about."""
    licenses = {}
    
    for meta_file in Path(os.path.expandvars("$CONDA_PREFIX/conda-meta")).glob("*.json"):
        with open(meta_file) as json_file:
            meta_data = json.load(json_file)
        
        direct_licenses = []
        modules = []
        
        for file in meta_data['files']:
            file = Path(file)
            if "licenses" in file.parents:
                direct_licenses.append(file)
            
            elif file.name == "__init__.py" or ".so" in file.suffixes:
                modules.append(file)
        
        for module in modules:
            found = list(Path(meta_data['extracted_package_dir']).glob("info/licenses/**/LICENSE"))
            found.extend(direct_licenses)
            
            if len(found) > 0:
                licenses[module] = found
    
    return licenses

conda_licenses = get_conda_licenses()

def find_licenses(module, module_path):
    """Find licenses for a given python module."""
    # Can we see any licenses?
    module_path = Path(module_path)
    module_name = Path(module)
    
    # Only worry about the main module
    if module_path.name != "__init__.py" and ".so" not in module_name.suffixes:
        return []
    
    licenses = []
    
    # Add any license found loose in the code.
    licenses.extend(module_path.parent.glob("LICENSE*"))
    licenses.extend(module_path.parent.glob("COPYING*"))
    
    # For the top-level module, have a look in the dist-info dir.
    module_bits = module.split(".")
    if ".py" in module_name.suffixes or ".so" in module_name.suffixes or len(module_bits) == 1:
        # Try and find a dist_info folder.
        dir_name = module_path.parent.name
        dist_dir = list(module_path.parent.parent.glob(dir_name + '-*.dist-info'))
        if len(dist_dir) == 1:
            licenses.extend(dist_dir[0].glob("LICENSE*"))
            licenses.extend(dist_dir[0].glob("COPYING*"))
            licenses.extend(dist_dir[0].glob("licenses/*"))
        
        if len(licenses) == 0:
            # Some conda packages store their licenses in a special conda location (I don't know why).
            # First, we need to try and dig out the conda-specifc metadata file for this package.
            try:
                look_for = module_path.relative_to(os.path.expandvars("$CONDA_PREFIX"))
                licenses.extend(conda_licenses.get(look_for, []))
            
            except Exception:
                # Not a conda package.
                pass
            
#             exit()
#             conda_meta = Path(os.path.expandvars("$CONDA_PREFIX/conda-meta"))
#             meta_file = list(conda_meta.glob(dir_name + '-*.json'))
#             if len(meta_file) > 0:
#                 with open(meta_file[0]) as meta_file:
#                     module_meta = json.load(meta_file)
#                 licenses.extend(Path(module_meta['extracted_package_dir']).glob("info/licenses/**/LICENSE"))
    
        # If we still can't find anything, we may be importing a local dev copy.
        # Have a look one folder up.
        if len(licenses) == 0:
            licenses.extend(module_path.parent.parent.glob("LICENSE*"))
            licenses.extend(module_path.parent.parent.glob("COPYING*"))
    
    return [license for license in licenses if license.is_file()]