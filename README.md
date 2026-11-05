# Smart Machine Condition Monitoring and Safety Alert System

DEX2013 Programming for Engineering

## Description
Reads the supplied machine dataset, classifies readings as NORMAL, WARNING or
CRITICAL (Critical is checked first), calculates summary statistics, and
creates temperature and vibration graphs.

## Requirements
- Python 3
- pandas
- matplotlib

## How to run
1. Keep machine_condition_dataset.csv in the same folder as the Python file.
2. Install the required libraries if needed: `python -m pip install pandas matplotlib`
3. Run: `python 1002580901_python_monitoring.py`

## Expected output files
- temperature_vs_time.png
- vibration_vs_time.png
- machine_condition_results.csv (dataset with Status and Recommended_Action columns)
