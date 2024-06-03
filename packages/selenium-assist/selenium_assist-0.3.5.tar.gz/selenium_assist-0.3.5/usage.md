# Update code and publish
- increment version in `setup.py`
- update download_url in `setup.py`
- commit and push to GitHub
- create a new [release](https://github.com/ivanmicetic/selenium-assist/releases) on GitHub (and verify download link in `setup.py`)
- remove the old package:
  ```sh
  rm -rf dist *.egg-info
  ```
- create a source distribution:
  ```sh
  ~/miniconda3/condabin/conda run -n planet-time python setup.py sdist
  ```
- upload to pypi (im; 7zCwexQL#etpA5c):
  ```sh
  ~/miniconda3/envs/planet-time/bin/twine upload dist/*
  ```
# package with pyproject.toml
Install build tools:
```sh
pip install --upgrade build
```

Generate distribution package:
```sh
rm -rf dist src/*.egg-info
python3 -m build
```

Install Twine for PyPI upload:
```sh
pip install --upgrade twine
```

Upload to PyPI (creds in .pypirc):
```sh
python3 -m twine upload --repository pypi dist/*
```
 

