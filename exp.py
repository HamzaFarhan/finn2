from pathlib import Path

from dotenv import load_dotenv
from dreamai.plan_act import run_plan_and_act_agent
from loguru import logger
from pydantic_ai.toolsets import FunctionToolset

from finn2.finn_deps import DataDirs, FinnDeps
from finn2.toolsets.arithmetic_toolset import (
    calculate_abs,
    calculate_average,
    calculate_cumprod,
    calculate_cumsum,
    calculate_exp,
    calculate_geometric_mean,
    calculate_harmonic_mean,
    calculate_ln,
    calculate_log,
    calculate_max,
    calculate_median,
    calculate_min,
    calculate_mod,
    calculate_mode,
    calculate_percentile,
    calculate_power,
    calculate_product,
    calculate_round,
    calculate_rounddown,
    calculate_roundup,
    calculate_sign,
    calculate_sqrt,
    calculate_sum,
    calculate_variance_weighted,
    calculate_weighted_average,
)
from finn2.toolsets.conditional_toolset import (
    aggregate,
    averageif,
    averageifs,
    counta,
    countblank,
    countif,
    countifs,
    maxifs,
    minifs,
    subtotal,
    sumif,
    sumifs,
    sumproduct,
)
from finn2.toolsets.date_and_time_toolset import (
    create_date,
    create_time,
    date_range,
    datedif,
    edate,
    eomonth,
    extract_day,
    extract_hour,
    extract_minute,
    extract_month,
    extract_second,
    extract_year,
    networkdays,
    now,
    quarter,
    today,
    weekday,
    workday,
    yearfrac,
)
from finn2.toolsets.file_toolset import describe_df, list_analysis_files, list_data_files
from finn2.toolsets.logical_and_errors_toolset import (
    is_blank,
    is_error,
    is_number,
    is_text,
    logical_and,
    logical_and_scalar,
    logical_if,
    logical_iferror,
    logical_ifna,
    logical_ifs,
    logical_not,
    logical_or,
    logical_or_scalar,
    logical_switch,
    logical_xor,
)
from finn2.toolsets.lookup_and_reference_toolset import (
    address_cell,
    choose_value,
    column_number,
    columns_count,
    hlookup,
    index_lookup,
    indirect_reference,
    lookup_vector,
    match_lookup,
    offset_range,
    row_number,
    rows_count,
    vlookup,
    xlookup,
)

load_dotenv()

if __name__ == "__main__":
    import asyncio

    arithmetic_toolset = FunctionToolset(
        [
            calculate_sum,
            calculate_average,
            calculate_min,
            calculate_max,
            calculate_product,
            calculate_median,
            calculate_mode,
            calculate_percentile,
            calculate_power,
            calculate_sqrt,
            calculate_exp,
            calculate_ln,
            calculate_log,
            calculate_abs,
            calculate_sign,
            calculate_mod,
            calculate_round,
            calculate_roundup,
            calculate_rounddown,
            calculate_weighted_average,
            calculate_geometric_mean,
            calculate_harmonic_mean,
            calculate_cumsum,
            calculate_cumprod,
            calculate_variance_weighted,
        ]
    )

    conditional_toolset = FunctionToolset(
        [
            sumif,
            sumifs,
            countif,
            countifs,
            averageif,
            averageifs,
            maxifs,
            minifs,
            sumproduct,
            aggregate,
            subtotal,
            countblank,
            counta,
        ]
    )

    date_and_time_toolset = FunctionToolset(
        [
            today,
            now,
            create_date,
            extract_year,
            extract_month,
            extract_day,
            edate,
            eomonth,
            datedif,
            yearfrac,
            weekday,
            quarter,
            create_time,
            extract_hour,
            extract_minute,
            extract_second,
            date_range,
            workday,
            networkdays,
        ]
    )

    logical_and_errors_toolset = FunctionToolset(
        [
            logical_if,
            logical_iferror,
            logical_ifna,
            logical_ifs,
            logical_and,
            logical_or,
            logical_not,
            logical_switch,
            logical_xor,
            is_blank,
            is_number,
            is_text,
            is_error,
            logical_and_scalar,
            logical_or_scalar,
        ]
    )

    lookup_and_reference_toolset = FunctionToolset(
        [
            vlookup,
            hlookup,
            index_lookup,
            match_lookup,
            xlookup,
            offset_range,
            indirect_reference,
            choose_value,
            lookup_vector,
            address_cell,
            row_number,
            column_number,
            rows_count,
            columns_count,
        ]
    )

    files_toolset = FunctionToolset([list_data_files, list_analysis_files, describe_df])

    workspace_dir = Path("./workspaces/session/")
    agent_deps = FinnDeps(
        dirs=DataDirs(
            workspace_dir=workspace_dir,
            thread_dir=workspace_dir / "threads/1",
        ),
        toolsets=[
            files_toolset,
            arithmetic_toolset,
            conditional_toolset,
            date_and_time_toolset,
            logical_and_errors_toolset,
            lookup_and_reference_toolset,
        ],
    )
    asyncio.run(
        run_plan_and_act_agent(Path("/Users/hamza/dev/finn2/ltv_prompt.md").read_text(), agent_deps=agent_deps)
    )
    logger.success("Agent run completed successfully.")
