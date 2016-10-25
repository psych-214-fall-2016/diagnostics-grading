# Assessing performance of the outliers projects

## The metrics

Remember that your job was to find outliers to remove that would improve our
estimation of the activation signal : see [the outliers homework
section](https://bic-berkeley.github.io/psych-214-fall-2016/diagnostics_project.html#outlier-detection-project).

For the impatient - the metrics are in the file
[project_metrics.txt](https://github.com/psych-214-fall-2016/diagnostics-grading/blob/master/project_metrics.txt`).

There you will see our assessments of how well your algorithms did in
assessing outliers (the "outliers" F tests - see below) and how well it did on
improving activation (the "HRF+out - HRF" test - see below).  We've run every
group's algorithm on all three datasets.

Comments and feedback welcome.  Feel free to run the assessment yourself.
We've written the assessment code to be similar to the stuff we've already
taught you, so we believe you should be able to follow it, at least in
outline.

## Setup for reproducing the metrics

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
outputs of the files of form `00_outliers_for_01.txt` etc for the outlier
detection results, where `00` here is the detection algorithm being used, and
`01` here is the data the algorithm is being used on.

Check `project_metrics.txt` for the metrics generated from these detected
outliers.  For each project algorithm, and each run of all three datasets, you
will see the metrics calculated by the `fmri_designs` module.  Definitions for
the metrics:

* "mean F test within mask" - MFwM - is the mean of all the F test values
  within the brain mask.  I calculated the brain mask with a standard image
  image processing algorithm called Otsu's method (see
  `fmri_designs/regressors.py` `f_for_outliers` function for details;
* "drift model" is a set of 4 regressors modeling the mean signal at each
  voxel, and linear, quadratic and cubic drift in signal over time.  See
  `poly_drift` in `fmri_designs/regressors.py`;
* "HRF model" is a set of 4 neural onset models convolved with a standard SPM
  hemodynamic response function.  These are the regressors for the specific
  subject and run in this experiment;
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
* "HRF+out" is the MFwM for the *HRF+out* F test;
* "HRF+out - HRF" is difference between the previous two values.
* there is one row for each run where the tested algorithm detected at least
  one outlier.

A good algorithm will have a high mean value for "outliers" and a high
positive value for "HRF+out - HRF".
