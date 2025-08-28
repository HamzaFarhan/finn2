from pathlib import Path
from typing import Any

import polars as pl


def load_file_standalone(file_path: str | Path) -> pl.DataFrame:
    """
    Load a file directly without RunContext dependencies.
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
    
    # Ensure the file exists
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    suffix = file_path.suffix.lower()
    if suffix == ".parquet":
        return pl.read_parquet(file_path)
    elif suffix in [".xlsx", ".xls", ".xlsb"]:
        return pl.read_excel(file_path)
    else:
        return pl.read_csv(file_path)


def describe_file_standalone(file_path: str | Path) -> dict[str, Any]:
    """
    Get the shape, schema, and description of a csv, excel, or parquet file at the given path.
    Standalone version without RunContext dependencies.
    """
    try:
        df = load_file_standalone(file_path)
        res: dict[str, Any] = {
            "shape": {"rows": df.height, "columns": df.width}, 
            "schema": str(df.schema)
        }
        
        # Try to get basic description statistics
        try:
            res["description"] = df.describe().to_dicts()
        except Exception as e:
            print(f"Error describing DataFrame: {e}")

        # Try to get unique values info
        try:
            unique_values_info = {}
            for col_name in df.columns:
                try:
                    n_unique = df[col_name].n_unique()
                    if n_unique < 20:
                        unique_values = df[col_name].unique().to_list()
                        unique_values_info[col_name] = unique_values
                    else:
                        unique_values_info[col_name] = f"{n_unique} unique values (too many to list)"
                except Exception:
                    pass  # Ignore columns that don't support n_unique, or other errors
            res["unique_values"] = unique_values_info
        except Exception:
            pass

        return res
    except Exception as e:
        raise Exception(f"Error in describe_file: {e}")


if __name__ == "__main__":
    # Test with the subscriptions.csv file
    file_path = "/Users/hamza/dev/finn2/workspaces/test_workspace/data/subscriptions.csv"
    
    try:
        result = describe_file_standalone(file_path)
        print("File description:")
        print(f"Shape: {result['shape']}")
        print(f"Schema: {result['schema']}")
        
        if "description" in result:
            print("\nDescription statistics:")
            for desc in result["description"]:
                print(desc)
        
        if "unique_values" in result:
            print("\nUnique values:")
            for col, values in result["unique_values"].items():
                print(f"{col}: {values}")
                
    except Exception as e:
        print(f"Error: {e}")
