from decimal import Decimal
from pathlib import Path

import polars as pl


def calculate_sum(data: list[Decimal] | str, column: str | None = None) -> Decimal:
    """
    Calculate the sum of a column in a DataFrame.

    Args:
        data: Either a list of numbers or a path to a polars DataFrame (CSV or Parquet)
              Will first check the `analysis_dir` and then the `data_dir` for the file.
        column: Name of the column to sum. In case of DataFrame, this is required.

    Returns:
        Sum of the column values

    Example:
        >>> calculate_sum([1, 2, 3, 4, 5])
        15.0

        >>> calculate_sum(data="data.parquet", column="sales")
        # Reads data.parquet and returns sum of sales column
    """
    if isinstance(data, list):
        return Decimal(sum(data))
    if column is None:
        raise ValueError("Column name must be provided when loading from a DataFrame.")
    try:
        df_path = Path(data)
        df = pl.read_parquet(df_path) if df_path.suffix.lower() == ".parquet" else pl.read_csv(df_path)
    except Exception as e:
        raise RuntimeError(f"Error loading DataFrame: {e}")
    result = df.select(pl.col(column).sum()).item()
    return Decimal(result)
