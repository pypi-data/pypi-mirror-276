# Description
[PyPi Page](https://pypi.org/project/WGSE-NG-3rd-party/)

This repository build a wheel that is used to distribute 3rd party executables used by WGSE-NG on Windows.

The executables are contained in a zip folder distributed as a release artifact for this project (to not check-in the binaries). The setup.py here is just to download that archive and build a wheel with it.
Once installed, this package will be available with `import wgse.third_party` but it doesn't offer any feature as there isn't any python code inside. The package is used to discover the executables through its location on disk.

## Make a new release
```batch
git clone https://github.com/WGSE-NG/External
cd External
rem Remember to bump the version inside setup.py
python -m build
rmdir /s /q WGSE_NG_3rd_party.egg-info & rmdir /s /q dist & python -m build
rem Upload (for testing)
python3 -m twine upload --repository testpypi dist/*
rem Upload (prod)
python3 -m twine upload --repository pypi dist/*
```

## Install (prod)
```batch
python -m pip install WGSE-NG-3rd-party
```

## Example usage
```python
from wgse import third_party
from pathlib import Path
from subprocess import Popen
folder = Path(third_party.__file__).parent
# Launch something, e.g., bcftools
Popen(folder.joinpath("bcftools.exe"))
```

## Latest release Content

Tools | Version
------|--------
fastp | v0.21.0
minimap2 | 
htslib suite (tabix, bcftools, htsfile, samtools, bgzip) | v1.15.1
bwa |0.7.17-r1198-dirty
haplogrep |v2.4.0
