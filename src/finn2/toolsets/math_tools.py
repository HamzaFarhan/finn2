from decimal import Decimal

import polars as pl
from pydantic_ai import RunContext

from finn2.finn_deps import FinnDeps
from finn2.toolsets.file_toolset import load_df


def calculate_sum(ctx: RunContext[FinnDeps], data: list[Decimal] | str, column: str | None = None) -> Decimal:
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
        df = load_df(ctx, data)
    except Exception as e:
        raise RuntimeError(f"Error loading DataFrame: {e}")
    result = df.select(pl.col(column).sum()).item()
    return Decimal(result)
