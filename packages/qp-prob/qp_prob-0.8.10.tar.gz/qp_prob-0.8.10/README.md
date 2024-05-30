# qp

Quantile parametrization for probability distribution functions.

![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/LSSTDESC/qp)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/LSSTDESC/qp/python-package.yml)
![Read the Docs](https://img.shields.io/readthedocs/qp)

## Motivation

In a scientific inference we typically seek to characterize the posterior probability density function (PDF) for our parameter(s), which means we need to find a suitable, calculable approximation to it. Popular choices include an ensemble of samples, a histogram estimator based on those samples, or (in 1 dimensional problems) a tabulation of the PDF on a regular parameter grid. qp is a python package that supports these approximations, as well as the “quantile parameterization” from which the package gets its name.

The [scipy.stats](https://docs.scipy.org/doc/scipy/reference/stats.html) package provides an interface to many probability distributions for parameterized analytic forms (e.g., Gaussians, LogNormal Distributions, etc...)  `qp` extends that functionality to numerically-evaluated forms, such as the histograms and interpolated grids mentioned above.



## Examples

Here are some example notebooks to help new users explore `qp` functionality.

* **[Basic Demo](http://htmlpreview.github.io/?https://github.com/LSSTDESC/qp/blob/master/docs/demo.html)** [(raw notebook)](https://github.com/LSSTDESC/qp/blob/master/nb/demo.ipynb)

* **[Practical Example](http://htmlpreview.github.io/?https://github.com/LSSTDESC/qp/blob/master/docs/practical_example.html)** [(raw notebook)](https://github.com/LSSTDESC/qp/blob/master/nb/practical_example.ipynb)

* **[Using Metrics](http://htmlpreview.github.io/?https://github.com/LSSTDESC/qp/blob/master/docs/metrics_examples.html)** [(raw notebook)](https://github.com/LSSTDESC/qp/blob/master/nb/metrics_examples.ipynb)

* **[Using iterarors](http://htmlpreview.github.io/?https://github.com/LSSTDESC/qp/blob/master/docs/iterator_demo.html)** [(raw notebook)](https://github.com/LSSTDESC/qp/blob/master/nb/iterator_demo.ipynb)

* **[Quantile parameterization](http://htmlpreview.github.io/?https://github.com/LSSTDESC/qp/blob/master/docs/quantile_parameterization_demo.html)** [(raw notebook)](https://github.com/LSSTDESC/qp/blob/master/nb/quantile_parameterization_demo.ipynb)


Also the read the docs page has significantly more information:  [Read the Docs](http://qp.readthedocs.io/)


## People

* [Alex Malz](https://github.com/LSSTDESC/qp/issues/new?body=@aimalz) (NYU)
* [Phil Marshall](https://github.com/LSSTDESC/qp/issues/new?body=@drphilmarshall) (SLAC)
* [Eric Charles](https://github.com/LSSTDESC/qp/issues/new?body=@eacharles) (SLAC)
* [Sam Schmidt](https://github.com/LSSTDESC/qp/issues/new?body=@sschmidt) (UC Davis)

## License, Contributing etc

The code in this repo is available for re-use under the MIT license, which means that you can do whatever you like with it, just don't blame us. If you end up using any of the code or ideas you find here in your academic research, please cite us as `Malz et al, ApJ 156 1 35`. If you are interested in this project, please do drop us a line via the hyperlinked contact names above, or by [writing us an issue](https://github.com/aimalz/qp/issues/new). To get started contributing to the `qp` project, just fork the repo - pull requests are always welcome!





