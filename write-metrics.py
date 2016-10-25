""" Write outlier estimates for each group

The script will:

* for each project:

    * validate the group dataset using validate_data.py script;
    * for each groupset:

        * run outlier detection using current project algorithm;
        * run outlier detection assessment metrics on this outlier detection.

See the ``fmri-designs`` package for the outlier detection metrics.
"""

from os.path import join as pjoin, abspath
from subprocess import run

from fmri_designs.metrics import print_metrics

PYTHON = 'python3'
PROJECT_DIRS = [abspath('diagnostics-{:02d}'.format(group))
                for group in range(3)]
DATA_DIRS = [pjoin(project_dir, 'data') for project_dir in PROJECT_DIRS]
COND_PATH = abspath('condition_files')
TR = 3.0


for project_no, project_dir in enumerate(PROJECT_DIRS):
    validate_script = pjoin(project_dir, 'scripts', 'validate_data.py')
    outlier_script = pjoin(project_dir, 'scripts', 'find_outliers.py')
    print('Validating data for group {}'.format(project_no))
    run([PYTHON, validate_script, 'data'], cwd=project_dir)
    for data_no, data_dir in enumerate(DATA_DIRS):
        out_fname = '{:02d}_outliers_for_{:02d}.txt'.format(
            project_no, data_no)
        print("Writing", out_fname)
        with open(out_fname, 'wt') as fobj:
            # Run outlier detection script, writing output to "out_fname".
            run([PYTHON, outlier_script, data_dir], cwd=project_dir,
                stdout=fobj)
        print("Measures for project {} detector on group {} data".
              format(project_no, data_no))
        print_metrics(out_fname, data_dir, COND_PATH, TR, data_no)
