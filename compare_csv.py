import pandas as pd
import numpy as np


def compare_files(file1, file2, output_file, id_cols, file_format="csv"):
    """
    Compare two CSV files and generate a comparison report in a new CSV file.

    This function reads two CSV files, sets a multi-level index based on the specified identifier columns,
    and compares the values in each column. It creates a new DataFrame with actual differences side by side,
    including row numbers from the original files. Additionally, it generates a summary of the number of differences
    per column and the unique rows for each file. Finally, it writes the comparison results and summary to separate
    output CSV files.

    Parameters
    ----------
    file1 : str
        Path to the first CSV file.
    file2 : str
        Path to the second CSV file.
    output_file : str
        Path to the output CSV file where the comparison results will be saved.
    id_cols : list of str
        List of column names to be used as the unique identifier columns for the multi-level index.

    Output
    ------
    A new CSV file with the comparison results is created at the specified output_file path. Additionally, a summary
    CSV file with the number of differences per column and unique rows for each file is created in the same directory
    with the "summary_" prefix added to the output_file name.
    """

    # Add a function to read different file formats
    def read_file(file, format):
        if format == "csv":
            return pd.read_csv(file)
        elif format == "excel":
            return pd.read_excel(file)
        else:
            raise ValueError("Unsupported file format.")

    # Read the files using the appropriate function
    df1 = read_file(file1, file_format)
    df2 = read_file(file2, file_format)

    # Set multi-level index
    df1["seq"] = df1.groupby(id_cols).cumcount()
    df2["seq"] = df2.groupby(id_cols).cumcount()
    df1 = df1.set_index(id_cols + ["seq"])
    df2 = df2.set_index(id_cols + ["seq"])

    # Merge DataFrames on index
    df1["row_number_file1"] = np.arange(2, len(df1) + 2)
    df2["row_number_file2"] = np.arange(2, len(df2) + 2)
    merged_df = df1.merge(
        df2,
        how="outer",
        left_index=True,
        right_index=True,
        suffixes=("_file1", "_file2"),
        indicator=True,
    )

    merged_df["row_number_file2"] = merged_df["row_number_file2"].fillna(0).astype(int)

    # Replace left_only and right_only in _merge column with actual file names
    merged_df["_merge"] = merged_df["_merge"].replace(
        {"left_only": file1 + "_ONLY", "right_only": file2 + "_ONLY"}
    )

    # Compare columns and store differences
    diff_data = {}
    summary_data = {}
    for col in df1.columns:
        if col in df2.columns:
            diff_col_name = f"{col}_diff"
            diff_data[diff_col_name] = np.where(
                merged_df[col + "_file1"] != merged_df[col + "_file2"], True, False
            )
            summary_data[col] = np.sum(diff_data[diff_col_name])

    # Create a DataFrame of actual differences
    actual_diff_df = pd.DataFrame(diff_data, index=merged_df.index)
    actual_diff_df["row_number_file1"] = merged_df["row_number_file1"]
    actual_diff_df["row_number_file2"] = merged_df["row_number_file2"]
    actual_diff_df["_merge"] = merged_df["_merge"]

    # Reorder columns to move the _merge column to the end
    columns = actual_diff_df.columns.tolist()
    columns.remove("_merge")
    columns.append("_merge")
    actual_diff_df = actual_diff_df[columns]

    # Filter out rows with no differences
    actual_diff_df = actual_diff_df[actual_diff_df.any(axis=1)]

    # Replace True with actual values side by side
    for col in actual_diff_df.columns:
        if col != "_merge" and not col.startswith("row_number"):
            actual_diff_col = col.replace("_diff", "")
            file1_col = actual_diff_col + "_file1"
            file2_col = actual_diff_col + "_file2"
            actual_diff_df[col] = np.where(
                actual_diff_df[col],
                merged_df[file1_col].astype(str).replace("nan", "--")
                + " | "
                + merged_df[file2_col].astype(str).replace("nan", "--"),
                "--",
            )

    # Calculate the number of differences per column
    summary_df = pd.DataFrame(summary_data, index=["num_differences"]).transpose()
    summary_df.index.name = "column_name"

    # Get the unique row numbers for each file
    unique_rows_file1 = merged_df[merged_df["_merge"] == file1 + "_ONLY"].index.tolist()
    unique_rows_file2 = merged_df[merged_df["_merge"] == file2 + "_ONLY"].index.tolist()

    # Add unique row numbers to the summary DataFrame
    summary_df.loc[file1 + "_unique_rows", "num_differences"] = str(unique_rows_file1)
    summary_df.loc[file2 + "_unique_rows", "num_differences"] = str(unique_rows_file2)

    # Write the summary to a separate CSV file
    summary_file = "summary_" + output_file
    summary_df.to_csv(summary_file, index_label="column_name")

    # Write the results to a new CSV file
    actual_diff_df.to_csv(output_file, index_label=id_cols)
