Use a virtual environment to run the provided scripts.

Create a virtual environment with `python -m venv .venv`.

Activate the venv with `source .venv/bin/activate`, then run `pip install -r requirements.txt`.

`apple_download.py` will populate an `apple` directory with all the pdfs necessary for the analysis, and `apple_parse_carbon.py` will output `apple.csv` into the `out` directory with filenames in one column and carbon footprints in kg in another.
