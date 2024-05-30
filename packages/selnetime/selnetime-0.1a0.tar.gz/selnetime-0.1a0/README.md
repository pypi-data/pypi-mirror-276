# SelNeTime: Estimate demography and selection from genetic time series

The `selnetime` python package implements methods for statistical
analysis of genetic data collected in time. This type of data is
typically encountered in experimental evolution studies, cohorts of
wild and domestic populations or ancient DNA studies.

The statistical approaches implemented in `selnetime` are based on
Hidden Markov Models (HMMs) of the evolution of allele frequencies of
biallelic loci through time. For computational efficiency, the methods
build on approximating this evolution using continuous distributions
(at the moment only the Beta distribution with point masses at 0 and
1, called the "Beta with Spikes" distribution). For more details on
the methods see [Paris et
al. (2019)](https://doi.org/10.1534/g3.119.400778).

## Installing the package

The package is available on the python package index
(https://pypi.org/project/selnetime) It can be installed with `pip`:
`pip install selnetime`, possibly inside a python or conda environment

## Analysing a dataset

The `selnetime` package comes with a command line program to analyze a
time series dataset: `snt`. A simple description of the option is
obtained by typing `snt -h`. The typical usage to estimate Ne and s
with the Beta-with-Spikes transition model is:

``` shell
snt -ft baypass -S <prefix>
```
where `<prefix>` gives the prefix of input files. Two input files are expected,
named `<prefix>.genobaypass` and `<prefix>.times`.

The `genobaypass` file is in the format used by the BayPass software:
one line per (biallelic) locus. On each row, successive pairs of
counts give the number of alleles observed at a given epoch. For example:

```
12 19 0 36 0 32 0 26 0 33
6 3 0 3 5 0 11 0 4 0
25 9 39 2 37 14 21 10 17 5
```
indicates at the first locus, for the first epoch of the time series 12
(resp. 19) copies of the first (resp. second) alleles were observed.

the `times` file is a simple csv file indicating the times (in
generations) at which the data were collected. For example:

```
11,27,45,58,70
```

will indicate 5 epochs, corresponding to sampling at generations 11, 27 etc.

The `snt` program will output two files:

- `<prefix>.snt.N` with the results of the estimation effective
  population size: for each Ne considered by the program, the
  corresponding loglikelihood.
- `<prefix>.snt.S` with the results of the estimation of selection  coefficients for each locus:
  - loc : locus index
  - mle : Maximum likelihood estimate of s
  - pmean : posterior mean for s
  - psd : posterior standard deviation for s
  - lo : lower bound of the 95% credible interval for s
  - hi : upper bound of the 95% credible interval for s
  - lfsr: local false-sign rate, i.e. the posterior probability that the MLE is of the wrong sign



## References

- Cyriel Paris, Bertrand Servin, Simon Boitard, Inference of Selection
  from Genetic Time Series Using Various Parametric Approximations to
  the Wright-Fisher Model, G3 Genes|Genomes|Genetics, Volume 9, Issue
  12, 1 December 2019, Pages 4073–4086
