from decimal import Decimal
from pathlib import Path

import polars as pl
from dotenv import load_dotenv
from pydantic_ai import Agent, ModelRetry, RunContext

from finn2.finn_deps import DataDirs, FinnDeps
from finn2.toolsets.toolset_utils import load_df

load_dotenv()


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

        >>> calculate_sum("data.csv", "sales")
        # Reads data.csv and returns sum of sales column
    """
    if isinstance(data, list):
        return Decimal(sum(data))
    if column is None:
        raise ModelRetry("Column name is required for DataFrame")
    try:
        df = load_df(ctx, data)
    except Exception as e:
        raise ModelRetry(f"Error loading DataFrame: {e}")
    result = df.select(pl.col(column).sum()).item()
    return Decimal(result)


agent = Agent(model="google-gla:gemini-2.5-flash", deps_type=FinnDeps, tools=[calculate_sum])


res = agent.run_sync(
    "what is the sum of 1 and 2?",
    deps=FinnDeps(dirs=DataDirs(thread_dir=Path("workspaces/1/threads/t1"), workspace_dir=Path("workspaces/1"))),
)
for message in res.all_messages():
    print(message, "\n--------\n")
