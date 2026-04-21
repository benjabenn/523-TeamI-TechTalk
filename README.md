Use a virtual environment to run the provided scripts.

Create a virtual environment with `python -m venv .venv`.

Activate the venv with `source .venv/bin/activate`, then run `pip install -r requirements.txt`.

`apple_download.py` will populate an `apple` directory with all the pdfs necessary for the analysis, and `apple_parse_carbon.py` will output `apple.csv` into the `out` directory with filenames in one column and carbon footprints in kg in another.

`apple_rag_carbon.py` will retrieve the data for `apple/14-inch_MacBook_Pro_PER_Oct2023.pdf`, so make sure to run `apple_download.py` first.

Methodology and Code References from: 
Zhao, K., Balaji, B., & Lee, S. (2025). CF-RAG: A Dataset and Method for Carbon Footprint QA Using Retrieval-Augmented Generation. arXiv [Cs.CL]. Retrieved from http://arxiv.org/abs/2508.03489
