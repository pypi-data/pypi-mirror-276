"""
collect all notebooks in examples, and check that they run without error
"""

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from pathlib import Path
from glob import glob
this_file_loc = Path(__file__).parent

def check_notebook_runs(notebook_loc):

    try:
        with open(notebook_loc) as f:
            nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        ep.preprocess(nb, {'metadata': {'path': Path(notebook_loc).parent}})
        with open(notebook_loc, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
    except Exception as e:
        print(f'failed to run notebook {notebook_loc}: rethrowing exception:')
        raise e

def test_all_notebooks_run():
    # get all notebooks:
    notebooks = glob(str(this_file_loc.parent / 'examples' / '*.ipynb'))
    notebooks_not_to_run = ['IAEA.ipynb']
    for notebook in notebooks:
        if any([nb in notebook for nb in notebooks_not_to_run]):
            continue
        check_notebook_runs(notebook)
