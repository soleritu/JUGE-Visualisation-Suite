# JUGE Visualisation Suite

The JUGE Visualisation Suite is a collection of Python scripts used for processing and visualizing benchmarking data for the [JUGE Framework](https://github.com/JUnitContest/JUGE). The suite includes the following scripts:

## JUGE-Chart

Generates bar charts from .tmp files. Each chart represents a unique benchmark found in the file, with coverage ratios on the x-axis and coverage types on the y-axis.

## JUGE-Tabelle

Generates comparison tables from .csv and .tmp files. Each table represents a unique time budget found in the files, with relevant columns selected based on the file type.

## JUGE-Score

Generates bar charts from 'score_per_subject.csv' files. Each chart represents a unique time budget found in the files, with 'score.mean' on the x-axis and 'benchmark' on the y-axis.

## JUGE-Comparison

Generates bar charts from 'results.tmp' files. Each chart represents a unique time budget found in the files, with average coverage ratios on the x-axis and benchmarks on the y-axis.

## Requirements

- Python 3.6 or higher
- pandas
- matplotlib
- seaborn
- glob

```bash
pip install pandas matplotlib seaborn
```

## Usage

To use these scripts, simply run them in a directory containing the required data files. The scripts will automatically find all relevant files in the current directory and its subdirectories, process the data, and generate the charts or tables.

```bash
python JUGE-Chart.py
python JUGE-Tabelle.py
python JUGE-Score.py
python JUGE-Comparison.py
```
