# Development Guide

To run the non-packaged sources locally, execute `python -m neno` from this directory.

To package the sources, install PyPA's `build`: `python3 -m pip install --upgrade build` and execute `python3 -m build` from the project root directory.
The built package will be located in the `dist/` directory.
To upload the newly built package, install twine `python3 -m pip install --upgrade twine` and then run `python3 -m twine upload --repository testpypi dist/*`.
