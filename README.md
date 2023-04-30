# CSV and Excel File Comparison Tool

This Python script allows you to compare two CSV or Excel files and generates a report highlighting the differences. It works by reading the input files, merging them based on a unique identifier, and then comparing the values in each column. The results are saved to an output file, and a summary of the differences is also generated.

## Prerequisites

- Python 3.6 or higher

## Dependencies

- pandas
- numpy

## Setting up a virtual environment

To set up a virtual environment using `venv`, follow these steps:

1. Open a terminal/command prompt.
2. Create a new directory for your project and navigate to it:
   `mkdir file_comparison`

`cd file_comparison`

3. Create a new virtual environment in the directory:
   `python -m venv venv`

4. Activate the virtual environment:

- On Windows:

`venv\Scripts\activate`

- On macOS/Linux:

`source venv/bin/activate`

5. Install the required dependencies in the virtual environment:

`pip install pandas numpy`

## Usage

To use the script, you need to call the `compare_files` function with the following parameters:

- `file1`: The path to the first CSV file.
- `file2`: The path to the second CSV file.
- `output_file`: The path where the comparison results will be saved.
- `id_cols`: A list of unique identifier columns that exist in both CSV files.

Example usage:

```
from compare_csv import compare_csv_files

file1 = "example_file1.csv"
file2 = "example_file2.csv"
output_file = "comparison_results.csv"
unique_id_columns = ["column1", "column2"]

compare_csv_files(file1, file2, output_file, id_cols=unique_id_columns)
```

This example assumes you have two CSV files named `example_file1.csv` and `example_file2.csv`. The script will compare these files and save the comparison results to `comparison_results.csv`. The unique identifier columns used for comparison are column1 and column2.
