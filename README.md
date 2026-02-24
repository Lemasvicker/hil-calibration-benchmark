[![DOI](https://zenodo.org/badge/1165629486.svg)](https://doi.org/10.5281/zenodo.18757094)

# HIL Calibration Benchmark

A minimal **human-in-the-loop (HIL)** benchmark for calibrating thresholds / operating points for streaming risk alerts, with synthetic demo data (non-proprietary).

## What this is
This repository provides a small reference implementation to:
- Define an interactive calibration loop (human feedback → threshold updates)
- Evaluate alerting policies with metrics like false-alarm burden, lead time, and stability
- Run a synthetic demo so results are reproducible without private datasets

## What this is not
- Not a medical device.
- Not clinical decision support.
- Not validated for any diagnostic or therapeutic use.

## Quick start (v0.1.0)
This release includes a runnable demo script and synthetic stream generator.
Run: `python src/demo.py`

## Citation
Use the GitHub “Cite this repository” feature once `CITATION.cff` is added.
After the Zenodo DOI is minted for `v0.1.0`, cite the DOI for the release.

## Author
Victory Nlemadim

## License
Apache License 2.0
