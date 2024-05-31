"""Test the oprattle program."""

import subprocess
from pathlib import Path

import pytest

from test import DATA


def run(signature):
    """Run a program."""

    proc = subprocess.run(
        signature,
        capture_output = True
    )

    if proc.returncode != 0:
        # Something has gone wrong.
        raise Exception("Command execution failed with retcode '{}', STDERR: {}".format(proc.returncode, proc.stderr))

    return proc


@pytest.mark.parametrize("input_file_type, backend", [
    ["cml", None],
    ["cml", "Pybel"],
    ["cml", "Obabel"],
    ["xyz", None],
    ["xyz", "Pybel"],
    ["xyz", "Obabel"],
    ["cdx", None],
    ["cdx", "Obabel"],
    # CDX cannot be converted with pybel
])
def test_conversion(input_file_type, backend, tmp_path):
    """Test simple file conversion."""
    
    input_file_path = Path(DATA, "Benzene." + input_file_type)
    output_file_path = Path(tmp_path, "Benzene.xyz")

    signature = [
        "oprattle",
        "{}".format(input_file_path),
        "-O", "{}".format(output_file_path)
    ]

    if backend:
        signature.extend([
            "--backend",
            backend
        ])

    run(signature)

@pytest.mark.parametrize("format_type", ["readable", "writable"])
@pytest.mark.parametrize("backend", [None, "Pybel", "Obabel"])
def test_formats(format_type, backend):
    """Test printing of supported formats."""

    signature = [
        "oprattle",
        "--{}".format(format_type)
    ]

    if backend:
        signature.extend([
            "--backend",
            backend
        ])

    run(signature)

@pytest.mark.parametrize("input_file_type", ["cml", "xyz", "cdx"])
def test_gen3d(input_file_type):
    first = run([
        "oprattle",
        str(Path(DATA, "Benzene.{}".format(input_file_type))),
        "-o", "xyz",
        "--gen3D", "False"
    ]).stdout

    same = run([
        "oprattle",
        str(Path(DATA, "Benzene.{}".format(input_file_type))),
        "-o", "xyz",
        "--gen3D", "False"
    ]).stdout
    different = run([
        "oprattle",
        str(Path(DATA, "Benzene.{}".format(input_file_type))),
        "-o", "xyz",
        "--gen3D", "True"
    ]).stdout

    assert first == same
    assert first != different