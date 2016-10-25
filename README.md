# Assessing performance of the outliers projects

## Setup

To start, get all the sub-projects with:

    git submodule update --init

You will now have the following directories:

    fmri-designs
    diagnostics-00
    diagnostics-01
    diagnostics-02

To put the code for the project onto the Python path:

    pip3 install --user --editable ./fmri-designs

For each project, copy the project data into the project `data` directory.
From the terminal, that might look something like:

    cd diagostics-00/data
    curl -LO http://nipy.bic.berkeley.edu/psych-214/group00.tar.gz
    tar zxvf group00.tar.gz
    cd ../diagostics-01/data
    curl -LO http://nipy.bic.berkeley.edu/psych-214/group01.tar.gz
    tar zxvf group01.tar.gz
    cd ../diagostics-02/data
    curl -LO http://nipy.bic.berkeley.edu/psych-214/group02.tar.gz
    tar zxvf group02.tar.gz

Run the validate / detect / metrics script with:

    python3 write-metrics.py

I've committed the results of the most recent run of this script.  Check the
outputs of the files `00_outliers_for_01.txt` etc files for the outlier
detection results, where `00`` here is the detection algorithm being used, and
`01` here is the data the algorithm is being used on.

Check `project_metrics.txt` for the metrics generated from these detected
outliers.  For each project algorithm, and each run of all three datasets, you
will see the metrics calculated by the `fmri_designs` module.  Definitions for
the metrics:

* "mean F test within mask" - MFwM - is the mean of all the F test values
  within the brain mask.  I calculated the brain mask with a standard image
  image processing algorithm called Otsu's method (see
  `fmri_designs/f_for_outliers.py` for details;
* "drift model" is a set of 4 regressors modeling the mean signal at each
  voxel, and linear, quadratic and cubic drift in signal over time.  See
  `poly_drift` in `fmri_designs/regressors.py`;
* "HRF model" is a set of 4 neural onset models convolved with a standard SPM
  hemodynamic response function;
* "outlier model" is a set of columns regressing out the effect of the outlier
  scans.  The outlier scans are each modeled by a column of zeros, with a
  single 1 in the row corresponding to the outlier scan;

The F test labeled "outlier" is the F test where the reduced model is the
concatenation of columns of the "HRF model" and "drift model. The full model
is the concatenation of the outlier model with the reduced model.  A high
value for the *outlier* F test implies that removing (regressing out) the
outliers explains a large amount of variance.

The F tests labeled "HRF" have reduced model equal to the *drift model*, and
the full model is the column concatenation of the *drift model* and the *HRF
model*.  A high value means the HRF regressors explain a large amount of
variance, without allowing for outliers.

The "HRF+out" F test has reduced model of the column concatenation of the
*drift model* and the *outlier* model. The full model adds the *HRF model*.  A
high value means the HRF regressors explain a large amount of variance, after
allowing for the outliers.

"HRF+out - HRF" is the difference between the "HRF" F and the "HRF+out" F.  A
positive value suggests that adding the outliers to the reduced model causes
the HRF regressors to do a better job of explaining variance.

In the output:

* "outliers" is the mean F within the brain mask for the *outlier* F test;
* "HRF" is the MFwM for the *HRF* F test;
* "HRF+out" is the MFwM for the *HRF+oust* F test;
* "HRF+out - HRF" is difference between the previous two values.
