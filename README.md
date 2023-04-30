# CSV File Comparison Tool

This Python script compares two CSV files and outputs a summary of differences and a detailed comparison file. The script now prompts the user for input and output file paths instead of using hardcoded file paths.

## Prerequisites

This script requires Python 3.6+ and the following libraries:

- pandas
- numpy

## Setting Up a Virtual Environment

It is recommended to set up a virtual environment for this project. You can do so using `venv`. To create a virtual environment, open a terminal, navigate to the project directory, and run:

```bash
python -m venv venv
```

This will create a virtual environment named venv in the project directory. To activate the virtual environment, run:

- On Windows:

`venv\Scripts\activate`

- On macOS and Linux:

`source venv/bin/activate`

## Installing Dependencies

After activating the virtual environment, you can install the required dependencies using `pip`. Run the following command:

`pip install pandas numpy`

## Usage

To use the script, simply run the following command:

`python compare_csv.py`

The script will prompt you for the file paths of the two CSV files you want to compare and the output file path. Provide the file paths, and the script will generate a summary file and a detailed comparison file in the specified output path.

Example:

```
Enter the path of the first CSV file: file1.csv
Enter the path of the second CSV file: file2.csv
Enter the path of the output file: comparison_results.csv
```

The above example will create a "comparison_results.csv" file in the same directory as the script.
